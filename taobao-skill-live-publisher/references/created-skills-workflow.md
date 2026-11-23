# 为飞书缺包记录创建 ATP 技能

本流程处理具名且“自建技能包”为空的记录。它不替换已有包，不把草稿生成或 BM 导入当作淘宝上架。飞书仍只通过本次已登录页面操作；账号、字段和目录以当前观察为准。

## 固定来源并创作

1. 按飞书来源流程原生导出、立即脱敏，固定完整表及 MCP 目录摘要。跳过空白名称行。保留每条记录的正式 J 编码；只有完全相同的正式编码、相容的业务属性才可共用一个包，仍分别绑定飞书 record_id。不能因 C、名称或原市场数字编号相近而合并身份。
2. 审阅每个属性步骤，将实际业务实体、范围、参数、分页和输出对应到指定目录的精确编码、版本、完整请求 schema 与示例。目录的历史“已调通”不能证明本轮调用成功。Top-N 不等于全量，本店交易评价不等于任意竞品评价，建议不等于写入。
3. 用户已指定电商浏览器补位时，无等价原子接口的业务步骤可使用运行环境实际注册的 ecom-borswer / EcommerceBrowserMCP。技能写明对象、筛选、日期、原生导出或分页终止证据、去重与缺口；工具 schema 在运行时读取，不能编造工具名、参数或页面选择器。缺失原模板、专有公式、固定文案或必要协议时保留具体缺口，按用户已给的重新设计决定处理。
4. 使用明确指定的 skill-creator 创作生产技能和每技能两个以上离线用例，成对运行带技能与基线测试，保存输出、评分、实际可得的耗时及审阅页。合成测试不调用商家业务接口，未取得的 token/耗时不填零。根据真实结果修订，再冻结生产 ZIP；测试文件和工作区不进入生产包。

`create_property_drafts.py --batch BATCH` 可从逐属性研究生成初稿。其 `draft-manifest.json` 全部标记未审阅，ATP helper 默认 dry-run 且禁止草案执行；这些包不能直接用于发布。初稿只降低重复整理工作，不能替代逐项语义审阅。

使用 `prepare_created_evals.py --manifest CURRENT_MANIFEST --iteration N --output NEW_REGISTRY` 从当前冻结清单生成评测登记。脚本核对 ZIP 中 SKILL.md 与当前技能一致，绑定 prompt/input 摘要，并拒绝已存在的工作区和登记文件。修订后使用全新 iteration；不能从旧 run-plan 手工改标题后复用旧输出路径。执行者开始前再次核对登记摘要。发生误覆盖时隔离受影响证据、记录不可恢复范围，并重新运行，不能保留旧评分冒充新结果。

## 新包校验与 BM 固定资产

已审阅创作清单为对象，含 `items`。每项包含 `primary_row/source_rows/name/formal_code/skill_name/skill_path/package_path/package_sha256/package_files/source_snapshot_sha256/catalog_sha256`。`package_files` 固定每个 ZIP 文件的路径及摘要。来源属性只保留业务字段，禁止 Z/AA 凭据列。

```bash
python scripts/validate_created_skills.py \
  --manifest BATCH/REVIEWED_MANIFEST.json \
  --catalog BATCH/source/catalog.json \
  --source BATCH/source/atp-target-before.json \
  --skill-validator /absolute/path/to/selected-skill-creator/scripts/quick_validate.py \
  --output BATCH/created-validation.json
```

校验器核对空附件来源、精确 J、别名、原始属性、目录契约、执行绑定、ZIP 字节及 creator 静态规则。这只是结构和来源证明，仍需独立语义审阅及用例结果。

不同创作分组可能固定完整导出、已脱敏缺包子集或规范化目录 JSON 的摘要。显式提供 `--derived-source VERIFIED_SUBSET.json --catalog-export RAW_CATALOG.xlsx` 时，校验器逐行核对子集中的每个原始值、空附件及无凭据列，核对目录原始导出摘要，再接受这些已证明的表示形式。它只在内存中适配已知来源记录和执行计划容器，不重写原 ZIP、不修改原文或假装摘要相同；未指定时仍使用原严格摘要检查。禁用编码仅能留在非执行参考中，所有实际执行绑定仍逐个核对完整契约、版本和可用性。空 J 的新身份仍单独阻断，不能因来源表示适配而自动建立平台关联。Creator 校验必须使用现有带依赖的 Python 环境；环境缺包须如实报告，不能算作包通过。

没有既有资产映射时使用新导入公开契约，不能给替换脚本伪造旧 catalogId：

```bash
python scripts/bm_import_created.py \
  --base-url http://VERIFIED_DEV_ORIGIN \
  --manifest BATCH/REVIEWED_MANIFEST.json \
  --validation BATCH/created-validation.json \
  --plan BATCH/bm-created-import-plan.json
```

默认只保存可审阅计划，零外部写入。核对目标 dev 实例、唯一包身份和清单后，加 `--apply --username ADMIN --receipts BATCH/bm-created-imports.json` 执行；密码交互输入，不放入参数或文件。可用 `--rows PRIMARY_ROW,...` 试点。原生接口每次接收一个 ZIP：`file`、JSON 字符串 `metadata`、`clientOperationId`，且 Idempotency-Key 相同。BM `public` 是本地库可见性，不是淘宝公开订购。

计划固定操作 UUID、原包摘要和元数据，写入前保存意图。恢复先 GET 原 operation；已有意图且仍无服务端记录时只报告待对账，不重新 POST。同步回执必须为 synced，再核对 asset/catalog/native package ID、原始 ZIP 下载 SHA256 和 ETag，并要求下载前后来源一致。保留实际新 ID，不伪造 originalBlobId 或 OSS 地址，不把 synced 改写为飞书同步成功。

## 上传、发布与同步

将已冻结包按来源别名展开成附件 manifest：每条飞书记录独立保留 `row/name`、record_id 和写前附件/链接；共享身份可以引用同一个冻结 ZIP。通过已有 `feishu-upload` 上传，回读“升级更新中 / 待同步”，最后全表导出核验，只允许本批已计划字段变化。

原生导出的 JSON 可能省略空单元格。不能用 Python `.get()` 返回 None 证明导出里有明确 null，也不能因此关闭 URL 漂移检查。在已核实正确记录详情后，使用 `capture_created_bindings.mjs` 的 `captureCreatedBindings(page,cfg)` 只读采集 `sourcePath/tableId/start/end/output` 范围的真实 record_id、名称、J、H 字段标题/可见文本/锚点及 I 文件名，逐条落盘。脚本不读取凭据列。调用期间保持同一浏览器串行；CLI 输出可能缓冲，可只读查看落盘进度，不能另起导航或通过终止 CLI 假定远程脚本已停止。

`prepare_created_upload.py --source RAW_EXPORT.json --native-capture CAPTURE.json --packages ATTACHMENT_MANIFEST.json --output-dir NEW_DIR` 保留原始导出，只为有明确原生证据的计划记录补充派生 `source_url` 元数据，固定证据摘要和 record_id。真实链接、名称、编码、原附件或 ZIP 漂移仍被拦截。上传用派生 baseline，最终整表核对仍使用原始 baseline；不回写来源 H 列。准备文件不同则拒绝覆盖。

淘宝先完整原生查重，保存当前账号、总数、分页和每个正式 code/AppKey。无法读取的草稿或不完整搜索不能认定不存在。相同 J 的别名只执行一次平台动作；不同 J 分别核对，不能为避开冲突自动改 code。既有对象使用已核验目标，确属新对象才通过实际“创建技能 / 上传技能包创建”入口创建，保存请求意图并回读实际身份。遇到文件选择器、验证码、协议等需人工步骤，准备具体表单后按同一 Ego TaskSpace handOff。

新建表单的编码限制以本轮实际界面为准。原 J 不满足限制时先固定无冲突对照表及用户决定；已有平台编码保持原样。原编码虽合规但校验失败时，不把 RPC 错误解释成已证实重名，可在未提交表单中做受控校验并记录结果，额外编码变更仍需对应授权。真实创建并回读 code/AppKey/账号后才更新 J，包内及说明保留原 code。创建请求未知时先回查原目标，不换 code 重提。

`browser_cli.py` 提供 `taobao-create` 与只读 `taobao-created-identity` 两个阶段（实现 `native_create.mjs`）。新建配置固定 `row/account/sourceName/sourceCode/formalCode/nativeName/categoryPath/packagePath/packageSha256`，以及原始 `sourcePath/sourceSnapshotSha256`、完整原生 `inventoryPath/inventorySha256/inventoryProofPath`、本批 `createdLedgerPath`、`bmReceiptsPath/attachmentReceiptsPath`、单条 `intentPath/receiptPath`。编码改变还须固定明确批准的 `approvalPath`；58项等批量对照使用额外的 `proposalPath`，审批文件必须绑定对照 SHA256。它要求完整同账号查重、当前总数与原清单加本批真实创建数一致、匹配固定资产和飞书附件；不从同名或 AB 编号推断目标。名称、类目和 code 均先在当前原生表单验证，固定 ZIP 上传后才保存单次创建意图。任何已有意图禁止重建；未知先只读回查同一 URL、code、AppKey 和账号。只读身份阶段核验原生卡片与同一工作区根名，并保存实际 AppKey，不提交版本或上架。

当前新建后的纯草稿尚无可用“去上架”按钮，也无既有授权列表；先用实际创建回执、工作区及原生卡片确认新目标并核验完整 ZIP，再提交界面实际提供的首版号。不能把旧目标的详情采集失败当成创建失败重建。新建后首次“当前草稿”原生下载可能保留带随机前缀的原上传文件名；必须以记录的下载动作、时间、唯一新文件和完整原包比对收集，不将本地原包复制冒充下载。审批版下载仍须独立核验并绑定版本/账号/AppKey。

该初始下载可用 `collect_created_download.py --operation NATIVE_DOWNLOAD.json --creation-receipt CREATED_IDENTITY.json --expected FROZEN.zip --directory NATIVE_DOWNLOAD_DIR --output NEW_COPY.zip --receipt NEW_RECEIPT.json`。它只接受已回读新身份、同一次原生当前草稿动作和冻结包摘要，匹配下载后唯一新文件（正式 code 前缀或原上传文件名），完整比对后才复制。重复候选、旧文件、改变的包及已有输出全部拒绝；已完成操作只能核对原副本，不再次收集覆盖。版本审批下载继续使用原 `package_io.py` 和审批绑定流程。

`taobao-first-version-offer` 是只读准备阶段：配置固定 `createdIdentityPath/proofPath/row/account/publicAppId/formalCode/packageSha256/listingMode/receiptPath`。它要求新身份和整包证明一致，重新查看原生版本记录且只允许唯一“当前草稿”，读取并取消发布表单，保存实际 `offeredVersion` 和初始 target。任何既有或未知版本都拒绝走首版路径。将该实际 target、offeredVersion、整包证明及固定 BM 回执交给既有 `taobao-submit-version` 单次提交；不猜首版号，也不为重试清理既有 journal。已出现版本记录的项目先按原版本 journal 对账。

当前窄视口会出现卡片元数据覆盖“去上架”按钮。可将该淘宝页面的渲染视口调整为 1440 像素宽后重读命中状态；不得强制点击被覆盖的按钮。技能图标经原生裁剪上传后回读实际图片尺寸，裁剪关闭不等于上传完成。协议处理交接返回时先观察：若用户已提交且显示审核中/已上架，保存实际状态并禁止再提交。

视口覆写在新的 SDK 执行轮次可能恢复为默认宽度。`taobao-create/taobao-created-identity` 在本轮自行设置；其余 `taobao-*` 阶段可在配置中给 `viewportWidth:1440`，脚本只接受 1280–1920 的整数，不影响飞书页。不能把上一轮设置过宽视口当成当前仍生效。

编码 J 的既有非空值默认仍不覆盖。仅 `approvedCodeTransition` 可将已批准的精确来源 code 改为真实新平台 code：绑定行/record_id、账号/AppKey、批准文件及摘要、可选批量对照及摘要、已核验审批包身份及摘要，并要求回填说明同时保留原/新 code。缺任何证据或真实目标漂移时，在任何字段写入前拒绝；不得把该选项用于旧目标改名。

后续使用批次版本与上架流程：原生整包下载比对、单次提交版本、具体审批版本下载、线上版本与商店状态回读。资料缺失的定向方式沿用用户已选边界；协议由用户处理。店铺授权独立核验，仅补用户指定店铺，不把灰度商家列当作授权结果。

使用 taobao-bm-listing-sync 取得本轮完整的已上架详情和当前 native 包快照；历史映射填写实际 `newCatalogId/newPackageId/sha256`，新建项不伪造旧包。原生卡片描述与固定资产元数据是不同层；只按该技能的计划写 description 并回读，不能因此声称线上包内容或商家使用已验证。

最后按真实结果回填飞书，保持实际线上版本、审核状态、定向授权、BM 同步和飞书同步的区别。完整导出核验未改已有包、凭据及其他记录；回填异常只对账回填，不重复发布。

附件和结果交错写入时，可用 `verify_created_table.py --baseline ORIGINAL_REDACTED.json --current FINAL_REDACTED.json --packages ATTACHMENT_MANIFEST.json --attachment-receipts NATIVE_RECEIPTS.json --writebacks EXACT_RESULT_PLANS.json --output VERIFY.json` 做全表对账。它从原始表和已回读附件生成中间期望，再应用精确结果字段；该中间值明确是计划推导，不冒充中间导出。要求原附件为空、名称/record_id/冻结 ZIP/回执一致，逐列检查所有未计划记录和字段，保留原有附件及其他说明。没有结果回填时省略 `--writebacks`。导出后先脱敏再读或校验，不对异常的未知结果重复平台提交。
