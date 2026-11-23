"""Prepare upload metadata from pinned native evidence; preserve the raw Feishu export."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(source, source_hash, capture, packages):
    if capture.get('source_snapshot_sha256') != source_hash:
        raise ValueError('Native capture is not bound to this source export')
    if capture.get('table_id') != 'tbl5c1ONsL2wKKNs':
        raise ValueError('Native capture target table differs')
    if source[0].get('H') != '技能包链接' or source[0].get('I') != '自建技能包':
        raise ValueError('Source field schema differs')
    native = capture['records']
    if len({x['source_excel_row'] for x in native}) != len(native):
        raise ValueError('Duplicate native row binding')
    if len({x['record_id'] for x in native}) != len(native):
        raise ValueError('Native record ID is bound to multiple source rows')
    by_row = {x['source_excel_row']: x for x in native}
    baseline = json.loads(json.dumps(source))
    bindings, additions = [], []
    seen = set()
    for item in packages:
        row = item['row']
        if row in seen or not isinstance(row, int) or row < 2 or row > len(source):
            raise ValueError('Invalid or duplicate package source row')
        seen.add(row)
        before = source[row - 1]
        proof = by_row.get(row)
        if not proof or not proof.get('record_id') or not proof.get('observed_at'):
            raise ValueError(f'No pinned native record evidence at row {row}')
        if not before.get('A') or before.get('I'):
            raise ValueError(f'Not a named empty-attachment source at row {row}')
        if proof['name'] != before['A'].strip() or proof['formal_code'] != str(before.get('J') or '').strip():
            raise ValueError(f'Native identity differs at row {row}')
        if item['name'] != before['A']:
            raise ValueError(f'Package source name differs at row {row}')
        if proof.get('field_caption') != '技能包链接' or proof.get('attachment_files') != []:
            raise ValueError(f'Native source link field evidence incomplete at row {row}')
        url = proof.get('source_url')
        if not isinstance(url, str):
            raise ValueError('Native URL must be an explicit string')
        if not url:
            if proof.get('anchors') != [] or proof.get('field_text') != '技能包链接':
                raise ValueError(f'Native link field is not proven empty at row {row}')
        elif not url.startswith('https://') or proof.get('anchors') != [url]:
            raise ValueError(f'Native URL evidence inconsistent at row {row}')
        raw_link = before.get('H')
        if raw_link not in (None, '') and raw_link != url:
            raise ValueError(f'Raw export/native source URL differs at row {row}')
        if raw_link in (None, '') and url:
            raise ValueError(f'Raw export omitted a nonempty native URL at row {row}')
        if 'source_url' in before and ('' if before['source_url'] is None else before['source_url']) != url:
            raise ValueError(f'Existing derived URL differs at row {row}')
        path = Path(item['package_path'])
        if digest(path) != item['package_sha256']:
            raise ValueError(f'Frozen package changed at row {row}')
        if 'source_url' not in before:
            baseline[row - 1]['source_url'] = url
            additions.append({'row': row, 'record_id': proof['record_id'], 'metadata_key': 'source_url', 'value': url})
        bindings.append({'source_excel_row': row, 'record_id': proof['record_id'], 'name': proof['name'],
                         'formal_code': proof['formal_code'], 'source_url': url, 'files': proof['files']})
    return baseline, bindings, additions


def save_frozen(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    if path.exists() and path.read_bytes() != raw:
        raise ValueError(f'Refusing to overwrite a different prepared artifact: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--native-capture', type=Path, required=True)
    p.add_argument('--packages', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    args = p.parse_args()
    baseline, bindings, additions = prepare(json.loads(args.source.read_text()), digest(args.source),
        json.loads(args.native_capture.read_text()), json.loads(args.packages.read_text()))
    save_frozen(args.output_dir / 'verified-upload-baseline.json', baseline)
    save_frozen(args.output_dir / 'record-bindings.json', bindings)
    save_frozen(args.output_dir / 'upload-baseline-preparation-proof.json', {
        'parent_source_sha256': digest(args.source), 'native_capture_sha256': digest(args.native_capture),
        'packages_sha256': digest(args.packages), 'derived_baseline_sha256': digest(args.output_dir / 'verified-upload-baseline.json'),
        'metadata_additions': additions, 'raw_source_modified': False,
        'whole_table_verification_baseline': str(args.source.resolve()),
    })
    print(json.dumps({'records': len(bindings), 'metadata_additions': len(additions), 'external_writes': 0}))


if __name__ == '__main__':
    main()
