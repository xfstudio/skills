import assert from 'node:assert/strict';
import {waitForUiIdle} from '../scripts/browser.mjs';

const forbidden=new Proxy({}, {get(){throw Error('Do not inspect request data');}});
let round=0;
const completed={events:async()=>round++===0?[
  {method:'Network.requestWillBeSent',params:{requestId:'worker',type:'Script',request:forbidden}},
  {method:'Network.requestWillBeSent',params:{requestId:'save',type:'Fetch',request:forbidden}},
]:round===2?[{method:'Network.loadingFinished',params:{requestId:'save'}}]:[]};
await waitForUiIdle(completed,{timeout:1000,quietMs:50});
assert.ok(round>=2,'A native save must finish before proceeding');
let first=true;
await assert.rejects(()=>waitForUiIdle({events:async()=>first?(first=false,[{method:'Network.requestWillBeSent',params:{requestId:'pending',type:'XHR',request:forbidden}}]):[]},{timeout:150,quietMs:50}),/did not settle/);
console.log('Browser request gates passed: worker ignored, native save awaited, unresolved save rejected, request data unread');

const {requireApprovedPackage}=await import('../scripts/taobao.mjs');
const context={account:'A',publicAppId:'1',formalCode:'sample',packageSha256:'a'.repeat(64)};
const approved={verified:true,expected_package_sha256:context.packageSha256,actual_download_sha256:'b'.repeat(64),approvalBinding:{...context,version:'1.0.1',downloadVersion:'1.0.1',actualDownloadSha256:'b'.repeat(64)}};
requireApprovedPackage(context,approved,'1.0.1');
for(const key of ['account','publicAppId','formalCode','packageSha256']) {
  let rejected=false;try{requireApprovedPackage({...context,[key]:'other'},approved,'1.0.1');}catch{rejected=true;}
  if(!rejected)throw Error('Unrelated approved proof was accepted for '+key);
}
let rejected=false;try{requireApprovedPackage(context,approved,'1.0.2');}catch{rejected=true;}
if(!rejected)throw Error('Different approved version was accepted');
console.log('Approved package identity gates passed');

const {platformFileContent}=await import('../scripts/browser.mjs');
const source='---\r\nname: source-name\r\ndescription: Keep.\r\n---\r\nBody source-name stays.\r\n';
const normalized=platformFileContent({path:'SKILL.md',content:source},'formal-code');
if(normalized!==source.replace('name: source-name','name: formal-code'))throw Error('Platform name normalization changed other bytes');
if(platformFileContent({path:'assets/SKILL.md',content:source},'formal-code')!==source)throw Error('Nested skill was normalized');
console.log('Primary formal-name normalization preserves all other bytes');

const {requireFreshOnlineVersion}=await import('../scripts/taobao.mjs');
const fresh={...context,approvedVersion:'1.0.1',onlineObservation:{...context,version:'1.0.1',reviewStatus:'审核通过',onlineStatus:'线上版本',observedAt:new Date().toISOString(),versionReadback:'1.0.1\t审核通过\t线上版本'}};
requireFreshOnlineVersion(fresh);
for(const observation of [{...fresh.onlineObservation,version:'1.0.0'},{...fresh.onlineObservation,observedAt:new Date(Date.now()-120000).toISOString()},{...fresh.onlineObservation,publicAppId:'other'},{...fresh.onlineObservation,versionReadback:'1.0.1\t审核通过'}]) {
  let rejected=false;try{requireFreshOnlineVersion({...fresh,onlineObservation:observation});}catch{rejected=true;}
  if(!rejected)throw Error('Stale, offline or mismatched online gate was accepted');
}
console.log('Fresh online-version gates reject drift and stale handoff evidence');

const {cardState}=await import('../scripts/taobao.mjs');
if(cardState('已上架规划器\n未公开\nAppkey\n1\n说明已上架条件','1').listed)throw Error('A title/description was mistaken for listing status');
if(!cardState('Skill\n定向\n已上架\nAppkey\n1','1').listed)throw Error('Actual listing tag was lost');
console.log('Card status parsing excludes names and descriptions');

const {menu,button,nativeClick}=await import('../scripts/browser.mjs');
const previousGlobals={document:globalThis.document,innerWidth:globalThis.innerWidth,innerHeight:globalThis.innerHeight,requestAnimationFrame:globalThis.requestAnimationFrame};
const body={},hidden={innerText:'新建文件',getBoundingClientRect:()=>({x:0,y:0,width:0,height:0}),scrollIntoView:()=>{throw Error('Hidden item selected');}};
const visible={innerText:'新建文件',parentElement:body,getBoundingClientRect:()=>({x:20,y:20,width:80,height:32,right:100,bottom:52}),scrollIntoView:()=>{},getAnimations:()=>[],getAttribute:()=>null,contains:e=>e===visible};
const offscreen={innerText:'新建文件',getBoundingClientRect:()=>({x:-9995,y:-9571,width:80,height:32,right:-9915,bottom:-9539}),scrollIntoView:()=>{throw Error('Offscreen measurement item selected');}};
const covered={...visible,scrollIntoView:()=>{throw Error('Covered retained item selected');},contains:()=>false};
const clicks=[];
globalThis.document={body,querySelectorAll:()=>[hidden,offscreen,covered,visible],elementFromPoint:()=>visible};globalThis.innerWidth=1000;globalThis.innerHeight=800;globalThis.requestAnimationFrame=callback=>callback(0);
const nativePage={cdp:async()=>{},evaluate:async(fn,arg)=>fn(arg),waitForFunction:async(fn,arg)=>{if(!fn(arg))throw Error('No unique visible target');},waitForSelector:async()=>{throw Error('Ambiguous semantic pre-wait must not run');},mouse:{move:async()=>{},click:async(x,y)=>clicks.push([x,y])}};
try {
  await menu(nativePage,'新建文件');
  hidden.innerText=offscreen.innerText=covered.innerText=visible.innerText='发布';await button(nativePage,'发布');
  if(clicks.length!==2||clicks.some(([x,y])=>x!==60||y!==36))throw Error('Hidden duplicate interfered with native actions');
  let emptyReads=1;globalThis.document.querySelectorAll=()=>emptyReads-->0?[]:[hidden,offscreen,covered,visible];
  await nativeClick(nativePage,'button',null,'发布');
  if(clicks.length!==3)throw Error('Transient target resolution retried the actual click');
  let reads=0;globalThis.document.querySelectorAll=()=>++reads===3?[]:[hidden,offscreen,covered,visible];
  await nativeClick(nativePage,'button',null,'发布');
  if(clicks.length!==4)throw Error('Hover redraw retried the actual click');
  console.log('Native actions ignore hidden/covered nodes and wait through pre-click redraws');
} finally {for(const [key,value] of Object.entries(previousGlobals)){if(value===undefined)delete globalThis[key];else globalThis[key]=value;}}

const {selectVersionDownload}=await import('../scripts/browser.mjs');
const versionRows=[{index:0,version:'当前草稿',reviewStatus:'-',buttons:['下载']},{index:1,version:'1.0.2',reviewStatus:'审核通过',buttons:['下载','评测报告']},{index:2,version:'1.0.1',reviewStatus:'审核通过',buttons:['下载','评测报告','上线']}];
if(selectVersionDownload(versionRows,'1.0.2',true).index!==1)throw Error('Wrong approved version selected');
for(const [rows,version] of [[versionRows,'当前草稿'],[versionRows,'9.0.0'],[[...versionRows,versionRows[1]],'1.0.2'],[[{...versionRows[1],reviewStatus:'审核中'}],'1.0.2'],[[{...versionRows[1],buttons:['上线','下载']}],'1.0.2']]) {
  let rejected=false;try{selectVersionDownload(rows,version,true);}catch{rejected=true;}
  if(!rejected)throw Error('Ambiguous, pending or changed approved-version download accepted');
}
console.log('Exact approved version download rejects draft, pending, duplicate and changed controls');

const {requireLatestActivation}=await import('../scripts/taobao.mjs');
requireLatestActivation('1.0.2',[{version:'当前草稿'},{version:'1.0.2'},{version:'1.0.1'}]);
for(const entries of [[{version:'1.0.2'},{version:'1.0.3'}],[{version:'1.1.0'},{version:'1.0.2'}],[{version:'1.0.1'}],[{version:'1.0.2'},{version:'unexpected'}]]) {
  let rejected=false;try{requireLatestActivation('1.0.2',entries);}catch{rejected=true;}
  if(!rejected)throw Error('Concurrent or unknown platform revision permitted an old activation');
}
console.log('Activation refuses newer, missing and unrecognized platform revisions');

const {requireRestorationState,restoreExistingListing}=await import('../scripts/taobao.mjs');
const existingListing={formalCode:'sample',mode:'1',fields:[{placeholder:'description',value:'Original'}],iconDimensions:[{width:200,height:200}]};
const restoreCfg={restoreExistingListingAuthorized:true,mode:'1',formalCode:'sample',existingListing};
const offlineCard={previouslyListed:true,listed:false,statusLabels:['定向','已下架']};
requireRestorationState(restoreCfg,offlineCard,existingListing);
for(const [cfg,card,listing] of [[{...restoreCfg,restoreExistingListingAuthorized:false},offlineCard,existingListing],[restoreCfg,{...offlineCard,listed:true},existingListing],[restoreCfg,offlineCard,{...existingListing,mode:'0'}],[restoreCfg,offlineCard,{...existingListing,fields:[]}],[restoreCfg,offlineCard,{...existingListing,iconDimensions:[]}]]) {
  let rejected=false;try{requireRestorationState(cfg,card,listing);}catch{rejected=true;}if(!rejected)throw Error('Unreviewed restoration state accepted');
}
let unauthorizedRejected=false;try{await restoreExistingListing({},{restoreExistingListingAuthorized:false});}catch{unauthorizedRejected=true;}
if(!unauthorizedRejected)throw Error('Restoration ran without explicit authorization');
console.log('Restoration binds existing metadata/mode and refuses unauthorised or changed state');

const {versionAuthorizationAllowed}=await import('../scripts/taobao.mjs');
const offlineContract=JSON.parse(await(await import('node:fs/promises')).readFile(new URL('./offline-auth-cases.json',import.meta.url),'utf8'));
for(const test of offlineContract.cases)if(versionAuthorizationAllowed({...offlineContract.base,...test.patch})!==test.allowed)throw Error('Offline version gate contract mismatch: '+test.name);
console.log('Python/JS version gates use the same offline authorization evidence cases');

const {requireRestorationConfirmation}=await import('../scripts/taobao.mjs');
const pureConfirmation={text:'上架\n确认上架技能？技能上架后，将可被展示及订购\n确定\n取消',checkboxes:0,buttons:['确定','取消']};
requireRestorationConfirmation(pureConfirmation);
for(const changed of [{...pureConfirmation,checkboxes:1},{...pureConfirmation,text:pureConfirmation.text+'请阅读协议'},{...pureConfirmation,text:pureConfirmation.text+'将清空授权'},{...pureConfirmation,buttons:['确定','删除']}]) {
  let rejected=false;try{requireRestorationConfirmation(changed);}catch{rejected=true;}if(!rejected)throw Error('Unknown restoration terms/action accepted');
}
console.log('Restoration confirmation accepts only the observed pure action, no agreements or scope changes');
