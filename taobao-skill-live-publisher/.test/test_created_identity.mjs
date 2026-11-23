import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {verifyCreatedCodeTransition} from '../scripts/created_identity.mjs';

const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'created-identity-'));
const sha = 'a'.repeat(64), download = 'b'.repeat(64);
async function save(name, value) {
  const file = path.join(dir, name), raw = JSON.stringify(value);
  await fs.writeFile(file, raw);
  return [file, createHash('sha256').update(raw).digest('hex')];
}
try {
  const [identityProofPath, identityProofSha256] = await save('identity.json', {
    verified: true, expected_package_sha256: sha, actual_download_sha256: download,
    approvalBinding: {account: 'TestAccount', publicAppId: '123', formalCode: 'native-code', packageSha256: sha,
      version: '1.0.0', downloadVersion: '1.0.0', actualDownloadSha256: download}});
  const approval = {user_decision: 'explicit approval', approved_at: '2026-11-23', source_rows: [2],
    source_code: 'source_code', approved_platform_code: 'native-code',
    write_J_only_after_native_creation_readback: true, preserve_source_code_in_package_and_note: true};
  const [approvalPath, approvalSha256] = await save('approval.json', approval);
  const transition = {row: 2, recordId: 'recPinned', sourceCode: 'source_code', targetCode: 'native-code',
    account: 'TestAccount', publicAppId: '123', identityProofPath, identityProofSha256, approvalPath, approvalSha256};
  const cfg = {row: 2, recordId: 'recPinned', formalCode: 'native-code', packageSha256: sha,
    resultNote: 'source_code → native-code; actual native result', approvedCodeTransition: transition};
  const state = {formalCode: 'source_code'};
  assert.equal((await verifyCreatedCodeTransition(cfg, state)).approved, true);
  for (const change of [{row: 3}, {recordId: 'recOther'}, {packageSha256: 'c'.repeat(64)},
    {resultNote: 'native-code only'}, {approvedCodeTransition: {...transition, publicAppId: '456'}},
    {approvedCodeTransition: {...transition, sourceCode: 'different'}}, {approvedCodeTransition: undefined}]) {
    await assert.rejects(verifyCreatedCodeTransition({...cfg, ...change}, state));
  }
  const proposal = {account: 'TestAccount', items: [{source_rows: [2], source_code: 'source_code', proposed_platform_code: 'native-code'}]};
  const [proposalPath, proposalSha256] = await save('proposal.json', proposal);
  const [batchApprovalPath, batchApprovalSha256] = await save('batch-approval.json', {approved: true, proposal_sha256: proposalSha256, proposal_count: 1});
  const batch = {...cfg, approvedCodeTransition: {...transition, proposalPath, proposalSha256, approvalPath: batchApprovalPath, approvalSha256: batchApprovalSha256}};
  assert.equal((await verifyCreatedCodeTransition(batch, state)).approved, true);
  await fs.writeFile(proposalPath, '{}');
  await assert.rejects(verifyCreatedCodeTransition(batch, state), /changed/);
  console.log('Created-code transitions require exact record, explicit approval, approved package identity, immutable evidence and preserved source code');
} finally {
  await fs.rm(dir, {recursive: true, force: true});
}
