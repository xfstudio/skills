/** Logged-in Ego UI operations. No cookies, private app objects, or hidden HTTP APIs. */
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';

/** Wait for native UI Fetch/XHR completion, ignoring persistent editor worker scripts.
 * Only event type and request IDs are read; URLs, headers and payloads are never inspected.
 */
export async function waitForUiIdle(page,{timeout=20000,quietMs=500}={}) {
  const pending=new Set();let lastActivity=Date.now();const deadline=lastActivity+timeout;
  while(Date.now()<deadline) {
    for(const event of await page.events()) {
      const params=event.params||{},key=String(event.sessionId||'')+':'+params.requestId;
      if(event.method==='Network.requestWillBeSent'&&['Fetch','XHR','Document'].includes(params.type)) {
        pending.add(key);lastActivity=Date.now();
      } else if(['Network.loadingFinished','Network.loadingFailed'].includes(event.method)&&pending.delete(key))lastActivity=Date.now();
    }
    if(!pending.size&&Date.now()-lastActivity>=quietMs)return;
    await new Promise(resolve=>setTimeout(resolve,50));
  }
  throw Error('Native UI requests did not settle; do not infer a saved workspace');
}

/** Use the observed DOM hit point when page-width scrolling makes locator input unreliable. */
export async function nativeClick(page,selector,index=null,text=null) {
  await page.cdp('Page.bringToFront');
  const target={selector,index,text};
  const resolve=async({selector,index,text,scroll})=>{
    await new Promise(requestAnimationFrame);
    const candidates=()=>[...document.querySelectorAll(selector)].filter(e=>{
      const r=e.getBoundingClientRect();
      return r.width>0&&r.height>0&&(!text||(e.innerText.trim()===text&&r.x>=0&&r.y>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))));
    });
    const list=candidates();
    if(index===null&&list.length!==1)return null;
    const e=list[index===null?0:index];
    if(!e||e.disabled||e.getAttribute('aria-disabled')==='true')return null;
    if(scroll){e.scrollIntoView({block:'nearest',inline:'nearest'});await new Promise(requestAnimationFrame);}
    const fresh=candidates();
    if((index===null&&fresh.length!==1)||fresh[index===null?0:index]!==e)return null;
    for(let node=e;node&&node!==document.body;node=node.parentElement) {
      if(node.getAnimations().some(a=>a.playState==='running'&&a.effect?.getTiming().iterations!==Infinity))return null;
    }
    const r=e.getBoundingClientRect();
    if(r.x<0||r.y<0||r.right>innerWidth||r.bottom>innerHeight||!e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)))return null;
    return {x:r.x+r.width/2,y:r.y+r.height/2};
  };
  const deadline=Date.now()+15000;
  while(Date.now()<deadline) {
    const point=await page.evaluate(resolve,{...target,scroll:true});
    if(!point)continue;
    await page.mouse.move(point.x,point.y);
    const ready=await page.evaluate(resolve,{...target,scroll:false});
    if(!ready||Math.abs(point.x-ready.x)>1||Math.abs(point.y-ready.y)>1)continue;
    // Only pre-click reads/hover are retried. Dispatch the actual click once.
    return page.mouse.click(ready.x,ready.y);
  }
  throw Error('Native click target did not stabilize: '+selector+' text='+String(text));
}

export async function nativeHover(page,selector,index=0) {
  await page.cdp('Page.bringToFront');
  const target={selector,index};
  await page.evaluate(({selector,index})=>[...document.querySelectorAll(selector)].filter(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0)[index]?.scrollIntoView({block:'nearest',inline:'nearest'}),target);
  const point=await page.evaluate(({selector,index})=>{const e=[...document.querySelectorAll(selector)].filter(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0)[index];const r=e?.getBoundingClientRect();if(!r?.width||!r?.height)throw Error('Hover target not visible');return {x:r.x+r.width/2,y:r.y+r.height/2};},target);
  await page.mouse.move(point.x,point.y);
}

async function visibleTextTarget(page,selector,text) {
  await page.waitForFunction(({selector,text})=>[...document.querySelectorAll(selector)].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.x>=0&&r.y>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&e.innerText.trim()===text&&e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));}).length===1,{selector,text},{timeout:20000});
}

export async function menu(page, text, hover=false) {
  await visibleTextTarget(page,'[role=menuitem]',text);
  return hover ? page.hover('loc=role:menuitem[name='+JSON.stringify(text)+']') : nativeClick(page,'[role=menuitem]',null,text);
}

export async function button(page,text) {
  await visibleTextTarget(page,'button',text);
  return nativeClick(page,'button',null,text);
}

export async function exportTable(page,cfg) {
  if (!cfg.url || !cfg.tableName || !cfg.output?.startsWith('/')) throw Error('Explicit table URL, name, and absolute output required');
  const expected=new URL(cfg.url);
  if (!expected.hostname.endsWith('.feishu.cn') || !expected.searchParams.get('table')) throw Error('Not a user-selected Feishu table');
  if (await page.url() !== cfg.url) await page.goto(cfg.url);
  await page.waitForSelector('button.more-btn',{timeout:20000});
  const opened=await page.evaluate(()=>[...document.querySelectorAll('[role=menuitem]')].some(
    e=>e.innerText?.trim()==='导出'&&e.getBoundingClientRect().height>0,
  ));
  if(!opened)await page.click('button.more-btn');
  await menu(page,'导出');
  await menu(page,'Excel/CSV 文件');
  await page.waitForFunction(name=>[...document.querySelectorAll('[role=dialog]')].some(
    e=>e.innerText.includes('下载设置')&&e.innerText.includes(name)&&e.innerText.includes('Excel'),
  ),cfg.tableName,{timeout:20000});
  const download=page.waitForEvent('download',{timeout:45000});
  await button(page,'下载');
  await (await download).saveAs(cfg.output);
  return {saved:cfg.output,tableUrl:cfg.url,credentialColumnsMustBeRedacted:true};
}

export async function tree(page) {
  return page.evaluate(()=>{
    const stack=[];
    return [...document.querySelectorAll('.tbd-tree-treenode[role=treeitem]')].map((node,index)=>{
      const depth=node.querySelectorAll('.tbd-tree-indent-unit').length;
      const name=node.querySelector('.tbd-tree-node-content-wrapper')?.getAttribute('title');
      stack[depth]=name;stack.length=depth+1;
      return {index,name,path:stack.slice(1).join('/'),expanded:node.getAttribute('aria-expanded')};
    });
  });
}

function treeRow(index) {return `xpath=(//*[@role="treeitem"])[${index+1}]`;}

async function treeMenu(page,path,label) {
  const node=(await tree(page)).find(x=>x.path===path);
  if (!node) throw Error('Folder not visible: '+path);
  const wrapper='.tbd-tree-node-content-wrapper[title='+JSON.stringify(node.name)+']';
  await nativeHover(page,wrapper);
  const more='.tbd-tree-treenode[role=treeitem]:has(> '+wrapper+') span[class*="moreIcon--"]';
  await nativeClick(page,more);
  await menu(page,label);
}

async function ensureFolder(page,path) {
  if (!path) return;
  const parts=path.split('/'),name=parts.pop(),parent=parts.join('/');
  await ensureFolder(page,parent);
  let node=(await tree(page)).find(x=>x.path===path);
  if (!node) {
    await treeMenu(page,parent,'新建文件夹');
    await page.fill('input[placeholder="文件夹名称"]',name);
    await page.press('input[placeholder="文件夹名称"]','Enter');
    await page.waitForFunction(()=>!document.querySelector('input[placeholder="文件夹名称"]'),undefined,{timeout:20000});
    node=(await tree(page)).find(x=>x.path===path);
    if (!node) throw Error('New folder not observed: '+path);
  }
  if (node.expanded==='false') {
    const switcher='.tbd-tree-treenode[role=treeitem]:has(> .tbd-tree-node-content-wrapper[title='+JSON.stringify(name)+']) > .tbd-tree-switcher';
    await nativeClick(page,switcher);
    await page.waitForFunction(name=>[...document.querySelectorAll('.tbd-tree-treenode[role=treeitem]')].some(
      x=>x.querySelector('.tbd-tree-node-content-wrapper')?.getAttribute('title')===name&&x.getAttribute('aria-expanded')==='true',
    ),name,{timeout:20000});
    await waitForUiIdle(page,{timeout:20000,quietMs:300});
  }
}

async function saveFile(page) {
  await page.waitForSelector('button[class*="flowingBorderBtn--"]',{timeout:20000});
  for (let attempt=0;attempt<2;attempt++) {
    // A minimum-width page can leave Save outside the viewport; moving away
    // from the account hover menu prevents that menu intercepting the click.
    await page.evaluate(()=>window.scrollTo({left:document.documentElement.scrollWidth,top:0}));
    await page.mouse.move(500,400);
    await page.waitForFunction(()=>{
      const b=document.querySelector('button[class*="flowingBorderBtn--"]');
      if(!b)return false;const r=b.getBoundingClientRect();
      return b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));
    },undefined,{timeout:10000});
    await nativeClick(page,'button[class*="flowingBorderBtn--"]');
    try {
      await page.waitForFunction(()=>!document.querySelector('button[class*="flowingBorderBtn--"]'),undefined,{timeout:25000});
      return;
    } catch(error) {
      const state=await page.evaluate(()=>({dirty:!!document.querySelector('button[class*="flowingBorderBtn--"]'),dialog:!!([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0))}));
      if(attempt || !state.dirty || state.dialog)throw error;
      // Re-save the same fixed file after observing an unchanged dirty state.
      // This does not retry a version/listing submission. ZIP readback remains mandatory.
    }
  }
}

// Existing platform codes can include underscores. A strict end assertion also
// rejects a final newline, which JavaScript's $ anchor would otherwise allow.
function validFormalCode(code) {
  return typeof code==='string'&&/^[a-z][a-z0-9_-]{0,63}(?![\s\S])/.test(code);
}

/** The platform workspace is keyed by its verified formal code. Normalize only
 * the primary frontmatter name line, which the whole-ZIP comparator explicitly permits.
 */
export function platformFileContent(file,formalCode) {
  if(file.path!=='SKILL.md')return file.content;
  if(!validFormalCode(formalCode))throw Error('Verified formal code required');
  const lines=file.content.match(/[^\n]*\n|[^\n]+$/g)||[];
  if(lines[0]?.trim()!=='---')throw Error('Primary SKILL frontmatter is missing');
  const end=lines.findIndex((line,index)=>index>0&&line.trim()==='---');
  const names=lines.map((line,index)=>({line,index})).filter(x=>x.index>0&&x.index<end&&x.line.startsWith('name: '));
  if(names.length!==1)throw Error('Unique primary name line required');
  const {line,index}=names[0],ending=line.endsWith('\r\n')?'\r\n':line.endsWith('\n')?'\n':'';
  lines[index]='name: '+formalCode+ending;
  return lines.join('');
}

export async function updateFiles(page,cfg) {
  if(await page.url()!==cfg.editorUrl)throw Error('Editor identity changed');
  if(!Array.isArray(cfg.files)||!cfg.files.length)throw Error('Explicit reviewed file changes required');
  const openMenu=await page.evaluate(()=>[...document.querySelectorAll('[role=menu]')].some(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0));
  if(openMenu) {
    await page.keyboard.press('Escape');
    const remains=await page.evaluate(()=>[...document.querySelectorAll('[role=menu]')].some(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0));
    if(remains)await page.click('text="工作空间"');
    await page.waitForFunction(()=>![...document.querySelectorAll('[role=menu]')].some(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0),undefined,{timeout:5000});
  }

  await page.cdp('Network.enable');
  await page.waitForFunction(code=>document.querySelector('.tbd-tree-treenode[role=treeitem] .tbd-tree-node-content-wrapper')?.getAttribute('title')===code,cfg.formalCode,{timeout:30000});
  const rootExpanded=await page.evaluate(()=>document.querySelector('.tbd-tree-treenode[role=treeitem]')?.getAttribute('aria-expanded'));
  if(rootExpanded==='false')await nativeClick(page,'.tbd-tree-treenode[role=treeitem]:has(> .tbd-tree-node-content-wrapper[title='+JSON.stringify(cfg.formalCode)+']) > .tbd-tree-switcher');
  await page.waitForFunction(()=>[...document.querySelectorAll('.tbd-tree-node-content-wrapper')].some(e=>e.getAttribute('title')==='SKILL.md'),undefined,{timeout:30000});
  const previous=cfg.receiptPath?await fs.readFile(cfg.receiptPath,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return {};throw e;}):{};
  const results=previous.row===cfg.row?(previous.files||[]):[];
  for(const file of cfg.files) {
    if(createHash('sha256').update(file.content,'utf8').digest('hex')!==file.sha256)throw Error('Reviewed editor payload digest changed');
    const content=platformFileContent(file,cfg.formalCode);
    const savedSha256=createHash('sha256').update(content,'utf8').digest('hex');
    // cfg.files came from a fresh full-ZIP diff. An older UI-save receipt
    // cannot override that observation; reapply these exact idempotent edits.
    const parts=file.path.split('/');
    if(parts.some(x=>!x||x==='.'||x==='..')||file.path.includes('\\'))throw Error('Unsafe workspace file path');
    const name=parts.pop(),parent=parts.join('/');
    await ensureFolder(page,parent);
    const node=(await tree(page)).find(x=>x.path===file.path);
    if(node) {
      const unique=await page.evaluate(name=>[...document.querySelectorAll('.tbd-tree-node-content-wrapper')].filter(e=>e.getAttribute('title')===name).length,name);
      if(unique===1)await nativeClick(page,'.tbd-tree-node-content-wrapper[title='+JSON.stringify(name)+']');
      else await page.click(treeRow(node.index)+'/span[contains(@class,"tbd-tree-node-content-wrapper")]');
    }
    else {
      await treeMenu(page,parent,'新建文件');
      await page.fill('input[placeholder="文件名称"]',name);
      await page.press('input[placeholder="文件名称"]','Enter');
      await page.waitForFunction(()=>!document.querySelector('input[placeholder="文件名称"]'),undefined,{timeout:20000});
    }
    await page.waitForFunction(name=>document.querySelector('.tbd-tree-node-selected')?.getAttribute('title')===name||document.querySelector('.tbd-tree-node-selected')?.innerText===name,name,{timeout:60000});
    const markdown=name.toLowerCase().endsWith('.md');
    const selector=markdown?'.cm-content':'textarea[aria-label="Editor content"]';
    await page.waitForSelector(selector,{timeout:20000});
    await waitForUiIdle(page,{timeout:20000,quietMs:300});
    await page.cdp('Page.bringToFront');
    await page.press(selector,'ControlOrMeta+A');
    const focused=await page.evaluate(()=>({cm:document.activeElement?.classList.contains('cm-content'),monaco:document.activeElement?.getAttribute('aria-label')==='Editor content'}));
    if(markdown?!focused.cm:!focused.monaco)throw Error('Wrong editable focus');
    await page.keyboard.paste(content);
    await page.press(selector,markdown?'ControlOrMeta+Home':'Meta+ArrowUp');
    await saveFile(page);
    await waitForUiIdle(page,{timeout:30000,quietMs:500});
    const previousIndex=results.findIndex(x=>x.path===file.path);
    if(previousIndex>=0)results.splice(previousIndex,1);
    results.push({path:file.path,sha256:savedSha256,sourceSha256:file.sha256,uiSaved:true});
    if(cfg.receiptPath)await fs.writeFile(cfg.receiptPath,JSON.stringify({row:cfg.row,files:results,zipReadbackRequired:true},null,2));
  }
  return {row:cfg.row,files:results,zipReadbackRequired:true};
}

export async function clickDraftDownload(page,cfg) {
  if(!validFormalCode(cfg.formalCode))throw Error('Verified formal skill code required');
  if(await page.url()!==cfg.editorUrl)throw Error('Editor identity changed');
  const dirty=await page.evaluate(()=>!!document.querySelector('button[class*="flowingBorderBtn--"]'));
  if(dirty)throw Error('Unsaved workspace must be resolved before downloading its persisted package');
  // A full reload is only a recovery option. Normal downloads use the native
  // version dialog after saved UI requests settle, avoiding redundant portal loads.
  if(cfg.reloadBeforeDownload)await page.reload();
  await page.waitForFunction(code=>document.querySelector('.tbd-tree-node-content-wrapper')?.getAttribute('title')===code,cfg.formalCode,{timeout:25000});
  await page.evaluate(()=>window.scrollTo({left:document.documentElement.scrollWidth,top:0}));
  const open=await page.evaluate(()=>([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0))?.innerText.includes('当前草稿'));
  if(!open) {
    await page.mouse.move(500,400);
    await nativeClick(page,'button:has(span[aria-label="field-time"])');
  }
  await page.waitForFunction(()=>([...document.querySelectorAll('[role=dialog]')].find(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0))?.innerText.includes('当前草稿'),undefined,{timeout:25000});
  return downloadVersionRecord(page,cfg);
}

export function selectVersionDownload(rows,version,requireApproved=false) {
  const matches=rows.filter(row=>row.version===version);
  if(matches.length!==1)throw Error('No unique requested version download control');
  const row=matches[0];
  if(row.buttons[0]!=='下载')throw Error('Requested version download button changed');
  if(requireApproved&&(!/^\d+\.\d+\.\d+$/.test(version)||row.reviewStatus!=='审核通过'))throw Error('Requested version is not approved');
  return row;
}

/** The caller binds the current native dialog to either its verified workspace
 * or a freshly located account/AppID card. Never resolve a download URL directly.
 */
export async function downloadVersionRecord(page,cfg) {
  if(!validFormalCode(cfg.formalCode))throw Error('Verified formal skill code required');
  const version=cfg.version||'当前草稿';
  const visible=await page.evaluate(()=>{
    const dialogs=[...document.querySelectorAll('[role=dialog]')].filter(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0&&e.innerText.includes('当前草稿'));
    if(dialogs.length!==1)throw Error('No unique native version dialog');
    const d=dialogs[0];
    return {rows:[...d.querySelectorAll('tbody tr')].map((row,index)=>({index,version:row.querySelector('td')?.innerText.trim(),reviewStatus:row.querySelectorAll('td')[1]?.innerText.trim(),buttons:[...row.querySelectorAll('button')].map(e=>e.innerText.trim())})),versionRecords:d.innerText};
  });
  const selected=selectVersionDownload(visible.rows,version,!!cfg.requireApproved);
  const before=(await fs.readdir(cfg.downloadsDir)).filter(x=>x.startsWith(cfg.formalCode)&&x.endsWith('.zip'));
  const operation={row:cfg.row,formalCode:cfg.formalCode,version,reviewStatus:selected.reviewStatus,startedAt:Date.now()/1000,files:before,versionRecords:visible.versionRecords};
  await fs.writeFile(cfg.operationFile,JSON.stringify(operation,null,2));
  // A transient native download child is not observed by the parent download event.
  await nativeClick(page,'[role=dialog] tbody tr:nth-child('+(selected.index+1)+') button',0);
  return {...operation,downloadClicked:true};
}

export async function run(api,cfg) {
  const entry=(await api.listTaskSpaces()).find(x=>x.id===cfg.spaceId);
  if(!entry)throw Error('The existing task space is unavailable; do not create a recovery space');
  if(entry.ownership==='user'||(entry.ownership==='agentDelegatedToUser'&&!cfg.resumeUserHandoff))throw Error('User control pending; stop browser work');
  const task=entry.ownership==='agentDelegatedToUser'?await api.takeOverTaskSpace(cfg.spaceId):await api.taskSpace(cfg.spaceId);
  const page=task.page(cfg.page);
  if(cfg.action==='export-table')return exportTable(page,cfg);
  if(cfg.action==='update-files')return updateFiles(page,cfg);
  if(cfg.action==='download-draft')return clickDraftDownload(page,cfg);
  throw Error('Unsupported explicit browser action');
}
