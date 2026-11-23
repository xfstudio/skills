"""Collect the native initial-draft ZIP, including preserved original-upload filenames."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import time
import zipfile

from package_io import compare, digest


def collect(operation, creation, expected, directory, output, timeout=45):
    expected, directory, output = Path(expected), Path(directory), Path(output)
    if (creation.get('phase') != 'created_identity_verified' or not creation.get('publicAppId') or
        creation.get('row') != operation.get('row') or creation.get('formalCode') != operation.get('formalCode') or
        creation.get('packageSha256') != digest(expected) or operation.get('version') != '当前草稿'):
        raise ValueError('Matching verified new identity and recorded native initial-draft action required')
    if output.exists():
        raise ValueError('Existing collection output needs reconciliation; refusing overwrite')
    started = operation.get('startedAt')
    if not isinstance(started, (int, float)) or not isinstance(operation.get('files'), list):
        raise ValueError('Native download start and before-file evidence required')
    deadline = time.monotonic() + timeout
    while True:
        candidates = [p for p in directory.glob('*.zip') if p.name not in operation['files'] and
                      p.stat().st_mtime >= started - 2 and
                      (p.name.startswith(operation['formalCode']) or p.name == expected.name or
                       p.name.endswith('-' + expected.name)) and zipfile.is_zipfile(p)]
        if len(candidates) > 1:
            raise ValueError('Ambiguous new native download; reconcile without guessing')
        if candidates:
            native = candidates[0]
            proof = compare(expected, native, operation['formalCode'])
            if not proof['verified']:
                raise ValueError('Native initial-draft ZIP differs from the frozen source package')
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(native, output)
            return {'path': str(output.resolve()), 'sha256': digest(output), 'native_filename': native.name,
                    'native_mtime': native.stat().st_mtime, 'native_source_path': str(native.resolve()),
                    'version': '当前草稿', 'publicAppId': creation['publicAppId'],
                    'formalCode': operation['formalCode'], 'package_proof': proof}
        if time.monotonic() >= deadline:
            raise RuntimeError('No unique completed matching native initial-draft download')
        time.sleep(1)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--operation', type=Path, required=True)
    p.add_argument('--creation-receipt', type=Path, required=True)
    p.add_argument('--expected', type=Path, required=True)
    p.add_argument('--directory', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--receipt', type=Path, required=True)
    args = p.parse_args()
    operation = json.loads(args.operation.read_text())
    if operation.get('collectedOutput'):
        if Path(operation['collectedOutput']) != args.output.resolve() or digest(args.output) != operation['collectedSha256']:
            raise ValueError('Completed native collection changed')
        saved = json.loads(args.receipt.read_text())
        if saved['sha256'] != digest(args.output):
            raise ValueError('Collection receipt changed')
        print(json.dumps({'resumed': True, 'sha256': saved['sha256']}))
        return
    if args.receipt.exists():
        raise ValueError('Existing collection receipt needs reconciliation')
    creation = json.loads(args.creation_receipt.read_text())
    result = collect(operation, creation, args.expected, args.directory, args.output)
    result.update(operation_sha256=digest(args.operation), creation_receipt_sha256=digest(args.creation_receipt))
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    operation.update(collectedOutput=result['path'], collectedSha256=result['sha256'])
    args.operation.write_text(json.dumps(operation, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'sha256': result['sha256'], 'native_filename': result['native_filename']}))


if __name__ == '__main__':
    main()
