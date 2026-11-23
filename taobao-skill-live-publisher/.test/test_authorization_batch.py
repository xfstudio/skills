import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from authorization_batch import targets
from package_io import digest
from prepare_authorization_writebacks import prepare
from report_authorization import report
from workflow import result_columns, save, verify_results


class AuthorizationReceipts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.batch = Path(self.temp.name)
        self.run = self.batch / 'authorization'
        self.run.mkdir()
        self.manifest = [{'row': 2, 'name': 'Skill', 'package_path': '/fixed/skill.zip', 'package_sha256': 'fixed'}]
        self.target = {'account': 'Account', 'publicAppId': '123', 'formalCode': 'skill', 'searchName': 'Skill'}
        self.intents = [{'row': 2, 'packageSha256': 'fixed', 'target': self.target}]
        save(self.batch / 'package-manifest.json', self.manifest)
        save(self.batch / 'taobao-version-journal.json', self.intents)
        self.binding = {'manifestSha256': digest(self.batch / 'package-manifest.json'),
                        'versionJournalSha256': digest(self.batch / 'taobao-version-journal.json'), 'merchant': 'Target'}
        save(self.run / 'run-binding.json', self.binding)
        self.receipt = {'row': 2, **self.target, 'merchant': 'Target', 'manifestSha256': self.binding['manifestSha256'],
                        'packageSha256': 'fixed', 'phase': 'authorization_added', 'listed': True,
                        'statusLabels': ['定向', '已上架'], 'authorization': {'complete': True, 'shops': ['Other', 'Target']},
                        'existingShopsPreserved': True, 'observedAt': '2026-11-23T00:00:00Z'}
        self.baseline = [{'E': '技能生成及状态', 'F': '当前版本', 'G': '线上版本', 'J': '技能code', 'AG': '同步说明'},
                         {'A': 'Skill', 'I': 'skill.zip', 'E': '上架完成', 'F': '1.0.2', 'G': '1.0.2', 'J': 'skill',
                          'AG': '[release] Existing release proof', 'AD': '待同步', 'H': 'https://fixed.example/skill.zip'}]
        self.records = [{'source_excel_row': 2, 'record_id': 'recPinned'}]

    def planned(self, receipt=None):
        save(self.run / 'authorization-results.json', [receipt or self.receipt])
        return prepare(self.batch, self.run, self.baseline, self.records, 'authorization-run')

    def test_authorization_writeback_only_changes_note_and_preserves_release_proof(self):
        plans = self.planned()
        columns = result_columns(self.baseline, plans)
        self.assertEqual([x['columnKey'] for x in columns], ['AG'])
        current = copy.deepcopy(self.baseline)
        current[1]['AG'] = columns[0]['values'][0]
        self.assertIn('[release] Existing release proof', current[1]['AG'])
        self.assertTrue(verify_results(self.baseline, current, plans)['verified'])
        current[1]['AD'] = '同步成功'
        self.assertFalse(verify_results(self.baseline, current, plans)['verified'])

    def test_wrong_merchant_target_package_and_incomplete_readback_cannot_claim_success(self):
        for key, value in [('merchant', 'Unexpected'), ('publicAppId', '456'), ('packageSha256', 'other'),
                           ('authorization', {'complete': False, 'shops': ['Target']}), ('existingShopsPreserved', False)]:
            receipt = {**self.receipt, key: value}
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.planned(receipt)

    def test_unknown_and_offline_receipts_do_not_become_authorization_success(self):
        for phase in ['authorization_unknown', 'not_listed', 'needs_reconciliation']:
            receipt = {**self.receipt, 'phase': phase, 'listed': False, 'authorization': None}
            plan = self.planned(receipt)[0]
            self.assertIsNone(plan['generationStatus'])
            self.assertIsNone(plan['onlineVersion'])
            self.assertNotIn('核验通过', plan['resultNote'])

    def test_unique_frozen_target_is_required(self):
        self.assertEqual(len(targets(self.batch)), 1)
        save(self.batch / 'taobao-version-journal.json', self.intents + self.intents)
        with self.assertRaises(ValueError):
            targets(self.batch)

    def test_report_requires_exact_latest_results_and_verified_writeback(self):
        plans = self.planned()
        writebacks = self.run / 'writebacks.json'
        save(writebacks, plans)
        current = copy.deepcopy(self.baseline)
        current[1]['AG'] = result_columns(self.baseline, plans)[0]['values'][0]
        proof = verify_results(self.baseline, current, plans)
        proof['writebacks_sha256'] = digest(writebacks)
        verification = self.run / 'verified.json'
        save(verification, proof)
        summary = report(self.batch, self.run, writebacks, verification)
        self.assertEqual(summary['directed_authorized_verified'], 1)
        self.assertEqual(summary['new_authorizations_verified'], 1)
        changed = {**self.receipt, 'observedAt': '2026-11-24T00:00:00Z'}
        save(self.run / 'authorization-results.json', [changed])
        with self.assertRaises(ValueError):
            report(self.batch, self.run, writebacks, verification)


if __name__ == '__main__':
    unittest.main()
