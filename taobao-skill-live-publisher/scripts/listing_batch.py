"""Prepare unlisted approved skills and submit only after the user handles their agreements."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from workflow import save, had_listing_target


def read(path):return json.loads(Path(path).read_text())


def fields(metadata):
    if not 0<len(metadata['description'])<45 or not 0<len(metadata['query'])<100:raise ValueError('Listing description/query exceeds reviewed platform limits')
    result=[{'placeholder':'一句话简要描述你的技能','value':metadata['description']},{'placeholder':'商家调用技能后，可自动显示当前预置query的文案内容','value':metadata['query']}]
    for key,placeholders in [('functions',['功能名称，如"查询商品基础信息"','功能说明，如"获取商品标题、价格、销量等数据"']),('examples',['使用场景，如"退款分析"','提问示例，如"帮我分析一下店铺的退款情况"'])]:
        if len(metadata[key])!=2:raise ValueError('The observed form requires two reviewed function/example rows')
        for index,(name,detail) in enumerate(metadata[key]):
            if not 0<len(name)<=12 or not 0<len(detail)<=50:raise ValueError('Listing function/example limits exceeded')
            result.extend({'placeholder':placeholder,'index':index,'value':value} for placeholder,value in zip(placeholders,[name,detail]))
    result.extend([{'placeholder':'用户调用技能时需传入的参数','value':metadata['input']},{'placeholder':'技能执行后返回的结果内容及格式','value':metadata['output']}])
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=Path,required=True)
    parser.add_argument('--metadata',type=Path,required=True)
    parser.add_argument('--pages',type=Path,required=True,help='Explicit row-to-existing-Ego-page mapping')
    parser.add_argument('--verification-page',required=True,help='Separate existing Ego page used for a fresh online-version gate')
    parser.add_argument('--space-id',type=int,required=True)
    parser.add_argument('--action',choices=['prepare','submit'],required=True)
    parser.add_argument('--user-agreement-handled',action='store_true',help='Use only after the user confirms handling the prepared platform agreements')
    args=parser.parse_args();batch=args.batch.resolve();scripts=Path(__file__).resolve().parent
    if args.action=='submit' and not args.user_agreement_handled:raise ValueError('User agreement action is required; the script never checks the box')
    metadata=read(args.metadata)['rows'];pages=read(args.pages)
    if args.verification_page in pages.values():raise ValueError('Verification page must not replace a prepared listing form')
    metadata_sha=hashlib.sha256(args.metadata.read_bytes()).hexdigest()
    manifest={x['row']:x for x in read(batch/'package-manifest.json')}
    results={x['row']:x for x in read(batch/'taobao-results.json')}
    intents={x['row']:x for x in read(batch/'taobao-version-journal.json')}
    preparation_path=batch/'listing-preparation-plan.json'
    preparations=read(preparation_path) if preparation_path.exists() else []
    for row_key,page in pages.items():
        row=int(row_key);result=results[row];item=manifest[row];intent=intents[row];target=intent['target']
        if result['phase']=='listed':continue
        if had_listing_target(target):raise ValueError('Existing offline listing must use its native restoration path; preserve its saved metadata')
        if result['phase']!='approved_online_not_listed' or not result.get('approved_package_verified') or result.get('online_version')!=intent['version']:raise ValueError('No verified approved online package awaiting listing at row '+str(row))
        if result['package_sha256']!=item['package_sha256'] or intent['packageSha256']!=item['package_sha256']:raise ValueError('Listing source changed')
        proof=read(result['approved_proof_path']);binding=proof.get('approvalBinding',{})
        expected={'account':target['account'],'publicAppId':target['publicAppId'],'formalCode':target['formalCode'],'version':intent['version'],'packageSha256':item['package_sha256'],'downloadVersion':intent['version']}
        if not proof.get('verified') or proof.get('expected_package_sha256')!=item['package_sha256'] or any(binding.get(k)!=v for k,v in expected.items()) or binding.get('actualDownloadSha256')!=proof.get('actual_download_sha256'):raise ValueError('Approved package proof identity mismatch')
        directory=batch/'platform'/f'{row:04d}';mode={'定向订购':'1','公开订购':'0'}[target['existingMode']]
        cfg={'row':row,'account':target['account'],'publicAppId':target['publicAppId'],'formalCode':target['formalCode'],'searchName':target['searchName'],'mode':mode,'fields':fields(metadata[row_key]),'receiptPath':str(directory/'listing-prepared.json'),'packageSha256':item['package_sha256'],'approvedVersion':intent['version'],'approvedVersionPackageProof':proof,'journalPath':str(batch/'taobao-listing-journal.json')}
        # Fresh UI evidence is independent of cached reconciliation and the
        # agreement form; stop if an operator changed the live version.
        verify_cfg={'action':'taobao-versions','row':row,'account':target['account'],'publicAppId':target['publicAppId'],'formalCode':target['formalCode'],'searchName':target['searchName'],'resultPath':str(directory/('listing-online-'+args.action+'-result.json'))}
        verify_path=directory/('listing-online-'+args.action+'-config.json');save(verify_path,verify_cfg)
        with (directory/('listing-online-'+args.action+'.log')).open('a') as log:
            process=subprocess.run([sys.executable,str(scripts/'browser_cli.py'),'--space-id',str(args.space_id),'--page',args.verification_page,'--config',str(verify_path)],stdout=log,stderr=subprocess.STDOUT)
        if process.returncode:raise RuntimeError('Current online-version readback needs observation; do not submit listing')
        actual=read(verify_cfg['resultPath'])
        online=[entry for entry in actual['entries'] if entry['onlineStatus']=='线上版本']
        if len(online)!=1 or online[0]['version']!=intent['version'] or online[0]['reviewStatus']!='审核通过':raise ValueError('Current online version drifted; stop and review the prepared listing')
        cfg['onlineObservation']={'account':target['account'],'publicAppId':target['publicAppId'],'formalCode':target['formalCode'],'version':intent['version'],'packageSha256':item['package_sha256'],'versionReadback':online[0]['raw'],'reviewStatus':online[0]['reviewStatus'],'onlineStatus':online[0]['onlineStatus'],'observedAt':datetime.now(timezone.utc).isoformat()}
        if metadata[row_key].get('iconPath'):
            cfg.update(iconPath=metadata[row_key]['iconPath'],iconSha256=metadata[row_key]['iconSha256'])
        if args.action=='prepare':cfg['action']='taobao-prepare-listing'
        else:
            prepared=next((x for x in preparations if x['row']==row),None)
            if not prepared or prepared['page']!=page or prepared['metadataSha256']!=metadata_sha or prepared['packageSha256']!=item['package_sha256'] or prepared['version']!=intent['version']:raise ValueError('Prepared listing plan changed before user agreement')
            cfg.update(action='taobao-submit-listing',userAgreementHandled=True)
        cfg['resultPath']=str(directory/('listing-'+args.action+'-result.json'))
        config=directory/('listing-'+args.action+'-config.json');save(config,cfg)
        with (directory/('listing-'+args.action+'.log')).open('a') as log:
            process=subprocess.run([sys.executable,str(scripts/'browser_cli.py'),'--space-id',str(args.space_id),'--page',page,'--config',str(config)],stdout=log,stderr=subprocess.STDOUT)
        if process.returncode:raise RuntimeError('Listing UI needs observation at row '+str(row)+'; reconcile any existing intent, do not repeat')
        outcome=read(cfg['resultPath'])
        if args.action=='prepare':
            if outcome.get('alreadyListed'):raise RuntimeError('Listing appeared externally; reconcile before preparing this row')
            entry={'row':row,'page':page,'metadataSha256':metadata_sha,'packageSha256':item['package_sha256'],'version':intent['version'],'preparedReceipt':cfg['receiptPath'],'userAgreementRequired':outcome.get('userAgreementRequired',True)}
            preparations=[x for x in preparations if x['row']!=row]+[entry];save(preparation_path,preparations)
        print(json.dumps({'row':row,'action':args.action,'phase':outcome.get('phase','prepared'),'agreement_checked_by_script':False}),flush=True)

if __name__=='__main__':main()
