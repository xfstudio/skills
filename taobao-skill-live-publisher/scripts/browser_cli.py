"""Run one explicit logged-in UI stage, serializing native focus/clipboard across pages."""
from __future__ import annotations
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--space-id', type=int, required=True)
    parser.add_argument('--page', required=True)
    args = parser.parse_args()
    os.umask(0o077)
    # Cross-process exclusion matters: native paste acts on the active browser.
    # Different tabs are not independent mutation surfaces.
    with (Path(tempfile.gettempdir()) / 'taobao-skill-publisher-browser.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        config = json.loads(args.config.read_text())
        config.update(spaceId=args.space_id, page=args.page)
        module = Path(__file__).resolve().parent
        code = r'''const fs=await import('node:fs/promises');
const cfg=CONFIG;
const entry=(await listTaskSpaces()).find(x=>x.id===cfg.spaceId);
if(!entry)throw Error('Existing task space missing; do not create a recovery space');
if(entry.ownership==='user'||(entry.ownership==='agentDelegatedToUser'&&!cfg.resumeUserHandoff))throw Error('User control or manual action pending; resume only after the user replies');
const task=entry.ownership==='agentDelegatedToUser'?await takeOverTaskSpace(cfg.spaceId):await taskSpace(cfg.spaceId);
const page=task.page(cfg.page);
await page.cdp('Page.bringToFront');
if(cfg.viewportWidth!==undefined){
if(!cfg.action.startsWith('taobao-')||!Number.isInteger(cfg.viewportWidth)||cfg.viewportWidth<1280||cfg.viewportWidth>1920)throw Error('Reviewed Taobao-only viewport width required');
await page.cdp('Emulation.setDeviceMetricsOverride',{width:cfg.viewportWidth,height:1802,deviceScaleFactor:1,mobile:false});
}
const browser=await import(BROWSER);
let result;
if(cfg.action==='close-version-records'){if(await page.url()!==cfg.editorUrl)throw Error('Editor changed');await (await import(TAOBAO)).closeDialog(page);result={closed:true};}
else if(cfg.action==='export-table')result=await browser.exportTable(page,cfg);
else if(cfg.action==='update-files')result=await browser.updateFiles(page,cfg);
else if(cfg.action==='download-draft')result=await browser.clickDraftDownload(page,cfg);
else if(cfg.action==='feishu-upload')result=await (await import(FEISHU)).uploadBatch(page,cfg);
else if(cfg.action==='capture-created-bindings')result=await (await import(CAPTURE)).captureCreatedBindings(page,cfg);
else if(cfg.action==='feishu-result-batch')result=await (await import(FEISHU)).writeResultsBatch(page,cfg);
else if(cfg.action==='feishu-result')result=await (await import(FEISHU)).writeResult(page,cfg);
else if(cfg.action==='feishu-result-column')result=await (await import(FEISHU)).pasteResultColumn(page,cfg);
else if(cfg.action==='feishu-oss-column')result=await (await import(FEISHU)).pasteOssColumn(page,cfg);
else if(cfg.action==='taobao-card')result=await (await import(TAOBAO)).findTarget(page,cfg);
else if(cfg.action==='open-known-editor'){
const url=new URL(cfg.editorUrl);
if(url.origin!=='https://work.open.taobao.com'||url.pathname!=='/open-skill/skill-detail'||!/^\d+$/.test(url.searchParams.get('dataId')||''))throw Error('Observed editor URL required');
await page.goto(cfg.editorUrl);await page.waitForSelector('.tbd-tree-node-content-wrapper',{timeout:20000});
const root=await page.evaluate(()=>document.querySelector('.tbd-tree-node-content-wrapper')?.getAttribute('title'));
if(root!==cfg.formalCode)throw Error('Workspace formal code changed');result={editorUrl:await page.url(),formalCode:root};
}
else if(cfg.action==='taobao-inspect')result=await (await import(TAOBAO)).inspectTarget(page,cfg);
else if(cfg.action==='taobao-create')result=await (await import(CREATION)).createNativeSkill(page,cfg);
else if(cfg.action==='taobao-created-identity')result=await (await import(CREATION)).readCreatedIdentity(page,cfg);
else if(cfg.action==='taobao-first-version-offer')result=await (await import(CREATION)).observeInitialVersion(page,cfg);
else if(cfg.action==='taobao-versions')result=await (await import(TAOBAO)).readVersions(page,cfg);
else if(cfg.action==='taobao-submit-version')result=await (await import(TAOBAO)).submitVersion(page,cfg);
else if(cfg.action==='taobao-activate-version')result=await (await import(TAOBAO)).activateVersion(page,cfg);
else if(cfg.action==='taobao-prepare-listing')result=await (await import(TAOBAO)).prepareListing(page,cfg);
else if(cfg.action==='taobao-submit-listing')result=await (await import(TAOBAO)).submitListing(page,cfg);
else if(cfg.action==='taobao-restore-listing')result=await (await import(TAOBAO)).restoreExistingListing(page,cfg);
else if(cfg.action==='taobao-ensure-authorization')result=await (await import(AUTHORIZATION)).ensureAuthorization(page,cfg);
else throw Error('Unsupported reviewed UI stage');
if(cfg.resultPath)await fs.writeFile(cfg.resultPath,JSON.stringify(result,null,2));
console.log({action:cfg.action,row:cfg.row,resultSaved:cfg.resultPath||null});
'''.replace('BROWSER', json.dumps((module/'browser.mjs').as_uri())).replace('FEISHU', json.dumps((module/'feishu.mjs').as_uri())).replace('TAOBAO', json.dumps((module/'taobao.mjs').as_uri())).replace('AUTHORIZATION', json.dumps((module/'authorization.mjs').as_uri())).replace('CREATION', json.dumps((module/'native_create.mjs').as_uri())).replace('CAPTURE', json.dumps((module/'capture_created_bindings.mjs').as_uri())).replace('CONFIG', json.dumps(config, ensure_ascii=False))
        result = subprocess.run(['ego-browser', 'nodejs'], input=code, text=True, check=False)
        if result.returncode==0 and config['action']=='export-table':
            result=subprocess.run([sys.executable,str(module/'redact_feishu_export.py'),config['output']],check=False)
        raise SystemExit(result.returncode)

if __name__ == '__main__':
    main()
