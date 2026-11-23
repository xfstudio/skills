"""A verified existing formal code may contain an underscore; no live browser."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from package_io import collect, compare


class ExistingFormalCode(unittest.TestCase):
    def test_whole_zip_name_normalization_keeps_existing_code(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            expected, actual = root / 'expected.zip', root / 'actual.zip'
            for path, name in [(expected, 'portable-skill'), (actual, 'existing_skill_code')]:
                with zipfile.ZipFile(path, 'w') as z:
                    z.writestr('root/SKILL.md', '---\nname: '+name+'\ndescription: example\n---\nBusiness unchanged\n')
            self.assertTrue(compare(expected, actual, 'existing_skill_code')['verified'])
            for code in ['../escape', 'bad*glob', 'bad/name', 'bad\\name', 'bad code', 'bad\ncode']:
                with self.assertRaises(ValueError):
                    compare(expected, actual, code)

    def test_collect_only_requested_safe_existing_prefix(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'existing_skill_code.zip'
            with zipfile.ZipFile(source, 'w') as z:
                z.writestr('SKILL.md', 'content')
            output = root / 'out' / 'collected.zip'
            collect({'formalCode': 'existing_skill_code', 'files': [], 'startedAt': time.time()-1}, root, output)
            self.assertEqual(source.read_bytes(), output.read_bytes())

    def test_browser_name_and_download_guards_accept_existing_identity(self):
        module = (ROOT / 'scripts/browser.mjs').as_uri()
        script = '''
import assert from 'node:assert/strict';
const {platformFileContent,clickDraftDownload,downloadVersionRecord}=await import(MODULE);
const source='---\\nname: portable-skill\\ndescription: example\\n---\\nBusiness unchanged\\n';
assert.equal(platformFileContent({path:'SKILL.md',content:source},'existing_skill_code'),source.replace('name: portable-skill','name: existing_skill_code'));
const fake={url:async()=>{throw Error('REACHED_PAGE');},evaluate:async()=>{throw Error('REACHED_PAGE');}};
for(const fn of [clickDraftDownload,downloadVersionRecord])await assert.rejects(()=>fn(fake,{formalCode:'existing_skill_code'}),/REACHED_PAGE/);
for(const code of ['../escape','bad*glob','bad/name','bad code','bad\\ncode']){
 assert.throws(()=>platformFileContent({path:'SKILL.md',content:source},code));
 for(const fn of [clickDraftDownload,downloadVersionRecord])await assert.rejects(()=>fn(fake,{formalCode:code}),e=>!e.message.includes('REACHED_PAGE'));
}
'''.replace('MODULE', json.dumps(module))
        result = subprocess.run(['node', '--input-type=module'], input=script, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
