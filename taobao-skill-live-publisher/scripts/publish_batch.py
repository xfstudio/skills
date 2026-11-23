"""Resume real Taobao workspace/version updates from fixed, verified batch sources."""
from __future__ import annotations
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from package_io import collect, compare
from workflow import merge_result, prepare_editor, publication_gate, save


def load(path):
    return json.loads(Path(path).read_text())


class UIStageError(RuntimeError):
    """Observe unexpected UI before any further browser action."""


def reconcile_public_target(prior, public):
    target=prior.get('target',{})
    keys=['account','publicAppId','formalCode']
    if any(not target.get(key) or (public.get(key) and target[key]!=public[key]) for key in keys):
        raise ValueError('Pinned version intent belongs to a different account or target')
    return {**public,**{key:target[key] for key in keys},'searchName':target.get('searchName') or public.get('searchName')}


def preserve_reconciled_evidence(existing, value):
    later={'listed','approved_online_not_listed','approved_online_store_version_pending','version_approved_waiting_online'}
    keys=['package_sha256','public_app_id','formal_code','version']
    if existing and existing.get('phase') in later and value.get('phase')=='version_approved' and all(existing.get(k)==value.get(k) for k in keys):
        return {**value,'prior_reconciliation':existing,'needs_online_recheck':True}
    return value


def reviewed_empty_markers(plan, row):
    """Keep individually reviewed empty paths scoped to their frozen record."""
    if not isinstance(plan, dict):
        raise ValueError('Empty-marker plan must map record rows to reviewed paths')
    extra = plan.get(str(row), [])
    if not isinstance(extra, list) or len(extra) > 20 or any(not isinstance(name, str) for name in extra):
        raise ValueError('Reviewed empty-marker paths must be a bounded list')
    for name in extra:
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or str(path) != name or not name.endswith('/.gitkeep'):
            raise ValueError('Reviewed empty-marker path must be a relative folder/.gitkeep')
    return list(dict.fromkeys(['references/.gitkeep', 'tests/.gitkeep', 'scripts/.gitkeep', *extra]))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=Path,required=True)
    parser.add_argument('--targets',type=Path,required=True)
    parser.add_argument('--space-id',type=int,required=True)
    parser.add_argument('--page',required=True)
    parser.add_argument('--account',required=True)
    parser.add_argument('--downloads-directory',type=Path,required=True)
    parser.add_argument('--fallback-mode',choices=['定向订购','公开订购'],required=True)
    parser.add_argument('--platform-metadata-plan',type=Path,help='Per-row exact hashes of individually reviewed installation sidecars')
    parser.add_argument('--platform-empty-marker-plan',type=Path,help='Per-row individually reviewed extra folder/.gitkeep paths; zero bytes and existing folders remain required')
    parser.add_argument('--prior-version-journal',type=Path,help='Verified previous-batch version intents, allowing an explicitly different upgraded source')
    parser.add_argument('--pause-file',type=Path,help='Pause at the next record boundary when this file exists')
    parser.add_argument('--rows',help='Explicit comma-separated Excel rows; otherwise all frozen packages')
    args=parser.parse_args()
    batch=args.batch.resolve();scripts=Path(__file__).resolve().parent
    manifest=load(batch/'package-manifest.json');selected={int(x) for x in args.rows.split(',')} if args.rows else None
    mappings={x['row']:x for x in load(args.targets)}
    previous_versions=load(args.prior_version_journal) if args.prior_version_journal else []
    metadata_plan=load(args.platform_metadata_plan) if args.platform_metadata_plan else {}
    marker_plan=load(args.platform_empty_marker_plan) if args.platform_empty_marker_plan else {}
    journal_path=batch/'taobao-version-journal.json'
    status_path=batch/'taobao-results.json'
    statuses=load(status_path) if status_path.exists() else []
    stage_root=batch/'platform';stage_root.mkdir(exist_ok=True)
    def record(value):
        nonlocal statuses
        statuses=merge_result(status_path,value,preserve_reconciled_evidence)
        value=next(x for x in statuses if x['row']==value['row'])
        print(json.dumps({'row':value['row'],'phase':value['phase'],'handled':len(statuses)},ensure_ascii=False),flush=True)
    def ui(row,phase,config):
        directory=stage_root/f'{row:04d}';directory.mkdir(exist_ok=True)
        config={**config,'row':row,'resultPath':str(directory/(phase+'-result.json'))}
        config_path=directory/(phase+'-config.json');save(config_path,config)
        with (directory/(phase+'.log')).open('a') as log:
            result=subprocess.run([sys.executable,str(scripts/'browser_cli.py'),'--config',str(config_path),'--space-id',str(args.space_id),'--page',args.page],stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:
            raise UIStageError('UI stage '+phase+' failed; inspect its sanitized local log and reconcile')
        return load(config['resultPath'])
    for item in manifest:
        row=item['row']
        if selected is not None and row not in selected:continue
        if args.pause_file and args.pause_file.exists():
            print(json.dumps({'phase':'paused_at_record_boundary','next_row':row}),flush=True);break
        mapping=mappings.get(row)
        if not mapping:
            record({'row':row,'phase':'target_missing'});continue
        fixed=next((x for x in load(batch/'bm-assets.json') if x['row']==row and x.get('phase')=='fixed_asset_verified' and x['sha256']==item['package_sha256']),None)
        attachment=next((x for x in load(batch/'feishu-attachments.json') if x['source_excel_row']==row and x['sha256']==item['package_sha256']),None)
        if not fixed or not attachment:
            record({'row':row,'phase':'source_not_ready'});continue
        directory=stage_root/f'{row:04d}';directory.mkdir(exist_ok=True)
        public={ 'account':args.account,'publicAppId':mapping['public_app_id'],'formalCode':mapping.get('platform_skill_code'),'searchName':mapping['platform_card']['name'],'fallbackMode':args.fallback_mode}
        try:
            journal=load(journal_path) if journal_path.exists() else []
            prior=next((x for x in journal if x['row']==row and x['packageSha256']==item['package_sha256']),None)
            if prior:
                public=reconcile_public_target(prior,public)
                versions=ui(row,'reconcile',{'action':'taobao-versions',**public})
                matches=[line for line in versions['rows'] if line.split('\t')[0].strip()==prior['version']]
                if len(matches)!=1:
                    record({'row':row,'phase':'version_unknown','version':prior['version'],'package_sha256':item['package_sha256'],'public_app_id':public['publicAppId']});continue
                line=matches[0]
                phase='version_review' if '审核中' in line else 'version_approved' if '审核通过' in line else 'version_rejected' if any(x in line for x in ['拒绝','不通过','驳回']) else 'version_unknown'
                record({'row':row,'phase':phase,'version':prior['version'],'version_readback':line,'package_sha256':item['package_sha256'],'public_app_id':public['publicAppId'],'formal_code':public['formalCode']})
                continue
            target_path=directory/'target.json'
            target=ui(row,'inspect',{'action':'taobao-inspect',**public,'receiptPath':str(target_path)})
            operation=directory/'before-operation.json'
            before_result=ui(row,'before-download',{'action':'download-draft','formalCode':target['formalCode'],'editorUrl':target['editorUrl'],'downloadsDir':str(args.downloads_directory),'operationFile':str(operation)})
            before=directory/'before.zip';collect(before_result,args.downloads_directory,before)
            # A known earlier package under review is not the same operation as
            # this newly authorized catalog upgrade. Unknown pending revisions
            # remain a source conflict; never duplicate an unresolved request.
            pending=[line.split('\t')[0].strip() for line in before_result['versionRecords'].splitlines() if '审核中' in line]
            unresolved=[]
            for version in pending:
                known=next((x for x in previous_versions if x['row']==row and x.get('submitted_version',x.get('version'))==version and x.get('public_app_id')==public['publicAppId'] and x.get('formal_code')==target['formalCode']),None)
                if not known or known.get('package_sha256')==item['package_sha256']:
                    unresolved.append(version)
            if unresolved:
                record({'row':row,'phase':'earlier_version_under_review','pending_versions':unresolved,'package_sha256':item['package_sha256'],'public_app_id':public['publicAppId'],'formal_code':target['formalCode']});continue
            markers=reviewed_empty_markers(marker_plan,row)
            metadata=metadata_plan.get(str(row),{})
            target['normalization']={'emptyMarkers':markers,'preservedMetadata':metadata}
            save(target_path,target)
            editor=prepare_editor(item,before,target['formalCode'],target['editorUrl'],directory/'files.json',markers,metadata)
            if editor['files']:
                # The native download left its version dialog open; close it through the documented UI.
                ui(row,'close-records',{'action':'close-version-records','editorUrl':target['editorUrl']})
                ui(row,'edit',editor)
            operation=directory/'after-operation.json'
            after_result=ui(row,'after-download',{'action':'download-draft','formalCode':target['formalCode'],'editorUrl':target['editorUrl'],'downloadsDir':str(args.downloads_directory),'operationFile':str(operation)})
            after=directory/'after.zip';collect(after_result,args.downloads_directory,after)
            proof=compare(item['package_path'],after,target['formalCode'],markers,metadata);proof_path=directory/'proof.json';save(proof_path,proof)
            if not proof['verified']:
                # Observe the entire saved ZIP first. Restore only exact reviewed
                # text differences once; UI receipts never substitute for bytes.
                save(directory/'proof-before-repair.json',proof)
                repair=prepare_editor(item,after,target['formalCode'],target['editorUrl'],directory/'repair-files.json',markers,metadata)
                if repair['files']:
                    ui(row,'repair-close-records',{'action':'close-version-records','editorUrl':target['editorUrl']})
                    ui(row,'repair-edit',repair)
                    operation=directory/'repaired-operation.json'
                    after_result=ui(row,'repaired-download',{'action':'download-draft','formalCode':target['formalCode'],'editorUrl':target['editorUrl'],'downloadsDir':str(args.downloads_directory),'operationFile':str(operation)})
                    after=directory/'after-repair.zip';collect(after_result,args.downloads_directory,after)
                    proof=compare(item['package_path'],after,target['formalCode'],markers,metadata);save(proof_path,proof)
            if not proof['verified']:
                raise ValueError('Workspace still differs after one observed repair: '+str({key:proof[key] for key in ['missing','extra','changed']}))
            publication_gate(item,target,fixed,proof,{})
            versions=[tuple(map(int,x)) for x in re.findall(r'(?m)^([0-9]+)\.([0-9]+)\.([0-9]+)\t',after_result['versionRecords'])]
            if not versions:raise ValueError('No existing semantic versions were observed')
            major,minor,patch=max(versions);next_version=f'{major}.{minor}.{patch+1}'
            ui(row,'close-records-after',{'action':'close-version-records','editorUrl':target['editorUrl']})
            intent=ui(row,'submit',{'action':'taobao-submit-version','target':target,'proofPath':str(proof_path),'packagePath':item['package_path'],'packageSha256':item['package_sha256'],'bm':fixed,'expectedVersion':next_version,'journalPath':str(journal_path),'note':'依据用户指定的核实后 MCP 目录更新编码、在线版本、嵌套参数及调用示例；未覆盖步骤使用电商浏览器 MCP。保留原业务范围及读写确认边界，工作区整包已核验。'})
            record({'row':row,'phase':intent['phase'],'version':intent['version'],'package_sha256':item['package_sha256'],'public_app_id':public['publicAppId'],'formal_code':target['formalCode']})
            # Read actual review status once, independently of submission success.
            versions=ui(row,'submitted-readback',{'action':'taobao-versions',**public})
            line=next((x for x in versions['rows'] if x.split('\t')[0].strip()==intent['version']),None)
            if line:record({'row':row,'phase':'version_review' if '审核中' in line else 'version_approved' if '审核通过' in line else 'version_unknown','version':intent['version'],'version_readback':line,'package_sha256':item['package_sha256'],'public_app_id':public['publicAppId'],'formal_code':target['formalCode']})
        except Exception as error:
            record({'row':row,'phase':'needs_reconciliation','error_type':type(error).__name__,'reason':str(error),'package_sha256':item['package_sha256'],'public_app_id':public['publicAppId']})
            if isinstance(error,UIStageError):raise

if __name__=='__main__':
    main()
