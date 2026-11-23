"""Validate one reviewed ATP invocation and print it; execute only on explicit request."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess


def validate(value, schema, path='$'):
    kind = schema.get('type')
    checks = {'object': isinstance(value, dict), 'array': isinstance(value, list),
              'string': isinstance(value, str), 'boolean': isinstance(value, bool),
              'number': isinstance(value, (int, float)) and not isinstance(value, bool),
              'integer': isinstance(value, int) and not isinstance(value, bool), 'null': value is None}
    if kind and not checks.get(kind, False):
        return [f'{path}: expected {kind}']
    errors = []
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: value outside documented enum')
    if isinstance(value, dict):
        errors.extend(f'{path}.{key}: required' for key in schema.get('required', []) if key not in value)
        for key, child in schema.get('properties', {}).items():
            if key in value:
                errors.extend(validate(value[key], child, path + '.' + key))
    if isinstance(value, list) and schema.get('items'):
        for index, child in enumerate(value):
            errors.extend(validate(child, schema['items'], f'{path}[{index}]'))
    return errors


def invocation(root, step_id, code, params, allow_write=False):
    plan = json.loads((root / 'references/operation-plan.json').read_text())
    steps = [s for s in plan['steps'] if s['id'] == step_id]
    if len(steps) != 1 or code not in steps[0]['candidate_codes']:
        raise ValueError('Code is outside this exact property step; review the business scope first')
    contracts = json.loads((root / 'references/mcp-contracts.json').read_text())['contracts']
    contract = contracts[code]
    if not contract.get('available') or not contract.get('schema_available'):
        raise ValueError('The directory does not confirm an available request contract')
    write = contract['operation_type'] != '只读查询'
    if write and (not steps[0].get('write_explicit') or not allow_write):
        raise ValueError('Write operation requires an explicit write step and runtime user confirmation')
    errors = validate(params, contract['request_schema'])
    if errors:
        raise ValueError('Request validation failed: ' + '; '.join(errors))
    argv = ['atp', 'invoke', '--code', code, '--version', contract['version'],
            '--params', json.dumps(params, ensure_ascii=False, separators=(',', ':'))]
    return plan, contract, argv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--step', required=True)
    parser.add_argument('--code', required=True)
    parser.add_argument('--params-file', type=Path, required=True)
    parser.add_argument('--allow-write', action='store_true', help='Records that runtime user confirmation has been obtained; never substitutes for it')
    parser.add_argument('--execute', action='store_true', help='Omitted by default; dry-run only prints a validated invocation')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    params = json.loads(args.params_file.read_text())
    plan, contract, argv = invocation(root, args.step, args.code, params, args.allow_write)
    if args.execute:
        if plan.get('review_status') != 'reviewed':
            raise ValueError('Draft operation plan has not passed semantic review; execution is disabled')
        if not shutil.which('atp'):
            raise ValueError('ATP CLI is not available in this execution environment')
        raise SystemExit(subprocess.run(argv).returncode)
    print(json.dumps({'mode': 'dry-run', 'business_call_executed': False,
                      'semantic_review_status': plan['review_status'], 'code': contract['code'],
                      'version': contract['version'], 'operation_type': contract['operation_type'],
                      'directory_verification': contract['verification_status'],
                      'command': shlex.join(argv)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
