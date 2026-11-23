import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('created_table', SCRIPTS / 'verify_created_table.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CreatedTableTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.package = Path(tmp.name) / 'new.zip'
        self.package.write_bytes(b'frozen bytes')
        self.before = [{'A': '技能名称'}, {'A': 'New', 'J': 'source-code'}, {'A': 'Existing', 'I': 'preserve.zip'}]
        self.items = [{'row': 2, 'name': 'New', 'package_path': str(self.package), 'package_sha256': module.digest(self.package)}]
        self.receipts = [{'source_excel_row': 2, 'sha256': module.digest(self.package), 'record_id': 'recPinned',
            'new_package': 'new.zip', 'attachment_replace_readback': True, 'generation_readback': '升级更新中', 'sync_status_readback': '待同步'}]

    def test_combined_expected_table_preserves_original_source_and_existing_packages(self):
        expected = module.expected_uploads(self.before, self.items, self.receipts)
        self.assertNotIn('I', self.before[1])
        self.assertEqual(expected[2]['I'], 'preserve.zip')
        self.assertTrue(module.verify_results(expected, expected, [])['verified'])
        expected[2]['I'] = 'unplanned.zip'
        self.assertFalse(module.verify_results(module.expected_uploads(self.before, self.items, self.receipts), expected, [])['verified'])

    def test_missing_receipt_or_original_nonempty_attachment_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'receipt'):
            module.expected_uploads(self.before, self.items, [])
        self.before[1]['I'] = 'old.zip'
        with self.assertRaisesRegex(ValueError, 'empty-package'):
            module.expected_uploads(self.before, self.items, self.receipts)

    def test_only_exact_planned_result_fields_may_change(self):
        expected = module.expected_uploads(self.before, self.items, self.receipts)
        after = [dict(x) for x in expected]
        after[1].update(J='native-code', F='1.0.0', AG='[batch] exact result')
        plan = {'row': 2, 'expectedName': 'New', 'packageName': 'new.zip', 'formalCode': 'native-code',
                'currentVersion': '1.0.0', 'batchId': 'batch', 'resultNote': 'exact result'}
        self.assertTrue(module.verify_results(expected, after, [plan])['verified'])
        after[1]['H'] = 'unplanned source link'
        self.assertFalse(module.verify_results(expected, after, [plan])['verified'])


if __name__ == '__main__':
    unittest.main()
