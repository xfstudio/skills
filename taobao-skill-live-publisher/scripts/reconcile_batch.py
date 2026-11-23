"""Reconcile review, approved version bytes, online status, listing and preserved shops."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import subprocess
import sys
import zipfile
from package_io import collect, compare, digest
from workflow import merge_result, save, was_listed_target, had_listing_target


def read(path):return json.loads(Path(path).read_text())


class UIStageError(RuntimeError):
    """Observe unexpected UI before any further browser action."""



def cached_approved_package(item,target,version,directory):
    """Reuse only a locally rechecked ZIP bound to the immutable approved revision."""
    if digest(item['package_path'])!=item['package_sha256']:raise ValueError('Frozen source changed before reconciliation')
    actual=directory/('approved-'+version+'.zip');proof_path=directory/('approved-'+version+'-proof.json')
    try:
        proof=read(proof_path);binding=proof.get('approvalBinding',{})
        expected={'account':target['account'],'publicAppId':target['publicAppId'],'formalCode':target['formalCode'],'version':version,'packageSha256':item['package_sha256'],'downloadVersion':version}
        if not proof.get('verified') or proof.get('expected_package_sha256')!=item['package_sha256'] or any(binding.get(k)!=v for k,v in expected.items()):return None
        if binding.get('actualDownloadSha256')!=proof.get('actual_download_sha256') or digest(actual)!=proof['actual_download_sha256']:return None
        normalization=target.get('normalization',{})
        checked=compare(item['package_path'],actual,target['formalCode'],normalization.get('emptyMarkers',['references/.gitkeep']),normalization.get('preservedMetadata',{}))
        if not checked['verified'] or checked['expected_package_sha256']!=item['package_sha256']:return None
        return proof,proof_path
    except (OSError,ValueError,zipfile.BadZipFile):
        return None


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=Path,required=True)
    parser.add_argument('--space-id',type=int,required=True)
    parser.add_argument('--page',required=True)
    parser.add_argument('--rows',help='Optional comma-separated Excel rows to reconcile')
    parser.add_argument('--restore-existing-listings',action='store_true',help='Only with explicit user authorization: restore existing offline listings without changing saved metadata or shop authorization')
    parser.add_argument('--downloads-directory',type=Path,required=True)
    args=parser.parse_args()
    selected={int(x) for x in args.rows.split(',')} if args.rows else None
    batch=args.batch.resolve();scripts=Path(__file__).resolve().parent
    manifest={x['row']:x for x in read(batch/'package-manifest.json')}
    journal_path=batch/'taobao-version-journal.json'
    journal=read(journal_path) if journal_path.exists() else []
    path=batch/'taobao-results.json';results=read(path) if path.exists() else []
    def record(value):
        nonlocal results
        results=merge_result(path,value)
        print(json.dumps({'row':value['row'],'phase':value['phase']},ensure_ascii=False),flush=True)
    def ui(row,phase,cfg):
        directory=batch/'platform'/f'{row:04d}';directory.mkdir(parents=True,exist_ok=True)
        cfg={**cfg,'row':row,'resultPath':str(directory/(phase+'-result.json'))}
        config=directory/(phase+'-config.json');save(config,cfg)
        with (directory/(phase+'.log')).open('a') as log:
            process=subprocess.run([sys.executable,str(scripts/'browser_cli.py'),'--config',str(config),'--space-id',str(args.space_id),'--page',args.page],stdout=log,stderr=subprocess.STDOUT)
        if process.returncode:raise UIStageError('Reconcile UI stage '+phase+' needs observation; do not repeat its mutation')
        return read(cfg['resultPath'])
    for intent in journal:
        if 'row' not in intent or 'target' not in intent:continue
        row=intent['row']
        if selected is not None and row not in selected:continue
        item=manifest[row]
        if item['package_sha256']!=intent['packageSha256']:continue
        target=intent['target'];version=intent['version'];directory=batch/'platform'/f'{row:04d}'
        public={'account':target['account'],'publicAppId':target['publicAppId'],'formalCode':target['formalCode'],'searchName':target.get('searchName') or target['listingBefore']['fields'][0]['value']}
        base={'row':row,'version':version,'public_app_id':target['publicAppId'],'formal_code':target['formalCode'],'package_sha256':item['package_sha256']}
        try:
            cached=cached_approved_package(item,target,version,directory)
            review_cfg={'action':'taobao-versions',**public}
            if not cached:review_cfg['approvedDownload']={'version':version,'downloadsDir':str(args.downloads_directory),'operationFile':str(directory/'approved-download-operation.json')}
            versions=ui(row,'review-readback',review_cfg)
            matches=[x for x in versions['entries'] if x['version']==version]
            if len(matches)!=1:
                record({**base,'phase':'version_unknown'});continue
            entry=matches[0];line=entry['raw']
            if entry['reviewStatus']=='审核中':
                record({**base,'phase':'version_review','version_readback':line});continue
            if entry['reviewStatus']!='审核通过':
                record({**base,'phase':'version_rejected_or_unknown','version_readback':line});continue
            if cached:
                proof,proof_path=cached
            else:
                downloaded=versions.get('approvedDownload')
                if not downloaded or downloaded.get('account')!=target['account'] or downloaded.get('publicAppId')!=target['publicAppId'] or downloaded.get('version')!=version or downloaded.get('reviewStatus')!='审核通过':raise ValueError('No matching native approved-version download')
                actual=directory/('approved-'+version+'.zip');collect(downloaded,args.downloads_directory,actual)
                normalization=target.get('normalization',{})
                proof=compare(item['package_path'],actual,target['formalCode'],normalization.get('emptyMarkers',['references/.gitkeep']),normalization.get('preservedMetadata',{}))
                proof['approvalBinding']={'account':target['account'],'publicAppId':target['publicAppId'],'formalCode':target['formalCode'],'version':version,'packageSha256':item['package_sha256'],'downloadVersion':downloaded['version'],'actualDownloadSha256':proof['actual_download_sha256']}
                proof_path=directory/('approved-'+version+'-proof.json');save(proof_path,proof)
                if not proof['verified'] or proof['expected_package_sha256']!=item['package_sha256']:raise ValueError('Approved version package differs from the frozen source')
            if entry['onlineStatus']!='线上版本':
                ui(row,'activate-approved',{'action':'taobao-activate-version',**public,'version':version,'packageSha256':item['package_sha256'],'packageProof':proof,'journalPath':str(batch/'taobao-online-journal.json')})
                refreshed=ui(row,'online-readback',{'action':'taobao-versions',**public})
                entry=next((x for x in refreshed['entries'] if x['version']==version),{});line=entry.get('raw','')
                if entry.get('reviewStatus')!='审核通过' or entry.get('onlineStatus')!='线上版本':
                    record({**base,'phase':'version_approved_waiting_online','version_readback':line,'approved_package_verified':True,'approved_proof_path':str(proof_path)});continue
            card=ui(row,'store-readback',{'action':'taobao-card',**public})
            listing_history=read(batch/'taobao-listing-journal.json') if (batch/'taobao-listing-journal.json').exists() else []
            pending_listing=next((x for x in listing_history if x.get('account')==target['account'] and x.get('publicAppId')==target['publicAppId'] and x.get('action') in {'listing','restore_listing'}),None)
            if not card['listed'] and card.get('previouslyListed') and had_listing_target(target) and args.restore_existing_listings and not pending_listing:
                pending_listing=ui(row,'restore-existing-listing',{'action':'taobao-restore-listing',**public,'restoreExistingListingAuthorized':True,'existingListing':target['listingBefore'],'mode':{'定向订购':'1','公开订购':'0'}[target['existingMode']],'approvedVersion':version,'packageSha256':item['package_sha256'],'approvedVersionPackageProof':proof,'journalPath':str(batch/'taobao-listing-journal.json')})
                card=ui(row,'restored-store-readback',{'action':'taobao-card',**public})
            if not card['listed']:
                phase='listing_review' if card['listingReview'] else 'approved_online_not_listed'
                record({**base,'phase':phase,'listing_review_confirmed':card['listingReview'],'online_version':version,'approved_package_verified':True,'approved_proof_path':str(proof_path),'card_readback':card['text'],'listing_outcome_unknown':bool(pending_listing and not card['listingReview']),'reason':'上架操作已有意图，当前仍未上架；回执待核对，未重复提交' if pending_listing and not card['listingReview'] else ''});continue
            displayed=re.search(r'当前版本\s+(\d+\.\d+\.\d+)',card['text'])
            if not displayed or displayed.group(1)!=version:
                record({**base,'phase':'approved_online_store_version_pending','online_version':version,'approved_package_verified':True,'approved_proof_path':str(proof_path),'card_readback':card['text']});continue
            after_cfg={'action':'taobao-inspect',**public,'skipEditorOpen':True,'fallbackMode':target['existingMode'],'receiptPath':str(directory/'target-after.json')}
            if target['authorizationReadback'].get('complete'):after_cfg['expectedExistingShops']=target['authorizationReadback']['shops']
            after=ui(row,'authorization-after',after_cfg)
            if after['existingMode']!=target['existingMode']:raise ValueError('Listing mode changed')
            record({**base,'phase':'listed','online_version':version,'approved_package_verified':True,'approved_proof_path':str(proof_path),'card_readback':card['text'],'listing_kind':'update' if was_listed_target(target) else 'restore' if had_listing_target(target) else 'new','listing_mode':after['existingMode'],'listing_mode_verified':True,'existing_mode_preserved':had_listing_target(target),'authorization_preserved':bool(target['authorizationReadback'].get('complete')),'authorization_before_unavailable':bool(target['authorizationReadback'].get('unavailableWhileUnlisted')),'authorization_current_readback_complete':bool(after['authorizationReadback'].get('complete')),'authorization_current_shops':after['authorizationReadback']['shops'],'authorization_not_changed_by_workflow':True})
        except Exception as error:
            record({**base,'phase':'needs_reconciliation','error_type':type(error).__name__,'reason':str(error)})
            if isinstance(error,UIStageError):raise

if __name__=='__main__':main()
