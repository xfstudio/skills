"""Inventory all package-bearing SOP rows and freeze public ZIPs before semantic review."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.request
from urllib.parse import urlsplit
from package_io import files, digest
from workflow import save


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory',type=Path,required=True)
    parser.add_argument('--output-directory',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--allowed-origin',action='append',required=True)
    parser.add_argument('--download-receipts',type=Path,help='Reuse only URL+SHA-bound prior native/public downloads')
    args=parser.parse_args()
    rows=json.loads(args.inventory.read_text())
    prior={x['row']:x for x in json.loads(args.download_receipts.read_text())} if args.download_receipts else {}
    args.output_directory.mkdir(parents=True,exist_ok=True)
    result=[];manual=[]
    for row,values in enumerate(rows[1:],2):
        url=values.get('source_url') or values.get('H','')
        if not url:
            if values.get('I'):manual.append({'row':row,'name':values.get('A',''),'reason':'attachment_requires_logged_in_UI_download'})
            continue
        parsed=urlsplit(url)
        if parsed.scheme!='https' or parsed.username or parsed.scheme+'://'+parsed.netloc not in args.allowed_origin:
            manual.append({'row':row,'name':values.get('A',''),'reason':'URL_requires_logged_in_UI_or_origin_review'});continue
        known=prior.get(row)
        if known and known['source_url']==url and digest(known['path'])==known['sha256']:
            path=Path(known['path']);sha=known['sha256']
        else:
            with urllib.request.urlopen(url,timeout=90) as response:
                final=urlsplit(response.url)
                if final.scheme+'://'+final.netloc not in args.allowed_origin:raise ValueError('Unexpected download redirect')
                raw=response.read(10*1024*1024+1)
            if len(raw)>10*1024*1024:raise ValueError('ZIP size limit exceeded')
            sha=hashlib.sha256(raw).hexdigest()
            path=args.output_directory/f'{row:04d}-{sha[:12]}.zip'
            try:
                with path.open('xb') as writer:writer.write(raw)
            except FileExistsError:
                if digest(path)!=sha:raise ValueError('Existing frozen download differs') from None
        content=files(path)
        text=content['SKILL.md'].decode('utf-8')
        front=re.match(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)',text,re.S)
        named=re.search(r'^name:[ \t]*(.*?)[ \t]*$',front.group(1),re.M) if front else None
        source_name=named.group(1).strip('"\'') if named else None
        canonical=source_name if source_name and re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',source_name) else None
        result.append({'row':row,'name':values.get('A',''),'source_skill_name':source_name,'skill_name':canonical,'original_package_path':str(path.resolve()),'source_sha256':sha,'source_url':url,'semantic_review_required':True})
    save(args.output,{'records':len(rows)-1,'packages':result,'manual_UI_rows':manual,'no_package_records':len(rows)-1-len(result)-len(manual)})
    print(json.dumps({'downloaded_or_verified_packages':len(result),'manual_UI_rows':len(manual),'no_package_records':len(rows)-1-len(result)-len(manual)}))

if __name__=='__main__':main()
