if (!Number.isInteger(syncConfig.spaceId) || !syncConfig.pageLabel || !syncConfig.output || !Number.isInteger(syncConfig.expectedTotal) || !syncConfig.account) throw Error('INVALID_SYNC_CONFIG');
const task=await taskSpace(syncConfig.spaceId), page=task.page(syncConfig.pageLabel);
const fs=await import('node:fs/promises');
const path=syncConfig.output;
if (!(await page.url()).startsWith('https://work.open.taobao.com/open-skill/list')) throw Error('OPEN_SKILL_LIST_FIRST');
const currentAccount=()=>page.evaluate(()=>[...(document.querySelector('#open-console-userLayout')?.childNodes||[])].filter(x=>x.nodeType===Node.TEXT_NODE).map(x=>x.textContent.trim()).join(''));
if ((await currentAccount())!==syncConfig.account) throw Error('ACCOUNT_MISMATCH');
let result=[];try {result=JSON.parse(await fs.readFile(path,'utf8'));} catch(e){if(e.code!=='ENOENT')throw e;}
const initialPage=await page.evaluate(()=>Number(document.querySelector('.tbd-pagination-item-active')?.getAttribute('title')));
if(initialPage!==1)throw Error('START_AT_FIRST_PAGE');
const visited=new Set();let newCount=0,partial=false;
outer: for(let pageNum=1;;pageNum++) {
 if ((await currentAccount())!==syncConfig.account) throw Error('ACCOUNT_CHANGED');
 await page.waitForFunction(n=>document.querySelector('.tbd-pagination-item-active')?.getAttribute('title')===String(n)&&document.querySelectorAll('[class*=skillCard--]').length>0,pageNum,{timeout:15000});
 const cards=await page.evaluate(()=>[...document.querySelectorAll('[class*=skillGrid--]>[class*=skillCard--]')].map(e=>({name:e.querySelector('[class*=skillName--]')?.textContent?.trim(),appkey:e.querySelector('[class*=appkeyValue--]')?.textContent?.trim(),status:e.querySelector('[class*=statusTag--]')?.textContent?.trim(),scope:e.querySelector('[class*=visibleScopeTag--]')?.textContent?.trim(),text:e.innerText})));
 for(let i=0;i<cards.length;i++){
  const card=cards[i];
  const key=card.name+'|'+card.appkey;if(visited.has(key))throw Error('DUPLICATE_PAGE_CARD '+key);visited.add(key);
  const prior=result.find(x=>x.name===card.name&&x.appkey===card.appkey);
  if(prior){
   const version=x=>x.text.match(/当前版本\s*\n([^\n]+)/)?.[1];
   if(prior.account!==syncConfig.account||prior.status!==card.status||prior.scope!==card.scope||version(prior)!==version(card))throw Error('OBSERVATION_CHANGED '+card.name);
   continue;
  }
  const s=`[class*=skillGrid--]>[class*=skillCard--]:nth-child(${i+1})`;
  await page.hover(`loc=css:${s}`);await page.click(`loc=css:${s} button[class*=actionBtnPrimary]`);
  await page.waitForFunction(name=>{const d=document.querySelector('[role=dialog]');return !!d && [...d.querySelectorAll('input')].some(x=>x.maxLength===20 && x.value===name) && !!d.querySelector('input[placeholder="技能code由小写字母、数字、中划线组成，必须以字母开头"]')?.value},card.name,{timeout:45000});
  const now=await page.evaluate(s=>{const e=document.querySelector(s);return {name:e?.querySelector('[class*=skillName--]')?.textContent?.trim(),appkey:e?.querySelector('[class*=appkeyValue--]')?.textContent?.trim()}},s);
  if(now.name!==card.name||now.appkey!==card.appkey)throw Error('CARD_ORDER_CHANGED '+card.name);
  if ((await currentAccount())!==syncConfig.account) throw Error('ACCOUNT_CHANGED');
  const detail=await page.evaluate(()=>{const d=document.querySelector('[role=dialog]');const inputs=[...d.querySelectorAll('input')];return {code:d.querySelector('input[placeholder="技能code由小写字母、数字、中划线组成，必须以字母开头"]')?.value,dialogName:inputs.find(x=>x.maxLength===20)?.value,description:d.querySelector('textarea[placeholder="一句话简要描述你的技能"]')?.value}});
  if(!detail.code||detail.dialogName!==card.name)throw Error(`DETAIL_MISMATCH ${pageNum} ${i+1} ${card.name} ${JSON.stringify(detail)}`);
  result.push({...card,account:syncConfig.account,code:detail.code,detailName:detail.dialogName,description:detail.description,page:pageNum,observedAt:new Date().toISOString()});
  await fs.writeFile(path,JSON.stringify(result,null,2));
  await page.click('text="取消"');
  try {await page.waitForSelector('[role=dialog]',{state:'hidden',timeout:5000});}
  catch(e){
    const state=await page.evaluate(()=>{const d=document.querySelector('[role=dialog]');const b=[...(d?.querySelectorAll('button')||[])].find(x=>x.innerText.trim()==='取消');return {dialog:!!d&&d.getBoundingClientRect().width>0,cancel:!!b&&b.getBoundingClientRect().width>0};});
    if(state.dialog&&state.cancel){await page.click('text="取消"');await page.waitForSelector('[role=dialog]',{state:'hidden',timeout:15000});}
    else if(state.dialog)await page.waitForSelector('[role=dialog]',{state:'hidden',timeout:15000});
  }
  newCount++;if(syncConfig.maxNew && newCount>=syncConfig.maxNew){partial=true;break outer;}

 }
 console.log(`page ${pageNum}: ${cards.length}; total ${result.length}`);
 const last=await page.evaluate(()=>document.querySelector('.tbd-pagination-next')?.classList.contains('tbd-pagination-disabled'));
 if(last)break;
 const prev=cards[0].name;await page.click('loc=css:.tbd-pagination-next button');await page.waitForFunction(o=>document.querySelector('.tbd-pagination-item-active')?.getAttribute('title')===String(o.page)&&document.querySelector('[class*=skillName--]')?.textContent?.trim()!==o.prev,{page:pageNum+1,prev},{timeout:30000});
}
if(partial) console.log(`PARTIAL ${result.length}; do not use for full synchronization`);
else {
 if(visited.size!==syncConfig.expectedTotal || result.length!==syncConfig.expectedTotal || result.some(r=>!visited.has(r.name+'|'+r.appkey)) || new Set(result.map(r=>r.code)).size!==result.length || new Set(result.map(r=>r.name+'|'+r.appkey)).size!==result.length)throw Error('INCOMPLETE_OR_DUPLICATE_OBSERVATION');
 console.log(`COMPLETE ${result.length} unique codes`);
}
