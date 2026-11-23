"""Export an evidence-bound batch status report without equating pending or BM sync with listing."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
from workflow import listed_evidence


def read(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=Path,required=True)
    parser.add_argument('--verified-writebacks',type=Path)
    parser.add_argument('--verification',type=Path)
    args=parser.parse_args();batch=args.batch.resolve()
    manifest=read(batch/'package-manifest.json',[])
    results={x['row']:x for x in read(batch/'taobao-results.json',[])}
    assets={x['row']:x for x in read(batch/'bm-assets.json',[])}
    verified_plans={};verified=set()
    if args.verified_writebacks or args.verification:
        if not (args.verified_writebacks and args.verification):raise ValueError('Both writeback plan and fresh export proof are required')
        proof=read(args.verification,{})
        sha=hashlib.sha256(args.verified_writebacks.read_bytes()).hexdigest()
        if not proof.get('verified') or proof.get('writebacks_sha256')!=sha:raise ValueError('Writeback proof does not match this plan')
        verified_plans={x['row']:x for x in read(args.verified_writebacks,[])}
    rows=[]
    for item in manifest:
        row=item['row'];result=results.get(row,{});asset=assets.get(row,{})
        if result.get('package_sha256') and result['package_sha256']!=item['package_sha256']:raise ValueError('Result source mismatch at row '+str(row))
        phase=result.get('phase','not_started')
        if phase=='listed' and not listed_evidence(result):raise ValueError('Incomplete listed evidence at row '+str(row))
        plan=verified_plans.get(row,{})
        if plan.get('packageSha256')==item['package_sha256'] and plan.get('platformPhase')==phase and (not plan.get('currentVersion') or plan['currentVersion']==result.get('version')) and (not plan.get('onlineVersion') or plan['onlineVersion']==result.get('online_version')):
            verified.add(row)
        rows.append({'来源Excel行':row,'技能名称':item['name'],'技能code':result.get('formal_code',''),'公开AppID':result.get('public_app_id',''),'包SHA256':item['package_sha256'],'BM固定修订':asset.get('asset_revision',''),'上架方式':result.get('listing_mode',''),'处理类型':result.get('listing_kind',''),'授权核验说明':'原授权一致' if result.get('authorization_preserved') else '下架前名单不可读取；当前名单已回读，本批未增删授权' if result.get('authorization_before_unavailable') and result.get('authorization_current_readback_complete') else '','实际阶段':phase,'已提交淘宝版本':result.get('version',''),'已核验线上版本':result.get('online_version','') if result.get('approved_package_verified') else '', '飞书结果整表核验':'已核验' if row in verified else '待核验','待处理原因':result.get('reason','')})
    output=batch/'publication-report.csv'
    with output.open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]) if rows else []);writer.writeheader();writer.writerows(rows)
    summary={'packages':len(manifest),'actual_phases':dict(Counter(x['实际阶段'] for x in rows)),'feishu_results_verified':len(verified),'report':str(output)}
    (batch/'publication-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
