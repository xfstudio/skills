"""Local batch ledger and exact package gates for the Feishu -> BM -> Taobao UI workflow."""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
from package_io import compare, digest, files


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2))
    temp.replace(path)


def read(path):
    return json.loads(Path(path).read_text())


def merge_result(path, value, preserve=None):
    """Reload and merge one row under a shared process lock; never rewrite stale rows."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.with_suffix(path.suffix+'.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        current=read(path) if path.exists() else []
        if len({x['row'] for x in current})!=len(current):raise ValueError('Duplicate result rows need reconciliation')
        existing=next((x for x in current if x['row']==value['row']),None)
        if preserve:value=preserve(existing,value)
        merged=[x for x in current if x['row']!=value['row']]+[value]
        save(path,merged)
        return merged


def prepare_editor(item, actual, formal_code, editor_url, receipt_path, markers=(), preserved_metadata=None):
    if digest(item['package_path']) != item['package_sha256']:
        raise ValueError('Frozen source changed')
    proof = compare(item['package_path'], actual, formal_code, markers, preserved_metadata)
    expected, current = files(item['package_path']), files(actual)
    changed = sorted(name for name in expected if name not in current or expected[name] != current[name])
    # Existing binary deletions or alterations need a real upload UI, not text coercion.
    if proof['extra']:
        raise ValueError('Unexpected workspace files require explicit reviewed cleanup: ' + str(proof['extra']))
    prepared = []
    for name in changed:
        if name in proof['platform_name_normalization']:
            continue
        try:
            content = expected[name].decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError('Changed binary file requires native ZIP upload: ' + name) from None
        if '\x00' in content:
            raise ValueError('Binary-like file cannot enter the text editor: ' + name)
        prepared.append({'path': name, 'content': content, 'sha256': hashlib.sha256(expected[name]).hexdigest()})
    return {'action': 'update-files', 'row': item['row'], 'formalCode': formal_code,
            'editorUrl': editor_url, 'receiptPath': str(receipt_path), 'files': prepared,
            'expectedPackageSha256': item['package_sha256'], 'zipReadbackRequired': True}


def was_listed_target(target):
    if isinstance(target.get('wasListed'),bool):return target['wasListed']
    lines=[line.strip() for line in target.get('cardBefore','').splitlines() if line.strip()]
    marker=next((i for i,line in enumerate(lines[:-1]) if line.lower()=='appkey' and lines[i+1]==target['publicAppId']),None)
    if marker is None or marker<1:raise ValueError('Original listing-state evidence is missing')
    return '已上架' in lines[1:marker]



def had_listing_target(target):
    if isinstance(target.get('hadListing'),bool):return target['hadListing']
    if was_listed_target(target):return True
    lines=[line.strip() for line in target.get('cardBefore','').splitlines() if line.strip()]
    marker=next((i for i,line in enumerate(lines[:-1]) if line.lower()=='appkey' and lines[i+1]==target['publicAppId']),None)
    if marker is None:raise ValueError('Original listing history is missing')
    return '已下架' in lines[1:marker]


def listed_evidence(result):
    mode=bool(result.get('existing_mode_preserved'))
    if result.get('listing_mode_verified') and result.get('listing_mode') in {'定向订购','公开订购'}:mode=True
    if result.get('listing_kind')=='new':mode=bool(result.get('listing_mode_verified')) and result.get('listing_mode') in {'定向订购','公开订购'}
    authorization=bool(result.get('authorization_preserved'))
    if result.get('listing_kind')=='restore':
        mode=bool(result.get('existing_mode_preserved') and result.get('listing_mode_verified') and result.get('listing_mode') in {'定向订购','公开订购'})
        if result.get('authorization_before_unavailable') and result.get('authorization_current_readback_complete') and result.get('authorization_not_changed_by_workflow') and isinstance(result.get('authorization_current_shops'),list):authorization=True
    return bool(mode and authorization and all(result.get(k) for k in ['online_version','approved_package_verified']))



def version_authorization_allowed(target):
    authorization=target.get('authorizationReadback',{})
    if authorization.get('complete') is True:return True
    menus=target.get('moreMenuBefore')
    return bool(target.get('hadListing') is True and target.get('offlineBefore') is True and target.get('wasListed') is False and authorization.get('unavailableWhileUnlisted') is True and isinstance(menus,list) and all(isinstance(x,str) for x in menus) and all(x in menus for x in ['修改上架详情','编辑技能','版本管理']) and '授权管理' not in menus and target.get('listingBefore',{}).get('mode') in {'0','1'} and {'0':'公开订购','1':'定向订购'}.get(target.get('listingBefore',{}).get('mode'))==target.get('existingMode'))


def publication_gate(item, target, bm, proof, receipt):
    required = ['account', 'publicAppId', 'formalCode', 'editorUrl', 'existingMode', 'authorizationReadback']
    if any(not target.get(key) for key in required):
        raise ValueError('Incomplete live target/account/mode/authorization evidence')
    if not version_authorization_allowed(target):
        raise ValueError('Existing authorization pagination is incomplete')
    if bm.get('phase') != 'fixed_asset_verified' or bm.get('sha256') != item['package_sha256']:
        raise ValueError('BM fixed asset not verified for this package')
    if not proof.get('verified') or proof.get('expected_package_sha256') != item['package_sha256']:
        raise ValueError('Entire workspace ZIP must match the frozen package')
    if receipt.get('phase') in {'version_submitting', 'version_unknown', 'version_review', 'version_approved', 'listed'}:
        raise ValueError('Existing version action must be reconciled; never submit again')
    if target.get('humanActionRequired'):
        raise ValueError('User must handle the visible agreement/verification')
    return True


def verify_source(baseline, current, manifest, original_directory):
    if baseline != current:
        raise ValueError('Source table changed after semantic review')
    proofs = []
    for item in manifest:
        row = item['row']
        path = original_directory / f'{row:04d}.zip'
        if digest(path) != item['source_sha256']:
            raise ValueError('Original package binding changed at ' + str(row))
        proofs.append({'row': row, 'source_sha256': item['source_sha256'], 'source_url': current[row-1].get('source_url'), 'original_download_verified': True})
    return proofs


def verify_feishu(baseline, current, manifest, allowed):
    if len(baseline) != len(current):
        raise ValueError('Record count changed')
    expected = {x['row']: x for x in manifest}
    failures = []
    for row, (before, after) in enumerate(zip(baseline, current), 1):
        item = expected.get(row)
        keys = set(before) | set(after)
        changes = [key for key in keys if before.get(key, '') != after.get(key, '')]
        if any(key not in allowed for key in changes) or (changes and not item):
            failures.append({'row': row, 'unexpected_fields': changes})
        if item and (after.get('I') != Path(item['package_path']).name or after.get('E') != '升级更新中' or after.get('AD') != '待同步'):
            failures.append({'row': row, 'reason': 'attachment_or_status_readback_mismatch'})
    return {'records': len(current)-1, 'packages': len(expected), 'failures': failures, 'verified': not failures}


def result_columns(baseline, writes):
    """Prepare full native clipboard columns while preserving every unplanned cell."""
    result=[dict(row) for row in baseline];seen=set()
    for plan in writes:
        row=plan['row']
        if row in seen or not 2<=row<=len(result):raise ValueError('Duplicate or invalid writeback row')
        seen.add(row);current=result[row-1]
        if current.get('A','').strip()!=plan['expectedName'].strip() or current.get('I','')!=plan['packageName'] or not plan.get('recordId'):
            raise ValueError('Pinned result row or package does not match the latest export')
        if plan.get('formalCode') and current.get('J') and current['J']!=plan['formalCode']:raise ValueError('Formal code conflicts with the verified target')
        if plan.get('currentVersion') and not plan.get('platformVersionConfirmed'):raise ValueError('Unconfirmed platform version')
        if plan.get('onlineVersion') and not plan.get('onlinePackageVerified'):raise ValueError('Unverified online package')
        if plan.get('generationStatus'):
            complete=plan['generationStatus']=='上架完成' and plan.get('listingVerified')
            review=plan['generationStatus']=='技能上架审核中' and plan.get('listingReviewConfirmed')
            if not (complete or review) or not plan.get('onlinePackageVerified'):raise ValueError('Unverified listing cannot complete generation status')
        for key,field in [('J','formalCode'),('F','currentVersion'),('G','onlineVersion'),('E','generationStatus')]:
            if plan.get(field):current[key]=plan[field]
        marker='['+plan['batchId']+']'
        lines=[x for x in current.get('AG','').splitlines() if x and not x.startswith(marker)]
        current['AG']='\n'.join([*lines,marker+' '+plan['resultNote']])
    columns=[]
    for key,caption in [('E','技能生成及状态'),('F','当前版本'),('G','线上版本'),('J','技能code'),('AG','同步说明')]:
        if baseline[0].get(key)!=caption:raise ValueError('Result column schema changed: '+key)
        values=[x.get(key,'') for x in result[1:]]
        if any(not isinstance(x,str) for x in values):raise ValueError('Native clipboard values must be strings')
        if any(a.get(key,'')!=b.get(key,'') for a,b in zip(baseline,result)):
            columns.append({'columnKey':key,'column':caption,'values':values})
    return columns


def verify_results(baseline, current, writes):
    if len(baseline)!=len(current):
        raise ValueError('Record count changed during result writeback')
    by_row={x['row']:x for x in writes};failures=[]
    for row,(before,after) in enumerate(zip(baseline,current),1):
        plan=by_row.get(row)
        changed=[key for key in before.keys()|after.keys() if before.get(key,'')!=after.get(key,'')]
        allowed={'AG'}|{key for key,field in [('J','formalCode'),('F','currentVersion'),('G','onlineVersion'),('E','generationStatus')] if plan and plan.get(field)}
        if (changed and not plan) or any(key not in allowed for key in changed):
            failures.append({'row':row,'unexpected_fields':changed})
        if not plan:continue
        expected={'A':plan['expectedName'],'I':plan['packageName']}
        for key,field in [('J','formalCode'),('F','currentVersion'),('G','onlineVersion'),('E','generationStatus')]:
            if plan.get(field):expected[key]=plan[field]
        for key,value in expected.items():
            if after.get(key,'').strip()!=value.strip():failures.append({'row':row,'field':key,'reason':'planned_value_not_persisted'})
        line='['+plan['batchId']+'] '+plan['resultNote']
        marker='['+plan['batchId']+']'
        preserved=[x for x in before.get('AG','').splitlines() if x and not x.startswith(marker)]
        expected_note='\n'.join([*preserved,line])
        if after.get('AG','').strip()!=expected_note.strip():failures.append({'row':row,'field':'AG','reason':'actual_result_note_missing_or_other_note_changed'})
    return {'records':len(current)-1,'writebacks':len(writes),'failures':failures,'verified':not failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    source = sub.add_parser('verify-source')
    source.add_argument('--baseline', type=Path, required=True)
    source.add_argument('--current', type=Path, required=True)
    source.add_argument('--manifest', type=Path, required=True)
    source.add_argument('--original-directory', type=Path, required=True)
    source.add_argument('--output', type=Path, required=True)
    prep = sub.add_parser('prepare-editor')
    prep.add_argument('--manifest', type=Path, required=True)
    prep.add_argument('--row', type=int, required=True)
    prep.add_argument('--actual', type=Path, required=True)
    prep.add_argument('--formal-code', required=True)
    prep.add_argument('--editor-url', required=True)
    prep.add_argument('--receipt-path', type=Path, required=True)
    prep.add_argument('--output', type=Path, required=True)
    prep.add_argument('--allow-empty-marker', action='append', default=[])
    check = sub.add_parser('verify-feishu')
    check.add_argument('--baseline', type=Path, required=True)
    check.add_argument('--current', type=Path, required=True)
    check.add_argument('--manifest', type=Path, required=True)
    check.add_argument('--allowed-fields', default='I,E,AD')
    check.add_argument('--output', type=Path, required=True)
    results = sub.add_parser('verify-results')
    results.add_argument('--baseline',type=Path,required=True)
    results.add_argument('--current',type=Path,required=True)
    results.add_argument('--writebacks',type=Path,required=True)
    results.add_argument('--output',type=Path,required=True)
    columns=sub.add_parser('prepare-result-columns')
    columns.add_argument('--baseline',type=Path,required=True)
    columns.add_argument('--writebacks',type=Path,required=True)
    columns.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if args.action == 'verify-source':
        result = verify_source(read(args.baseline), read(args.current), read(args.manifest), args.original_directory)
        save(args.output, result)
        print(json.dumps({'original_downloads_verified': len(result)}))
    elif args.action == 'prepare-editor':
        item = next(x for x in read(args.manifest) if x['row'] == args.row)
        result = prepare_editor(item, args.actual, args.formal_code, args.editor_url, args.receipt_path, args.allow_empty_marker)
        save(args.output, result)
        print(json.dumps({'row': args.row, 'changed_text_files': len(result['files']), 'zip_readback_required': True}))
    elif args.action=='prepare-result-columns':
        columns=result_columns(read(args.baseline),read(args.writebacks))
        result={'baseline_sha256':digest(args.baseline),'writebacks_sha256':digest(args.writebacks),'columns':columns};save(args.output,result)
        print(json.dumps({'prepared_columns':[x['columnKey'] for x in columns],'rows':len(read(args.baseline))-1}))
    elif args.action=='verify-results':
        result=verify_results(read(args.baseline),read(args.current),read(args.writebacks))
        result.update(baseline_sha256=digest(args.baseline),current_sha256=digest(args.current),writebacks_sha256=digest(args.writebacks))
        save(args.output,result);print(json.dumps(result))
        if not result['verified']:raise SystemExit(1)
    else:
        result = verify_feishu(read(args.baseline), read(args.current), read(args.manifest), set(args.allowed_fields.split(',')))
        save(args.output, result)
        print(json.dumps(result))
        if not result['verified']:
            raise SystemExit(1)

if __name__ == '__main__':
    main()
