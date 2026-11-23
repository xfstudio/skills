# 飞书技能包升级、真实发布与对账脚本

这些脚本支持同一个批次恢复执行；它们不会运行技能包的业务脚本，也不会试调目录中的商家读写示例。淘宝、飞书使用用户已登录的 Ego 页面。BM 使用明确选定的 dev 实例，密码通过 getpass 输入，令牌只留在进程内存。

## 批次输入与固定来源

把批次数据放在技能目录之外。固定源表 URL、目标表 URL、MCP 表 URL、导出文件 SHA256、record_id、淘宝账号、公开 AppID、正式 code 和本次动作。不要提交业务导出、账号密钥、包或回执到本技能仓库。

1. 用现有 TaskSpace 的页面导出两个 SOP 表和用户指定的 MCP 表。`browser_cli.py` 的 `export-table` 配置含 `url/tableName/output`。页面为 canvas 时先查看截图，再通过行菜单“查看详情”打开记录；不要猜测行内图标位置。可先在表内用 Ctrl/Cmd+F“在数据表中查找”按唯一名称定位，等待真实匹配计数后查看截图；原生滚动或搜索只作定位，record_id 才是写入绑定。只从 DOM 的记录编辑器 ID 读取 record_id。记录详情可能显示密钥，不输出全页快照。
2. `browser_cli.py` 导出 SOP 后会自动调用脱敏器；直接使用浏览器模块导出时立即运行 `redact_feishu_export.py TABLE.xlsx`，移除 Z/AA 数据和共享字符串，输出同名 JSON。禁止先打印原始行。它要求实际 SOP 表头，若列位置改变，先修改并测试脱敏器。
3. `inventory_sources.py` 从该 UI 导出的所有包链接建立初始下载清单，限定 origin、大小和安全路径，报告需登录页面下载的附件；原始 frontmatter 不规范时留给语义审阅，不丢弃该 ZIP。已有受审阅摘要时使用 `download_sources.py` 重新下载并核验原包绑定。私有附件使用页面原生下载，不读取 cookies、token、浏览器 profile 或隐藏接口。无包记录保持原样。
4. 使用 skill-creator 逐技能审阅原业务步骤与能力等价性，保留本地分析、报告、只读/写入确认边界，产出受审阅的 `references/atp-routing.json`。`build_batch.py` 只复用受审阅的语义映射，不按近似名称自动猜测接口；新技能或目录删码必须重新审阅。

初始清单示例（origin 来自用户选定表中已核实的包地址）：

```bash
python3 scripts/inventory_sources.py --inventory BATCH/source/source-table.json --output-directory BATCH/original-packages --output BATCH/source-package-inventory.json --allowed-origin https://VERIFIED_OSS_ORIGIN
```

原包清单不是受审阅的升级 manifest。代理完成 skill-creator 审阅和操作映射后，再填写基准包路径/摘要并进入重建。

## 目录与重建

```bash
python3 scripts/mcp_catalog.py CATALOG.xlsx --source 'USER_SELECTED_CATALOG_URL' --output BATCH/source/catalog.json
python3 scripts/build_batch.py --base-manifest REVIEWED_BASE_MANIFEST.json --catalog BATCH/source/catalog.json --output BATCH
python3 scripts/validate_batch.py --manifest BATCH/package-manifest.json --catalog BATCH/source/catalog.json --skill-validator /absolute/path/to/skill-creator/scripts/quick_validate.py --output BATCH/validation.json
```

目录解析器固定在线版本、原始调用示例和完整嵌套请求 schema，按分段表还原超长参数，拒绝缺段/重复段。保留“调用失败”“无权限”“写操作仅 schema 核实”和示例与必填项不一致等限制。示例中的业务 ID、日期、预算必须在实际执行时替换为本轮真实输入；不自动补造系统上下文。无等价能力使用用户明确指定的电商浏览器 MCP。

基准 manifest 每项至少含 `row/name/skill_name/package_path/package_sha256/source_sha256`。row 是本次导出 Excel 行号，仅供定位；写入时必须另外核对已固定的 record_id。原始包摘要或来源字段变化时停止旧计划。

重建后冻结 ZIP 和 SHA256。后续内容修正另存新路径/新文件名，保留先前包与回执；不要覆盖已导入、已上传或已提交版本所引用的文件。`workflow.py verify-source` 复核源表完整快照及原始下载摘要。

## BM 固定资产与 OSS

默认继续遵守可信同步绑定规则。只有用户明确选择 BM 固定资产替代核验时，才使用下列路径，并记录该决定；BM `synced` 不代表飞书同步成功。

```bash
python3 scripts/bm_assets.py --base-url http://127.0.0.1:8088 --username ADMIN_NAME --manifest BATCH/package-manifest.json --prior-sources PRIOR_FIXED_SOURCES.json --receipts BATCH/bm-assets.json
```

当前适配器调用源码公开的 BM v2 `/skills/{catalogId}/package`，提交 expectedRevision 和稳定 operation UUID，保留旧资产快照；恢复先查同一 operation。成功后核对 assetId、固定修订、原始 ZIP SHA256、ETag、下载前后来源一致。未知结果只回查，不换键重发。新批次没有既有资产时，先使用实例原生导入流程取得固定资产映射，不伪造已有 catalogId。

若系统已配置 OSS 且数据库 `blob.content` 存储其不可变 HTTPS 地址，使用 `oss_links.py` 读取**匹配 packageId 的 originalBlobId**，限定已核实的 OSS origin，并匿名下载核验 ZIP SHA256。不要使用 derived ZIP URL 冒充原包 URL，不打印私有配置，不修改 RLS。

## 飞书附件与字段

统一通过下列入口操作页面，避免不同页面争抢原生焦点/剪贴板：

```bash
python3 scripts/browser_cli.py --space-id EXISTING_SPACE_ID --page EXISTING_PAGE --config REVIEWED_STAGE.json
```

`feishu-upload` 配置：`baselinePath/manifestPath/bindingsPath/receiptPath/start/end/targetTableId`；bindings 含 `source_excel_row/record_id`。可选 `previousManifestPaths` 只允许本批已核实的中间附件名；`pauseFile` 存在时在下一记录边界暂停。开始前页面已打开对应起始记录。

脚本核对唯一记录、来源 URL 和已有附件，只上传固定新包，回读文件名后移除已知旧附件，设置“升级更新中 / 待同步”，逐记录落盘。文件名包含目录或内容指纹，不能因旧文件同名就误判升级成功。

结束后再次导出、脱敏，运行 `workflow.py verify-feishu`。默认只允许 I/E/AD 变化，并逐行检查无包记录和其他字段。链接改为新版 OSS 时，仅对目标表使用各自当前包地址；原表保留其原包地址。`feishu-oss-column` 要求代理先观察已选中“技能包链接”列的截图，再粘贴完整、已对账的列；**不发送 Ctrl+A**。粘贴后整表导出，允许字段包含 H/source_url，其余字段必须保持一致。

## 淘宝目标、工作区和版本

- `taobao-inspect`：通过实际列表搜索和唯一公开 AppID 定位，打开当前上架详情读正式 code/模式，完整读现有定向授权，不修改店铺；从“编辑技能”取得实际 editorUrl。已有方式优先，缺失方式仅使用用户已选的 fallbackMode。分页授权不完整时停止。 原名称查询为空不代表目标不存在。可用已观察到的关键词扩大原生查询，仍须唯一匹配原公开 AppID 并核对未变的名称/code，保存查询回执后仅调整批次的 searchName（搜索词）；不改变 AppID、不创建替代目标。
- `download-draft`：从版本记录“当前草稿”原生下载，记录该正式 code 的 Downloads 文件基线。`package_io.py collect` 只收集该次新 ZIP，不把父页未收到 download 事件当作没有下载；同一下载意图不能冒充另一次导出。
- 工作区“上传文件”不等于已确认的整包替换入口。当前实测中，其原生 chooser 的 `setFiles` 曾报缺少 nodeId/backendNodeId/objectId，页面也没有 file input，且树未出现上传内容；这不构成上传成功。不要重复探测或猜隐藏接口。文本变化可继续已验证的编辑器路径；确需二进制上传时交由用户处理原生选择器，再整包回读核验。
- `workflow.py prepare-editor`：对比整个当前 ZIP 与固定包，输出待修改文本文件配置。二进制变化、未知多余文件停止，使用已观察到的原生 ZIP 上传或明确清理。`update-files` 使用实际 CodeMirror/Monaco 编辑器和原生粘贴，逐文件保存；大 JSON 不用 fill。最后必须再次下载整个 ZIP。新的完整 ZIP 差异优先于旧 UI 保存回执；如保存后产生了不同的已知文本文件，批处理最多依据该次实测差异恢复原已审阅字节一次，再整包回读，仍不一致则停止该项。未知多余文件或二进制变化不自动清理。
- `package_io.py compare`：检查所有文件路径及字节，最多允许**已验证正式 code 对应的主 SKILL frontmatter name 行**归一。UI 编辑时也仅将该主 name 行对齐正式 code；原包和业务正文保持原样。部分平台对象的包内名称与正式 code 不同，未对齐时当前草稿下载曾返回旧包，故保存并等待完成后下载实际完整包验证；仅在已观察到页面恢复需要时显式使用 reloadBeforeDownload，避免每次重复加载公告服务。平台新建目录生成且界面隐藏的空 `.gitkeep`，只能通过逐路径 `--allow-empty-marker` 显式记录；非空标记或其他未知文件不允许。遗留 `.version.json` 安装 sidecar 逐项审阅后，通过 `--platform-metadata-plan` 按行传入逐文件 SHA256，要求更新前后字节保持一致。已支持的格式仅为固定完整字段、正式 code 一致且 `zip-install/user-created` 的安装记录，或仅含带时区 `createdAt` 与 `source=user-created` 的旧格式记录；旧格式不含内部 code，绑定依赖该行已核实目标和实际原生下载摘要，不能声称其自身证明了编码。未知字段或格式继续停止。安装版本不等于淘宝发布版本。审阅计划保存在批次目录，不能自动放行任意额外 JSON。业务文件差异均不通过。
- `taobao-submit-version`：配置包含固定包、完整包 proof、匹配的 BM 回执、已读目标、版本说明和平台实际 offered version。提交前持久化意图，只点击一次。超时标记 unknown，先使用 `taobao-versions` 回查同账号/AppID/版本，不重复发布。
- 对账时从列表“版本管理”的原生弹窗读取结构化审核/线上状态；`taobao-versions` 的可选 `approvedDownload`（version/downloadsDir/operationFile）仅在该具体版本审核通过、唯一且首个按钮确为“下载”时下载，同一次回读保留账号/AppID/code 与下载意图。它不依赖重新进入编辑页，也不读取下载 URL。
- 恢复对账可复用已核验的不可变版本 ZIP：先重新核对固定源包 SHA、账号/AppID/code/版本/下载版本绑定、下载 ZIP SHA 及完整文件差异。缓存只省去重复下载；审核、线上、商店和授权仍重新回读。身份或字节失配时不复用，源包变化则停止。
- 审核通过后下载该**具体版本**核验包，将 proof 绑定到账号、AppID、正式 code、版本、固定包摘要和该次下载；若仍非线上版本，使用 `taobao-activate-version` 选择已核验的审批版本；若重新回读发现更高或无法识别的版本，停止切换并核对并发变更。审核中、审核通过、线上版本和商店已上架分别记录。
- 已上架且资料不变的技能保留原上架信息/方式/店铺授权。未上架的使用 `taobao-prepare-listing` 准备可审阅资料；协议必须由用户阅读处理，脚本不勾选。需要登录、验证码、协议等用户动作时按 ego-browser handOff，同空间恢复后再用 `taobao-submit-listing`。提交后只以平台审核和卡片状态认定结果。

## 批量版本执行与恢复

`publish_batch.py --batch BATCH --targets VERIFIED_PUBLIC_TARGET_MAP.json --space-id ID --page PAGE --account ACCOUNT --downloads-directory ABS_DOWNLOADS --fallback-mode 定向订购` 串行执行目标核验、工作区完整下载/差异更新/回读及单次版本提交，逐项保存实际状态；需用户明确选择的 fallback mode，不能照抄这个示例扩大范围。先完成本批全部附件/来源校验，再启动真实版本写入。`--rows` 可先运行一个已明确目标的项目；`--pause-file ABS_PATH` 在该文件出现时于下一记录边界暂停。前批已确认不同包的审核中版本，可通过 `--prior-version-journal` 固定其真实意图后提交本轮新版本；未知来源的审核中版本先核对，不能因相同目标就认定是同一包，也不能重复提交相同包。

浏览器发布、核对和回填分阶段串行运行，避免争抢原生焦点。结果台账通过共享进程锁重新读取并按单行合并，防止其他行结果被旧快照覆盖。

原生树中删除已审阅的旧生成目录后，条目消失可能尚未持久化；必须连同本轮固定文本文件保存后，再原生下载整个工作区验证。先保留删除前 ZIP、逐路径摘要及与固定包的引用核对，不删除未审阅业务文件。本地排除已审阅删除项形成的 ZIP 只能用于生成文本编辑计划，明确标为规划产物，不能作为平台下载、版本包或上架证明。最终仍要求真实原生下载包逐文件通过固定包比对，旧目录重新出现则停止该项。

个别平台工作区另有空目录占位文件时，先检查该次原生下载中的完整路径和 0 字节内容，确认固定包确有该目录的业务文件，或它是既有脚本目录下仅含该空标记的 `__pycache__` 子目录。平台文件树及搜索可能隐藏后一种空目录，不能声称已删除。可用 `--platform-empty-marker-plan PLAN.json` 按行传入已审阅路径，例如 `{"124":["agents/.gitkeep"]}`；该项记录仅供格式示例。此计划只补充指定行的允许路径，仍逐次拒绝非空占位文件、含其他文件的缓存目录、未知父目录和其他额外文件，实际清单写入目标回执并用于审核包复核。不要按同名目录自动放行整批。

`reconcile_batch.py --batch BATCH --space-id ID --page PAGE --downloads-directory ABS_DOWNLOADS` 读取已提交意图，回查审核；通过后下载具体版本校验，核对线上版本、商店状态及原授权。未上架项目留给完整资料/用户协议阶段；`--rows` 可仅核对指定记录，避免为回填再次核对已完成的整批。只在用户明确要求持续跟进时按实际需要再次运行；它不建立后台任务。

## 已下架的既有技能

卡片“已下架 / 去上架”可能直接打开“确认上架技能”弹窗。不要把它当新上架资料表单。先从该卡片“更多 → 修改上架详情”只读核对正式 code、原方式、完整资料和图标，不保存、不覆盖。保留已观察的菜单与卡片状态。既有定向方式优先于缺失来源字段的 fallback。

下架时菜单可能没有“授权管理”。没有可用历史回执时明确记录原名单不可读取，保留 `complete:false / unavailableWhileUnlisted:true`；不能补造空名单、改成 complete:true 或使用灰度商家列替代证据。版本提交只为具备严格离线证据且原方式已观察的对象接纳该状态；已上架对象和分页不完整仍要求完整原名单。浏览器与 Python 门槛共用同一组离线契约用例。

用户已授权恢复这些技能时，`reconcile_batch.py ... --restore-existing-listings` 在具体审核包、当前线上版本及原详情/方式一致后，使用官方“去上架”纯确认入口，单次提交恢复；默认不执行恢复。该分支不保存详情、不勾选协议、不增删店铺，遇到协议、验证码或未知确认内容时停止并按 Ego 流程交接。恢复意图写入原 listing journal，未知结果只回查，不重复确认；后续整批对账遇到已有意图且仍未上架的对象时，保留待核对结果并继续其他对象，不再次调用恢复入口。页面可见错误即时记录，敏感认证提示只保留概述。

恢复后重新读取商店状态与完整当前授权。若原名单不可见，只回填“当前名单已回读、本批未增删授权”；不能写“原授权一致”。只有原名单可读并逐项相同时才能记录保留一致。此类结果标记为 restore，与新上架、已上架技能更新分开。

## 新上架资料和人工协议

从未保存上架资料的对象使用以下入口；已有“已下架”资料的对象走上方恢复流程。

`listing_batch.py --batch BATCH --metadata REVIEWED_METADATA.json --pages ROW_TO_EXISTING_PAGE.json --verification-page SEPARATE_EXISTING_PAGE --space-id ID --action prepare` 只处理已通过具体版本包校验且线上、尚未上架的对象。metadata 的 `rows` 按 Excel 行号保存已审阅的 description/query/functions（两对名称与说明）/examples（两对场景与问题）/input/output。缺少图标时提供已审阅 PNG/JPEG 的 `iconPath/iconSha256`；脚本核对原图摘要，通过实际 logo 文件输入、原生方形裁剪“确认并上传”，回读预览尺寸。保持既有已上架技能的图标。pages 明确绑定各行与同一 TaskSpace 的现有页面，不新建恢复空间。另用一个现有 verification-page 在准备及提交前重新读取同账号/AppID 的当前线上版本；它不能覆盖已准备表单。人工协议期间版本漂移时停止，不能用历史包 proof 冒充当前线上身份。提交时还要求该绑定回读不超过一分钟。

脚本按已核实的既有方式或用户 fallback 准备表单，回读字段和模式，固定元数据与包摘要；**不勾选协议，不提交**。代理检查每张表单的必填资料、图标及可见校验，再按 ego-browser handOff 让用户阅读处理协议。用户确认后，在同一 TaskSpace 恢复，使用相同文件及 `--action submit --user-agreement-handled`；该参数只记录用户已处理，不能代替实际勾选状态。再次核对账号、编码、模式、资料、特定版本包及已有意图后才单次提交。结果未知只回查同一对象，不重复提交；随后用 reconcile_batch 的指定 rows 核验商店和原授权，最后回填。

## 对账与回填

### 批次商家授权核验

用户明确指定一个目标商家后，按固定 manifest 与版本意图中的账号、唯一 AppID、正式 code 和摘要核验整批；不按历史 `listed` 结果跳过当前平台状态。`authorization_batch.py --batch BATCH --output-directory AUTH_RUN --merchant EXACT_MERCHANT --space-id ID --page PAGE` 默认只读。只有用户已授权补齐时加 `--ensure`，仅向当前已上架的定向技能添加这个店铺。公开技能保持公开，未上架项目不恢复、不授权；两者分别报告。

脚本使用原生授权管理遍历完整名单，只有明确从第一页读到末页才能判断缺失。未知分页或目标冲突停止。已有店铺不重复添加；缺失时保存提交意图后仅点一次“添加”，再重新定位该 AppID、打开授权管理并完整回读，要求原名单加目标店铺与实际一致。其他店铺不移除。超时或已有意图仍未见目标时保留未知结果，不能重发。既有版本与上架意图、包文件和原发布回执保持原样，授权结果另存。

同一运行目录绑定 manifest、目标版本意图、商家和补齐权限。提交意图使用批次根目录的 `taobao-authorization-journal.json`，父执行器也以批次级锁互斥；更换报告目录不能绕过旧意图。`--rows` 用于小批实测或异常后继续独立对象；`--resume` 仅复用该固定运行中已完成的观察，未解决项目仍按旧意图只读回查。`--pause-file ABS_PATH` 在记录边界暂停。浏览器仍经 `browser_cli.py` 全局串行锁执行，不并发操作其他页。

结束后先导出最新脱敏飞书快照，再运行 `prepare_authorization_writebacks.py --batch BATCH --authorization-directory AUTH_RUN --baseline LATEST.json --bindings RECORD_BINDINGS.json --batch-id AUTH_BATCH_ID --output AUTH_RUN/writebacks.json`。此计划只更新 AG 同步说明，保留发布结果、附件、线上版本、同步状态与其他列。沿用下方原生整列或逐记录回填，并用 `workflow.py verify-results` 对全表导出验证；只声明后台授权已核实，商家客户端展示和实际调用须另行验证。

`report_authorization.py --batch BATCH --authorization-directory AUTH_RUN --writebacks AUTH_RUN/writebacks.json --verification VERIFIED_EXPORT_PROOF.json` 要求每个固定目标恰有一项当前结果、回填计划与结果阶段一致且全表核验摘要相符，随后输出授权 CSV 与统计 JSON。已上架但授权结果未知不能算全批核验完成，未上架对象单列。

### 发布结果回填

`prepare_writebacks.py --batch BATCH --bindings RECORD_BINDINGS.json --batch-id ID --baseline LATEST_REDACTED_TARGET.json` 根据真实结果生成字段级回填计划；`feishu-result-batch` 在已定位的记录详情内逐行对账回填，不重新提交平台动作。

`feishu-result` 仅给已固定 recordId/name/附件的记录追加带 batchId 的实际结果说明，可回填已核实正式 code；不覆盖其他渠道说明，也不把审核中写成成功。待审时保留“线上版本”；具体线上版本及其包已核实后，可按证据回填“当前版本/线上版本”，另行记录商店上架状态。永不把 BM `synced` 改写为飞书同步成功。仅在具体线上包、商店已上架和授权保持均已核实后，将已观察到的“技能生成及状态”选项设为“上架完成”；待审项目继续保留“升级更新中”。字段写入同时核对字段 ID 与实际中文表头，保留“技能编码”，仅回填“技能code”；最后整表导出后运行 `workflow.py verify-results --baseline BEFORE.json --current AFTER.json --writebacks PLAN.json --output PROOF.json`，同时核对允许变化的字段和每个计划值是否确实保存。

大批量可用 `workflow.py prepare-result-columns --baseline LATEST.json --writebacks PLAN.json --output COLUMNS.json` 生成完整列值，保留所有非本批单元格。代理在原生表格中逐列选中确切表头并查看蓝色选择截图后，才调用 `feishu-result-column`；配置包括 `columnKey/column/targetTableId/baselinePath/baselineSha256/columnPlanPath/columnPlanSha256/selectedHeaderEvidence`，值从已固定摘要的列计划读取。仅允许 E/F/G/J/AG，不能粘贴跨越附件等字段的连续区域，不发送 Ctrl+A。多行说明通过 HTML 单元格保留。粘贴后仍须整表导出并运行 `verify-results`，不能用粘贴提示代替保存证明。原生列选择不明确时使用逐记录入口。

飞书回填失败时单独重试回填，不能重新发淘宝请求。每项保留来源/包摘要、BM 修订、账号/AppID/code、既有授权、版本意图、平台回读和飞书回执。报告未审核、待人工协议和真实失败；不能把脚本运行结束当作全部上架成功。

完成后用 `report_batch.py --batch BATCH --verified-writebacks PLAN.json --verification EXPORT_PROOF.json` 输出无凭据 CSV 和按实际阶段计数的 JSON；它要求回填 proof 与计划 SHA256 一致，不把历史回填当成本轮成功。

## 离线验证

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s .test -v
node --check scripts/browser.mjs
node --check scripts/feishu.mjs
node --check scripts/taobao.mjs
```

单元测试仅覆盖契约、归一规则和防重提交门槛。实际页面操作仍须在获授权批次逐阶段回读；未经实操的 UI 分支不能宣称已验证。
