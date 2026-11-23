"""Derive a fresh evaluation registry from the current frozen creation manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(items, iteration):
    if not isinstance(iteration, int) or iteration < 1:
        raise ValueError('A positive fresh iteration is required')
    runs, workspaces = [], set()
    for item in items:
        skill = Path(item['skill_path']).resolve()
        package = Path(item['package_path'])
        if digest(package) != item['package_sha256']:
            raise ValueError('Frozen package changed: ' + str(package))
        with zipfile.ZipFile(package) as archive:
            name = item['skill_name'] + '/SKILL.md'
            if archive.read(name) != (skill / 'SKILL.md').read_bytes():
                raise ValueError('Evaluation subject differs from frozen production skill')
        cases = sorted((skill / 'evals').iterdir())
        cases = [case for case in cases if case.is_dir()]
        if len(cases) < 2:
            raise ValueError('Each creation skill requires at least two cases')
        for case in cases:
            if case.is_symlink() or not case.resolve().is_relative_to(skill):
                raise ValueError('Case escaped the current skill root')
            workspace = skill.parent / (skill.name + '-workspace') / f'iteration-{iteration}' / case.name
            if workspace in workspaces or workspace.exists():
                raise ValueError('Refusing to reuse or overwrite an evaluation workspace: ' + str(workspace))
            workspaces.add(workspace)
            files = sorted(x for x in (case / 'files').rglob('*') if x.is_file())
            if any(x.is_symlink() or not x.resolve().is_relative_to(case) for x in files):
                raise ValueError('Evaluation input escaped its case root')
            runs.append({'skill_path': str(skill), 'case_path': str(case), 'workspace': str(workspace),
                'primary_row': item['primary_row'], 'package_sha256': item['package_sha256'],
                'skill_md_sha256': digest(skill / 'SKILL.md'), 'prompt_sha256': digest(case / 'prompt.md'),
                'prompt': (case / 'prompt.md').read_text(), 'input_files': [str(x) for x in files],
                'input_sha256': {str(x.relative_to(case / 'files')): digest(x) for x in files}})
    return runs


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--iteration', type=int, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise ValueError('Refusing to overwrite an existing evaluation registry')
    runs = prepare(json.loads(args.manifest.read_text())['items'], args.iteration)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(runs, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cases': len(runs), 'registry_sha256': digest(args.output), 'external_writes': 0}))


if __name__ == '__main__':
    main()
