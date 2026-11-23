"""Import newly authored, validated ZIPs through BM dev's public V2 API.

Never executes skills. Durable operation identities and unknown-result receipts
prevent a resumed run from creating another asset for the same planned import.
"""
from __future__ import annotations
import argparse
import getpass
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request
from urllib.parse import urlsplit
import uuid

from bm_assets import multipart, save


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(base, manifest_path, validation_path):
    parsed = urlsplit(base)
    if parsed.scheme not in {'http', 'https'} or not parsed.netloc or parsed.path not in {'', '/'} or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Explicit BM dev origin required without credentials or path')
    base = base.rstrip('/')
    manifest = json.loads(manifest_path.read_text())
    validation = json.loads(validation_path.read_text())
    if validation.get('passed') is not True or validation.get('manifest_sha256') != digest(manifest_path):
        raise ValueError('Matching successful fixed-provenance validation required')
    verified = {x['formal_code']: x for x in validation['items']}
    if len(verified) != len(manifest['items']):
        raise ValueError('Validation coverage differs')
    result = []
    seen = set()
    for item in manifest['items']:
        code = item['formal_code']
        if code in seen or not verified[code]['passed'] or verified[code]['package_sha256'] != item['package_sha256']:
            raise ValueError('Non-unique identity or package validation mismatch')
        seen.add(code)
        package = Path(item['package_path'])
        if digest(package) != item['package_sha256']:
            raise ValueError('Frozen ZIP changed')
        metadata = {'displayName': item['name'].strip(),
                    'summary': '来源：飞书福客技能库 ATP 表，记录行 ' + ','.join(map(str, item['source_rows'])) + '；尚未核对淘宝上架。',
                    'categoryId': None, 'visibility': 'public'}
        identity = {'origin': base, 'formalCode': code, 'sourceRows': item['source_rows'],
                    'sha256': item['package_sha256'], 'metadata': metadata}
        operation = str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(identity, ensure_ascii=False, sort_keys=True)))
        result.append({'row': item['primary_row'], 'source_rows': item['source_rows'], 'formal_code': code,
                       'skill_name': item['skill_name'], 'package_path': str(package),
                       'sha256': item['package_sha256'], 'metadata': metadata, 'operation_id': operation})
    return {'origin': base, 'manifest_sha256': digest(manifest_path), 'items': result,
            'bm_public_visibility_is_not_taobao_listing_scope': True}


def import_one(item, call, journal, persist):
    operation, row = item['operation_id'], item['row']
    prior = next((x for x in journal if x['operation_id'] == operation), None)
    if prior and (prior['sha256'] != item['sha256'] or prior['formal_code'] != item['formal_code']):
        raise ValueError('Import journal identity drift')
    status, result = call('/api/v2/bm/skills/imports/' + operation)
    if status == 404:
        if prior:
            raise RuntimeError('Prior intent has no confirmed server operation; reconcile without reposting')
        intent = {**item, 'phase': 'submitting'}
        journal.append(intent)
        persist(journal)
        body, headers = multipart({'metadata': json.dumps(item['metadata'], ensure_ascii=False),
                                   'clientOperationId': operation}, Path(item['package_path']))
        try:
            status, result = call('/api/v2/bm/skills/imports', 'POST', body,
                                  {**headers, 'Idempotency-Key': operation})
        except Exception:
            intent['phase'] = 'unknown'
            persist(journal)
            raise
    if status >= 300 or result.get('status') != 'synced':
        raise RuntimeError(f'Import requires reconciliation: HTTP {status}, status {result.get("status")}')
    identifier = result['catalogId']
    status, before = call('/api/v2/bm/skills/' + identifier)
    if status != 200 or before['source']['packageSha256'] != item['sha256'] or before['source']['skillName'] != item['skill_name'] or not before.get('assetId') or not before.get('octopPackageId'):
        raise RuntimeError('Imported source identity mismatch')
    status, download = call('/api/v2/bm/skills/' + identifier + '/download', binary=True)
    raw, etag = download
    if status != 200 or hashlib.sha256(raw).hexdigest() != item['sha256'] or etag != '"' + item['sha256'] + '"':
        raise RuntimeError('Imported original ZIP download mismatch')
    status, after = call('/api/v2/bm/skills/' + identifier)
    if status != 200 or before != after:
        raise RuntimeError('Asset changed during source verification')
    receipt = {**item, 'phase': 'fixed_asset_verified', 'catalog_id': identifier,
               'asset_id': before['assetId'], 'asset_revision': before.get('assetRevision', before['revision']),
               'octop_package_id': before['octopPackageId'], 'source': before['source'],
               'bm_synced_is_not_feishu_sync_success': True}
    journal[:] = [x for x in journal if x['operation_id'] != operation] + [receipt]
    persist(journal)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--validation', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--receipts', type=Path)
    parser.add_argument('--username')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--rows', help='Canonical primary rows, comma-separated')
    args = parser.parse_args()
    plan = prepare(args.base_url, args.manifest, args.validation)
    if args.plan.exists() and json.loads(args.plan.read_text()) != plan:
        raise ValueError('Existing import plan differs; preserve and use another reviewed plan')
    if not args.plan.exists():
        save(args.plan, plan)
    if not args.apply:
        print(json.dumps({'planned': len(plan['items']), 'mutations': 0}))
        return
    if not args.username or not args.receipts:
        raise ValueError('Explicit username and receipt path required to apply')
    base, token = plan['origin'], None
    def call(path, method='GET', body=None, headers=None, binary=False):
        request = urllib.request.Request(base + path, body,
            {**({'Authorization': 'Bearer ' + token} if token else {}), **(headers or {})}, method=method)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                if binary:
                    return response.status, (response.read(10 * 1024 * 1024 + 1), response.headers.get('ETag'))
                return response.status, json.load(response)
        except urllib.error.HTTPError as exc:
            return exc.code, json.load(exc)
    password = getpass.getpass('BM dev password (not saved): ')
    status, auth = call('/api/auth/login', 'POST', json.dumps({'username': args.username, 'password': password}).encode(), {'Content-Type': 'application/json'})
    password = None
    if status != 200:
        raise RuntimeError('BM login failed: HTTP ' + str(status))
    token = auth['access_token']
    journal = json.loads(args.receipts.read_text()) if args.receipts.exists() else []
    selected = set(map(int, args.rows.split(','))) if args.rows else None
    for item in plan['items']:
        if selected is not None and item['row'] not in selected:
            continue
        receipt = import_one(item, call, journal, lambda value: save(args.receipts, value))
        print(json.dumps({'row': item['row'], 'source_rows': item['source_rows'], 'phase': receipt['phase']}), flush=True)


if __name__ == '__main__':
    main()
