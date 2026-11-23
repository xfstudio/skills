"""No-network checks for new fixed-asset import recovery."""
import hashlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import bm_import_created as importer


class CreatedImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.raw = b'synthetic archive bytes for transport test'
        package = Path(self.temp.name) / 'fixture.zip'
        package.write_bytes(self.raw)
        self.sha = hashlib.sha256(self.raw).hexdigest()
        self.item = {'row': 2, 'source_rows': [2, 3], 'formal_code': 'fixture-code',
            'skill_name': 'fixture-code', 'package_path': str(package), 'sha256': self.sha,
            'metadata': {'displayName': 'fixture', 'summary': '', 'categoryId': None, 'visibility': 'public'},
            'operation_id': 'ad1d6ce7-1600-440a-89fd-70c46e47eb0c'}
        self.detail = {'id': 'catalog', 'assetId': 'asset', 'revision': 1, 'assetRevision': 1,
            'octopPackageId': 'native', 'source': {'skillName': 'fixture-code',
            'packageSha256': self.sha, 'packageId': 'package'}}

    def test_durable_intent_precedes_unknown_post_and_is_not_retried(self):
        journal, saves, posts = [], [], []
        def persist(value):
            saves.append([dict(x) for x in value])
        def call(path, method='GET', body=None, headers=None, binary=False):
            if method == 'POST':
                self.assertEqual(saves[-1][0]['phase'], 'submitting')
                self.assertEqual(headers['Idempotency-Key'], self.item['operation_id'])
                self.assertIn(b'name="metadata"', body)
                self.assertIn(b'name="clientOperationId"', body)
                posts.append(path)
                raise TimeoutError('synthetic unknown')
            return 404, {}
        with self.assertRaises(TimeoutError):
            importer.import_one(self.item, call, journal, persist)
        self.assertEqual(journal[0]['phase'], 'unknown')
        with self.assertRaisesRegex(RuntimeError, 'without reposting'):
            importer.import_one(self.item, call, journal, persist)
        self.assertEqual(len(posts), 1)

    def test_success_requires_original_download_and_stable_source(self):
        calls, journal = [], []
        def call(path, method='GET', body=None, headers=None, binary=False):
            calls.append((path, method))
            if '/imports/' in path:
                return 200, {'status': 'synced', 'catalogId': 'catalog'}
            if binary:
                return 200, (self.raw, '"' + self.sha + '"')
            return 200, self.detail
        receipt = importer.import_one(self.item, call, journal, lambda _: None)
        self.assertEqual(receipt['phase'], 'fixed_asset_verified')
        self.assertEqual(receipt['octop_package_id'], 'native')
        self.assertTrue(receipt['bm_synced_is_not_feishu_sync_success'])
        self.assertEqual(sum(method == 'POST' for _, method in calls), 0)
        self.assertEqual(len(calls), 4)

    def test_wrong_download_cannot_become_fixed_asset_proof(self):
        def call(path, method='GET', body=None, headers=None, binary=False):
            if '/imports/' in path:
                return 200, {'status': 'synced', 'catalogId': 'catalog'}
            if binary:
                return 200, (b'other bytes', '"' + self.sha + '"')
            return 200, self.detail
        with self.assertRaisesRegex(RuntimeError, 'download mismatch'):
            importer.import_one(self.item, call, [], lambda _: None)

    def test_source_drift_after_download_is_rejected(self):
        reads = []
        def call(path, method='GET', body=None, headers=None, binary=False):
            if '/imports/' in path:
                return 200, {'status': 'synced', 'catalogId': 'catalog'}
            if binary:
                return 200, (self.raw, '"' + self.sha + '"')
            reads.append(path)
            return 200, {**self.detail, 'revision': len(reads)}
        with self.assertRaisesRegex(RuntimeError, 'changed during'):
            importer.import_one(self.item, call, [], lambda _: None)


if __name__ == '__main__':
    unittest.main()
