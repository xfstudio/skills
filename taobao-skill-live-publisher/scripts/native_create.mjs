/** New-skill native UI flow. Existing and unknown targets must be reconciled, never recreated. */
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {button, nativeClick, nativeHover} from './browser.mjs';
import {closeDialog} from './taobao.mjs';

const sha = raw => createHash('sha256').update(raw).digest('hex');
async function json(path) { return JSON.parse(await fs.readFile(path, 'utf8')); }
async function save(path, value) {
  await fs.writeFile(path + '.tmp', JSON.stringify(value, null, 2) + '\n');
  await fs.rename(path + '.tmp', path);
}

export function checkCreationPlan(cfg, data) {
  if (!Number.isInteger(cfg.row) || cfg.row < 2 || !cfg.account || !/^[a-f0-9]{64}$/.test(cfg.packageSha256 || '') ||
      typeof cfg.formalCode !== 'string' || !/^[a-z][a-z0-9-]{0,29}$/.test(cfg.formalCode) ||
      typeof cfg.nativeName !== 'string' || !/^[\p{Script=Han}A-Za-z0-9]{1,20}$/u.test(cfg.nativeName) ||
      !Array.isArray(cfg.categoryPath) || cfg.categoryPath.length !== 3 || cfg.categoryPath[0] !== '电商' || cfg.categoryPath[1] !== '全部')
    throw Error('Explicit new-form identity, native name and observed category required');
  if (!/^[a-f0-9]{64}$/.test(cfg.sourceSnapshotSha256 || '') || data.sourceSha256 !== cfg.sourceSnapshotSha256 ||
      !/^[a-f0-9]{64}$/.test(cfg.inventorySha256 || '') || data.inventorySha256 !== cfg.inventorySha256)
    throw Error('Pinned source or complete inventory snapshot changed');
  const source = data.source[cfg.row - 1];
  if (!source?.A || source.I || source.A !== cfg.sourceName || String(source.J || '').trim() !== cfg.sourceCode)
    throw Error('Named empty-attachment source identity changed');
  const inventory = data.inventory, proof = data.inventoryProof;
  if (!proof.complete || proof.account !== cfg.account || proof.observed !== inventory.length || proof.expected !== inventory.length ||
      inventory.some(x => x.account !== cfg.account) || new Set(inventory.map(x => x.code)).size !== inventory.length ||
      new Set(inventory.map(x => x.appkey)).size !== inventory.length)
    throw Error('Complete native same-account inventory required');
  if ([...inventory, ...data.created].some(x => [cfg.sourceCode, cfg.formalCode].includes(x.code || x.formalCode)))
    throw Error('Existing platform identity; use the verified update target');
  if (cfg.formalCode !== cfg.sourceCode) {
    const approval = data.approval;
    if (data.proposal) {
      if (approval?.approved !== true || approval.proposal_sha256 !== data.proposalSha256 ||
          data.proposal.account !== cfg.account || data.proposal.source_snapshot_sha256 !== cfg.sourceSnapshotSha256 ||
          data.proposal.platform_inventory_sha256 !== cfg.inventorySha256 || approval.proposal_count !== data.proposal.items.length ||
          data.proposal.items.filter(x => x.source_rows.includes(cfg.row) && x.source_code === cfg.sourceCode &&
            x.proposed_platform_code === cfg.formalCode).length !== 1)
        throw Error('Exact code normalization approval required');
    } else if (!approval?.user_decision || !approval.approved_at || !approval.source_rows?.includes(cfg.row) ||
               approval.source_code !== cfg.sourceCode || approval.approved_platform_code !== cfg.formalCode ||
               approval.write_J_only_after_native_creation_readback !== true || approval.preserve_source_code_in_package_and_note !== true) {
      throw Error('Exact additional code-change approval required');
    }
  }
  const bm = data.bm.find(x => (x.row === cfg.row || x.source_rows?.includes(cfg.row)) && x.sha256 === cfg.packageSha256);
  const attachment = data.attachments.find(x => x.source_excel_row === cfg.row && x.sha256 === cfg.packageSha256);
  if (!bm || bm.formal_code !== (cfg.sourceCode || cfg.formalCode) || bm.phase !== 'fixed_asset_verified' || !bm.asset_id || !bm.asset_revision ||
      !attachment?.attachment_replace_readback || !attachment.record_id)
    throw Error('Matching fixed BM asset and pinned Feishu attachment required');
  return {bm, attachment, expectedTotal: inventory.length + data.created.length};
}

async function account(page, expected) {
  await page.waitForFunction(expected => {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      const r = node.parentElement.getBoundingClientRect();
      if (node.textContent.trim() === expected && r.width > 0 && r.height > 0 && r.y >= 0 && r.y < 80) return true;
    }
    return false;
  }, expected, {timeout: 15000});
}

export async function createNativeSkill(page, cfg) {
  if (await fs.stat(cfg.intentPath).then(() => true).catch(e => { if (e.code === 'ENOENT') return false; throw e; }))
    throw Error('Existing creation intent; reconcile it without another creation request');
  const rawPackage = await fs.readFile(cfg.packagePath);
  if (sha(rawPackage) !== cfg.packageSha256) throw Error('Frozen package changed');
  const data = {
    source: await json(cfg.sourcePath), inventory: await json(cfg.inventoryPath), inventoryProof: await json(cfg.inventoryProofPath),
    sourceSha256: sha(await fs.readFile(cfg.sourcePath)), inventorySha256: sha(await fs.readFile(cfg.inventoryPath)),
    created: await json(cfg.createdLedgerPath), bm: await json(cfg.bmReceiptsPath), attachments: await json(cfg.attachmentReceiptsPath),
    approval: cfg.approvalPath ? await json(cfg.approvalPath) : null,
    proposal: cfg.proposalPath ? await json(cfg.proposalPath) : null,
    proposalSha256: cfg.proposalPath ? sha(await fs.readFile(cfg.proposalPath)) : null,
  };
  const checked = checkCreationPlan(cfg, data);
  await page.goto('https://work.open.taobao.com/open-skill/list');
  await account(page, cfg.account);
  // A wider viewport resolves the observed metadata/button overlap; never force a covered click.
  await page.cdp('Emulation.setDeviceMetricsOverride', {width: 1440, height: 1802, deviceScaleFactor: 1, mobile: false});
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.fill('input[placeholder="请输入"]', '');
  await page.press('input[placeholder="请输入"]', 'Enter');
  await page.waitForFunction(total => new RegExp('共\\s*' + total + '\\s*项数据').test(document.body.innerText), checked.expectedTotal, {timeout: 20000});
  await button(page, '创建技能');
  await page.fill('input[placeholder="仅允许中文、英文、数字；禁止特殊符号（如 @#$%）及 Emoji"]', cfg.nativeName);
  await page.fill('input[placeholder="仅允许小写字母、数字、中划线 (-),创建后不允许修改"]', cfg.formalCode);
  await page.click('[role=dialog] input[type=search]');
  for (const category of cfg.categoryPath) await page.click('text=' + JSON.stringify(category));
  await page.click('text="上传技能包创建"');
  await page.waitForLoadState('networkidle', {timeout: 15000, idleMs: 800});
  const error = await page.evaluate(() => [...document.querySelectorAll('[role=dialog] [class*="explain-error"]')].map(e => e.innerText).join('\n'));
  if (error) throw Error('Native code/form validation rejected; no creation submitted: ' + error.slice(0, 200));
  await page.setInputFiles('[role=dialog] input#file', [cfg.packagePath]);
  const filename = cfg.packagePath.split('/').at(-1);
  await page.waitForFunction(filename => document.querySelector('[role=dialog]')?.innerText.includes(filename), filename, {timeout: 20000});
  const state = await page.evaluate(() => {
    const d = document.querySelector('[role=dialog]');
    return {text: d?.innerText, values: [...d.querySelectorAll('input[type=text]')].map(e => e.value)};
  });
  if (state.values[0] !== cfg.nativeName || state.values[1] !== cfg.formalCode ||
      !state.text.includes(cfg.categoryPath.join(' / ')) || state.text.includes('RPC调用失败')) throw Error('Final creation form changed');
  const intent = {row: cfg.row, account: cfg.account, sourceCode: cfg.sourceCode, formalCode: cfg.formalCode,
    nativeName: cfg.nativeName, packageSha256: cfg.packageSha256, categoryPath: cfg.categoryPath,
    recordId: checked.attachment.record_id, assetId: checked.bm.asset_id, assetRevision: checked.bm.asset_revision,
    phase: 'creation_submitting', intentAt: new Date().toISOString()};
  await fs.writeFile(cfg.intentPath, JSON.stringify(intent, null, 2) + '\n', {flag: 'wx'});
  try {
    await nativeClick(page, '[role=dialog] button[class*="createBtn--"]');
    await page.waitForURL('**/open-skill/skill-detail?dataId=*', {timeout: 30000});
    intent.editorUrl = await page.url();
    await page.waitForFunction(code => document.querySelector('.tbd-tree-node-content-wrapper')?.getAttribute('title') === code,
      cfg.formalCode, {timeout: 30000});
    intent.phase = 'workspace_created';
    await save(cfg.intentPath, intent);
  } catch (error) {
    intent.phase = 'creation_unknown';
    await save(cfg.intentPath, intent);
    throw error;
  }
  return intent;
}

export async function readCreatedIdentity(page, cfg) {
  const intent = await json(cfg.intentPath);
  if (intent.row !== cfg.row || intent.account !== cfg.account || intent.formalCode !== cfg.formalCode ||
      intent.packageSha256 !== cfg.packageSha256 || !intent.editorUrl) throw Error('Pinned creation intent needs reconciliation');
  await page.goto('https://work.open.taobao.com/open-skill/list');
  await page.cdp('Emulation.setDeviceMetricsOverride', {width: 1440, height: 1802, deviceScaleFactor: 1, mobile: false});
  await page.evaluate(() => window.scrollTo(0, 0));
  await account(page, cfg.account);
  await page.fill('input[placeholder="请输入"]', cfg.nativeName);
  await page.press('input[placeholder="请输入"]', 'Enter');
  await page.waitForFunction(({name, code}) => [...document.querySelectorAll('[class^="skillCard--"]')].some(
    e => e.innerText.split('\n')[0].trim() === name && e.innerText.includes(code)), {name: cfg.nativeName, code: cfg.formalCode}, {timeout: 20000});
  const cards = await page.evaluate(({name, code}) => [...document.querySelectorAll('[class^="skillCard--"]')]
    .filter(e => e.innerText.split('\n')[0].trim() === name && e.innerText.includes(code)).map(e => {
      const lines = e.innerText.split('\n').map(s => s.trim()), i = lines.findIndex(s => s.toLowerCase() === 'appkey');
      return {text: e.innerText, appkey: lines[i + 1], ordinal: [...e.parentElement.children].indexOf(e)};
    }), {name: cfg.nativeName, code: cfg.formalCode});
  if (cards.length !== 1 || !/^\d+$/.test(cards[0].appkey)) throw Error('No unique native created code/AppKey card');
  const card = cards[0], selector = '[class^="skillGrid--"] > [class^="skillCard--"]:nth-child(' + (card.ordinal + 1) + ')';
  await nativeHover(page, selector);
  await nativeClick(page, selector + ' button', 1);
  await page.click('text="编辑技能"');
  await page.waitForURL(intent.editorUrl, {timeout: 20000});
  await page.waitForFunction(code => document.querySelector('.tbd-tree-node-content-wrapper')?.getAttribute('title') === code,
    cfg.formalCode, {timeout: 30000});
  const result = {...intent, phase: 'created_identity_verified', publicAppId: card.appkey, cardReadback: card.text,
    observedAt: new Date().toISOString(), listingVerified: false, merchantUseVerified: false};
  const ledger = await json(cfg.createdLedgerPath);
  if (ledger.some(x => (x.formalCode === cfg.formalCode || x.publicAppId === card.appkey) &&
      (x.formalCode !== cfg.formalCode || x.publicAppId !== card.appkey))) throw Error('Created identity ledger conflict');
  await save(cfg.receiptPath, result);
  await save(cfg.createdLedgerPath, ledger.filter(x => x.formalCode !== cfg.formalCode).concat(result));
  await save(cfg.intentPath, result);
  return result;
}

export function requireInitialDraftVersions(versions) {
  if (!Array.isArray(versions) || versions.length !== 1 || versions[0] !== '当前草稿')
    throw Error('This is not a current-only new draft; reconcile existing versions without another first-version submission');
}

/** Observe and cancel the first-version form; submitting remains a separate journaled stage. */
export async function observeInitialVersion(page, cfg) {
  const created = await json(cfg.createdIdentityPath), proof = await json(cfg.proofPath);
  if (created.phase !== 'created_identity_verified' || created.account !== cfg.account || created.row !== cfg.row ||
      created.publicAppId !== cfg.publicAppId || created.formalCode !== cfg.formalCode ||
      created.packageSha256 !== cfg.packageSha256 || !proof.verified || proof.expected_package_sha256 !== cfg.packageSha256 ||
      !['定向订购', '公开订购'].includes(cfg.listingMode)) throw Error('Verified new identity, whole package and explicit listing mode required');
  if (await page.url() !== created.editorUrl) await page.goto(created.editorUrl);
  await account(page, cfg.account);
  await page.cdp('Emulation.setDeviceMetricsOverride', {width: 1440, height: 1802, deviceScaleFactor: 1, mobile: false});
  await page.waitForFunction(code => document.querySelector('.tbd-tree-node-content-wrapper')?.getAttribute('title') === code,
    cfg.formalCode, {timeout: 30000});
  await closeDialog(page);
  await nativeClick(page, 'button:has(span[aria-label="field-time"])');
  await page.waitForFunction(() => [...document.querySelectorAll('[role=dialog]')].some(d => d.innerText.includes('当前草稿')), undefined, {timeout: 15000});
  const versions = await page.evaluate(() => {
    const d = [...document.querySelectorAll('[role=dialog]')].find(e => e.getBoundingClientRect().height > 0);
    return [...d.querySelectorAll('tbody tr')].map(r => r.querySelector('td')?.innerText.trim());
  });
  requireInitialDraftVersions(versions);
  await closeDialog(page);
  await button(page, '发布');
  await page.waitForSelector('[role=dialog] input[disabled]', {timeout: 15000});
  const offeredVersion = await page.evaluate(() => document.querySelector('[role=dialog] input[disabled]')?.value);
  if (!/^\d+\.\d+\.\d+$/.test(offeredVersion || '')) throw Error('No actual semantic version offer');
  await closeDialog(page);
  const target = {row: cfg.row, account: cfg.account, publicAppId: cfg.publicAppId, formalCode: cfg.formalCode,
    searchName: created.nativeName, editorUrl: created.editorUrl, wasListed: false, hadListing: false, offlineBefore: false,
    existingMode: cfg.listingMode, listingBefore: {formalCode: cfg.formalCode, notYetListed: true},
    authorizationReadback: {complete: true, shops: [], existingListingAbsent: true,
      readback: 'Verified native new identity; version dialog contains only 当前草稿; no existing store listing'},
    createdIdentityPath: cfg.createdIdentityPath, observedAt: new Date().toISOString()};
  const result = {target, offeredVersion, observedVersions: versions, packageSha256: cfg.packageSha256,
    submitted: false, observedAt: new Date().toISOString()};
  await save(cfg.receiptPath, result);
  return result;
}
