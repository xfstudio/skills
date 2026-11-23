/** Native directed-shop authorization; never publishes, removes, or retries an intent. */
import fs from 'node:fs/promises';
import {randomUUID} from 'node:crypto';
import {findTarget} from './taobao.mjs';
import {button,menu,nativeClick,nativeHover} from './browser.mjs';

const nextSelector='[role="dialog"] .tbd-pagination-next';
const placeholder='textarea[placeholder="如需添加多个店铺，请用英文逗号或换行分隔"]';
const same=(a,b)=>JSON.stringify([...a].sort())===JSON.stringify([...b].sort());
async function save(path,value) {
  await fs.writeFile(path+'.tmp',JSON.stringify(value,null,2));
  await fs.rename(path+'.tmp',path);
}
async function journal(path) {
  return fs.readFile(path,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return [];throw e;});
}
export function requireMerchant(merchant) {
  if(typeof merchant!=='string'||!merchant.trim()||merchant!==merchant.trim()||/[,，;；\r\n\t\u0000-\u001f]/u.test(merchant)||merchant.length>45)throw Error('Exactly one explicit merchant name is required');
  return merchant;
}
export function authorizationDecision(cfg,found,authorization,history) {
  requireMerchant(cfg.merchant);
  if(!found.listed)return 'not_listed';
  if(found.statusLabels.includes('公开'))return 'public_listing';
  if(!found.statusLabels.includes('定向'))throw Error('Listing mode is unresolved');
  if(!authorization?.complete||!Array.isArray(authorization.shops)||authorization.shops.some(x=>typeof x!=='string'||!x)||new Set(authorization.shops).size!==authorization.shops.length)throw Error('Complete unambiguous authorization readback required');
  if(authorization.shops.includes(cfg.merchant))return 'already_authorized';
  if(history.some(x=>x.account===cfg.account&&x.publicAppId===cfg.publicAppId&&x.merchant===cfg.merchant))return 'authorization_unknown';
  return cfg.ensureAuthorization===true?'add_missing':'authorization_missing';
}
export function requirePreservedScope(before,after,merchant) {
  requireMerchant(merchant);
  if(!before.complete||!after.complete||!same([...new Set([...before.shops,merchant])],after.shops))throw Error('Authorization after readback differs from the original scope plus the approved merchant');
}

async function openAuthorization(page,found) {
  // Move directly to the observed footer control; the description can show a tooltip.
  await nativeHover(page,found.selector+' button',1);
  const visible=await page.evaluate(()=>[...document.querySelectorAll('[role="menuitem"]')].some(e=>e.innerText.trim()==='授权管理'&&e.getBoundingClientRect().width>0));
  if(!visible)await nativeClick(page,found.selector+' button',1);
  await menu(page,'授权管理');
  await page.waitForFunction(()=>[...document.querySelectorAll('[role="dialog"]')].some(e=>e.getBoundingClientRect().width>0&&e.innerText.includes('添加授权店铺')),undefined,{timeout:15000});
}
async function authorizationPage(page) {
  await page.waitForLoadState('networkidle',{timeout:15000,idleMs:700});
  await page.waitForFunction(()=>{
    const d=[...document.querySelectorAll('[role="dialog"]')].find(e=>e.getBoundingClientRect().width>0&&e.innerText.includes('授权管理'));
    return !!d&&!!d.querySelector('table')&&!d.querySelector('[aria-busy="true"],.tbd-spin-spinning')&&([...d.querySelectorAll('tbody tr')].some(e=>e.innerText.trim())||d.innerText.includes('暂无授权店铺'));
  },undefined,{timeout:15000});
  return page.evaluate(()=>{
    const dialogs=[...document.querySelectorAll('[role="dialog"]')].filter(e=>e.getBoundingClientRect().width>0);
    if(dialogs.length!==1)throw Error('One authorization dialog is required');
    const d=dialogs[0],headers=[...d.querySelectorAll('th')].map(e=>e.innerText.trim());
    if(!d.innerText.includes('授权管理')||JSON.stringify(headers)!==JSON.stringify(['店铺名称','添加时间','操作']))throw Error('Authorization table schema changed');
    const rows=[...d.querySelectorAll('tbody tr')].map(e=>[...e.querySelectorAll('td')].map(x=>x.innerText.trim()));
    const shops=rows.filter(x=>x.length===3).map(x=>x[0]);
    if(rows.some(x=>x.length!==3&&!x.join('').includes('暂无授权店铺')))throw Error('Unrecognized authorization row');
    const pagination=d.querySelector('[class*="pagination"]'),next=d.querySelector('.tbd-pagination-next'),prev=d.querySelector('.tbd-pagination-prev');
    const disabled=e=>!!e&&(e.disabled||e.getAttribute('aria-disabled')==='true'||String(e.className).includes('disabled'));
    return {shops,rows,readback:d.innerText,hasPagination:!!pagination,recognized:!pagination||!!(next&&prev),first:!pagination||disabled(prev),last:!pagination||disabled(next)};
  });
}
async function readAllAuthorization(page) {
  const pages=[],shops=[];let first=true;
  for(let n=0;n<100;n++) {
    const current=await authorizationPage(page);
    if(!current.recognized||(first&&!current.first))throw Error('Pagination must start at a recognized first page');
    const signature=JSON.stringify(current.rows);
    if(pages.some(p=>JSON.stringify(p.rows)===signature))throw Error('Repeated authorization page needs manual reconciliation');
    pages.push(current);shops.push(...current.shops);
    if(new Set(shops).size!==shops.length)throw Error('Duplicate shops across authorization pages');
    if(current.last)return {complete:true,shops,pages,observedAt:new Date().toISOString()};
    await nativeClick(page,nextSelector);
    await page.waitForFunction(previous=>{
      const d=[...document.querySelectorAll('[role="dialog"]')].find(e=>e.getBoundingClientRect().width>0&&e.innerText.includes('授权管理'));
      return d&&!d.querySelector('[aria-busy="true"],.tbd-spin-spinning')&&JSON.stringify([...d.querySelectorAll('tbody tr')].map(e=>[...e.querySelectorAll('td')].map(x=>x.innerText.trim())))!==previous;
    },signature,{timeout:15000});first=false;
  }
  throw Error('Authorization pagination exceeded the bounded readback');
}
async function observe(page,cfg) {
  const found=await findTarget(page,cfg);
  if(!found.listed||!found.statusLabels.includes('定向'))return {found,authorization:null};
  await openAuthorization(page,found);
  return {found,authorization:await readAllAuthorization(page)};
}
function result(cfg,observation,phase,extra={}) {
  return {row:cfg.row,account:cfg.account,publicAppId:cfg.publicAppId,formalCode:cfg.formalCode,merchant:cfg.merchant,phase,listed:observation.found.listed,statusLabels:observation.found.statusLabels,cardReadback:observation.found.text,authorization:observation.authorization,manifestSha256:cfg.manifestSha256,packageSha256:cfg.packageSha256,observedAt:new Date().toISOString(),...extra};
}

export async function ensureAuthorization(page,cfg) {
  requireMerchant(cfg.merchant);
  if(!cfg.account||!/^\d+$/.test(cfg.publicAppId)||!cfg.formalCode||!cfg.journalPath)throw Error('Pinned target and authorization journal are required');
  const history=await journal(cfg.journalPath),before=await observe(page,cfg);
  const decision=authorizationDecision(cfg,before.found,before.authorization,history);
  if(decision!=='add_missing') {
    // Leave the read-only dialog visible; the next pinned navigation dismisses it.
    return result(cfg,before,decision,{requestSubmitted:false});
  }
  await button(page,'添加授权店铺');
  await page.waitForSelector(placeholder,{timeout:10000});
  await page.fill(placeholder,cfg.merchant);
  const exact=await page.evaluate(({selector,id,merchant,placeholder})=>{
    const cards=[...document.querySelectorAll(selector)].filter(e=>e.innerText.split(/\s+/).includes(id));
    const inputs=[...document.querySelectorAll(placeholder)].filter(e=>e.getBoundingClientRect().width>0);
    const d=inputs[0]?.closest('[role="dialog"]');
    return cards.length===1&&cards[0].innerText.includes('已上架')&&cards[0].innerText.includes('定向')&&inputs.length===1&&inputs[0].value===merchant&&d?.innerText.includes('添加授权店铺')&&!d.querySelector('input[type="checkbox"]');
  },{selector:'[class^="skillCard--"]',id:cfg.publicAppId,merchant:cfg.merchant,placeholder});
  if(!exact)throw Error('Prepared authorization target, merchant, or form changed');
  const intent={operationId:randomUUID(),action:'add_directed_shop',row:cfg.row,account:cfg.account,publicAppId:cfg.publicAppId,formalCode:cfg.formalCode,merchant:cfg.merchant,beforeShops:before.authorization.shops,phase:'authorization_submitting',at:new Date().toISOString(),manifestSha256:cfg.manifestSha256};
  // Recheck the durable ledger immediately before the one click.
  const latest=await journal(cfg.journalPath);
  if(latest.some(x=>x.account===cfg.account&&x.publicAppId===cfg.publicAppId&&x.merchant===cfg.merchant))throw Error('An authorization intent already exists; only readback is allowed');
  latest.push(intent);await save(cfg.journalPath,latest);
  try {
    await button(page,'添加');
    await page.waitForFunction(placeholder=>![...document.querySelectorAll(placeholder)].some(e=>e.getBoundingClientRect().width>0),placeholder,{timeout:20000});
    intent.phase='authorization_requested';await save(cfg.journalPath,latest);
    const after=await observe(page,cfg);
    if(!after.found.listed||!after.found.statusLabels.includes('定向'))throw Error('Listing changed after authorization');
    requirePreservedScope(before.authorization,after.authorization,cfg.merchant);
    intent.phase='authorization_verified';intent.afterShops=after.authorization.shops;intent.verifiedAt=new Date().toISOString();await save(cfg.journalPath,latest);
    return result(cfg,after,'authorization_added',{requestSubmitted:true,originalShops:before.authorization.shops,existingShopsPreserved:true,operationId:intent.operationId});
  } catch(error) {
    intent.phase='authorization_unknown';intent.outcomeObservedAt=new Date().toISOString();await save(cfg.journalPath,latest);
    // The host observes the same target before resuming. Never click Add again.
    throw error;
  }
}
