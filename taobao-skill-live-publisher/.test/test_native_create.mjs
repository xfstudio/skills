import assert from 'node:assert/strict';
import {checkCreationPlan, requireInitialDraftVersions} from '../scripts/native_create.mjs';
const sha = 'a'.repeat(64);
const cfg = {row: 2, account: 'TestAccount', nativeName: '类目查询', categoryPath: ['电商', '全部', '商品管理Skill'],
  sourceName: 'source name', sourceCode: 'new-code', formalCode: 'new-code', packageSha256: sha,
  sourceSnapshotSha256: 'c'.repeat(64), inventorySha256: 'd'.repeat(64)};
const data = {source: [{}, {A: 'source name', J: 'new-code'}], sourceSha256: cfg.sourceSnapshotSha256, inventorySha256: cfg.inventorySha256,
  inventory: [{account: 'TestAccount', appkey: '123', code: 'existing-code'}],
  inventoryProof: {complete: true, account: 'TestAccount', observed: 1, expected: 1}, created: [],
  bm: [{row: 2, formal_code: 'new-code', sha256: sha, phase: 'fixed_asset_verified', asset_id: 'asset', asset_revision: 1}],
  attachments: [{source_excel_row: 2, sha256: sha, attachment_replace_readback: true, record_id: 'recPinned'}]};
assert.equal(checkCreationPlan(cfg, data).expectedTotal, 1);
for (const patch of [{source: [{}, {A: 'source name', J: 'new-code', I: 'existing.zip'}]},
  {inventoryProof: {...data.inventoryProof, complete: false}}, {inventoryProof: {...data.inventoryProof, account: 'Other'}},
  {inventory: [{...data.inventory[0], code: 'new-code'}]}, {created: [{formalCode: 'new-code', publicAppId: '456'}]},
  {attachments: []}, {bm: [{...data.bm[0], formal_code: 'different'}]}, {bm: [{...data.bm[0], sha256: 'b'.repeat(64)}]}]) {
  assert.throws(() => checkCreationPlan(cfg, {...data, ...patch}));
}
assert.throws(() => checkCreationPlan(cfg, {...data, sourceSha256: 'e'.repeat(64)}));
const renamed = {...cfg, formalCode: 'native-code'};
assert.throws(() => checkCreationPlan(renamed, data), /approval/);
const approval = {user_decision: 'explicit approval', approved_at: '2026-11-23', source_rows: [2],
  source_code: 'new-code', approved_platform_code: 'native-code', write_J_only_after_native_creation_readback: true,
  preserve_source_code_in_package_and_note: true};
assert.equal(checkCreationPlan(renamed, {...data, approval}).bm.asset_id, 'asset');
assert.throws(() => checkCreationPlan(renamed, {...data, approval: {...approval, source_rows: [3]}}));
assert.throws(() => checkCreationPlan({...cfg, formalCode: 'a'.repeat(31)}, data));
assert.throws(() => checkCreationPlan({...cfg, nativeName: 'bad-name'}, data));
requireInitialDraftVersions(['当前草稿']);
for (const versions of [[], ['当前草稿', '1.0.0'], ['1.0.0'], ['当前草稿', 'unknown']])
  assert.throws(() => requireInitialDraftVersions(versions));
console.log('Native creation rejects existing/unknown identities, missing fixed assets/attachments, unapproved renames and invalid new-form fields');
