"""Prepare exact Feishu result notes from actual Taobao and BM receipts, never inferred success."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from workflow import listed_evidence, save


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=Path,required=True)
    parser.add_argument('--bindings',type=Path,required=True)
    parser.add_argument('--batch-id',required=True)
    parser.add_argument('--baseline',type=Path,required=True,help='Latest redacted target-table export for concurrent-field checks')
    args=parser.parse_args();batch=args.batch.resolve()
    read=lambda path:json.loads(path.read_text())
    manifest=read(batch/'package-manifest.json')
    baseline=read(args.baseline)
    results={x['row']:x for x in read(batch/'taobao-results.json')}
    bindings={x['source_excel_row']:x for x in read(args.bindings)}
    assets={x['row']:x for x in read(batch/'bm-assets.json')}
    notes={
        'version_review':'淘宝版本 {version} 审核中',
        'version_requested':'淘宝版本 {version} 已提交，审核结果待回查',
        'version_approved':'淘宝版本 {version} 审核通过，线上版本及商店状态待核验',
        'version_approved_waiting_online':'淘宝版本 {version} 审核通过，等待上线回读',
        'approved_online_store_version_pending':'淘宝版本 {version} 已上线，商店展示版本仍待核对',
        'approved_online_not_listed':'淘宝版本 {version} 已上线，商店上架待处理',
        'listing_review':'淘宝版本 {version} 已上线，商店上架审核中',
        'listed':'淘宝技能已上架，已核验线上版本 {version} 及对应包，既有订购方式和授权保持一致',
        'earlier_version_under_review':'本批待发布，平台已有审核中版本，需先核对该版本结果',
        'needs_reconciliation':'平台结果需核对，按原目标回查后继续，不重复提交',
        'version_unknown':'淘宝版本结果未知，需回查原提交',
        'version_rejected':'淘宝版本 {version} 未通过审核，需按平台原因处理',
        'version_rejected_or_unknown':'淘宝版本 {version} 审核未确认通过，需核对平台原因',
        'source_not_ready':'本批来源附件或 BM 固定资产尚待核验',
        'target_missing':'尚未取得唯一淘宝目标映射',
    }
    output=[]
    for item in manifest:
        row=item['row'];result=results.get(row)
        if not result:continue
        if result.get('package_sha256') and result['package_sha256']!=item['package_sha256']:
            raise ValueError('Platform result belongs to a different frozen package')
        asset=assets.get(row)
        if not asset or asset.get('sha256')!=item['package_sha256'] or asset.get('phase')!='fixed_asset_verified':
            raise ValueError('No verified BM source for writeback row '+str(row))
        phase=result['phase']
        if phase=='listed' and not listed_evidence(result):
            raise ValueError('Insufficient evidence to write listed success')
        if phase not in notes:raise ValueError('Unmapped actual platform phase: '+phase)
        text=notes[phase].format(version=result.get('version','待核对'))
        if result.get('listing_outcome_unknown'):text=f"淘宝版本 {result.get('version','待核对')} 已上线，上架操作回执待核对；当前仍未上架，未重复提交"
        if phase=='needs_reconciliation' and result.get('version_intent_recorded') is False:text='本批版本尚未提交；'+result.get('reason_zh','平台页面待恢复后继续核对')
        if phase=='listed' and result.get('listing_kind')=='new':text=f"淘宝技能按{result['listing_mode']}新上架，已核验线上版本 {result['version']} 及对应包，上架前的授权保持一致"
        if phase=='listed' and result.get('listing_kind')=='restore':
            scope='原授权名单一致' if result.get('authorization_preserved') else '下架时原授权名单不可读取，已回读当前名单，本批未增删授权'
            text=f"淘宝技能按既有{result['listing_mode']}恢复上架，已核验线上版本 {result['version']} 及对应包；{scope}"
        if result.get('public_app_id'):text+='；淘宝 AppID '+result['public_app_id']
        text+=f"；BM 固定资产修订 {asset['asset_revision']}，包 SHA256 {item['package_sha256']}；飞书同步状态：待同步。"
        binding=bindings[row]
        confirmed=phase in {'version_review','version_approved','version_approved_waiting_online','approved_online_not_listed','approved_online_store_version_pending','listing_review','listed','version_rejected','version_rejected_or_unknown'}
        online=result.get('online_version') if result.get('approved_package_verified') else None
        output.append({'row':row,'platformPhase':phase,'packageSha256':item['package_sha256'],'recordId':binding['record_id'],'expectedName':item['name'].strip(),'packageName':Path(item['package_path']).name,'expectedGenerationStatus':baseline[row-1].get('E',''),'generationStatus':'上架完成' if phase=='listed' else '技能上架审核中' if phase=='listing_review' else None,'listingVerified':phase=='listed','listingReviewConfirmed':bool(result.get('listing_review_confirmed')),'expectedCurrentVersion':baseline[row-1].get('F',''),'expectedOnlineVersion':baseline[row-1].get('G',''),'batchId':args.batch_id,'resultNote':text,'formalCode':result.get('formal_code'),'currentVersion':result.get('version') if confirmed else None,'platformVersionConfirmed':confirmed,'onlineVersion':online,'onlinePackageVerified':bool(online),'receiptPath':str(batch/'platform'/f'{row:04d}'/'feishu-result.json')})
    save(batch/'feishu-writeback-plan.json',output)
    print(json.dumps({'prepared_actual_result_notes':len(output)}))

if __name__=='__main__':main()
