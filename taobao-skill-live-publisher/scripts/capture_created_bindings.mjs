/** Read only: pin native record IDs and source-link evidence without reading credential fields. */
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';

export async function captureCreatedBindings(page, cfg) {
  const raw = await fs.readFile(cfg.sourcePath);
  const rows = JSON.parse(raw);
  if (new URL(await page.url()).searchParams.get('table') !== cfg.tableId)
    throw Error('Target table changed');
  if (rows[0].H !== '技能包链接' || rows[0].I !== '自建技能包')
    throw Error('Source field schema changed');
  const delta = cfg.end >= cfg.start ? 1 : -1;
  if (![cfg.start, cfg.end].every(x => Number.isInteger(x) && x >= 2 && x <= rows.length))
    throw Error('Explicit valid source range required');
  const hash = createHash('sha256').update(raw).digest('hex');
  const proof = await fs.readFile(cfg.output, 'utf8').then(JSON.parse).catch(e => {
    if (e.code === 'ENOENT') return {source_snapshot_sha256: hash, table_id: cfg.tableId, records: []};
    throw e;
  });
  if (proof.source_snapshot_sha256 !== hash || proof.table_id !== cfg.tableId)
    throw Error('Previous capture provenance changed');
  for (let row = cfg.start; ; row += delta) {
    if (cfg.pauseFile && await fs.stat(cfg.pauseFile).then(() => true).catch(e => { if (e.code === 'ENOENT') return false; throw e; }))
      return {paused_at_row: row, captured_records: proof.records.length};
    const name = (rows[row - 1].A || '').trim();
    await page.waitForFunction(name => {
      const e = document.querySelector('label[data-field-id="fldM6QPKxC"] .bitable-card-edit-cell-editor-Text');
      return !!e && e.innerText.replace(/\u200b/g, '').trim() === name;
    }, name, {timeout: 15000});
    const state = await page.evaluate(() => {
      const f = id => document.querySelector('label[data-field-id="' + id + '"]');
      const text = id => f(id)?.querySelector('.bitable-card-edit-cell-editor-Text')?.innerText.replace(/\u200b/g, '').trim() || '';
      const link = f('fldNAnKWKe');
      return {
        record_id: f('fldM6QPKxC')?.querySelector('[id^="BITABLE_TEXT_EDITOR_CONTAINER_ID_PREFIX_"]')?.id.match(/PREFIX_(rec[A-Za-z0-9]+)_/)?.[1],
        name: text('fldM6QPKxC'), formal_code: text('fld4EtxMCr'),
        field_caption: link?.querySelector('.bitable-card-field-label__name')?.innerText.trim(),
        field_text: link?.innerText.replace(/\u200b/g, '').trim(),
        anchors: [...(link?.querySelectorAll('a') || [])].map(e => e.href),
        attachment_files: [...(link?.querySelectorAll('span.attach-item-title') || [])].map(e => e.title),
        files: [...(f('fldTjEnH15')?.querySelectorAll('span.attach-item-title') || [])].map(e => e.title),
      };
    });
    if (!state.record_id || state.name !== name || state.formal_code !== String(rows[row - 1].J || '').trim())
      throw Error('Native source identity differs at row ' + row);
    if (state.field_caption !== '技能包链接') throw Error('Native link field schema changed');
    if (state.anchors.length > 1) throw Error('Ambiguous source link at row ' + row);
    const sourceUrl = state.anchors[0] || '';
    if (!sourceUrl && (state.field_text !== '技能包链接' || state.attachment_files.length))
      throw Error('Link field is not demonstrably empty at row ' + row);
    const old = proof.records.find(x => x.source_excel_row === row);
    if (old && (old.record_id !== state.record_id || old.formal_code !== state.formal_code || old.source_url !== sourceUrl))
      throw Error('Pinned native binding changed at row ' + row);
    const item = {...state, source_excel_row: row, source_url: sourceUrl, observed_at: new Date().toISOString()};
    proof.records = proof.records.filter(x => x.source_excel_row !== row).concat(item).sort((a, b) => a.source_excel_row - b.source_excel_row);
    await fs.writeFile(cfg.output, JSON.stringify(proof, null, 2) + '\n');
    if (row % 10 === 0 || row === cfg.start || row === cfg.end) console.log({captured_row: row, total: proof.records.length});
    if (row === cfg.end) break;
    const before = state.record_id;
    await page.click('.bitable-card-modal-header-v2-btn-' + (delta > 0 ? 'next' : 'prev'));
    await page.waitForFunction(before => {
      const id = document.querySelector('label[data-field-id="fldM6QPKxC"] [id^="BITABLE_TEXT_EDITOR_CONTAINER_ID_PREFIX_"]')?.id;
      return !!id && !id.includes('_' + before + '_');
    }, before, {timeout: 15000});
  }
  return {captured_records: proof.records.length, source_snapshot_sha256: hash};
}
