/** Taobao's real UI: read account/target/mode/shops, submit a fixed version once, reconcile. */
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {button,nativeClick,nativeHover,downloadVersionRecord,menu} from './browser.mjs';

async function persist(path,value) {await fs.writeFile(path+'.tmp',JSON.stringify(value,null,2));await fs.rename(path+'.tmp',path);}
const cardSelector='[class^="skillCard--"]';
async function account(page,expected) {
  if(!expected)throw Error('Explicit authorized account required');
  await page.waitForFunction(expected=>{
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let node;
    while(node=walker.nextNode()) {
      if(node.textContent.trim()!==expected)continue;
      const r=node.parentElement.getBoundingClientRect();
      if(r.width>0&&r.height>0&&r.y>=0&&r.y<80)return true;
    }
    return false;
  },expected,{timeout:15000});
}
export async function closeDialog(page) {
  const open=await page.evaluate(()=>[...document.querySelectorAll('[role=dialog]')].some(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0));
  if(!open)return;
  await page.evaluate(()=>window.scrollTo({left:document.documentElement.scrollWidth,top:0}));
  await page.waitForFunction(()=>[...document.querySelectorAll('button[aria-label="Close"]')].some(b=>{
    const r=b.getBoundingClientRect();
    return r.width>0&&r.height>0&&r.x>=0&&r.y>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));
  }),undefined,{timeout:10000});
  await nativeClick(page,'button[aria-label="Close"]');
  await page.waitForFunction(()=>![...document.querySelectorAll('[role=dialog]')].some(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0),undefined,{timeout:15000});
  await page.mouse.move(500,400);
}
export function cardState(text,publicAppId) {
  const lines=text.split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
  const key=lines.findIndex((line,index)=>/^appkey$/i.test(line)&&lines[index+1]===publicAppId);
  if(key<1)throw Error('Public card status section is not identifiable');
  const labels=lines.slice(1,key);
  return {listed:labels.includes('已上架'),previouslyListed:labels.includes('已下架'),listingReview:labels.includes('审核中'),statusLabels:labels};
}
async function card(page,cfg) {
  await account(page,cfg.account);
  if(!/^\d+$/.test(cfg.publicAppId))throw Error('Pinned public application ID required');
  const matches=await page.evaluate(({selector,id})=>[...document.querySelectorAll(selector)].map((e,i)=>({i,ordinal:[...e.parentElement.children].indexOf(e),text:e.innerText})).filter(x=>x.text.split(/\s+/).includes(id)),{selector:cardSelector,id:cfg.publicAppId});
  if(matches.length!==1)throw Error('Expected one exact public AppID card; search/pagination needs reconciliation');
  return {selector:'[class^="skillGrid--"] > '+cardSelector+':nth-child('+(matches[0].ordinal+1)+')',text:matches[0].text,index:matches[0].i,...cardState(matches[0].text,cfg.publicAppId)};
}
async function cardButton(page,cfg,index) {
  const found=await card(page,cfg);
  await nativeHover(page,found.selector);
  await page.waitForFunction(({selector,index})=>{
    const b=document.querySelector(selector)?.querySelectorAll('button')[index];
    if(!b)return false;const r=b.getBoundingClientRect();
    return b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));
  },{selector:found.selector,index},{timeout:10000});
  await nativeClick(page,found.selector+' button',index);
  return found;
}
async function more(page,cfg,label) {
  const found=await card(page,cfg);
  await nativeHover(page,found.selector);
  await nativeHover(page,found.selector+' button',1);
  let opened=false;
  try {
    await page.waitForFunction(label=>[...document.querySelectorAll('span.tbd-dropdown-menu-title-content')].some(e=>e.innerText.trim()===label&&e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0),label,{timeout:1000});
    opened=true;
  } catch(error) {
    opened=await page.evaluate(label=>[...document.querySelectorAll('span.tbd-dropdown-menu-title-content')].some(e=>e.innerText.trim()===label&&e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0),label);
  }
  if(!opened)await nativeClick(page,found.selector+' button',1);
  await page.waitForFunction(label=>[...document.querySelectorAll('span.tbd-dropdown-menu-title-content')].some(e=>e.innerText.trim()===label&&e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0),label,{timeout:10000});
  await nativeClick(page,'span.tbd-dropdown-menu-title-content',null,label);
}
async function offlineMenu(page,cfg,label=null) {
  const found=await card(page,cfg);
  await page.hover(found.selector);
  const labels=()=>page.evaluate(()=>[...document.querySelectorAll('[role=menuitem]')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.x>=0&&r.y>=0;}).map(e=>e.innerText.trim()));
  if(!(await labels()).length)await page.click(found.selector+' button >> nth=1');
  await page.waitForFunction(()=>[...document.querySelectorAll('[role=menuitem]')].some(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.x>=0&&r.y>=0;}),undefined,{timeout:10000});
  const items=await labels();
  if(label){if(!items.includes(label))throw Error('Observed offline menu lacks '+label);await menu(page,label);}
  return items;
}

export async function findTarget(page,cfg) {
  await page.goto('https://work.open.taobao.com/open-skill/list');
  const dialog=await page.evaluate(()=>([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0))?.innerText.slice(0,60));
  if(dialog&&/版本记录|授权管理|上架到技能商店/.test(dialog))await closeDialog(page);
  await page.waitForSelector('input[placeholder="请输入"]',{timeout:20000});
  await account(page,cfg.account);
  if(cfg.searchName) {
    await page.fill('input[placeholder="请输入"]',cfg.searchName);
    await page.press('input[placeholder="请输入"]','Enter');
  }
  await page.waitForFunction(({selector,id,name})=>{
    const cards=[...document.querySelectorAll(selector)];
    return cards.length>0&&cards.some(e=>e.innerText.split(/\s+/).includes(id))&&(!name||cards.every(e=>e.innerText.includes(name)));
  },{selector:cardSelector,id:cfg.publicAppId,name:cfg.searchName},{timeout:20000});
  return card(page,cfg);
}
export async function readVersions(page,cfg) {
  await findTarget(page,cfg);
  await more(page,cfg,'版本管理');
  await page.waitForFunction(()=>([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0))?.innerText.includes('当前草稿'),undefined,{timeout:25000});
  const result=await page.evaluate(()=>{
    const d=[...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0);
    const rows=[...d.querySelectorAll('tr')];
    const entries=rows.map(row=>({raw:row.innerText,cells:[...row.querySelectorAll('td')].map(e=>e.innerText.trim())})).filter(x=>x.cells.length>=6).map(x=>({version:x.cells[0],reviewStatus:x.cells[1],onlineStatus:x.cells[3],raw:x.raw}));
    return {text:d.innerText,rows:rows.map(e=>e.innerText),entries};
  });
  if(cfg.receiptPath)await persist(cfg.receiptPath,{...cfg,action:undefined,versionReadback:result,observedAt:new Date().toISOString()});
  if(cfg.approvedDownload) {
    const matches=result.entries.filter(entry=>entry.version===cfg.approvedDownload.version);
    if(matches.length===1&&matches[0].reviewStatus==='审核通过') {
      result.approvedDownload=await downloadVersionRecord(page,{...cfg.approvedDownload,row:cfg.row,formalCode:cfg.formalCode,requireApproved:true});
      result.approvedDownload.account=cfg.account;result.approvedDownload.publicAppId=cfg.publicAppId;
    }
  }
  return result;
}
async function readListingForm(page) {
  await page.waitForLoadState('networkidle',{timeout:15000,idleMs:500});
  return page.evaluate(()=>{
    const d=([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0));
    const visible=e=>e.type!=='hidden'&&e.type!=='password'&&e.getBoundingClientRect().width>0;
    return {formalCode:d.querySelector('input[placeholder^="技能code"]')?.value,mode:d.querySelector('input[type=radio]:checked')?.value,
      fields:[...d.querySelectorAll('input[placeholder],textarea[placeholder]')].filter(visible).map(e=>({placeholder:e.placeholder,value:e.value})),
      agreementChecked:!!d.querySelector('input[type=checkbox]:checked'),iconDimensions:[...d.querySelectorAll('img')].filter(e=>e.complete&&e.naturalWidth>=128).map(e=>({width:e.naturalWidth,height:e.naturalHeight}))};
  });
}

export async function inspectTarget(page,cfg) {
  const mark=async stage=>{if(cfg.receiptPath)await fs.appendFile(cfg.receiptPath+'.trace.jsonl',JSON.stringify({stage,at:new Date().toISOString(),url:await page.url()})+'\n');};
  await mark('start');
  const found=await findTarget(page,cfg);
  await mark('target_found');
  let moreMenuBefore=[];
  if(found.previouslyListed){moreMenuBefore=await offlineMenu(page,cfg);await menu(page,'修改上架详情');}
  else await cardButton(page,cfg,0);
  await mark('listing_opened');
  const codeSelector='input[placeholder="技能code由小写字母、数字、中划线组成，必须以字母开头"]';
  await page.waitForSelector(codeSelector,{timeout:15000});
  const listing=await readListingForm(page);
  await mark('listing_read');
  if((found.listed||found.previouslyListed)&&!['0','1'].includes(listing.mode))throw Error('Existing listing mode must be observed before claiming it is preserved');
  if(cfg.formalCode&&listing.formalCode!==cfg.formalCode)throw Error('Formal code conflict');
  await closeDialog(page);
  await mark('listing_closed');
  let authorization={complete:false,shops:[],readback:''};
  if((found.listed||found.previouslyListed)&&listing.mode==='1'&&(!found.previouslyListed||moreMenuBefore.includes('授权管理'))) {
    if(found.previouslyListed)await offlineMenu(page,cfg,'授权管理');else await more(page,cfg,'授权管理');
    await mark('authorization_opened');
    await page.waitForFunction(()=>([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0))?.innerText.includes('添加授权店铺'),undefined,{timeout:15000});
    await page.waitForLoadState('networkidle',{timeout:15000,idleMs:800});
    authorization=await page.evaluate(()=>{
      const d=([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0));
      const pagination=d.querySelector('[class*="pagination"]');
      const disabled=e=>!!e&&(e.disabled||e.getAttribute('aria-disabled')==='true'||e.className.includes('disabled'));
      const next=d.querySelector('.tbd-pagination-next,[title="下一页"],[title="Next Page"],[aria-label="Next Page"]');
      const previous=d.querySelector('.tbd-pagination-prev,[title="上一页"],[title="Previous Page"],[aria-label="Previous Page"]');
      return {complete:!pagination||(disabled(next)&&disabled(previous)),shops:[...d.querySelectorAll('tbody tr')].map(e=>e.querySelector('td')?.innerText).filter(x=>x&&x!=='暂无授权店铺'),readback:d.innerText};
    });
    if(cfg.expectedExistingShops&&JSON.stringify([...authorization.shops].sort())!==JSON.stringify([...cfg.expectedExistingShops].sort()))throw Error('Existing shop authorization differs from the previous verified readback');
    await mark('authorization_read');
    if(!authorization.complete)throw Error('Paginated shop authorization needs full readback');
    await closeDialog(page);
  } else if(found.previouslyListed&&listing.mode==='1')authorization={complete:false,shops:[],unavailableWhileUnlisted:true,readback:'已下架的现有定向技能；当前更多菜单不提供授权管理，原授权名单不可读取'};
  else authorization={complete:true,shops:[],readback:'No existing targeted listing on the verified card'};
  let editorUrl;
  if(!cfg.skipEditorOpen) {
    await mark('before_open_editor');
    if(found.previouslyListed)await offlineMenu(page,cfg,'编辑技能');else await more(page,cfg,'编辑技能');
    await mark('editor_clicked');
    await page.waitForURL('**/open-skill/skill-detail?dataId=*',{timeout:20000});
    editorUrl=await page.url();
  }
  const result={row:cfg.row,account:cfg.account,publicAppId:cfg.publicAppId,searchName:cfg.searchName,formalCode:listing.formalCode,editorUrl,wasListed:found.listed,hadListing:found.listed||found.previouslyListed,offlineBefore:found.previouslyListed,moreMenuBefore,existingMode:(found.listed||found.previouslyListed)?(listing.mode==='1'?'定向订购':listing.mode==='0'?'公开订购':cfg.fallbackMode):(cfg.sourceMode||cfg.fallbackMode),authorizationReadback:authorization,listingBefore:listing,cardBefore:found.text,observedAt:new Date().toISOString()};
  if(!result.existingMode)throw Error('Unresolved listing mode');
  await persist(cfg.receiptPath,result);
  return result;
}
export function versionAuthorizationAllowed(target) {
  const authorization=target.authorizationReadback||{},menus=target.moreMenuBefore;
  if(authorization.complete===true)return true;
  return target.hadListing===true&&target.offlineBefore===true&&target.wasListed===false&&authorization.unavailableWhileUnlisted===true&&Array.isArray(menus)&&menus.every(x=>typeof x==='string')&&['修改上架详情','编辑技能','版本管理'].every(x=>menus.includes(x))&&!menus.includes('授权管理')&&({'0':'公开订购','1':'定向订购'}[target.listingBefore?.mode]===target.existingMode)&&['0','1'].includes(target.listingBefore?.mode);
}

export async function submitVersion(page,cfg) {
  if(await page.url()!==cfg.target.editorUrl)throw Error('Editor identity changed');
  await account(page,cfg.target.account);
  const proof=JSON.parse(await fs.readFile(cfg.proofPath,'utf8'));
  const sha=createHash('sha256').update(await fs.readFile(cfg.packagePath)).digest('hex');
  if(!proof.verified||proof.expected_package_sha256!==sha||sha!==cfg.packageSha256)throw Error('Entire fixed package must be verified before publish');
  const journal=await fs.readFile(cfg.journalPath,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return [];throw e;});
  if(journal.some(x=>x.row===cfg.row&&x.packageSha256===sha))throw Error('Version already has an intent; reconcile it, never repeat');
  if(!cfg.bm?.asset_revision||cfg.bm.phase!=='fixed_asset_verified'||cfg.bm.sha256!==sha)throw Error('Missing matching fixed BM asset');
  if(!versionAuthorizationAllowed(cfg.target))throw Error('Existing authorization requires a complete readback or observed offline unavailability');
  if(!cfg.note||cfg.note.length>200)throw Error('Reviewable version note required (max 200 characters)');
  await page.evaluate(()=>window.scrollTo({left:document.documentElement.scrollWidth,top:0}));
  await page.mouse.move(500,400);
  await button(page,'发布');
  await page.waitForFunction(()=>([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0))?.innerText.includes('发布版本'),undefined,{timeout:15000});
  const offered=await page.evaluate(()=>([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0))?.querySelector('input[disabled]')?.value);
  if(!/^\d+\.\d+\.\d+$/.test(offered)||offered!==cfg.expectedVersion)throw Error('Offered version differs; reconcile actual version records');
  await page.fill('[role=dialog] textarea[placeholder="请输入"]',cfg.note);
  const intent={row:cfg.row,target:cfg.target,packageSha256:sha,bm:{assetId:cfg.bm.asset_id,revision:cfg.bm.asset_revision,catalogId:cfg.bm.catalog_id},version:offered,note:cfg.note,phase:'version_submitting',intentAt:new Date().toISOString()};
  journal.push(intent);await persist(cfg.journalPath,journal);
  try {
    await nativeClick(page,'[role=dialog] button[class*="confirmBtn--"]');
    await page.waitForURL('https://work.open.taobao.com/open-skill/list',{timeout:30000});
    intent.phase='version_requested';intent.requestReturnedAt=new Date().toISOString();
    await persist(cfg.journalPath,journal);
  } catch(error) {
    intent.phase='version_unknown';await persist(cfg.journalPath,journal);throw error;
  }
  return intent;
}

/** A boolean proof alone cannot identify the approved package to activate/list. */
export function requireApprovedPackage(cfg,proof,version) {
  const b=proof?.approvalBinding;
  if(!proof?.verified||!version||!cfg.packageSha256||proof.expected_package_sha256!==cfg.packageSha256||
      !b||b.account!==cfg.account||b.publicAppId!==cfg.publicAppId||b.formalCode!==cfg.formalCode||
      b.version!==version||b.packageSha256!==cfg.packageSha256||b.downloadVersion!==version||
      b.actualDownloadSha256!==proof.actual_download_sha256)throw Error('Approved package proof is not bound to this account, target, version and frozen package');
}

export function requireLatestActivation(version,entries) {
  if(!/^\d+\.\d+\.\d+$/.test(version))throw Error('Exact semantic activation version required');
  const target=version.split('.').map(Number);
  const versions=entries.filter(e=>e.version!=='当前草稿').map(e=>{
    if(!/^\d+\.\d+\.\d+$/.test(e.version))throw Error('Unknown platform revision needs reconciliation');
    return e.version.split('.').map(Number);
  });
  if(!versions.some(v=>v.every((part,index)=>part===target[index])))throw Error('Activation version not observed');
  if(versions.some(v=>v[0]>target[0]||(v[0]===target[0]&&(v[1]>target[1]||(v[1]===target[1]&&v[2]>target[2])))))throw Error('Newer platform revision observed; do not activate an older batch revision');
}

export async function activateVersion(page,cfg) {
  requireApprovedPackage(cfg,cfg.packageProof,cfg.version);
  const versions=await readVersions(page,{...cfg,receiptPath:undefined});
  requireLatestActivation(cfg.version,versions.entries);
  const row=await page.evaluate(version=>{
    const rows=[...([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0)).querySelectorAll('tbody tr')];
    const matches=rows.map((e,index)=>({index,version:e.querySelector('td')?.innerText.trim(),text:e.innerText,buttons:[...e.querySelectorAll('button')].map(x=>x.innerText)})).filter(x=>x.version===version);
    if(matches.length!==1)return null;return matches[0];
  },cfg.version);
  if(!row||!row.text.includes('审核通过'))throw Error('Version approval not observed');
  if(row.text.includes('线上版本'))return {version:cfg.version,alreadyOnline:true,readback:row.text};
  if(!row.buttons.includes('上线'))throw Error('No observed version activation control');
  const journal=await fs.readFile(cfg.journalPath,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return [];throw e;});
  if(journal.some(x=>x.action==='activate-version'&&x.publicAppId===cfg.publicAppId&&x.version===cfg.version))throw Error('Existing activation intent needs reconciliation');
  const intent={action:'activate-version',publicAppId:cfg.publicAppId,version:cfg.version,phase:'activation_submitting',at:new Date().toISOString()};journal.push(intent);await persist(cfg.journalPath,journal);
  // The visible row was verified before selecting its exact native button.
  const selector='[role=dialog] tbody tr:nth-child('+(row.index+1)+') button';
  const buttons=await page.evaluate(selector=>[...document.querySelectorAll(selector)].map(x=>x.innerText),selector);
  const index=buttons.indexOf('上线');
  await page.click(selector+' >> nth='+index);
  intent.phase='activation_requested';await persist(cfg.journalPath,journal);
  return intent;
}

export async function prepareListing(page,cfg) {
  const found=await findTarget(page,cfg);
  if(found.listed&&!cfg.explicitMetadataUpdate)return {alreadyListed:true,cardReadback:found.text,metadataUnchanged:true};
  if(found.previouslyListed)throw Error('Existing offline listing requires restoration; preserve its metadata');
  await cardButton(page,cfg,0);
  await page.waitForSelector('input[placeholder^="技能code"]',{timeout:15000});
  const formal=await page.evaluate(()=>document.querySelector('[role=dialog] input[placeholder^="技能code"]')?.value);
  if(formal!==cfg.formalCode)throw Error('Listing formal code changed');
  if(!['0','1'].includes(cfg.mode))throw Error('Explicit observed or user-selected listing mode required');
  await nativeClick(page,'[role=dialog] label:has(input[type=radio][value='+JSON.stringify(cfg.mode)+'])');
  // Every field is supplied from reviewed publication metadata. Repeated names
  // are selected by an explicit occurrence index, never a global Select All.
  for(const field of cfg.fields||[]) {
    if(!field.placeholder||typeof field.value!=='string')throw Error('Reviewed listing field required');
    const selector='[role=dialog] :is(input,textarea)[placeholder='+JSON.stringify(field.placeholder)+']';
    await page.fill(selector+' >> nth='+(field.index||0),field.value);
  }
  let iconReadback=await page.evaluate(()=>{
    const f=[...document.querySelectorAll('[role=dialog] .tbd-form-item')].find(e=>e.querySelector('label[for="logo"]'));
    const e=[...(f?.querySelectorAll('img')||[])].find(e=>e.complete&&e.naturalWidth>=128);
    return e?{width:e.naturalWidth,height:e.naturalHeight,preservedExisting:true}:null;
  });
  if(cfg.iconPath&&!iconReadback) {
    const bytes=await fs.readFile(cfg.iconPath);
    const sha=createHash('sha256').update(bytes).digest('hex');
    const image=bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))||(bytes[0]===255&&bytes[1]===216);
    if(!image||sha!==cfg.iconSha256)throw Error('Reviewed PNG/JPEG icon bytes changed');
    await page.setInputFiles('[role=dialog] .tbd-form-item:has(label[for="logo"]) input[type=file]',cfg.iconPath);
    await page.waitForFunction(()=>[...document.querySelectorAll('[role=dialog]')].some(e=>e.getBoundingClientRect().width>0&&e.innerText.includes('裁剪图片')&&e.innerText.includes('确认并上传')),undefined,{timeout:15000});
    await button(page,'确认并上传');
    await page.waitForFunction(()=>{const f=[...document.querySelectorAll('[role=dialog] .tbd-form-item')].find(e=>e.querySelector('label[for="logo"]'));return [...(f?.querySelectorAll('img')||[])].some(e=>e.complete&&e.naturalWidth>=128);},undefined,{timeout:30000});
    iconReadback=await page.evaluate(()=>{const f=[...document.querySelectorAll('[role=dialog] .tbd-form-item')].find(e=>e.querySelector('label[for="logo"]'));const e=[...(f?.querySelectorAll('img')||[])].find(e=>e.complete&&e.naturalWidth>=128);return {width:e.naturalWidth,height:e.naturalHeight};});
    iconReadback.sourceSha256=sha;
  }
  const result=await page.evaluate(()=>{
    const d=([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0));
    return {formalCode:d.querySelector('input[placeholder^="技能code"]')?.value,mode:d.querySelector('input[type=radio]:checked')?.value,agreementChecked:!!d.querySelector('input[type=checkbox]:checked'),visibleValidation:[...d.querySelectorAll('[class*="explain-error"]')].map(e=>e.innerText),text:d.innerText};
  });
  if(result.mode!==cfg.mode)throw Error('Prepared listing mode did not persist');
  for(const field of cfg.fields||[]) {
    const actual=await page.evaluate(field=>{const d=[...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0);return [...d.querySelectorAll('input[placeholder],textarea[placeholder]')].filter(e=>e.placeholder===field.placeholder)[field.index||0]?.value;},field);
    if(actual!==field.value)throw Error('Prepared listing field differs from reviewed metadata');
  }
  await persist(cfg.receiptPath,{...result,iconReadback,account:cfg.account,publicAppId:cfg.publicAppId,preparedAt:new Date().toISOString()});
  return {...result,iconReadback,userAgreementRequired:!result.agreementChecked};
}

export function requireFreshOnlineVersion(cfg,now=Date.now()) {
  const o=cfg.onlineObservation,age=o?now-Date.parse(o.observedAt):NaN;
  if(!o||!Number.isFinite(age)||age< -5000||age>60000||o.account!==cfg.account||o.publicAppId!==cfg.publicAppId||o.formalCode!==cfg.formalCode||o.version!==cfg.approvedVersion||o.packageSha256!==cfg.packageSha256||o.versionReadback?.split('\t')[0].trim()!==cfg.approvedVersion||o.reviewStatus!=='审核通过'||o.onlineStatus!=='线上版本'||!o.versionReadback.includes('线上版本')||!o.versionReadback.includes('审核通过'))throw Error('Fresh same-target online-version evidence required before listing');
}

export async function submitListing(page,cfg) {
  await account(page,cfg.account);
  const state=await page.evaluate(()=>{
    const d=([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0));
    return {formalCode:d?.querySelector('input[placeholder^="技能code"]')?.value,mode:d?.querySelector('input[type=radio]:checked')?.value,agreementChecked:!!d?.querySelector('input[type=checkbox]:checked'),text:d?.innerText,iconPresent:[...(d?.querySelector('.tbd-form-item:has(label[for="logo"])')?.querySelectorAll('img')||[])].some(e=>e.complete&&e.naturalWidth>=128)};
  });
  if(state.formalCode!==cfg.formalCode||state.mode!==cfg.mode)throw Error('Prepared listing identity or mode changed');
  for(const field of cfg.fields||[]) {
    const actual=await page.evaluate(field=>{const d=[...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0);return [...d.querySelectorAll('input[placeholder],textarea[placeholder]')].filter(e=>e.placeholder===field.placeholder)[field.index||0]?.value;},field);
    if(actual!==field.value)throw Error('Listing metadata changed after preparation; review it before submitting');
  }
  if(!state.agreementChecked||!cfg.userAgreementHandled)throw Error('User must read and handle the visible platform agreement before this listing submission');
  requireFreshOnlineVersion(cfg);
  if(cfg.iconPath&&!state.iconPresent)throw Error('Prepared listing icon is missing');
  requireApprovedPackage(cfg,cfg.approvedVersionPackageProof,cfg.approvedVersion);
  const journal=await fs.readFile(cfg.journalPath,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return [];throw e;});
  if(journal.some(x=>['listing','restore_listing'].includes(x.action)&&x.publicAppId===cfg.publicAppId))throw Error('Existing listing intent needs reconciliation');
  const intent={action:'listing',account:cfg.account,publicAppId:cfg.publicAppId,formalCode:cfg.formalCode,mode:cfg.mode,version:cfg.approvedVersion,packageSha256:cfg.packageSha256,phase:'listing_submitting',at:new Date().toISOString()};journal.push(intent);await persist(cfg.journalPath,journal);
  // Current listing forms use submitBtn; older forms retain confirmBtn.
  // nativeClick still requires one visible, enabled control before dispatch.
  await nativeClick(page,'[role=dialog] button:is([class*="confirmBtn--"],[class*="submitBtn--"])');
  intent.phase='listing_requested';await persist(cfg.journalPath,journal);
  return intent;
}


export function requireRestorationState(cfg,cardState,listing) {
  const expected=cfg.existingListing;
  if(cfg.restoreExistingListingAuthorized!==true||!cardState.previouslyListed||cardState.listed||!expected||!['0','1'].includes(cfg.mode))throw Error('Explicit restoration of an existing offline listing required');
  const tag=cfg.mode==='1'?'定向':'公开';
  if(!cardState.statusLabels.includes(tag)||listing.formalCode!==cfg.formalCode||listing.mode!==cfg.mode||expected.formalCode!==cfg.formalCode||expected.mode!==cfg.mode)throw Error('Existing restoration identity or mode changed');
  if(JSON.stringify(listing.fields)!==JSON.stringify(expected.fields)||JSON.stringify(listing.iconDimensions||[])!==JSON.stringify(expected.iconDimensions||[]))throw Error('Existing listing metadata changed; review before restoring');
}

export function requireRestorationConfirmation(confirmation) {
  const expected='上架确认上架技能？技能上架后，将可被展示及订购确定取消';
  if(!confirmation||confirmation.checkboxes||confirmation.text.replace(/\s+/gu,'')!==expected||JSON.stringify(confirmation.buttons.filter(Boolean))!==JSON.stringify(['确定','取消']))throw Error('Unexpected restoration confirmation or user agreement; stop for review');
}

export async function restoreExistingListing(page,cfg) {
  if(cfg.restoreExistingListingAuthorized!==true)throw Error('Explicit existing-listing restoration authorization required');
  requireApprovedPackage(cfg,cfg.approvedVersionPackageProof,cfg.approvedVersion);
  const versions=await readVersions(page,{account:cfg.account,publicAppId:cfg.publicAppId,formalCode:cfg.formalCode,searchName:cfg.searchName});
  requireLatestActivation(cfg.approvedVersion,versions.entries);
  const online=versions.entries.filter(e=>e.onlineStatus==='线上版本');
  if(online.length!==1||online[0].version!==cfg.approvedVersion||online[0].reviewStatus!=='审核通过')throw Error('Restoration requires the verified approved online version');
  const observation={account:cfg.account,publicAppId:cfg.publicAppId,formalCode:cfg.formalCode,version:cfg.approvedVersion,packageSha256:cfg.packageSha256,reviewStatus:online[0].reviewStatus,onlineStatus:online[0].onlineStatus,versionReadback:online[0].raw,observedAt:new Date().toISOString()};
  const found=await findTarget(page,cfg);
  if(!found.previouslyListed||found.listed)throw Error('Offline listing changed; reconcile before restoration');
  await offlineMenu(page,cfg,'修改上架详情');
  await page.waitForSelector('input[placeholder^="技能code"]',{timeout:15000});
  const listing=await readListingForm(page);
  requireRestorationState(cfg,found,listing);
  await closeDialog(page);
  // The existing official "去上架" control restores saved metadata. Do not save
  // the detail form or handle its agreement checkbox on the user's behalf.
  const current=await card(page,cfg);
  if(!current.previouslyListed||current.listed)throw Error('Restoration card changed');
  await page.hover(current.selector);
  await page.click(current.selector+' button >> nth=0');
  await page.waitForFunction(()=>[...document.querySelectorAll('[role=dialog]')].some(e=>e.getBoundingClientRect().width&&e.innerText.includes('确认上架技能')),undefined,{timeout:15000});
  const confirmation=await page.evaluate(()=>{
    const dialogs=[...document.querySelectorAll('[role=dialog]')].filter(e=>e.getBoundingClientRect().width&&e.getBoundingClientRect().height);
    if(dialogs.length!==1)return null;const d=dialogs[0];return {text:d.innerText,checkboxes:d.querySelectorAll('input[type=checkbox]').length,buttons:[...d.querySelectorAll('button')].map(e=>e.innerText.trim())};
  });
  requireRestorationConfirmation(confirmation);
  requireFreshOnlineVersion({...cfg,onlineObservation:observation});
  const journal=await fs.readFile(cfg.journalPath,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return [];throw e;});
  if(journal.some(x=>['listing','restore_listing'].includes(x.action)&&x.publicAppId===cfg.publicAppId))throw Error('Existing listing/restoration intent needs reconciliation');
  const intent={action:'restore_listing',row:cfg.row,account:cfg.account,publicAppId:cfg.publicAppId,formalCode:cfg.formalCode,mode:cfg.mode,version:cfg.approvedVersion,packageSha256:cfg.packageSha256,metadataNotChangedByWorkflow:true,authorizationNotChangedByWorkflow:true,phase:'listing_submitting',at:new Date().toISOString()};
  journal.push(intent);await persist(cfg.journalPath,journal);
  try {
    await button(page,'确定');
    await page.waitForFunction(()=>{
      const visible=e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0;
      const errors=[...document.querySelectorAll('[role=alert],[class*="message-notice"],[class*="explain-error"]')].filter(visible).some(e=>/失败|错误|不支持|不可|不能|无法|无权|不足|未通过|异常|请勾选/.test(e.innerText));
      return ![...document.querySelectorAll('[role=dialog]')].some(visible)||errors;
    },undefined,{timeout:20000});
    const outcome=await page.evaluate(()=>{
      const visible=e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0;
      return {dialogOpen:[...document.querySelectorAll('[role=dialog]')].some(visible),errors:[...document.querySelectorAll('[role=alert],[class*="message-notice"],[class*="explain-error"]')].filter(visible).map(e=>e.innerText.trim()).filter(t=>/失败|错误|不支持|不可|不能|无法|无权|不足|未通过|异常|请勾选/.test(t)).map(t=>/token|secret|password|cookie|密钥|密码/i.test(t)?'平台显示认证或敏感配置提示，请在页面核对':t.slice(0,300))};
    });
    if(outcome.dialogOpen||outcome.errors.length){intent.visiblePlatformErrors=outcome.errors;throw Error('Restoration not confirmed: '+(outcome.errors.join('；')||'confirmation remains open'));}
    await page.waitForLoadState('networkidle',{timeout:20000,idleMs:800});
    intent.phase='listing_requested';await persist(cfg.journalPath,journal);
  } catch(error) {
    intent.phase='listing_unknown';intent.outcomeObservedAt=new Date().toISOString();await persist(cfg.journalPath,journal);throw error;
  }
  return intent;
}
