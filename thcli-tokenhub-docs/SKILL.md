---
name: thcli-tokenhub-docs
description: 提供腾讯云大模型服务平台 TokenHub 官方产品文档的索引地图，以及把 TokenHub 模型接入各类 AI 工具/Agent（WorkBuddy、Claude Code、Cursor、CodeBuddy Code、OpenCode、Cline、OpenClaw、Hermes Agent、Kilo Code、Roo Code、Codex 等）的完整配置模板。**同时区分国内站（cloud.tencent.com，域名 tokenhub.tencentmaas.com）与国际站（tencentcloud.com，域名 tokenhub-intl.tencentcloudmaas.com）**——两站的 Base URL、控制台地址、部分可用模型均不同，绝不能用国内站配置套给国际站用户，反之亦然。当用户用自然语言表达"帮我把 TokenHub 的 xxx 模型接入 workbuddy/claude code/cursor 等"这类接入配置需求时使用；也在用户询问 TokenHub 的功能、计费、API Key 管理、Token Plan、模型列表等任何官方文档涉及的问题、且需要快速定位到对应文档或直接给出答案（而不是让用户自己翻文档）时使用。
agent_created: true
---

# 腾讯云 TokenHub 文档助手（由 thcli 分发）

> 本 skill 由 thcli 通过 `thcli +connect` 分发到本地 Agent。**它面向的是"把腾讯云 TokenHub 模型接入其他 AI 工具"的场景**（如 Cursor / Claude Code / Codex 等），与同批分发的其它 `thcli-*` skill（教 Agent 使用 thcli 命令）职责互补。
>
> **快照时间与实时校验**：本 skill 的 `references/*.md` 是编写时的文档快照。文档更新频繁（尤其模型清单、价格、下线时间），Agent 遇到时间敏感信息或用户报的模型 ID 查不到时，应主动用 `WebFetch` 抓取 `references/doc-index.md` 中对应站点、对应文档 URL 的最新内容再回答，不要仅凭快照作答。

腾讯云大模型服务平台 TokenHub 的官方产品文档索引与 AI 工具接入配置助手。TokenHub **有两个独立站点**，文档、控制台、API 域名均不同：

| | 国内站 | 国际站 |
|---|---|---|
| 文档根目录 | `https://cloud.tencent.com/document/product/1823` | `https://www.tencentcloud.com/document/product/1300` |
| 控制台 | `https://console.cloud.tencent.com/tokenhub/` | `https://console.tencentcloud.com/tokenhub/` |
| 数据面 API Base URL | `https://tokenhub.tencentmaas.com/v1` | `https://tokenhub-intl.tencentcloudmaas.com/v1` |

解决两类问题：**帮用户把模型接入某个 AI 工具/Agent**，以及**帮用户在文档中快速找到答案**，避免用户手动翻阅整份文档。**两类任务都必须先确定用户是国内站还是国际站用户**，见下方「能力零」。

## 能力零：判断站点（国内站 / 国际站）—— 必须先做这一步

在执行能力一或能力二之前，先判断用户使用的是国内站还是国际站：

1. 若用户已明确说明（如"国际站""International""海外账号""codebuddy.ai 登录"等关键词），直接采用。
2. 若用户提到了具体域名（`tokenhub.tencentmaas.com` 为国内站；`tokenhub-intl.tencentcloudmaas.com` 为国际站）或控制台地址（`console.cloud.tencent.com` 国内 / `console.tencentcloud.com` 国际），据此判断。
3. 若无法从上下文判断（多数情况下如此，因为大部分用户默认使用国内站且不会主动说明），**直接问用户**："您使用的是腾讯云 TokenHub 国内站还是国际站？（可以看您控制台的网址：`console.cloud.tencent.com` 是国内站，`console.tencentcloud.com` 是国际站）"。不要默认按国内站处理后再让用户自己发现错了——两站配置字段值不同，配错会导致用户接入失败或产生跨站调用错误。
4. 确定站点后，后续所有查阅 `references/` 文件、给出的域名/URL，都必须切换到对应站点的那一套，不能混用。

## 能力一：把腾讯云 TokenHub 模型接入 AI 工具（配置生成）

触发示例："帮我把腾讯云 TokenHub 的 hy3、deepseek-v4-pro 接入 workbuddy"、"把这个模型接到 Claude Code 里"、"Cursor 怎么配腾讯云 TokenHub 的模型"。

按以下顺序执行（前提：已完成「能力零」确定好站点）：

1. **识别目标工具**。用户可能用简称、别名或拼错的名字表达，按下表归一化到标准工具名：

   | 用户可能的说法 | 标准工具名 | 配置方式 |
   |---|---|---|
   | workbuddy / 工作伙伴 / 工作台 | WorkBuddy | GUI 设置界面 |
   | claude code / cc / claude | Claude Code | `settings.json` 环境变量 |
   | cursor | Cursor | GUI 设置界面 |
   | codebuddy / codebuddy code / cb | CodeBuddy Code | `models.json` |
   | opencode | OpenCode | GUI 或 `opencode.json` |
   | cline | Cline | GUI 设置界面 |
   | openclaw | OpenClaw | 终端交互式向导 `openclaw onboard` |
   | hermes / hermes agent | Hermes Agent | 终端交互式向导 `hermes setup` |
   | kilo / kilo code | Kilo Code | GUI 设置界面 |
   | roo / roo code | Roo Code | GUI 设置界面 |
   | codex | Codex | `config.toml` + 环境变量注入 |

   若用户提到的工具不在此表中，明确告知"该工具的接入方式未在本 Skill 中收录，需要先到对应站点的文档目录（国内站 `https://cloud.tencent.com/document/product/1823`「接入 AI 工具」分类 / 国际站 `https://www.tencentcloud.com/document/product/1300`「AI Tools Integration」分类）下确认是否有官方文档"，不要凭空编造配置字段。

2. **确定要接入的模型 ID**。读取 `references/model-quick-list.md`，按用户确定的站点查对应表格，找到用户描述对应的 `model（调用参数）` 值（例如用户说"混元3"要对应到 `hy3`，"DeepSeek V4 Pro"对应 `deepseek-v4-pro`）。
   - **国内站与国际站的模型清单不完全相同**，同一个模型 ID 在两站可能都支持，但也存在只在一个站点提供的模型（如国内站的 `qwen3.5-flash`/`qwen3.5-plus`、国际站的 `deepseek-v3.2`、`minimax-m2.5`；国际站的图片/视频/3D生成模型种类明显少于国内站）。用户要接入的模型若在对应站点的表里查不到，不要假设"另一站有所以这站应该也有"，必须用 `WebFetch` 重新抓取该站点的模型列表文档确认（国内站 `https://cloud.tencent.com/document/product/1823/130051`；国际站 `https://www.tencentcloud.com/document/product/1300/78934`）。
   - 若用户报的模型名找不到，或怀疑该模型已改名/下线，同样重新抓取确认，不要猜测拼写。
   - 模型 ID 是区分大小写、含短横线的精确字符串，直接照抄，不要意译或简化。

3. **确认 API Key**。
   - 若用户已提供 API Key，直接使用。
   - 若用户未提供，先问用户是否已有 API Key；没有的话告知需前往对应站点的 API Key 管理页面创建（国内站 `console.cloud.tencent.com/tokenhub/apikey` / 国际站 `console.tencentcloud.com/tokenhub/apikey`），并提醒：**如果 API Key 的可访问范围选择"限定范围"，必须确保勾选了本次要接入的模型**，否则配置完成后调用会报权限错误。
   - **两站的 API Key 互相不通用**——国内站创建的 Key 不能用于国际站域名调用，反之亦然。若用户说"用之前配置过的 Key"，要先确认那把 Key 是在哪个站点创建的。
   - 不要在对话记录、日志、其他配置文件中重复回显完整的 API Key 明文，写入目标配置文件即可。

4. **生成/写入配置**。打开 `references/ai-tool-configs.md`，找到目标工具对应的小节，**该小节内会分别给出「国内站」和「国际站」两套配置**，按已确定的站点选用对应那一套的**配置文件路径**（区分 macOS/Linux/Windows）与**配置内容模板**，把模型 ID 与 API Key 代入模板：
   - 若目标工具是"配置文件型"（Claude Code / CodeBuddy Code / OpenCode CLI 版 / Codex）：直接用文件读写工具创建或更新对应路径的配置文件；若文件已存在且包含其他配置，采用「合并追加」而非整体覆盖，保留用户原有的其他字段。
   - 若目标工具是"GUI 设置型"（WorkBuddy / Cursor / Cline / Kilo Code / Roo Code / OpenCode 桌面端）：无法用工具直接改，按模板逐字段列出，指导用户在界面里怎么填。
   - 若目标工具是"终端交互向导型"（OpenClaw / Hermes Agent）：给出完整的交互式命令与每一步终端提示对应该填的值；OpenClaw 还提供非交互式命令，若用户是自动化场景优先给非交互式命令。
   - **两站配置的差异不只是域名字符串替换**，个别工具的字段格式也不同（例如 Codex 的 `base_url`：国内站带 `/v1` 后缀，国际站不带；OpenClaw/Hermes Agent 终端向导里国内站/国际站的分步提示文案也略有差异），必须按 `ai-tool-configs.md` 里该站点小节的实际内容操作，不要自行"推理"出一个看似合理但未经验证的域名拼接结果。

5. **给出验证方式**。参考 `references/ai-tool-configs.md` 每个工具小节末尾的验证步骤（如 Claude Code 的 `/status`、OpenClaw 的 `openclaw models list --provider tencent-tokenhub`），告知用户如何确认接入成功，注意验证步骤里出现的域名/字段也要对应站点。

**通用注意事项（适用于所有工具）**：
- 鉴权方式统一是 Bearer Token（`Authorization: Bearer <API Key>`），兼容 OpenAI API 协议，两站一致。
- 不要在没有官方文档依据的情况下，为未在 `references/ai-tool-configs.md` 收录的工具/站点组合编造配置字段名或接口路径。

## 能力二：文档检索与快速问答

触发示例：任何关于腾讯云 TokenHub 功能、计费、Token Plan、API Key 规则等的提问。

1. 先完成「能力零」确定站点，再看 `references/doc-index.md` 中对应站点的文档目录索引（该文件里国内站、国际站的索引是分开列的），定位问题所属的文档标题和 URL。
2. 若 `references/` 下已有覆盖该主题的摘要文件（如 API Key 规则、模型列表速查），优先直接引用对应站点的摘要回答，减少一次网络请求；**不要用国内站的摘要回答国际站用户的问题**，即使内容看起来大体相似（例如额度限制的周期规则文字表述几乎一致，但具体控制台入口、页面用词、计费货币单位等可能不同）。
3. 若摘要不覆盖细节，或用户问题涉及**易变信息**（模型是否已下线、价格、额度上限、具体操作步骤截图位置等），用 `WebFetch` 重新抓取 `references/doc-index.md` 中对应站点、对应 URL 的最新内容再回答，不要仅凭 references 里的旧摘要作答。
4. 若用户没有指明站点、问题本身也和站点无关（比如纯概念性问题"什么是 Token Plan"），可以先按国内站文档回答，但**若问题涉及具体数值、URL、模型清单等站点相关内容，必须先确认站点再回答**，避免文档张冠李戴。
5. 回答时附上文档原文链接（注意链接本身就已经区分了站点，不要把国内站链接发给国际站用户），方便用户自行跳转核实。

## 重要原则

- **不编造**：模型 ID、配置字段、API 路径、价格、额度等具体数值只能来自官方文档（本 Skill 的 references 文件或实时 WebFetch 抓取的页面），不确定时明确告知用户"需要核实"，不要给出看似合理但未经验证的答案。
- **不跨站套用**：国内站和国际站是两套独立的产品文档、控制台、API 域名和（部分）模型清单。任何时候都不能假设"国内站是这样，国际站应该也差不多"，必须先看该站点自己的文档/references 内容，找不到就重新抓取确认，而不是拿另一站的内容改个域名就当作答案。
- **文档会更新**：腾讯云 TokenHub 处于活跃迭代中，模型会上线/下线（文档里常标注"YYYY-MM-DD下线"），文档路径也可能调整。`references/` 下的内容是编写本 Skill 时的快照，遇到时间敏感问题优先重新抓取确认。
- **API Key 安全**：协助用户配置时不要把明文 API Key 写入非目标配置文件之外的任何地方（如日志、注释、多余的中间文件）。
