"""Download explicit public source ZIP URLs from a redacted Feishu UI inventory."""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
import urllib.request
from package_io import files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--allowed-origin', action='append', required=True)
    args = parser.parse_args()
    rows = json.loads(args.inventory.read_text())
    manifest = json.loads(args.manifest.read_text())
    args.output_directory.mkdir(parents=True, exist_ok=True)
    def download(item):
        row = rows[item['row']-1]
        if row.get('A','').strip() != item['name'].strip():
            raise ValueError('Source record name binding changed')
        url = row.get('source_url')
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or parsed.username or parsed.scheme+'://'+parsed.netloc not in args.allowed_origin:
            raise ValueError('Source URL is not an explicitly allowed public origin')
        with urllib.request.urlopen(url, timeout=90) as response:
            final = urlsplit(response.url)
            if final.scheme+'://'+final.netloc not in args.allowed_origin:
                raise ValueError('Source download redirected outside the allowed origin')
            raw = response.read(10*1024*1024+1)
        if len(raw)>10*1024*1024:
            raise ValueError('Source ZIP exceeds size limit')
        sha = hashlib.sha256(raw).hexdigest()
        if sha != item['source_sha256']:
            raise ValueError('Source changed since semantic review at row ' + str(item['row']))
        path=args.output_directory/f"{item['row']:04d}.zip"
        path.write_bytes(raw)
        files(path)
        return {'row':item['row'],'source_url':url,'sha256':sha,'path':str(path.resolve()),'public_download_verified':True}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(download,manifest))
    args.receipts.write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print(json.dumps({'source_zip_downloads_verified':len(results),'business_calls_executed':0}))

if __name__=='__main__':
    main()
