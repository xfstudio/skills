"""Verify frozen package content and collect only an explicitly requested UI download."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import time
import zipfile
from build_batch import read_archive


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def files(path):
    raw = read_archive(path)
    skills = [name for name in raw if name.split('/')[-1] == 'SKILL.md']
    if not skills:
        raise ValueError('No SKILL.md')
    depth = min(name.count('/') for name in skills)
    main = [name for name in skills if name.count('/') == depth]
    if len(main) != 1:
        raise ValueError('Ambiguous primary SKILL.md')
    prefix = main[0][:-len('SKILL.md')]
    if any(not name.startswith(prefix) for name in raw):
        raise ValueError('File outside primary skill root')
    return {name[len(prefix):]: data for name, data in raw.items()}


def compare(expected, actual, formal_code, allowed_empty_markers=(), preserved_metadata=None):
    if not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', formal_code):
        raise ValueError('Verified formal code required')
    left, right = files(expected), files(actual)
    changed, normalized = [], []
    for name in sorted(left.keys() & right.keys()):
        if left[name] == right[name]:
            continue
        if name == 'SKILL.md':
            a, b = left[name].splitlines(keepends=True), right[name].splitlines(keepends=True)
            difference = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
            if len(a) == len(b) and len(difference) == 1:
                i = difference[0]
                # Only a frontmatter name line may be normalized by the platform.
                front_end = next((j for j in range(1, len(a)) if a[j].strip() == b'---'), 0)
                if a[0].strip() == b'---' and i < front_end and a[i].startswith(b'name: ') and b[i].rstrip(b'\r\n') == ('name: ' + formal_code).encode() and a[i].endswith(b'\r\n') == b[i].endswith(b'\r\n'):
                    normalized.append(name)
                    continue
        changed.append(name)
    markers = []
    source_folders = {n.rsplit('/', 1)[0] for n in left if '/' in n}
    for name in allowed_empty_markers:
        if name not in right or name in left:
            continue
        folder = name.rsplit('/', 1)[0]
        isolated_cache = folder.endswith('/__pycache__') and folder.rsplit('/', 1)[0] in source_folders and not any(n.startswith(folder + '/') and n != name for n in right)
        if not name.endswith('/.gitkeep') or (folder not in source_folders and not isolated_cache):
            raise ValueError('Only explicit existing-folder or isolated empty-cache markers can be allowed')
        if name in right and name not in left:
            if right[name] != b'':
                raise ValueError('Nonempty platform marker is not allowed')
            markers.append(name)
    metadata = {}
    allowed_keys = {'skillId','skillCode','skillName','skillDescription','skillVersion','dataSensitive','source','installedAt','createMethod','createdAt','ossUploaded'}
    for name, expected_sha in (preserved_metadata or {}).items():
        if name != '.version.json' or name in left or name not in right:
            raise ValueError('Only explicitly reviewed extra installation metadata can be preserved')
        raw = right[name]
        value = json.loads(raw)
        current_schema = isinstance(value, dict) and set(value) == allowed_keys and value.get('skillCode') == formal_code and value.get('createMethod') == 'zip-install' and value.get('source') == 'user-created'
        legacy_schema = isinstance(value, dict) and set(value) == {'createdAt', 'source'} and value.get('source') == 'user-created'
        if legacy_schema:
            try:
                legacy_schema = isinstance(value['createdAt'], str) and datetime.fromisoformat(value['createdAt'].replace('Z', '+00:00')).tzinfo is not None
            except ValueError:
                legacy_schema = False
        if not (current_schema or legacy_schema):
            raise ValueError('Unknown installation metadata schema or target code')
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha != expected_sha:
            raise ValueError('Reviewed installation metadata changed')
        metadata[name] = actual_sha
    missing, extra = sorted(left.keys() - right.keys()), sorted(right.keys() - left.keys() - set(markers) - metadata.keys())
    return {'formal_code': formal_code, 'expected_package_sha256': digest(expected), 'actual_download_sha256': digest(actual),
            'expected_files': len(left), 'actual_files': len(right), 'missing': missing, 'extra': extra,
            'changed': changed, 'platform_name_normalization': normalized, 'empty_platform_markers': markers, 'preserved_installation_metadata': metadata,
            'verified': not (missing or extra or changed)}


def collect(operation, directory, output):
    code = operation['formalCode']
    if not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', code):
        raise ValueError('Invalid download prefix')
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        candidates = [p for p in Path(directory).glob(code + '*.zip')
                      if p.name not in operation['files'] and p.stat().st_mtime >= operation['startedAt'] - 2]
        valid = [p for p in candidates if zipfile.is_zipfile(p)]
        if len(valid) > 1:
            raise ValueError('Ambiguous native downloads; reconcile instead of guessing')
        if valid:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(valid[0], output)
            return {'path': str(Path(output).resolve()), 'sha256': digest(output)}
        time.sleep(1)
    raise RuntimeError('No completed matching UI download; do not infer package content')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    check = sub.add_parser('compare')
    check.add_argument('--expected', type=Path, required=True)
    check.add_argument('--actual', type=Path, required=True)
    check.add_argument('--formal-code', required=True)
    check.add_argument('--output', type=Path, required=True)
    check.add_argument('--allow-empty-marker', action='append', default=[])
    native = sub.add_parser('collect')
    native.add_argument('--operation', type=Path, required=True)
    native.add_argument('--directory', type=Path, required=True)
    native.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.action == 'compare':
        result = compare(args.expected, args.actual, args.formal_code, args.allow_empty_marker)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        print(json.dumps(result, ensure_ascii=False))
        if not result['verified']:
            raise SystemExit(1)
    else:
        operation = json.loads(args.operation.read_text())
        if operation.get('collectedOutput'):
            if Path(operation['collectedOutput']) != args.output.resolve() or digest(args.output) != operation['collectedSha256']:
                raise ValueError('This native download intent was already collected elsewhere')
            result = {'path': operation['collectedOutput'], 'sha256': operation['collectedSha256'], 'resumed': True}
        else:
            result = collect(operation, args.directory, args.output)
            operation.update(collectedOutput=result['path'], collectedSha256=result['sha256'])
            args.operation.write_text(json.dumps(operation, ensure_ascii=False, indent=2))
        print(json.dumps(result))

if __name__ == '__main__':
    main()
