import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('created_evals', Path(__file__).parents[1] / 'scripts/prepare_created_evals.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CreatedEvalsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.skill = self.root / 'current-skill-r3'
        self.skill.mkdir()
        (self.skill / 'SKILL.md').write_text('current production revision')
        for name in ['happy', 'missing']:
            case = self.skill / 'evals' / name
            (case / 'files').mkdir(parents=True)
            (case / 'prompt.md').write_text('case ' + name)
            (case / 'files' / 'fixture.json').write_text('{}')
        package = self.root / 'frozen.zip'
        with zipfile.ZipFile(package, 'w') as archive:
            archive.write(self.skill / 'SKILL.md', 'skill/SKILL.md')
        self.item = {'skill_path': str(self.skill), 'skill_name': 'skill', 'package_path': str(package),
                     'package_sha256': module.digest(package), 'primary_row': 2}

    def test_registry_uses_current_manifest_root_and_binds_input_hashes(self):
        result = module.prepare([self.item], 2)
        self.assertEqual(len(result), 2)
        self.assertTrue(all('/current-skill-r3-workspace/iteration-2/' in x['workspace'] for x in result))
        self.assertTrue(all(x['input_sha256']['fixture.json'] == module.digest(Path(x['input_files'][0])) for x in result))

    def test_existing_output_workspace_never_reused(self):
        old = self.root / 'current-skill-r3-workspace/iteration-2/happy/with_skill/outputs'
        old.mkdir(parents=True)
        sentinel = old / 'report.md'
        sentinel.write_text('previous evidence')
        with self.assertRaisesRegex(ValueError, 'reuse or overwrite'):
            module.prepare([self.item], 2)
        self.assertEqual(sentinel.read_text(), 'previous evidence')

    def test_stale_skill_root_fails_frozen_subject_binding(self):
        stale = self.root / 'stale-r2'
        stale.mkdir()
        (stale / 'SKILL.md').write_text('old production revision')
        self.item['skill_path'] = str(stale)
        with self.assertRaisesRegex(ValueError, 'subject differs'):
            module.prepare([self.item], 1)


if __name__ == '__main__':
    unittest.main()
