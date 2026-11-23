"""Bind current merchant-authorization receipts to Feishu records; update notes only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from authorization_batch import targets
from package_io import digest
from workflow import read, save


def prepare(batch, directory, baseline, bindings, batch_id):
    bound = read(directory / 'run-binding.json')
    if bound['manifestSha256'] != digest(batch / 'package-manifest.json') or bound['versionJournalSha256'] != digest(batch / 'taobao-version-journal.json'):
        raise ValueError('Authorization run target binding changed')
    records = {x['source_excel_row']: x for x in bindings}
    items = {item['row']: (item, target) for item, target in targets(batch)}
    results = read(directory / 'authorization-results.json')
    if len({x['row'] for x in results}) != len(results):
        raise ValueError('Duplicate authorization result rows')
    output = []
    for result in results:
        row = result['row']
        item, target = items[row]
        if any(result.get(k) != expected for k, expected in [('account', target['account']), ('publicAppId', target['publicAppId']), ('formalCode', target['formalCode']), ('merchant', bound['merchant']), ('manifestSha256', bound['manifestSha256']), ('packageSha256', item['package_sha256'])]):
            raise ValueError('Authorization receipt belongs to another target or merchant')
        phase = result['phase']
        if phase in {'already_authorized', 'authorization_added'}:
            auth = result.get('authorization', {})
            if not result.get('listed') or '定向' not in result.get('statusLabels', []) or not auth.get('complete') or bound['merchant'] not in auth.get('shops', []):
                raise ValueError('No complete listed-skill authorization proof')
            if phase == 'authorization_added' and not result.get('existingShopsPreserved'):
                raise ValueError('Original authorization scope not verified after addition')
            text = '已补齐并回读核验定向授权' if phase == 'authorization_added' else '已有定向授权，完整名单回读核验通过'
            text += f"；目标店铺：{bound['merchant']}；当前授权店铺共 {len(auth['shops'])} 家"
        elif phase == 'public_listing':
            text = '当前为公开上架，未改动订购方式或添加定向授权；商家实际订购及客户端展示未验证'
        elif phase == 'not_listed':
            text = '当前未上架，未执行店铺授权或恢复上架；状态：' + '、'.join(result.get('statusLabels', []))
        elif phase == 'authorization_missing':
            text = f"未发现 {bound['merchant']} 的定向授权；本次仅核验，未提交授权"
        elif phase in {'authorization_unknown', 'needs_reconciliation'}:
            text = '定向授权结果待核对，未重复提交；目标店铺：' + bound['merchant']
        else:
            raise ValueError('Unknown authorization result phase')
        text += f"；淘宝 AppID {target['publicAppId']}；核验时间 {result.get('observedAt', '见本次回执')}；商家端实际展示与调用未验证。"
        current = baseline[row-1]
        if current.get('A', '').strip() != item['name'].strip() or current.get('I') != Path(item['package_path']).name:
            raise ValueError('Latest Feishu record or attachment changed')
        output.append({'row': row, 'recordId': records[row]['record_id'], 'expectedName': item['name'].strip(),
                       'packageName': Path(item['package_path']).name, 'batchId': batch_id, 'resultNote': text,
                       'authorizationResultsSha256': digest(directory / 'authorization-results.json'),
                       'authorizationPhase': phase, 'authorizationMerchant': bound['merchant'],
                       'formalCode': None, 'currentVersion': None, 'onlineVersion': None, 'generationStatus': None})
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--authorization-directory', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--bindings', type=Path, required=True)
    parser.add_argument('--batch-id', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = prepare(args.batch.resolve(), args.authorization_directory.resolve(), read(args.baseline), read(args.bindings), args.batch_id)
    save(args.output, output)
    print(json.dumps({'authorization_notes': len(output), 'fields': ['AG']}))


if __name__ == '__main__':
    main()
