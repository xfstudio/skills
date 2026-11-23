"""Replace or verify native BM fixed assets, preserving old snapshots and operation IDs."""
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


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2))
    temporary.replace(path)


def multipart(fields, package):
    boundary = 'bmSkillAsset' + uuid.uuid4().hex
    parts = [(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n').encode() for key, value in fields.items()]
    if any(x in package.name for x in ['"', '\r', '\n']):
        raise ValueError('Unsafe filename')
    parts += [(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{package.name}"\r\nContent-Type: application/zip\r\n\r\n').encode(), package.read_bytes(), f'\r\n--{boundary}--\r\n'.encode()]
    return b''.join(parts), {'Content-Type': 'multipart/form-data; boundary=' + boundary}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--prior-sources', type=Path, required=True)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    parsed = urlsplit(args.base_url)
    if parsed.scheme not in {'http', 'https'} or parsed.username or parsed.password or parsed.query:
        raise ValueError('Explicit BM dev origin required without credentials')
    base = args.base_url.rstrip('/')
    token = None
    def call(path, method='GET', body=None, headers=None, binary=False):
        request = urllib.request.Request(base + path, body, {**({'Authorization': 'Bearer ' + token} if token else {}), **(headers or {})}, method=method)
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                return response.status, (response.read(10*1024*1024+1), response.headers.get('ETag')) if binary else json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, json.load(error)
    password = getpass.getpass('BM dev password (not saved): ')
    status, auth = call('/api/auth/login', 'POST', json.dumps({'username': args.username, 'password': password}).encode(), {'Content-Type': 'application/json'})
    password = None
    if status != 200:
        raise RuntimeError('BM login failed: ' + str(status))
    token = auth['access_token']
    prior = {x['row']: x for x in json.loads(args.prior_sources.read_text())}
    manifest = json.loads(args.manifest.read_text())
    receipts = json.loads(args.receipts.read_text()) if args.receipts.exists() else []
    for item in manifest[args.start:args.limit]:
        old = prior[item['row']]
        package = Path(item['package_path'])
        if hashlib.sha256(package.read_bytes()).hexdigest() != item['package_sha256']:
            raise RuntimeError('Frozen package changed')
        operation = str(uuid.uuid5(uuid.NAMESPACE_URL, base + '/skill/' + old['catalog_id'] + '/' + item['package_sha256']))
        status, result = call('/api/v2/bm/skills/imports/' + operation)
        if status == 404:
            if args.verify_only:
                raise RuntimeError('No imported fixed revision for row ' + str(item['row']))
            status, parent = call('/api/v2/bm/skills/' + old['catalog_id'])
            if status != 200 or parent['source']['packageSha256'] != old['sha256'] or parent['assetId'] != old['asset_id'] or parent.get('assetRevision', parent['revision']) != old['asset_revision']:
                raise RuntimeError('Prior source changed; reconcile')
            payload, headers = multipart({'expectedRevision': old['asset_revision'], 'clientOperationId': operation}, package)
            # Durable intent before any mutation; an unknown outcome is reconciled by this same ID.
            receipts = [r for r in receipts if r['row'] != item['row']] + [{'row': item['row'], 'operation_id': operation, 'phase': 'submitting', 'sha256': item['package_sha256']}]
            save(args.receipts, receipts)
            status, result = call('/api/v2/bm/skills/' + old['catalog_id'] + '/package', 'POST', payload, {**headers, 'Idempotency-Key': operation})
        if status >= 300 or result.get('status') != 'synced':
            raise RuntimeError('BM operation needs reconciliation: row ' + str(item['row']) + ', HTTP ' + str(status) + ', status ' + str(result.get('status')))
        identifier = result['catalogId']
        status, before = call('/api/v2/bm/skills/' + identifier)
        if status != 200 or before['source']['packageSha256'] != item['package_sha256'] or before['assetId'] != old['asset_id']:
            raise RuntimeError('Fixed source mismatch')
        status, (raw, etag) = call('/api/v2/bm/skills/' + identifier + '/download', binary=True)
        if status != 200 or hashlib.sha256(raw).hexdigest() != item['package_sha256'] or etag != '"' + item['package_sha256'] + '"':
            raise RuntimeError('Fixed ZIP download mismatch')
        status, after = call('/api/v2/bm/skills/' + identifier)
        if status != 200 or before != after:
            raise RuntimeError('Source changed during readback')
        receipt = {'row': item['row'], 'operation_id': operation, 'phase': 'fixed_asset_verified', 'catalog_id': identifier, 'asset_id': before['assetId'], 'asset_revision': before.get('assetRevision', before['revision']), 'sha256': item['package_sha256'], 'source': before['source'], 'prior_catalog_id': old['catalog_id'], 'bm_synced_is_not_feishu_sync_success': True}
        receipts = [r for r in receipts if r['row'] != item['row']] + [receipt]
        save(args.receipts, receipts)
        print(json.dumps({'row': item['row'], 'asset_revision': receipt['asset_revision'], 'phase': receipt['phase'], 'verified_count': sum(r['phase'] == 'fixed_asset_verified' for r in receipts)}), flush=True)

if __name__ == '__main__':
    main()
