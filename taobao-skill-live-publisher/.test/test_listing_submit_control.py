"""Synthetic current/legacy listing controls; no browser, business data or network."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ListingSubmitControlTest(unittest.TestCase):
    def run_case(self, control_class, agreement=True, fresh=True):
        with tempfile.TemporaryDirectory() as directory:
            script = r'''
const {submitListing}=await import(MODULE);
const fs=await import('node:fs/promises');
const p=PARAMS,sha='a'.repeat(64),download='b'.repeat(64);
const cfg={account:'SyntheticAccount',publicAppId:'123',formalCode:'sample-skill',mode:'1',
  approvedVersion:'1.0.0',packageSha256:sha,userAgreementHandled:p.agreement,journalPath:p.journal};
cfg.onlineObservation={account:cfg.account,publicAppId:cfg.publicAppId,formalCode:cfg.formalCode,version:'1.0.0',
  packageSha256:sha,reviewStatus:'审核通过',onlineStatus:'线上版本',versionReadback:'1.0.0\t审核通过\t线上版本',
  observedAt:new Date(Date.now()-(p.fresh?0:120000)).toISOString()};
cfg.approvedVersionPackageProof={verified:true,expected_package_sha256:sha,actual_download_sha256:download,
 approvalBinding:{account:cfg.account,publicAppId:cfg.publicAppId,formalCode:cfg.formalCode,version:'1.0.0',
 packageSha256:sha,downloadVersion:'1.0.0',actualDownloadSha256:download}};
let clicks=0;
const page={waitForFunction:async()=>true,cdp:async()=>{},mouse:{move:async()=>{},click:async()=>{clicks++;}},
 evaluate:async(fn,arg)=>{
   if(arg&&typeof arg==='object'&&arg.selector){
     const selector=arg.selector;
     const match=[...selector.matchAll(/class\*=\\?["']([^"']+)["']/g)].map(x=>x[1]);
     if(!match.some(part=>p.controlClass.includes(part)))throw Error('Native form control not found: '+selector);
     return {x:100,y:100};
   }
   return {formalCode:'sample-skill',mode:'1',agreementChecked:p.agreement,iconPresent:true,text:'上架到技能商店 提交 取消'};
 }};
let error=null,result=null;
try{result=await submitListing(page,cfg);}catch(e){error=e.message;}
const journal=await fs.readFile(p.journal,'utf8').then(JSON.parse).catch(()=>[]);
console.log(JSON.stringify({clicks,error,result,journal}));
'''.replace('MODULE', json.dumps((ROOT / 'scripts/taobao.mjs').as_uri())).replace('PARAMS', json.dumps({
                'controlClass': control_class, 'agreement': agreement, 'fresh': fresh,
                'journal': str(Path(directory) / 'journal.json')}))
            process = subprocess.run(['node', '--input-type=module'], input=script, text=True, capture_output=True, timeout=20)
            self.assertEqual(process.returncode, 0, process.stderr)
            return json.loads(process.stdout)

    def test_current_native_submit_button_dispatches_once(self):
        result = self.run_case('tbd-btn submitBtn--synthetic')
        self.assertIsNone(result['error'], result)
        self.assertEqual(result['clicks'], 1)
        self.assertEqual(result['journal'][0]['phase'], 'listing_requested')

    def test_legacy_submit_button_remains_supported(self):
        result = self.run_case('tbd-btn confirmBtn--synthetic')
        self.assertIsNone(result['error'], result)
        self.assertEqual(result['clicks'], 1)

    def test_agreement_and_fresh_version_guards_still_block(self):
        for options in [{'agreement': False}, {'fresh': False}]:
            result = self.run_case('tbd-btn submitBtn--synthetic', **options)
            self.assertIsNotNone(result['error'])
            self.assertEqual(result['clicks'], 0)
            self.assertEqual(result['journal'], [])


if __name__ == '__main__':
    unittest.main()
