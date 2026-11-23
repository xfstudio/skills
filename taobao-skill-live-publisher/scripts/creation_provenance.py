"""Explicit adapters for fixed creation-source representations, without rewriting ZIPs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verified_chain(source_path, catalog_path, derived_source=None, catalog_export=None):
    source = json.loads(Path(source_path).read_text())
    catalog = json.loads(Path(catalog_path).read_text())
    source_hashes = {digest(source_path)}
    catalog_hashes = {catalog['source_sha256']}
    chain = {'full_source_sha256': digest(source_path), 'catalog_contracts_sha256': digest(catalog_path)}
    if derived_source:
        subset = json.loads(Path(derived_source).read_text())
        seen = set()
        for record in subset:
            row = record.get('row')
            if type(row) is not int or row < 2 or row > len(source) or row in seen:
                raise ValueError('Invalid or duplicate derived source row')
            seen.add(row)
            actual = source[row - 1]
            if actual.get('I'):
                raise ValueError('Derived missing-source row has an existing attachment')
            for key, value in record.items():
                if key == 'row':
                    continue
                if not re.fullmatch(r'[A-Z]{1,2}', key) or key in {'Z', 'AA'} or actual.get(key) != value:
                    raise ValueError(f'Derived source property differs at row {row}: {key}')
        source_hashes.add(digest(derived_source))
        chain['derived_source_sha256'] = digest(derived_source)
        chain['derived_rows_verified'] = len(subset)
    if catalog_export:
        if digest(catalog_export) != catalog['source_sha256']:
            raise ValueError('Catalog export differs from the fixed catalog provenance')
        catalog_hashes.add(digest(catalog_path))
        chain['catalog_export_sha256'] = digest(catalog_export)
    return source_hashes, catalog_hashes, chain


def property_view(value):
    """Normalize only known authored record containers, preserving every source value."""
    records = value.get('records', value.get('rows'))
    if not isinstance(records, list) or not records:
        raise ValueError('Bundled source records missing')
    normalized = []
    for record in records:
        if not isinstance(record, dict) or type(record.get('row')) is not int:
            raise ValueError('Invalid bundled source record')
        properties = record.get('properties')
        if properties is None:
            properties = {k: v for k, v in record.items() if k != 'row'}
        if not isinstance(properties, dict) or any(not re.fullmatch(r'[A-Z]{1,2}', k) or k in {'Z', 'AA'} for k in properties):
            raise ValueError('Invalid or credential-bearing source properties')
        normalized.append({'row': record['row'], 'properties': properties})
    source_hash = value.get('source_snapshot_sha256', value.get('source_snapshot_file_sha256'))
    return source_hash, value.get('source_rows', [r['row'] for r in normalized]), normalized


def execution_view(plan):
    """Return actual execution bindings; never traverse documented/not-bound contracts."""
    if 'exact_atp_steps' in plan:
        if plan.get('authoring_readiness') != 'ready_conditional_runtime_evidence':
            raise ValueError('Unreviewed exact-step authoring representation')
        roots = plan['exact_atp_steps']
        representation = 'exact_atp_steps_v1'
    elif 'execution_bindings' in plan:
        if plan.get('execution_bindings_exact') is not True:
            raise ValueError('Exact binding review marker missing')
        roots = list(plan['execution_bindings'].values())
        representation = 'execution_bindings_v1'
    else:
        if plan.get('execution_bindings_exact') is not True or not isinstance(plan.get('ordered_execution_plan'), list):
            raise ValueError('Exact execution plan missing')
        roots = plan['ordered_execution_plan']
        representation = 'ordered_execution_plan_v1'
    bindings = []

    def walk(node):
        if isinstance(node, list):
            for child in node:
                walk(child)
        elif isinstance(node, dict):
            if node.get('code'):
                bindings.append({'code': node['code'], 'version': node.get('version')})
            if 'ordered_steps' in node:
                walk(node['ordered_steps'])

    walk(roots)
    if 'executable_atp_codes' in plan and set(plan['executable_atp_codes']) != {x['code'] for x in bindings}:
        raise ValueError('Executable code allowlist differs from actual bindings')
    return bindings, representation
