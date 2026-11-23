import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest
import zipfile

SCRIPTS = Path(__file__).parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('created_download', SCRIPTS / 'collect_created_download.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CreatedDownloadTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.downloads = self.root / 'native'
        self.downloads.mkdir()
        self.expected = self.root / 'original-skill.zip'
        with zipfile.ZipFile(self.expected, 'w') as archive:
            archive.writestr('original-skill/SKILL.md', '---\nname: original-skill\n---\nFrozen source\n')
        self.operation = {'row': 2, 'formalCode': 'native-code', 'version': '当前草稿', 'startedAt': time.time(), 'files': []}
        self.creation = {'phase': 'created_identity_verified', 'publicAppId': '123', 'row': 2,
                         'formalCode': 'native-code', 'packageSha256': module.digest(self.expected)}
        self.native = self.downloads / ('native-random-prefix-' + self.expected.name)
        shutil.copyfile(self.expected, self.native)
        self.output = self.root / 'collected.zip'

    def collect(self):
        return module.collect(self.operation, self.creation, self.expected, self.downloads, self.output, timeout=0)

    def test_original_upload_filename_is_collected_with_actual_native_proof(self):
        result = self.collect()
        self.assertEqual(result['native_filename'], self.native.name)
        self.assertEqual(result['sha256'], module.digest(self.expected))
        self.assertTrue(result['package_proof']['verified'])

    def test_ambiguity_never_chooses_a_file(self):
        shutil.copyfile(self.native, self.downloads / ('second-' + self.expected.name))
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            self.collect()
        self.assertFalse(self.output.exists())

    def test_other_identity_or_changed_download_rejected(self):
        self.creation['formalCode'] = 'other-code'
        with self.assertRaisesRegex(ValueError, 'identity'):
            self.collect()
        self.creation['formalCode'] = 'native-code'
        with zipfile.ZipFile(self.native, 'w') as archive:
            archive.writestr('original-skill/SKILL.md', 'changed')
        with self.assertRaisesRegex(ValueError, 'differs'):
            self.collect()

    def test_existing_output_is_preserved(self):
        self.output.write_bytes(b'previous evidence')
        with self.assertRaisesRegex(ValueError, 'refusing overwrite'):
            self.collect()
        self.assertEqual(self.output.read_bytes(), b'previous evidence')


if __name__ == '__main__':
    unittest.main()
