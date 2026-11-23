"""Read canonical original-blob OSS URLs from explicitly configured BM fixed revisions."""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import sys
import urllib.request
from urllib.parse import urlsplit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--octop-root', type=Path, required=True)
    parser.add_argument('--asset-config', type=Path, required=True)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--allowed-origin', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--audit-output', type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(args.octop_root / 'bm-integration/asset-runtime/src'))
    import psycopg
    from psycopg.rows import dict_row
    from bm_skill_api.assets.deployment import load_configuration
    config, _ = load_configuration(args.asset_config)
    receipts = json.loads(args.receipts.read_text())
    links = []
    audits = []
    with psycopg.connect(config['databaseUrl'], row_factory=dict_row, options='-c default_transaction_read_only=on') as db:
        for tenant in sorted({identity['tenant'] for identity in config['identities']}):
            db.execute("SELECT set_config('fuke.tenant',%s,true)", (tenant,))
            if args.audit_output:
                deployment=db.execute('SELECT deployment_id,schema_version FROM bm_skill_assets.deployment WHERE singleton').fetchone()
                datatype=db.execute('SELECT data_type FROM information_schema.columns WHERE table_schema=%s AND table_name=%s AND column_name=%s',('bm_skill_assets','blob','content')).fetchone()
                counts=db.execute('SELECT COUNT(*) AS blob_count, COUNT(*) FILTER (WHERE content NOT LIKE %s) AS non_configured_oss_count FROM bm_skill_assets.blob WHERE tenant=%s',(args.allowed_origin.rstrip('/')+'/%',tenant)).fetchone()
                if deployment['deployment_id']!=config['deploymentId'] or deployment['schema_version']!=2 or datatype['data_type']!='text' or counts['non_configured_oss_count']:
                    raise RuntimeError('Configured OSS content schema or blob audit failed')
                audits.append({'deployment_id':deployment['deployment_id'],'schema_version':deployment['schema_version'],'content_type':datatype['data_type'],**counts,'read_only':True})
            for item in receipts:
                if item.get('phase') != 'fixed_asset_verified':
                    continue
                package = db.execute("SELECT body->>'originalHash' AS original_hash, body->>'originalBlobId' AS original_blob_id FROM bm_skill_assets.document WHERE tenant=%s AND kind=%s AND id=%s", (tenant, 'package', item['source']['packageId'])).fetchone()
                if not package:
                    continue
                if package['original_hash'] != item['sha256']:
                    raise RuntimeError('Fixed package binding mismatch')
                blob = db.execute('SELECT content FROM bm_skill_assets.blob WHERE tenant=%s AND id=%s', (tenant, package['original_blob_id'])).fetchone()
                url = blob['content']
                parsed = urlsplit(url)
                if parsed.scheme != 'https' or parsed.scheme+'://'+parsed.netloc != args.allowed_origin.rstrip('/') or parsed.query or parsed.fragment or parsed.username:
                    raise RuntimeError('Canonical blob is not the explicitly configured immutable OSS origin')
                links.append({'row': item['row'], 'catalog_id': item['catalog_id'], 'asset_id': item['asset_id'], 'asset_revision': item['asset_revision'], 'package_id': item['source']['packageId'], 'blob_id': package['original_blob_id'], 'sha256': item['sha256'], 'url': url})
    if len(links) != len(receipts) or len({x['row'] for x in links}) != len(links):
        raise RuntimeError('Missing or ambiguous asset bindings')
    def verify(item):
        with urllib.request.urlopen(item['url'], timeout=90) as response:
            raw = response.read(10*1024*1024+1)
        if hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise RuntimeError('Anonymous OSS download digest mismatch at row ' + str(item['row']))
        return {**item, 'status': 'verified'}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(verify, links))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix('.tmp')
    temporary.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    temporary.replace(args.output)
    if args.audit_output:
        args.audit_output.write_text(json.dumps(audits,ensure_ascii=False,indent=2))
    print(json.dumps({'canonical_oss_links_verified': len(results)}))

if __name__ == '__main__':
    main()
