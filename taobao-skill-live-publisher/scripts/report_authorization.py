"""Report a complete pinned authorization run only after exact Feishu readback."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
from authorization_batch import targets
from package_io import digest
from workflow import read, save


def report(batch, directory, writebacks, verification):
    values = read(directory / 'authorization-results.json')
    expected = {item['row']: (item, target) for item, target in targets(batch)}
    by_row = {x['row']: x for x in values}
    if len(by_row) != len(values) or set(by_row) != set(expected):
        raise ValueError('Every pinned manifest target must have one current authorization outcome')
    proof = read(verification)
    plans = read(writebacks)
    if not proof.get('verified') or proof.get('writebacks_sha256') != digest(writebacks) or proof.get('writebacks') != len(expected):
        raise ValueError('Full current Feishu authorization writeback verification required')
    plan_map = {x['row']: x for x in plans}
    if len(plan_map) != len(plans) or set(plan_map) != set(expected):
        raise ValueError('Writebacks do not cover exactly this run')
    binding = read(directory / 'run-binding.json')
    if binding['manifestSha256'] != digest(batch / 'package-manifest.json') or binding['versionJournalSha256'] != digest(batch / 'taobao-version-journal.json'):
        raise ValueError('Run target binding changed')
    rows = []
    for row, result in sorted(by_row.items()):
        item, target = expected[row]
        if result.get('account') != target['account'] or result.get('publicAppId') != target['publicAppId'] or result.get('merchant') != binding['merchant'] or result.get('packageSha256') != item['package_sha256']:
            raise ValueError('Receipt target or merchant mismatch')
        if plan_map[row].get('authorizationPhase') != result['phase'] or plan_map[row].get('authorizationMerchant') != binding['merchant'] or plan_map[row].get('authorizationResultsSha256') != digest(directory / 'authorization-results.json'):
            raise ValueError('Writeback describes an older authorization result')
        auth = result.get('authorization') or {}
        verified = result['phase'] in {'already_authorized', 'authorization_added'}
        if verified and (not result.get('listed') or not auth.get('complete') or binding['merchant'] not in auth.get('shops', [])):
            raise ValueError('Claimed authorization success lacks complete live evidence')
        rows.append({'row': row, 'name': item['name'], 'appkey': target['publicAppId'], 'formal_code': target['formalCode'],
                     'merchant': binding['merchant'], 'phase': result['phase'], 'listed': result.get('listed'),
                     'authorization_verified': verified, 'current_shop_count': len(auth.get('shops', [])),
                     'observed_at': result.get('observedAt', ''), 'feishu_note_verified': True})
    path = directory / 'authorization-report.csv'
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = dict(Counter(x['phase'] for x in values))
    summary = {'targets': len(expected), 'merchant': binding['merchant'], 'phases': counts,
               'directed_authorized_verified': sum(x['authorization_verified'] for x in rows),
               'new_authorizations_verified': counts.get('authorization_added', 0),
               'all_listed_directed_targets_verified': all(x['phase'] in {'already_authorized', 'authorization_added', 'public_listing', 'not_listed'} for x in values),
               'feishu_notes_verified': len(plans), 'merchant_client_visibility_verified': False, 'report': str(path)}
    save(directory / 'authorization-summary.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--authorization-directory', type=Path, required=True)
    parser.add_argument('--writebacks', type=Path, required=True)
    parser.add_argument('--verification', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(report(args.batch.resolve(), args.authorization_directory.resolve(), args.writebacks, args.verification), ensure_ascii=False))


if __name__ == '__main__':
    main()
