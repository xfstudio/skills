"""Synthetic UI-stub reproduction: a blank exported link is null, not drift."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


class EmptySourceLink(unittest.TestCase):
    def test_null_blank_only_normalization_preserves_nonempty_and_missing_guards(self):
        module = Path(__file__).resolve().parents[1] / 'scripts/feishu.mjs'
        program = r'''
import fs from 'node:fs/promises';
import path from 'node:path';
const {uploadBatch} = await import(process.argv[1]);
const root = process.argv[2];
const cases = [
  {source:null, actual:'', expected:'REACHED_ATTACHMENT_UI'},
  {source:'', actual:'', expected:'REACHED_ATTACHMENT_UI'},
  {source:'https://example.test/a.zip', actual:'https://example.test/a.zip', expected:'REACHED_ATTACHMENT_UI'},
  {source:'https://example.test/a.zip', actual:'https://example.test/b.zip', expected:'Source changed at 2'},
  {source:null, actual:'https://example.test/a.zip', expected:'Source changed at 2'},
  {actual:'', expected:'Source changed at 2'},
  {source:false, actual:'', expected:'Source changed at 2'},
  {source:0, actual:'', expected:'Source changed at 2'},
];
const results = [];
for (let i = 0; i < cases.length; i++) {
  const c = cases[i], directory = path.join(root, String(i));
  await fs.mkdir(directory);
  const baseline = [{A:'header'}, {A:'Synthetic skill',I:null}];
  if (Object.hasOwn(c,'source')) baseline[1].source_url = c.source;
  const manifest = [{row:2,name:'Synthetic skill',package_path:path.join(directory,'frozen.zip'),package_sha256:'f'.repeat(64)}];
  const bindings = [{source_excel_row:2,record_id:'recSynthetic1'}];
  const cfg = {start:2,end:2,targetTableId:'tblSynthetic',baselinePath:path.join(directory,'baseline.json'),manifestPath:path.join(directory,'manifest.json'),bindingsPath:path.join(directory,'bindings.json'),receiptPath:path.join(directory,'receipt.json')};
  await fs.writeFile(cfg.baselinePath,JSON.stringify(baseline));
  await fs.writeFile(cfg.manifestPath,JSON.stringify(manifest));
  await fs.writeFile(cfg.bindingsPath,JSON.stringify(bindings));
  let reads = 0;
  const page = {
    url: async ()=>'https://example.test/wiki?table=tblSynthetic',
    waitForFunction: async ()=>true,
    evaluate: async ()=>{
      if (reads++ === 0) return {name:'Synthetic skill',record_id:'recSynthetic1',source_url:c.actual,files:[],generation:'',sync:''};
      throw Error('REACHED_ATTACHMENT_UI');
    }
  };
  let observed = 'unexpected success';
  try {await uploadBatch(page,cfg);} catch(e) {observed=e.message;}
  results.push({case:i,observed,expected:c.expected});
}
console.log(JSON.stringify(results));
'''
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(['node', '--input-type=module', '-e', program, module.as_uri(), directory], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        cases = json.loads(result.stdout)
        for case in cases:
            with self.subTest(case=case['case']):
                self.assertEqual(case['observed'], case['expected'])


if __name__ == '__main__':
    unittest.main()
