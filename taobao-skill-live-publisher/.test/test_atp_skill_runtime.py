"""Offline checks for operation scope and draft execution boundaries."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'scripts/atp_skill_runtime.py'
SPEC = importlib.util.spec_from_file_location('atp_skill_runtime', SOURCE)
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


class RuntimeBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'references').mkdir()
        self.plan = {'review_status': 'draft', 'steps': [
            {'id': 'read', 'candidate_codes': ['read-code'], 'write_explicit': False},
            {'id': 'write', 'candidate_codes': ['write-code'], 'write_explicit': True}]}
        self.contracts = {code: {'code': code, 'version': '0.1.0', 'available': True,
            'schema_available': True, 'operation_type': kind, 'verification_status': 'fixture',
            'request_schema': {'type': 'object', 'required': ['entity'], 'properties': {
                'entity': {'type': 'string'}, 'ids': {'type': 'array', 'items': {'type': 'integer'}}}}}
            for code, kind in [('read-code', '只读查询'), ('write-code', '写操作')]}
        self.save()

    def save(self):
        (self.root / 'references/operation-plan.json').write_text(json.dumps(self.plan))
        (self.root / 'references/mcp-contracts.json').write_text(json.dumps({'contracts': self.contracts}))

    def test_cannot_select_code_from_other_step(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            runtime.invocation(self.root, 'read', 'write-code', {'entity': 'fixture'}, True)

    def test_write_needs_confirmation_record(self):
        with self.assertRaisesRegex(ValueError, 'confirmation'):
            runtime.invocation(self.root, 'write', 'write-code', {'entity': 'fixture'})

    def test_write_cannot_be_inferred_from_confirmation_alone(self):
        self.plan['steps'][0]['candidate_codes'].append('write-code')
        self.save()
        with self.assertRaisesRegex(ValueError, 'explicit write step'):
            runtime.invocation(self.root, 'read', 'write-code', {'entity': 'fixture'}, True)

    def test_unavailable_contract_rejected(self):
        self.contracts['read-code']['available'] = False
        self.save()
        with self.assertRaisesRegex(ValueError, 'available'):
            runtime.invocation(self.root, 'read', 'read-code', {'entity': 'fixture'})

    def test_nested_required_and_boolean_not_integer(self):
        schema = {'type': 'object', 'required': ['request'], 'properties': {'request': {
            'type': 'object', 'required': ['ids'], 'properties': {
                'ids': {'type': 'array', 'items': {'type': 'integer'}}}}}}
        self.assertEqual(runtime.validate({'request': {}}, schema), ['$.request.ids: required'])
        self.assertEqual(runtime.validate({'request': {'ids': [True]}}, schema), ['$.request.ids[0]: expected integer'])

    def test_user_text_stays_one_json_argv_value(self):
        text = "茶叶' $(printf injected); `id`"
        _, _, argv = runtime.invocation(self.root, 'read', 'read-code', {'entity': text})
        self.assertEqual(argv[:3], ['atp', 'invoke', '--code'])
        self.assertEqual(json.loads(argv[-1]), {'entity': text})
        self.assertEqual(len(argv), 8)

    def test_draft_execute_never_reaches_atp(self):
        scripts = self.root / 'scripts'
        scripts.mkdir()
        shutil.copyfile(SOURCE, scripts / 'atp_call.py')
        params = self.root / 'params.json'
        params.write_text(json.dumps({'entity': 'fixture'}))
        fake = self.root / 'atp'
        marker = self.root / 'executed'
        fake.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\n')
        fake.chmod(0o700)
        result = subprocess.run([sys.executable, str(scripts / 'atp_call.py'), '--step', 'read',
            '--code', 'read-code', '--params-file', str(params), '--execute'],
            capture_output=True, text=True, env={**os.environ, 'PATH': str(self.root) + os.pathsep + os.environ.get('PATH', '')})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Draft operation plan', result.stderr)
        self.assertFalse(marker.exists())


if __name__ == '__main__':
    unittest.main()
