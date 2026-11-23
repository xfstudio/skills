"""Verify the whole redacted table against planned new attachments and actual result writes."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

from workflow import verify_results


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def expected_uploads(baseline, packages, receipts):
    expected = copy.deepcopy(baseline)
    seen = set()
    for item in packages:
        row = item['row']
        if row in seen or type(row) is not int or row < 2 or row > len(baseline):
            raise ValueError('Duplicate or invalid planned attachment row')
        seen.add(row)
        before = baseline[row - 1]
        if before.get('A') != item['name'] or before.get('I'):
            raise ValueError('New attachment source name or empty-package condition differs')
        if digest(item['package_path']) != item['package_sha256']:
            raise ValueError('Frozen package changed')
        matches = [x for x in receipts if x['source_excel_row'] == row and x['sha256'] == item['package_sha256']]
        if len(matches) != 1:
            raise ValueError('Missing or ambiguous native attachment receipt')
        receipt = matches[0]
        filename = Path(item['package_path']).name
        if (not receipt.get('record_id') or not receipt.get('attachment_replace_readback') or
            receipt.get('new_package') != filename or receipt.get('generation_readback') != '升级更新中' or
            receipt.get('sync_status_readback') != '待同步'):
            raise ValueError('Native attachment/status readback incomplete')
        expected[row - 1].update(I=filename, E='升级更新中', AD='待同步')
    return expected


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['baseline', 'current', 'packages', 'attachment-receipts', 'output']:
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--writebacks', type=Path)
    args = p.parse_args()
    load = lambda path: json.loads(path.read_text())
    packages, receipts = load(args.packages), load(args.attachment_receipts)
    baseline = load(args.baseline)
    expected = expected_uploads(baseline, packages, receipts)
    writes = load(args.writebacks) if args.writebacks else []
    by_row = {x['row']: x for x in packages}
    for plan in writes:
        item = by_row.get(plan['row'])
        if not item or plan['packageName'] != Path(item['package_path']).name or plan['expectedName'] != item['name']:
            raise ValueError('Result plan is not bound to this exact new-package source')
        receipt = next(x for x in receipts if x['source_excel_row'] == plan['row'] and x['sha256'] == item['package_sha256'])
        if plan.get('recordId') != receipt['record_id']:
            raise ValueError('Result/native attachment record ID differs')
    result = verify_results(expected, load(args.current), writes)
    result.update(original_baseline_sha256=digest(args.baseline), current_sha256=digest(args.current),
        packages_sha256=digest(args.packages), attachment_receipts_sha256=digest(args.attachment_receipts),
        planned_attachments=len(packages), scope='whole_table_combined_attachment_and_result_plan',
        intermediate_state_is_derived_expectation_not_an_observed_export=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': result['verified'], 'records': result['records'], 'attachments': len(packages), 'writebacks': len(writes), 'failures': len(result['failures'])}))
    raise SystemExit(0 if result['verified'] else 1)


if __name__ == '__main__':
    main()
