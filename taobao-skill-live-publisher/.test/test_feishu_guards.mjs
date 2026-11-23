import assert from 'node:assert/strict';
import {writeResult} from '../scripts/feishu.mjs';
const cfg={recordId:'recPinned',expectedName:'Skill',packageName:'skill.zip',resultNote:'Actual review',batchId:'batch',formalCode:'sample',expectedCurrentVersion:'1.0.0',expectedOnlineVersion:'1.0.0',currentVersion:'1.0.1',platformVersionConfirmed:true};
const baseline={id:'recPinned',name:'Skill',files:['skill.zip'],note:'Prior note',formalCode:'sample',currentVersion:'1.0.0',onlineVersion:'1.0.0'};
for(const [state,message] of [[{...baseline,formalCode:'other'},/conflicts/],[{...baseline,currentVersion:'1.0.2'},/changed/],[{...baseline,onlineVersion:'1.0.2'},/changed/]]) {
  let actions=0;
  const page={evaluate:async()=>state,waitForSelector:async()=>{},click:async()=>{actions++;throw Error('Unexpected mutation');}};
  await assert.rejects(writeResult(page,cfg),message);
  assert.equal(actions,0);
}
console.log('Feishu conflict checks passed before any field mutation');
