import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pasteResultColumn} from '../scripts/feishu.mjs';
const dir=await fs.mkdtemp(path.join(os.tmpdir(),'publisher-columns-test-'));
const sha=value=>createHash('sha256').update(value).digest('hex');
try {
  const baseline=JSON.stringify([{AG:'同步说明'},{AG:'old'},{AG:'preserved'}]);
  const plan=JSON.stringify({baseline_sha256:sha(baseline),writebacks_sha256:'reviewed',columns:[{columnKey:'AG',column:'同步说明',values:['Literal <script>value</script>\nSecond line','preserved']}]});
  const cfg={columnKey:'AG',column:'同步说明',targetTableId:'tblPinned',baselinePath:path.join(dir,'baseline.json'),baselineSha256:sha(baseline),columnPlanPath:path.join(dir,'plan.json'),columnPlanSha256:sha(plan),selectedHeaderEvidence:path.join(dir,'selection.png')};
  await fs.writeFile(cfg.baselinePath,baseline);await fs.writeFile(cfg.columnPlanPath,plan);await fs.writeFile(cfg.selectedHeaderEvidence,'test fixture');
  const pastes=[];
  const page={url:async()=> 'https://example.feishu.cn/wiki/example?table=tblPinned',evaluate:async()=>({editable:false,drawer:false}),keyboard:{paste:async value=>pastes.push(value)},waitForLoadState:async()=>{}};
  const result=await pasteResultColumn(page,cfg);assert.equal(result.rows,2);assert.equal(pastes.length,1);
  assert.equal((pastes[0].html.match(/<tr>/g)||[]).length,2);assert(!pastes[0].html.includes('<script>'));assert(pastes[0].html.includes('&lt;script&gt;'));assert(pastes[0].html.includes('<br>Second line'));
  await assert.rejects(pasteResultColumn(page,{...cfg,targetTableId:'other'}),/target table/);
  await assert.rejects(pasteResultColumn({...page,evaluate:async()=>({editable:true,drawer:false})},cfg),/select the exact/);
  await fs.appendFile(cfg.columnPlanPath,' ');await assert.rejects(pasteResultColumn(page,cfg),/plan changed/);assert.equal(pastes.length,1);
  console.log('Column plan binding, multiline boundaries and conflict gates passed');
} finally {await fs.rm(dir,{recursive:true,force:true});}
