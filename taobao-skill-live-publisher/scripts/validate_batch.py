"""Validate every rebuilt skill without executing packaged scripts or MCP examples."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re
import tempfile
from package_io import files, digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--skill-validator', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('creator_quick_validate', args.skill_validator)
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    catalog = json.loads(args.catalog.read_text())
    results = []
    for item in json.loads(args.manifest.read_text()):
        if digest(item['package_path']) != item['package_sha256'] or digest(item['base_package_path']) != item['base_package_sha256']:
            raise ValueError('Frozen source digest mismatch at row ' + str(item['row']))
        new, old = files(item['package_path']), files(item['base_package_path'])
        if set(new) != set(old):
            raise ValueError('Package file scope changed')
        business = [name for name in old if not name.endswith('.md') and name != 'references/atp-routing.json']
        if any(old[name] != new[name] for name in business):
            raise ValueError('Business implementation changed during catalog migration')
        routing = json.loads(new['references/atp-routing.json'])
        if routing['source_sha256'] != catalog['source_sha256'] or routing['source'] != catalog['source']:
            raise ValueError('Catalog snapshot mismatch')
        for code, contract in routing['contracts'].items():
            expected = catalog['contracts'][code]
            for key in ['version', 'request_schema', 'example_command', 'verification_status']:
                if contract.get(key) != expected.get(key):
                    raise ValueError('Public MCP contract differs from source')
        legacy_labels = 0
        for name, content in new.items():
            if not name.endswith('.md'):
                continue
            for line in content.decode('utf-8').splitlines():
                if re.search(r'(?:mcp__)?taobao__[a-zA-Z0-9_]+', line):
                    if name == 'references/atp-routing.md' and line.startswith('### '):
                        legacy_labels += 1
                    else:
                        raise ValueError('Legacy execution alias remains at row ' + str(item['row']))
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'SKILL.md').write_bytes(new['SKILL.md'])
            ok, message = validator.validate_skill(directory)
            if not ok:
                raise ValueError(str(item['row']) + ': ' + message)
        results.append({'row': item['row'], 'sha256': item['package_sha256'], 'files': len(new), 'quick_validate': True, 'business_files_unchanged': True, 'catalog_bound': True, 'legacy_mapping_labels': legacy_labels, 'business_calls_executed': 0})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(json.dumps({'validated_packages': len(results), 'business_calls_executed': 0}))

if __name__ == '__main__':
    main()
