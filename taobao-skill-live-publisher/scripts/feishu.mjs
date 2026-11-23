/** Feishu UI attachments and exact status updates in an already opened record drawer. */
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {nativeClick} from './browser.mjs';
import {verifyCreatedCodeTransition} from './created_identity.mjs';
export async function uploadBatch(page,cfg) {
const rows=JSON.parse(await fs.readFile(cfg.baselinePath,'utf8'));
const packages=JSON.parse(await fs.readFile(cfg.manifestPath,'utf8'));
const bindings=JSON.parse(await fs.readFile(cfg.bindingsPath,'utf8'));
const receipts=await fs.readFile(cfg.receiptPath,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return [];throw e;});
const previous=[];
for(const path of cfg.previousManifestPaths||[])previous.push(...JSON.parse(await fs.readFile(path,'utf8')));
if(cfg.targetTableId&&new URL(await page.url()).searchParams.get('table')!==cfg.targetTableId)throw Error('Target table changed');
const range={start:cfg.start,end:cfg.end};
const byRow=new Map(packages.map(x=>[x.row,x]));
if(!Number.isInteger(range.start)||range.start<2||range.end>rows.length||range.end<range.start)throw Error('Explicit valid record range required');
async function readState() {
  return page.evaluate(() => {
    const field = id => [...document.querySelectorAll('label[data-field-id="' + id + '"]')]
      .find(element => element.getBoundingClientRect().height > 0);
    const name = field('fldM6QPKxC');
    const editor = [...(name?.querySelectorAll('[id^="BITABLE_TEXT_EDITOR_CONTAINER_ID_PREFIX_"]') || [])]
      .map(element => element.id).find(id => id.includes('_rec'));
    return {
      name: (name?.querySelector('.bitable-card-edit-cell-editor-Text')?.innerText || '').replace(/\u200b/g, '').trim(),
      record_id: editor?.match(/PREFIX_(rec[A-Za-z0-9]+)_/)?.[1],
      source_url: field('fldNAnKWKe')?.querySelector('a')?.href || '',
      files: [...(field('fldTjEnH15')?.querySelectorAll('span.attach-item-title') || [])]
        .map(element => element.getAttribute('title')),
      generation: field('fldBfirQRf')?.querySelector('ul')?.innerText || '',
      sync: field('fldugbap1N')?.querySelector('ul')?.innerText || '',
    };
  });
}
async function choose(field, value) {
  const selector = 'label[data-field-id="' + field + '"]';
  await page.evaluate(selector => document.querySelector(selector)?.scrollIntoView({ block: 'center', inline: 'nearest' }), selector);
  await page.click(selector + ' .b-select-dropdown-menu');
  await page.fill(selector + ' input.b-select-search', value);
  await page.click(selector + ' .b-select-option');
}
for (let row = range.start; row <= range.end; row++) {
  if(cfg.pauseFile&&await fs.stat(cfg.pauseFile).then(()=>true).catch(e=>{if(e.code==='ENOENT')return false;throw e;}))return {pausedAtRow:row,uploaded:receipts.length};
  const expected = rows[row - 1];
  await page.waitForFunction(name => [...document.querySelectorAll('label[data-field-id="fldM6QPKxC"] .bitable-card-edit-cell-editor-Text')]
    .some(element => element.getBoundingClientRect().height > 0 && element.innerText.replace(/\u200b/g, '').trim() === name),
    expected.A.trim(), { timeout: 15000 });
  const before = await readState();
  if (before.name !== expected.A.trim() || !before.record_id) throw new Error('Record identity mismatch at ' + row);
  const item = byRow.get(row);
  if (item) {
    const filename = item.package_path.split('/').at(-1);
    const saved = receipts.find(receipt => receipt.source_excel_row === row && receipt.sha256 === item.package_sha256);
    const binding=bindings.find(x=>x.source_excel_row===row);
    if(!binding || binding.record_id!==before.record_id) throw Error("Pinned record ID changed at "+row);
    if (saved) {
      if (saved.record_id !== before.record_id || before.files.length !== 1 || before.files[0] !== filename)
        throw new Error('Completed record changed at ' + row);
    } else {
      if (before.source_url !== (expected.source_url === null ? '' : expected.source_url)) throw new Error('Source changed at ' + row);
      const oldFiles = before.files.filter(file => file !== filename);
      const allowedOld=[expected.I,...previous.filter(x=>x.row===row).map(x=>x.package_path.split('/').at(-1))];
      if (oldFiles.some(file => !allowedOld.includes(file))) throw new Error('Attachment changed at ' + row);
      if (!before.files.includes(filename)) {
        await page.evaluate(() => document.querySelector('label[data-field-id="fldTjEnH15"]')?.scrollIntoView({ block: 'center' }));
        if (!(await page.evaluate(() => !!document.querySelector('#attachment-upload')))) {
          await page.click('label[data-field-id="fldTjEnH15"] button');
          await page.waitForFunction(() => !!document.querySelector('#attachment-upload'), undefined, { timeout: 10000 });
        }
        await page.setInputFiles('#attachment-upload', [item.package_path]);
        await page.waitForFunction(file => [...document.querySelectorAll('label[data-field-id="fldTjEnH15"] span.attach-item-title')]
          .some(element => element.getAttribute('title') === file), filename, { timeout: 20000 });
        await page.waitForLoadState('networkidle', { timeout: 15000, idleMs: 800 });
      }
      for (const file of oldFiles) {
        const selector = 'label[data-field-id="fldTjEnH15"] .item-content:has(span[title="' + file.replaceAll('"', '\\"') + '"])';
        await page.evaluate(selector => document.querySelector(selector)?.scrollIntoView({ block: 'center' }), selector);
        await page.hover(selector);
        await page.click(selector + ' .delete-img');
      }
      if (before.generation !== '升级更新中') await choose('fldBfirQRf', '升级更新中');
      if (before.sync !== '待同步') await choose('fldugbap1N', '待同步');
      await page.waitForLoadState('networkidle', { timeout: 15000, idleMs: 800 });
      const after = await readState();
      if (after.files.length !== 1 || after.files[0] !== filename || after.generation !== '升级更新中' || after.sync !== '待同步')
        throw new Error('Write readback mismatch at ' + row);
      receipts.push({ record_id: before.record_id, table_id: 'tbl5c1ONsL2wKKNs', source_excel_row: row,
        name: item.name, new_package: filename, sha256: item.package_sha256,
        attachment_replace_readback: true, generation_readback: after.generation, sync_status_readback: after.sync });
      await fs.writeFile(cfg.receiptPath, JSON.stringify(receipts, null, 2));
      console.log({ uploaded_row: row, name: item.name, record_id: before.record_id, total_uploaded: receipts.length });
    }
  }
  if (row < range.end) await page.click('.bitable-card-modal-header-v2-btn-next');
}
return {next_excel_row:range.end+1,state:await readState(),uploaded:receipts.length};

}

/** Update an exact field only after focusing its actual editable descendant. */
export async function writeTextField(page,field,value) {
  const captions={fldIgMHYrS:'同步说明',fld4EtxMCr:'技能code',fld3Du7PxL:'当前版本',fldMsDtU8O:'线上版本'};
  if(!captions[field])throw Error('Field is not in the result-writeback allowlist');
  const actualCaption=await page.evaluate(field=>document.querySelector('label[data-field-id='+JSON.stringify(field)+'] .bitable-card-field-label__name')?.innerText.trim(),field);
  if(actualCaption!==captions[field])throw Error('Writeback field schema changed');
  const selector='label[data-field-id='+JSON.stringify(field)+'] [contenteditable=true]';
  await page.waitForSelector(selector,{timeout:15000});
  await page.click(selector);
  const focused=await page.evaluate(field=>document.activeElement?.closest('label[data-field-id]')?.getAttribute('data-field-id')===field,field);
  if(!focused)throw Error('Exact result editor is not focused; do not send Select All');
  await page.press(selector,'ControlOrMeta+A');
  await page.keyboard.paste(value);
  // Tab can leave this rich-text editor in an uncommitted edit session.
  // A native click on another field's caption blurs it without changing data.
  await nativeClick(page,'label[data-field-id="fldM6QPKxC"] .bitable-card-field-label__name');
  await page.waitForFunction(field=>document.activeElement?.closest('label[data-field-id]')?.getAttribute('data-field-id')!==field,field,{timeout:10000});
  await page.waitForFunction(({field,value})=>{
    const e=document.querySelector('label[data-field-id='+JSON.stringify(field)+'] [contenteditable=true]');
    return e?.innerText.replace(/\u200b/g,'').trim()===value.trim();
  },{field,value},{timeout:20000});
}

export async function writeResult(page,cfg) {
  if(!cfg.recordId||!cfg.expectedName||!cfg.packageName||!cfg.resultNote)throw Error('Pinned record and actual platform result required');
  await page.evaluate(()=>document.querySelector('label[data-field-id="fldIgMHYrS"]')?.scrollIntoView({block:'center'}));
  await page.waitForSelector('label[data-field-id="fldIgMHYrS"] [contenteditable=true]',{timeout:15000});
  const state=await page.evaluate(()=>{
    const f=id=>document.querySelector('label[data-field-id="'+id+'"]');
    return {id:f('fldM6QPKxC')?.querySelector('[id^="BITABLE_TEXT_EDITOR_CONTAINER_ID_PREFIX_rec"]')?.id.match(/PREFIX_(rec[A-Za-z0-9]+)_/)?.[1],name:f('fldM6QPKxC')?.querySelector('.bitable-card-edit-cell-editor-Text')?.innerText.replace(/\u200b/g,'').trim(),files:[...(f('fldTjEnH15')?.querySelectorAll('span.attach-item-title')||[])].map(e=>e.title),note:f('fldIgMHYrS')?.querySelector('[contenteditable=true]')?.innerText.replace(/\u200b/g,'').trim()||'',formalCode:f('fld4EtxMCr')?.querySelector('.bitable-card-edit-cell-editor-Text')?.innerText.replace(/\u200b/g,'').trim()||'',currentVersion:f('fld3Du7PxL')?.querySelector('.bitable-card-edit-cell-editor-Text')?.innerText.replace(/\u200b/g,'').trim()||'',onlineVersion:f('fldMsDtU8O')?.querySelector('.bitable-card-edit-cell-editor-Text')?.innerText.replace(/\u200b/g,'').trim()||'',generation:f('fldBfirQRf')?.querySelector('.b-select-value-list')?.innerText.trim()||''};
  });
  if(state.id!==cfg.recordId||state.name!==cfg.expectedName||state.files.length!==1||state.files[0]!==cfg.packageName)throw Error('Result target/source changed');
  if(cfg.formalCode&&state.formalCode&&state.formalCode!==cfg.formalCode)await verifyCreatedCodeTransition(cfg,state);
  for(const key of ['currentVersion','onlineVersion']) {
    const expected=cfg['expected'+key[0].toUpperCase()+key.slice(1)];
    if(expected!==undefined&&state[key]!==expected&&state[key]!==cfg[key])throw Error('Version field changed since the reviewed baseline: '+key);
  }
  if(cfg.expectedNote!==undefined&&state.note!==cfg.expectedNote)throw Error('Result note changed since read');
  if(cfg.generationStatus) {
    const complete=cfg.generationStatus==='上架完成'&&cfg.listingVerified;
    const review=cfg.generationStatus==='技能上架审核中'&&cfg.listingReviewConfirmed;
    if(!(complete||review)||!cfg.onlinePackageVerified)throw Error('Verified actual listing or confirmed store review required for generation status');
    if(cfg.expectedGenerationStatus!==undefined&&state.generation!==cfg.expectedGenerationStatus&&state.generation!==cfg.generationStatus)throw Error('Generation status changed since reviewed baseline');
  }
  if(!cfg.batchId)throw Error('Stable writeback batch marker required');
  if(cfg.currentVersion&&(!cfg.platformVersionConfirmed||!/^\d+\.\d+\.\d+$/.test(cfg.currentVersion)))throw Error('Actual platform version evidence required');
  if(cfg.onlineVersion&&(!cfg.onlinePackageVerified||!/^\d+\.\d+\.\d+$/.test(cfg.onlineVersion)))throw Error('Specific verified online package evidence required');
  const marker='['+cfg.batchId+']';
  const lines=state.note.split('\n').filter(x=>!x.startsWith(marker));
  const value=[...lines.filter(Boolean),marker+' '+cfg.resultNote].join('\n');
  if(state.note!==value)await writeTextField(page,'fldIgMHYrS',value);
  if(cfg.formalCode&&state.formalCode!==cfg.formalCode)await writeTextField(page,'fld4EtxMCr',cfg.formalCode);
  if(cfg.currentVersion) {
    if(!cfg.platformVersionConfirmed||!/^\d+\.\d+\.\d+$/.test(cfg.currentVersion))throw Error('Actual platform version evidence required');
    if(state.currentVersion!==cfg.currentVersion)await writeTextField(page,'fld3Du7PxL',cfg.currentVersion);
  }
  if(cfg.onlineVersion) {
    if(!cfg.onlinePackageVerified||!/^\d+\.\d+\.\d+$/.test(cfg.onlineVersion))throw Error('Specific verified online package evidence required');
    if(state.onlineVersion!==cfg.onlineVersion)await writeTextField(page,'fldMsDtU8O',cfg.onlineVersion);
  }
  if(cfg.generationStatus&&state.generation!==cfg.generationStatus) {
    const selector='label[data-field-id="fldBfirQRf"]';
    const caption=await page.evaluate(selector=>document.querySelector(selector+' .bitable-card-field-label__name')?.innerText.trim(),selector);
    if(caption!=='技能生成及状态')throw Error('Generation field schema changed');
    await nativeClick(page,selector+' .b-select-dropdown-menu');
    await page.fill(selector+' input.b-select-search',cfg.generationStatus);
    await page.waitForFunction(({selector,value})=>[...document.querySelectorAll(selector+' .b-select-option')].filter(x=>x.innerText.trim()===value).length===1,{selector,value:cfg.generationStatus},{timeout:10000});
    await nativeClick(page,selector+' .b-select-option',null,cfg.generationStatus);
    await page.waitForFunction(value=>document.querySelector('label[data-field-id="fldBfirQRf"] .b-select-value-list')?.innerText.trim()===value,cfg.generationStatus,{timeout:15000});
  }
  const result={recordId:state.id,row:cfg.row,actualResult:cfg.resultNote,generationStatus:cfg.generationStatus||null,currentVersion:cfg.currentVersion||null,onlineVersion:cfg.onlineVersion||null,onlineVersionPreserved:!cfg.onlineVersion,syncStatusNotChanged:true,resultNoteReadback:true};
  await fs.writeFile(cfg.receiptPath,JSON.stringify(result,null,2));
  return result;
}

/** Caller first observes a screenshot of the selected link header. No Select All. */
export async function pasteOssColumn(page,cfg) {
  if(!cfg.selectedHeaderEvidence||cfg.column!=='技能包链接'||!Array.isArray(cfg.values))throw Error('Exact selected link-column screenshot evidence required');
  await fs.access(cfg.selectedHeaderEvidence);
  if(cfg.values.some(x=>typeof x!=='string'||(x&&!/^https:\/\//.test(x))||/[\t\r\n]/.test(x)))throw Error('Invalid link cell');
  const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
  await page.keyboard.paste({text:cfg.values.join('\n'),html:'<table>'+cfg.values.map(x=>'<tr><td>'+escape(x)+'</td></tr>').join('')+'</table>'});
  await page.waitForLoadState('networkidle',{timeout:30000,idleMs:1000});
  return {rows:cfg.values.length,column:cfg.column,persistedExportReadbackRequired:true};
}

export async function writeResultsBatch(page,cfg) {
  const rows=JSON.parse(await fs.readFile(cfg.baselinePath,'utf8'));
  const writes=JSON.parse(await fs.readFile(cfg.writebacksPath,'utf8'));
  const byRow=new Map(writes.map(x=>[x.row,x]));
  const receiptPath=cfg.receiptPath;
  const completed=await fs.readFile(receiptPath,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return [];throw e;});
  for(let row=cfg.start;row<=cfg.end;row++) {
    await page.waitForFunction(name=>document.querySelector('label[data-field-id="fldM6QPKxC"] .bitable-card-edit-cell-editor-Text')?.innerText.replace(/\u200b/g,'').trim()===name,rows[row-1].A.trim(),{timeout:15000});
    const write=byRow.get(row);
    if(write) {
      await writeResult(page,write);
      const value={row,recordId:write.recordId,resultNote:write.resultNote,uiReadback:true};
      const index=completed.findIndex(x=>x.row===row);if(index>=0)completed.splice(index,1);completed.push(value);
      await fs.writeFile(receiptPath,JSON.stringify(completed,null,2));
    }
    if(row<cfg.end)await page.click('.bitable-card-modal-header-v2-btn-next');
  }
  return {resultsWritten:completed.length,persistedExportReadbackRequired:true};
}

/** After an agent observes the selected exact header, paste a reviewed full column. */
export async function pasteResultColumn(page,cfg) {
  const captions={E:'技能生成及状态',F:'当前版本',G:'线上版本',J:'技能code',AG:'同步说明'};
  if(captions[cfg.columnKey]!==cfg.column||!cfg.targetTableId||new URL(await page.url()).searchParams.get('table')!==cfg.targetTableId)throw Error('Exact allowed result column and target table required');
  if(!cfg.selectedHeaderEvidence||!cfg.columnPlanPath||!cfg.columnPlanSha256)throw Error('Observed selected header and frozen column plan required');
  await fs.access(cfg.selectedHeaderEvidence);
  const planRaw=await fs.readFile(cfg.columnPlanPath);
  if(createHash('sha256').update(planRaw).digest('hex')!==cfg.columnPlanSha256)throw Error('Reviewed column plan changed');
  const plan=JSON.parse(planRaw),matches=plan.columns.filter(x=>x.columnKey===cfg.columnKey);
  if(matches.length!==1||matches[0].column!==cfg.column||plan.baseline_sha256!==cfg.baselineSha256)throw Error('Column plan identity or baseline mismatch');
  const values=matches[0].values;
  if(!Array.isArray(values)||values.some(x=>typeof x!=='string'))throw Error('Reviewed string values required');
  const raw=await fs.readFile(cfg.baselinePath);
  if(createHash('sha256').update(raw).digest('hex')!==cfg.baselineSha256)throw Error('Reviewed table baseline changed');
  const rows=JSON.parse(raw);
  if(rows.length-1!==values.length||rows[0][cfg.columnKey]!==cfg.column)throw Error('Table row count or field caption changed');
  const focus=await page.evaluate(()=>{
    const active=document.activeElement;
    // Native whole-column selection focuses Feishu's zero-width readonly clipboard input.
    const capture=active?.tagName==='INPUT'&&active.readOnly&&active.parentElement?.classList.contains('bitable-input-editor-container')&&active.parentElement.getBoundingClientRect().width===0&&!!active.closest('.faster-overlay .bitable-editor-container');
    return {editable:!capture&&(active?.isContentEditable||['INPUT','TEXTAREA'].includes(active?.tagName)),drawer:!!document.querySelector('.bitable-card-modal-header-v2-btn-close')};
  });
  if(focus.editable||focus.drawer)throw Error('Close the record drawer and select the exact native table column header first');
  const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
  const text=values.map(s=>/[\t\r\n"]/u.test(s)?'"'+s.replaceAll('"','""')+'"':s).join('\n');
  const html='<table>'+values.map(s=>'<tr><td style="white-space:pre-wrap">'+escape(s).replaceAll('\n','<br>')+'</td></tr>').join('')+'</table>';
  await page.keyboard.paste({text,html});
  await page.waitForLoadState('networkidle',{timeout:30000,idleMs:1000});
  return {column:cfg.column,rows:values.length,baselineSha256:cfg.baselineSha256,persistedExportReadbackRequired:true};
}
