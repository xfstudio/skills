"""Offline native-menu contract: hover-only submenu closes before pointer dispatch."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FeishuExportMenuTest(unittest.TestCase):
    def run_case(self, table_name):
        with tempfile.TemporaryDirectory() as directory:
            cfg = {'url': 'https://sample.feishu.cn/wiki/sample?table=tblSample', 'tableName': table_name,
                   'output': str(Path(directory) / 'export.xlsx')}
            script = r'''
const {exportTable}=await import(MODULE);
const cfg=CONFIG;let mainOpen=false,sticky=false,settings=false,lastTarget=null;
const trace=[];
const page={url:async()=>cfg.url,goto:async()=>{},cdp:async()=>{},waitForSelector:async()=>{},
 click:async selector=>{if(selector==='button.more-btn'){mainOpen=true;trace.push('open-main');}},
 hover:async()=>{trace.push('hover-parent');},
 waitForFunction:async(fn,arg)=>{if(typeof arg==='string'&&arg!=='Sample table')throw Error('Download settings table binding differs');return true;},
 evaluate:async(fn,arg)=>{
   if(arg&&typeof arg==='object'&&arg.selector){
     if(arg.text==='Excel/CSV 文件'&&!sticky)throw Error('Hover-only submenu dismissed before native click');
     if(arg.text==='下载'&&!settings)throw Error('Download settings absent');
     lastTarget=arg.text;return {x:100,y:100};
   }
   return mainOpen;
 },
 mouse:{move:async()=>{},click:async()=>{
   trace.push('click:'+lastTarget);
   if(lastTarget==='导出')sticky=true;
   if(lastTarget==='Excel/CSV 文件')settings=true;
 }},
 waitForEvent:()=>{trace.push('arm-download');return Promise.resolve({saveAs:async()=>trace.push('save-download')});}
};
let error=null,result=null;
try{result=await exportTable(page,cfg);}catch(e){error=e.message;}
console.log(JSON.stringify({error,result,trace}));
'''.replace('MODULE', json.dumps((ROOT / 'scripts/browser.mjs').as_uri())).replace('CONFIG', json.dumps(cfg))
            process = subprocess.run(['node', '--input-type=module'], input=script, text=True, capture_output=True, timeout=20)
            self.assertEqual(process.returncode, 0, process.stderr)
            return json.loads(process.stdout)

    def test_click_opens_stable_export_submenu_and_download_is_armed_first(self):
        result = self.run_case('Sample table')
        self.assertIsNone(result['error'], result)
        self.assertEqual(result['trace'].count('click:导出'), 1)
        self.assertEqual(result['trace'].count('click:Excel/CSV 文件'), 1)
        self.assertLess(result['trace'].index('arm-download'), result['trace'].index('click:下载'))
        self.assertEqual(result['trace'].count('save-download'), 1)

    def test_wrong_download_table_never_starts_download(self):
        result = self.run_case('Other table')
        self.assertIsNotNone(result['error'])
        self.assertNotIn('arm-download', result['trace'])
        self.assertNotIn('click:下载', result['trace'])


if __name__ == '__main__':
    unittest.main()
