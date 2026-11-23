// Supply syncConfig in the same ego-browser nodejs input; never print credentials.
const fs = await import('node:fs/promises');
if (!Number.isInteger(syncConfig.spaceId) || !syncConfig.pageLabel || !syncConfig.plan || !syncConfig.receipt || !syncConfig.expectedOrigin) throw Error('INVALID_SYNC_CONFIG');
const task = await taskSpace(syncConfig.spaceId), page = task.page(syncConfig.pageLabel);
if (new URL(await page.url()).origin !== syncConfig.expectedOrigin) throw Error('WRONG_BM_ORIGIN');
const plan = JSON.parse(await fs.readFile(syncConfig.plan,'utf8'));
if (!Array.isArray(plan.planned) || new Set(plan.planned.map(x=>x.packageId)).size !== plan.planned.length) throw Error('INVALID_PLAN');
let audit=[]; try {audit=JSON.parse(await fs.readFile(syncConfig.receipt,'utf8'));} catch(e) {if(e.code!=='ENOENT') throw e;}
let count=0;
for(const item of plan.planned) {
 if (syncConfig.limit && count>=syncConfig.limit) break;
 if (!item.packageId || !item.packageName || !item.skillName || typeof item.before !== 'string' || !item.after || !item.platformCode || !item.observedAt) throw Error('INVALID_PLAN_ITEM');
 const outcome=await page.evaluate(async item=>{
   const token=localStorage.getItem('auth_token')||sessionStorage.getItem('auth_token');
   if(!token)return {result:'auth-unavailable'};
   const url='/api/skill-packages/'+encodeURIComponent(item.packageId);
   const headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'};
   async function get(){const r=await fetch(url,{headers});if(!r.ok)return {error:'read-failed',status:r.status};return await r.json();}
   try {
     const before=await get();if(before.error)return {result:before.error,status:before.status};
     if(before.name!==item.packageName || !before.can_write || !Array.isArray(before.skills) || before.skills.length!==1 || before.skills[0].slug!==item.skillName)return {result:'identity-or-permission-changed'};
     if(before.description===item.after)return {result:'already-matched',after:before.description};
     if(before.description!==item.before || String(before.updated_at)!==String(item.expectedUpdatedAt))return {result:'concurrent-change'};
     const response=await fetch(url,{method:'PATCH',headers,body:JSON.stringify({description:item.after})});
     if(!response.ok)return {result:'write-failed',status:response.status};
     const after=await get();if(after.error || after.name!==item.packageName || after.description!==item.after)return {result:'readback-unconfirmed'};
     return {result:'updated',after:after.description};
   } catch {return {result:'outcome-unknown'};}
 },item);
 audit.push({packageId:item.packageId,platformCode:item.platformCode,result:outcome.result,after:outcome.after,checkedAt:new Date().toISOString(),httpStatus:outcome.status});
 await fs.writeFile(syncConfig.receipt,JSON.stringify(audit,null,2));
 console.log(item.packageId,outcome.result);
 count++;
 if(!['updated','already-matched','identity-or-permission-changed','concurrent-change'].includes(outcome.result))throw Error('STOP_AND_RECONCILE: '+item.packageId+' '+outcome.result);
}
console.log('verified items:',new Set(audit.filter(x=>['updated','already-matched'].includes(x.result)).map(x=>x.packageId)).size);
