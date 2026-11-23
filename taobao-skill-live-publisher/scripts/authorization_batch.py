"""Audit pinned listed skills and add one explicitly authorized merchant if missing."""
from __future__ import annotations
import argparse
import fcntl
import json
from pathlib import Path
import subprocess
import sys
from package_io import digest
from workflow import merge_result, read, save


def targets(batch):
    manifest = read(batch / 'package-manifest.json')
    intents = read(batch / 'taobao-version-journal.json')
    if len({x['row'] for x in manifest}) != len(manifest):
        raise ValueError('Duplicate manifest rows')
    output = []
    for item in manifest:
        matches = [x for x in intents if x.get('row') == item['row'] and x.get('packageSha256') == item['package_sha256']]
        if len(matches) != 1:
            raise ValueError('One exact frozen-package target intent is required per manifest row')
        target = matches[0]['target']
        if not all(target.get(k) for k in ['account', 'publicAppId', 'formalCode', 'searchName']):
            raise ValueError('Incomplete pinned target')
        output.append((item, target))
    if len({(t['account'], t['publicAppId']) for _, t in output}) != len(output):
        raise ValueError('Duplicate public targets')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    parser.add_argument('--merchant', required=True)
    parser.add_argument('--space-id', type=int, required=True)
    parser.add_argument('--page', required=True)
    parser.add_argument('--ensure', action='store_true', help='Only with explicit user authorization: add this merchant when missing')
    parser.add_argument('--rows', help='Optional comma-separated manifest rows')
    parser.add_argument('--resume', action='store_true', help='Keep completed observations in this same fixed run; recheck unresolved rows')
    parser.add_argument('--pause-file', type=Path)
    args = parser.parse_args()
    batch = args.batch.resolve()
    directory = args.output_directory.resolve()
    directory.mkdir(parents=True, exist_ok=True)
    scripts = Path(__file__).resolve().parent
    selected = {int(x) for x in args.rows.split(',')} if args.rows else None
    binding = {'batch': str(batch), 'manifestSha256': digest(batch / 'package-manifest.json'),
               'versionJournalSha256': digest(batch / 'taobao-version-journal.json'), 'merchant': args.merchant,
               'ensureAuthorization': args.ensure}
    binding_path = directory / 'run-binding.json'
    if binding_path.exists() and read(binding_path) != binding:
        raise ValueError('Existing run belongs to different targets, packages, merchant, or mutation permission')
    save(binding_path, binding)
    # Both the parent-run lock and intent ledger span output directories.
    # A new report directory is never a way to retry an unknown grant.
    with (batch / 'authorization-batch.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for item, target in targets(batch):
            row = item['row']
            if selected is not None and row not in selected:
                continue
            if args.pause_file and args.pause_file.exists():
                print(json.dumps({'paused_before_row': row}), flush=True)
                return
            results_path = directory / 'authorization-results.json'
            previous = next((x for x in read(results_path) if x['row'] == row), None) if results_path.exists() else None
            if args.resume and previous and previous['phase'] in {'already_authorized', 'authorization_added', 'not_listed', 'public_listing'}:
                continue
            stage = directory / f'{row:04d}'
            stage.mkdir(exist_ok=True)
            cfg = {'action': 'taobao-ensure-authorization', 'row': row, **{k: target[k] for k in ['account', 'publicAppId', 'formalCode', 'searchName']},
                   'merchant': args.merchant, 'ensureAuthorization': args.ensure, 'manifestSha256': binding['manifestSha256'],
                   'packageSha256': item['package_sha256'], 'journalPath': str(batch / 'taobao-authorization-journal.json'),
                   'resultPath': str(stage / 'result.json')}
            config_path = stage / 'config.json'
            save(config_path, cfg)
            with (stage / 'browser.log').open('a') as log:
                run = subprocess.run([sys.executable, str(scripts / 'browser_cli.py'), '--space-id', str(args.space_id),
                                      '--page', args.page, '--config', str(config_path)], stdout=log, stderr=subprocess.STDOUT)
            if run.returncode:
                merge_result(results_path, {'row': row, 'account': target['account'], 'publicAppId': target['publicAppId'],
                                           'formalCode': target['formalCode'], 'merchant': args.merchant, 'phase': 'needs_reconciliation',
                                           'manifestSha256': binding['manifestSha256'], 'packageSha256': item['package_sha256'],
                                           'reason': 'Native UI requires observation; never repeat an existing authorization intent'})
                raise RuntimeError(f'Authorization UI row {row} needs observation; no automatic retry')
            value = read(Path(cfg['resultPath']))
            if any(value.get(k) != cfg[k] for k in ['row', 'account', 'publicAppId', 'formalCode', 'merchant', 'manifestSha256', 'packageSha256']):
                raise ValueError('Authorization receipt target binding changed')
            merge_result(results_path, value)
            print(json.dumps({'row': row, 'phase': value['phase']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
