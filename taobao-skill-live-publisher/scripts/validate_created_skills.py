"""Check newly authored ATP ZIPs against fixed source properties and catalog contracts.

This is structural/provenance validation, not semantic review, business execution,
platform publication or merchant-visibility evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile
from creation_provenance import verified_chain, property_view, execution_view


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_item(item, catalog, source_rows, source_hash, validator, provenance=None):
    errors = []
    package, root = Path(item['package_path']), Path(item['skill_path'])
    code = item['formal_code']
    rows = item['source_rows']
    if not rows or len(rows) != len(set(rows)) or item['primary_row'] not in rows:
        errors.append('Invalid source row aliases')
    for row in rows:
        source = source_rows.get(row)
        if not source or not str(source.get('A') or '').strip() or source.get('I'):
            errors.append(f'Row {row} is not a named empty-attachment source')
        elif str(source.get('J') or '').strip() != code:
            errors.append(f'Row {row} formal identity differs; separate reviewed identity required')
    source_hashes, catalog_hashes = provenance[:2] if provenance else ({source_hash}, {catalog['source_sha256']})
    if item['source_snapshot_sha256'] not in source_hashes:
        errors.append('Source snapshot SHA256 differs')
    if item['catalog_sha256'] not in catalog_hashes:
        errors.append('Catalog source SHA256 differs')
    if digest(package) != item['package_sha256']:
        errors.append('Frozen ZIP SHA256 differs')
    with zipfile.ZipFile(package) as archive:
        entries = archive.infolist()
        if len(entries) > 512 or sum(e.file_size for e in entries) > 20 * 1024 * 1024:
            errors.append('Archive size/entry limit exceeded')
        seen = set()
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if entry.filename in seen or path.is_absolute() or '..' in path.parts or '\\' in entry.filename:
                errors.append('Unsafe or duplicate archive path')
                continue
            seen.add(entry.filename)
            if not path.parts or path.parts[0] != item['skill_name']:
                errors.append('Archive root identity differs')
                continue
            if entry.is_dir():
                continue
            if len(path.parts) < 2 or path.parts[1] in {'evals', '__pycache__'}:
                errors.append('Evaluation/cache files included in production ZIP')
                continue
            relative = Path(*path.parts[1:])
            original = root / relative
            if original.is_symlink() or not original.is_file() or archive.read(entry) != original.read_bytes():
                errors.append(f'Archive differs from authored file: {relative}')
        expected = {x['path']: x for x in item['package_files']}
        if set(expected) != seen:
            errors.append('Frozen entry manifest differs')
        for name, info in expected.items():
            if name in seen and hashlib.sha256(archive.read(name)).hexdigest() != info['sha256']:
                errors.append(f'Entry SHA256 differs: {name}')
    contracts = json.loads((root / 'references/mcp-contracts.json').read_text())
    bundled_catalog_hash = contracts.get('source_sha256', contracts.get('catalog_sha256')) if provenance else contracts['source_sha256']
    if bundled_catalog_hash not in catalog_hashes:
        errors.append('Bundled catalog provenance differs')
    for bound_code, contract in contracts['contracts'].items():
        if catalog['contracts'].get(bound_code) != contract:
            errors.append(f'Bundled contract differs from fixed catalog: {bound_code}')
    plan = json.loads((root / 'references/operation-plan.json').read_text())
    if plan['formal_code'] != code:
        errors.append('Exact semantic binding identity differs')
    if provenance:
        try:
            steps, _ = execution_view(plan)
        except ValueError as error:
            errors.append(str(error))
            steps = []
    else:
        if plan.get('execution_bindings_exact') is not True:
            errors.append('Exact semantic binding record missing')
        steps = plan['ordered_execution_plan']
    for step in steps:
        if not step.get('code'):
            continue
        contract = contracts['contracts'].get(step['code'])
        if not contract or step.get('version') != contract['version'] or not contract.get('available'):
            errors.append(f'Execution binding unavailable or wrong version: {step.get("code")}')
    properties = json.loads((root / 'references/source-properties.json').read_text())
    if provenance:
        try:
            prop_hash, prop_rows, prop_records = property_view(properties)
        except ValueError as error:
            errors.append(str(error))
            prop_hash, prop_rows, prop_records = None, [], []
    else:
        prop_hash, prop_rows, prop_records = properties['source_snapshot_sha256'], properties['source_rows'], properties['records']
    if prop_hash not in source_hashes or prop_rows != rows or [x['row'] for x in prop_records] != rows:
        errors.append('Bundled source provenance differs')
    for record in prop_records:
        if any(k in record['properties'] for k in ('Z', 'AA', 'appsecret', 'appSecret')):
            errors.append('Credential column included in properties')
        actual = source_rows.get(record['row'])
        if actual is None or any(actual.get(k) != v for k, v in record['properties'].items()):
            errors.append('Bundled source property differs')
    result = subprocess.run([sys.executable, str(validator), str(root)], text=True, capture_output=True)
    if result.returncode:
        errors.append('Skill creator validation: ' + (result.stdout + result.stderr).strip())
    return {'primary_row': item['primary_row'], 'source_rows': rows, 'formal_code': code,
            'package_sha256': item['package_sha256'], 'passed': not errors, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--skill-validator', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--derived-source', type=Path, help='Explicit source subset; every included row/value is verified against the full export')
    parser.add_argument('--catalog-export', type=Path, help='Raw catalog export backing the normalized catalog JSON hash')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    catalog = json.loads(args.catalog.read_text())
    source = json.loads(args.source.read_text())
    source_rows = {index + 1: item for index, item in enumerate(source)}
    source_hash = digest(args.source)
    provenance = verified_chain(args.source, args.catalog, args.derived_source, args.catalog_export) if args.derived_source or args.catalog_export else None
    items = [validate_item(x, catalog, source_rows, source_hash, args.skill_validator, provenance) for x in manifest['items']]
    codes = [x['formal_code'] for x in items]
    errors = [] if len(codes) == len(set(codes)) else ['Duplicate formal code: canonicalize exact-code aliases']
    report = {'manifest_sha256': digest(args.manifest), 'source_sha256': source_hash,
              'catalog_sha256': catalog['source_sha256'], 'passed': not errors and all(x['passed'] for x in items),
              'items': items, 'errors': errors, 'validation_scope': 'structure_and_fixed_provenance_only',
              'business_calls_executed': 0, 'platform_publication_verified': False}
    if provenance:
        report['verified_representation_chain'] = provenance[2]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'items': len(items), 'passed': report['passed'], 'failed_items': sum(not x['passed'] for x in items)}))
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
