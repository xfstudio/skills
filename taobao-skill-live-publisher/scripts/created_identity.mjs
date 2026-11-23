/** Exact, approved source-code transition after native creation; never an automatic rename. */
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';

async function pinnedJson(path, sha256) {
  if (!path?.startsWith('/') || !/^[a-f0-9]{64}$/.test(sha256 || '')) throw Error('Pinned identity evidence required');
  const raw = await fs.readFile(path);
  if (createHash('sha256').update(raw).digest('hex') !== sha256) throw Error('Identity evidence changed');
  return JSON.parse(raw);
}

export async function verifyCreatedCodeTransition(cfg, state) {
  const t = cfg.approvedCodeTransition;
  if (!t || t.row !== cfg.row || t.recordId !== cfg.recordId || t.sourceCode !== state.formalCode ||
      t.targetCode !== cfg.formalCode || !t.account || !/^\d+$/.test(t.publicAppId || '') ||
      !/^[a-z][a-z0-9-]{0,29}$/.test(t.targetCode)) throw Error('Existing formal skill code conflicts with the verified platform target');
  const identity = await pinnedJson(t.identityProofPath, t.identityProofSha256);
  const binding = identity.approvalBinding;
  if (!identity.verified || !binding || binding.account !== t.account || binding.publicAppId !== t.publicAppId ||
      binding.formalCode !== t.targetCode || binding.packageSha256 !== cfg.packageSha256 ||
      identity.expected_package_sha256 !== cfg.packageSha256 || !binding.version ||
      binding.downloadVersion !== binding.version || binding.actualDownloadSha256 !== identity.actual_download_sha256)
    throw Error('Created identity is not bound to the verified approved package');
  const approval = await pinnedJson(t.approvalPath, t.approvalSha256);
  if (t.proposalPath) {
    const proposal = await pinnedJson(t.proposalPath, t.proposalSha256);
    if (approval.approved !== true || approval.proposal_sha256 !== t.proposalSha256 ||
        proposal.account !== t.account || proposal.items.length !== approval.proposal_count ||
        proposal.items.filter(x => x.source_rows.includes(t.row) && x.source_code === t.sourceCode &&
          x.proposed_platform_code === t.targetCode).length !== 1)
      throw Error('Code normalization approval does not cover this exact source/target');
  } else if (!approval.user_decision || !approval.approved_at || !approval.source_rows?.includes(t.row) ||
             approval.source_code !== t.sourceCode || approval.approved_platform_code !== t.targetCode ||
             approval.write_J_only_after_native_creation_readback !== true ||
             approval.preserve_source_code_in_package_and_note !== true) {
    throw Error('Explicit code-change approval does not cover this exact source/target');
  }
  if (!cfg.resultNote.includes(t.sourceCode) || !cfg.resultNote.includes(t.targetCode))
    throw Error('Writeback must preserve original and native platform codes');
  return {approved: true, sourceCode: t.sourceCode, targetCode: t.targetCode, publicAppId: t.publicAppId};
}
