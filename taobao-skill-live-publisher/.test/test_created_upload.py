import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('created_upload', Path(__file__).parents[1] / 'scripts/prepare_created_upload.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CreatedUploadTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        package = Path(self.tmp.name) / 'skill.zip'
        package.write_bytes(b'frozen test bytes')
        self.source = [{'H': '技能包链接', 'I': '自建技能包'}, {'A': '名称', 'J': 'code'}]
        self.capture = {'source_snapshot_sha256': 'full-source', 'table_id': 'tbl5c1ONsL2wKKNs', 'records': [{
            'source_excel_row': 2, 'record_id': 'recTest', 'name': '名称', 'formal_code': 'code',
            'field_caption': '技能包链接', 'field_text': '技能包链接', 'source_url': '',
            'anchors': [], 'attachment_files': [], 'files': [], 'observed_at': '2026-11-23T00:00:00Z'}]}
        self.packages = [{'row': 2, 'name': '名称', 'package_path': str(package),
                          'package_sha256': hashlib.sha256(package.read_bytes()).hexdigest()}]

    def run_prepare(self):
        return module.prepare(self.source, 'full-source', self.capture, self.packages)

    def test_sparse_raw_is_preserved_and_only_verified_metadata_added(self):
        original = copy.deepcopy(self.source)
        baseline, bindings, additions = self.run_prepare()
        self.assertEqual(self.source, original)
        self.assertEqual(baseline[1], {**original[1], 'source_url': ''})
        self.assertEqual(bindings[0]['record_id'], 'recTest')
        self.assertEqual(len(additions), 1)

    def test_native_text_without_anchor_is_not_assumed_blank(self):
        self.capture['records'][0]['field_text'] += '\nunknown content'
        with self.assertRaisesRegex(ValueError, 'not proven empty'):
            self.run_prepare()

    def test_changed_native_identity_rejected(self):
        self.capture['records'][0]['formal_code'] = 'different'
        with self.assertRaisesRegex(ValueError, 'identity differs'):
            self.run_prepare()

    def test_nonempty_native_link_missing_in_raw_rejected(self):
        self.capture['records'][0].update(source_url='https://example.test/asset', anchors=['https://example.test/asset'])
        with self.assertRaisesRegex(ValueError, 'omitted a nonempty'):
            self.run_prepare()

    def test_unrelated_capture_source_rejected(self):
        self.capture['source_snapshot_sha256'] = 'other-source'
        with self.assertRaisesRegex(ValueError, 'not bound'):
            self.run_prepare()

    def test_existing_attachment_and_zip_drift_rejected(self):
        self.source[1]['I'] = 'existing.zip'
        with self.assertRaisesRegex(ValueError, 'empty-attachment'):
            self.run_prepare()
        del self.source[1]['I']
        Path(self.packages[0]['package_path']).write_bytes(b'drift')
        with self.assertRaisesRegex(ValueError, 'package changed'):
            self.run_prepare()


if __name__ == '__main__':
    unittest.main()
