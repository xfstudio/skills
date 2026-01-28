# Claude Skills 技能集合

这是一个 Claude Code Skills 集合，为 AI 编程助手提供专业化的技能扩展。

---

## 快速安装

```bash
# 一键安装所有 skills
npx skills add xfstudio/skills

# 安装单个 skill
npx skills add xfstudio/skills --skill skill-name

# 更新已安装的 skills
npx skills update xfstudio/skills
```

---


## Skills 列表 (317 个)

> 每个 skill 的功能与触发条件见下表，全部为中文说明。

| Skill 名称 | 功能与触发条件 |
|------------|----------------|
| `3d-web-experience` | 功能：Web 3D 体验：Three.js、R3F、Spline、WebGL、互动场景、产品配置器、作品集 触发：用户提及 3D 网站、three.js、WebGL、react three fiber、3D 体验 |
| `ab-test-setup` | 功能：设计并实施 A/B 测试与实验，保证统计严谨、可执行 触发：用户要规划/设计/实施 A/B 测试、分流实验、假设检验，或提及 实验、变异文案、多变量测试 |
| `active-directory-attacks` | 功能：AD 域渗透：Kerberoasting、DCSync、Pass-the-Hash、BloodHound、金/银票据等 触发：用户提及 攻击 AD、Kerberoasting、DCSync、域渗透 |
| `address-github-comments` | 功能：用 gh CLI 处理 GitHub PR 的评审或 issue 评论 触发：需要回复 PR 评审或 issue 评论时 |
| `advanced-evaluation` | 功能：LLM-as-judge、模型输出对比、评估准则、缓解评估偏差、自动化质量评估 触发：用户提及 实现 LLM 评判、对比模型输出、评估准则、评估流水线 |
| `agent-evaluation` | 功能：智能体测试与基准：行为测试、能力评估、可靠性指标、生产监控 触发：用户提及 agent 测试、评估智能体、基准测试、智能体可靠性 |
| `agent-manager-skill` | 功能：通过 tmux 管理多个本地 CLI 智能体：启停、监控、分配、cron 调度 触发：用户要管理多智能体、tmux 调度时 |
| `agent-memory-mcp` | 功能：智能体混合记忆：架构/模式/决策的持久化、可检索知识管理 触发：用户要智能体记忆、MCP 记忆时 |
| `agent-memory-systems` | 功能：智能体记忆架构：短期上下文、长期向量库、分块与检索 触发：用户要设计/实现智能体记忆、跨会话持久化时 |
| `agent-tool-builder` | 功能：智能体工具设计：JSON Schema、描述撰写、校验、MCP 标准 触发：用户要设计 agent 工具、MCP 工具时 |
| `ai-agents-architect` | 功能：设计与构建自主 AI 智能体：工具使用、记忆、规划、多智能体编排 触发：用户提及 构建 agent、AI 智能体、工具调用、function calling |
| `ai-product` | 功能：LLM 集成、RAG、可扩展提示工程、AI UX、成本优化 触发：用户做 AI 产品、关键词/文件/代码模式匹配时 |
| `ai-wrapper-product` | 功能：用 AI API 做专注型付费工具：提示工程、成本与限流、可防御 AI 业务 触发：用户提及 AI wrapper、GPT 产品、AI 工具、AI SaaS |
| `algolia-search` | 功能：Algolia 接入、索引策略、React InstantSearch、相关性调优 触发：用户要加搜索、algolia、instantsearch、search api |
| `algorithmic-art` | 功能：用 p5.js 做算法艺术：种子随机、互动参数、粒子/流场 触发：用户要 代码生成艺术、生成艺术、算法艺术、粒子系统 |
| `analytics-tracking` | 功能：配置、改进与审计分析埋点与转化追踪 触发：用户要搭建/改进 埋点、GA4、Google Analytics、转化追踪、事件追踪、UTM、GTM、追踪计划 |
| `api-documentation-generator` | 功能：从代码生成 API 文档：端点、参数、示例、最佳实践 触发：用户要生成 API 文档时 |
| `api-fuzzing-bug-bounty` | 功能：API 安全测试、模糊测试、IDOR、REST/GraphQL 渗透 触发：用户提及 API 安全、fuzz API、IDOR、API 渗透、bug bounty |
| `api-patterns` | 功能：API 设计：REST vs GraphQL vs tRPC、响应格式、版本、分页 触发：用户做 API 设计决策时 |
| `api-security-best-practices` | 功能：安全 API 设计：鉴权、授权、校验、限流、防常见漏洞 触发：用户要实现安全 API 时 |
| `app-builder` | 功能：从自然语言构建全栈应用：确定项目类型、技术栈、协调智能体 触发：用户要构建完整应用时 |
| `app-store-optimization` | 功能：ASO：研究与优化 App Store / Google Play 表现 触发：用户做 ASO、应用商店优化时 |
| `architecture` | 功能：架构决策：需求分析、权衡、ADR 文档 触发：用户做架构决策、分析系统设计时 |
| `artifacts-builder` | 功能：用 React/Tailwind/shadcn 创建多组件 claude.ai HTML 制品 触发：复杂制品需状态、路由、shadcn 时 |
| `autonomous-agent-patterns` | 功能：自主编码智能体模式：工具集成、权限、浏览器自动化、人机回环 触发：用户构建 AI 智能体、设计工具 API、权限系统时 |
| `autonomous-agents` | 功能：自主智能体：目标分解、ReAct/Plan-Execute、反思、生产可靠性 触发：用户要设计/实现自主智能体时 |
| `avalonia-layout-zafiro` | 功能：Avalonia + Zafiro 布局：共享样式、通用组件、减少 XAML 重复 触发：用户做 Avalonia UI 布局时 |
| `avalonia-viewmodels-zafiro` | 功能：Avalonia ViewModel 与向导模式：Zafiro、ReactiveUI 触发：用户做 Avalonia ViewModel/向导时 |
| `avalonia-zafiro-development` | 功能：Avalonia + Zafiro 开发约定与行为规则 触发：用户用 Zafiro 开发 Avalonia 时 |
| `aws-penetration-testing` | 功能：AWS 渗透：IAM 枚举、S3、SSRF、Lambda 等 触发：用户提及 pentest AWS、AWS 安全、IAM 枚举、云渗透 |
| `aws-serverless` | 功能：AWS 无服务：Lambda、API Gateway、DynamoDB、SQS/SNS、SAM/CDK、冷启动 触发：用户做 AWS 无服务应用时 |
| `azure-functions` | 功能：Azure Functions：独立 worker、Durable、冷启动、.NET/Python/Node 触发：用户提及 azure function、durable functions、azure serverless |
| `backend-dev-guidelines` | 功能：Node.js + Express + TS 微服务后端规范：分层、BaseController、Prisma、Zod、Sentry 触发：用户做 Express/TS 后端时 |
| `backend-patterns` | 功能：后端模式：API 设计、数据库优化、Node/Express/Next API 触发：用户做后端架构时 |
| `baoyu-article-illustrator` | 功能：文章配图：分析结构、识别位点、类型×风格二维配图 触发：用户要 为文章配图、插图、生成配图 |
| `baoyu-comic` | 功能：知识/教育漫画：多风格、分镜、顺序图生成 触发：用户要 知识漫画、教育漫画、传记漫画、教程漫画 |
| `baoyu-compress-image` | 功能：图片压缩为 WebP 或 PNG，自动选工具 触发：用户要 压缩图片、转 webp、优化图片 |
| `baoyu-cover-image` | 功能：文章封面图：类型/调色/渲染/文案/情绪，多比例 触发：用户要 生成封面、做封面、封面图 |
| `baoyu-danger-gemini-web` | 功能：通过 Gemini Web API 生成图文；支持多轮、视觉输入 触发：用户要 Gemini 生成图/文、或其它技能需图生后端时 |
| `baoyu-danger-x-to-markdown` | 功能：X 推文/文章转 Markdown（YAML front matter），逆向 API 触发：用户提及 X to markdown、推文转 md、保存推文、x.com 链接 |
| `baoyu-image-gen` | 功能：OpenAI/Google 图生：文生图、参考图、比例、并行生成 触发：用户要 生成/创建/画 图片 |
| `baoyu-infographic` | 功能：信息图：20 布局×17 风格，分析内容、推荐组合、出图 触发：用户要 信息图、可视化、视觉摘要 |
| `baoyu-post-to-wechat` | 功能：通过 Chrome CDP 向微信公众号发布内容，支持文章与图文 触发：用户提及 发布公众号、post to wechat、微信公众号、图文/文章 |
| `baoyu-post-to-x` | 功能：向 X 发帖与 X Articles；CDP 绕过反自动化 触发：用户要 post to X、发推、发到 Twitter |
| `baoyu-slide-deck` | 功能：从内容生成幻灯片图片：大纲、风格、单页图 触发：用户要 做幻灯片、presentation、deck、PPT |
| `baoyu-url-to-markdown` | 功能：抓取 URL 转 Markdown（Chrome CDP）；自动捕获或等用户信号 触发：用户要保存网页为 md 时 |
| `baoyu-xhs-images` | 功能：小红书信息图系列：9 风格×6 布局，1–10 张 触发：用户提及 小红书图片、XHS、RedNote、小红书种草 |
| `bash-linux` | 功能：Bash/Linux 终端：命令、管道、错误处理、脚本 触发：用户在 macOS/Linux 上工作时 |
| `bdi-mental-states` | 功能：BDI 架构：信念-愿望-意图、心智状态建模、RDF→信念 触发：用户提及 智能体心智、BDI、认知智能体 |
| `behavioral-modes` | 功能：AI 工作模式：头脑风暴、实现、调试、评审、教学、交付、编排 触发：用户要按任务类型切换行为时 |
| `blockrun` | 功能：调用 Claude 缺失能力：图生、实时 X 数据、外部模型 触发：用户要 blockrun、grok、gpt、dall-e、deepseek 等时 |
| `brainstorming` | 功能：创意/构建前结构化头脑风暴与验证 触发：用户要做 功能、组件、架构、行为变更 等前使用 |
| `brand-guidelines` | 功能：Anthropic 品牌色与排版，用于制品 触发：用户要品牌色、样式指南、视觉规范时 |
| `broken-authentication` | 功能：认证与会话安全测试：凭证 stuffing、会话固定、绕过 触发：用户要测试 认证漏洞、会话管理、密码策略 时 |
| `browser-automation` | 功能：浏览器自动化：Playwright/Puppeteer、选择器、等待、反检测 触发：用户要做 自动化、爬虫、端到端测试、agent 控浏览器 时 |
| `browser-extension-builder` | 功能：浏览器扩展：Chrome/Firefox、Manifest v3、内容脚本、上架 触发：用户提及 浏览器扩展、chrome extension、manifest v3 |
| `building-native-ui` | 功能：Expo Router 构建原生 UI：基础、样式、组件、导航、动效 触发：用户用 Expo 做原生 UI 时 |
| `bullmq-specialist` | 功能：BullMQ：Redis 任务队列、后台任务、可靠异步 触发：用户提及 bullmq、redis 队列、background job |
| `bun-development` | 功能：Bun 运行时：包管理、打包、测试、从 Node 迁移 触发：用户用 Bun、优化 JS/TS 开发、从 Node 迁移时 |
| `burp-suite-testing` | 功能：Burp 抓包、改请求、扫描、Repeater、代理配置 触发：用户要 拦截 HTTP、Burp 测试、漏洞扫描、代理 时 |
| `busybox-on-windows` | 功能：在 Windows 用 BusyBox 跑常见 UNIX 命令行工具 触发：用户在 Windows 上需要 UNIX 工具时 |
| `canvas-design` | 功能：用设计哲学创作 .png/.pdf 视觉作品；原创不抄袭 触发：用户要 海报、艺术品、静态视觉 时 |
| `changelog-generator` | 功能：从 git 提交自动生成用户向 changelog 触发：用户要生成 changelog、发布说明时 |
| `ciphey` | 功能：解密/解码：Base64、Caesar、Vigenère、XOR、Morse、哈希等 50+ 类型 触发：用户说 解密、decode、crack、破解密码 或提供密文时 |
| `claude-code-guide` | 功能：Claude Code 使用：配置、提示策略、调试、最佳实践 触发：用户要高效使用 Claude Code 时 |
| `clean-code` | 功能：简洁、直接、少过度设计、少冗余注释的编码标准 触发：用户要代码规范时 |
| `clerk-auth` | 功能：Clerk 鉴权：中间件、组织、Webhook、用户同步 触发：用户要 加鉴权、clerk、登录注册 时 |
| `clickhouse-io` | 功能：ClickHouse：查询优化、分析、数据工程 触发：用户做 ClickHouse、分析型库时 |
| `cloud-penetration-testing` | 功能：云渗透：AWS/Azure/GCP、O365、云配置、密钥提取 触发：用户要 云渗透、云安全评估、云审计 时 |
| `code-review-checklist` | 功能：代码评审检查清单：功能、安全、性能、可维护性 触发：用户做 Code Review 时 |
| `codex-review` | 功能：专业评审 + 自动 CHANGELOG，对接 Codex AI 触发：用户要 Codex 评审时 |
| `coding-standards` | 功能：TS/JS/React/Node 通用编码标准与模式 触发：用户要统一编码规范时 |
| `competitive-ads-extractor` | 功能：从广告库提取竞品广告，分析文案、创意、打法 触发：用户要分析竞品广告、Facebook/LinkedIn 广告库时 |
| `competitor-alternatives` | 功能：创建竞品对比或替代方案页，用于 SEO 与销售赋能 触发：用户要做 替代页、vs 页、竞品对比、对比页、竞品落地页 |
| `computer-use-agents` | 功能：像人一样操作电脑的智能体：看屏、光标、点击、输入；沙箱与安全 触发：用户提及 computer use、桌面自动化 agent、屏幕控制 AI |
| `concise-planning` | 功能：为编码任务生成清晰、可执行、原子化清单 触发：用户要 计划、规划 编码任务时 |
| `connect` | 功能：连接 Gmail、Slack、GitHub、Notion 等，发邮件、建 issue、更新库 触发：用户要 Claude 跨应用执行操作时 |
| `content-creator` | 功能：SEO 营销内容、品牌声线、内容框架、社媒模板 触发：用户要 写博客、社媒、品牌声线、SEO、内容日历 时 |
| `content-research-writer` | 功能：调研、引用、改钩子、迭代大纲、逐段反馈，协作写作 触发：用户要高质量内容写作时 |
| `content-strategy` | 功能：内容策略：写什么、覆盖哪些话题 触发：用户提及 内容策略、写什么、内容点子、博客策略、选题 时 |
| `context-compression` | 功能：上下文压缩、对话摘要、 compaction、降 token、长会话 触发：用户要 压缩 context、摘要历史、减 token 时 |
| `context-degradation` | 功能：诊断 context 问题、lost-in-middle、context 污染、性能下降 触发：用户要 排查 context、修复 agent 失败 时 |
| `context-fundamentals` | 功能：Context 基础：窗口、组件、注意力、渐进披露、预算 触发：用户要 理解 context、设计 agent 架构、调试 context 时 |
| `context-optimization` | 功能：优化 context、降成本、KV 缓存、分区、扩展有效容量 触发：用户要 优化 context、降 token 成本 时 |
| `context-window-management` | 功能：Context 管理：摘要、裁剪、路由、避免腐化 触发：用户提及 context 窗口、token 限制、context 工程 |
| `context7-auto-research` | 功能：通过 Context7 API 自动拉取库/框架最新文档 触发：用户要查库文档、Context7 时 |
| `continuous-learning` | 功能：从 Claude Code 会话提取可复用模式，存为技能 触发：用户要持续学习、沉淀技能时 |
| `conversation-memory` | 功能：对话记忆：短期、长期、实体记忆 触发：用户提及 对话记忆、记住、持久记忆、聊天历史 时 |
| `copy-editing` | 功能：系统性编辑、润色与改进现有营销文案 触发：用户要 编辑/审阅/改进 文案，或提及 校对、润色、文案扫一遍 |
| `copywriting` | 功能：撰写、重写与优化营销文案（首页、落地页、定价页、功能页等） 触发：用户要 写文案、改文案、重写页面、营销文案、标题、CTA 等；邮件见 email-sequence，弹窗见 popup-cro |
| `core-components` | 功能：核心组件库与设计系统、design tokens 触发：用户构建 UI、用 design tokens 时 |
| `crewai` | 功能：CrewAI 多智能体：角色与目标、任务、编排、顺序/层级/并行、记忆与 Flow 触发：用户提及 crewai、多智能体团队、agent 角色 |
| `d3-viz` | 功能：d3.js 交互可视化：图表、网络图、地理、自定义 SVG 触发：用户要做 自定义图表、d3、复杂可视化 时 |
| `daily-news-report` | 功能：按预设 URL 抓取、筛技术信息、生成每日 Markdown 报告 触发：用户要每日技术报告时 |
| `database-design` | 功能：库设计：Schema、索引、ORM、无服务库 触发：用户做库设计决策时 |
| `deployment-procedures` | 功能：生产部署：安全流程、回滚、验证 触发：用户做部署决策时 |
| `design-orchestration` | 功能：编排设计流程：头脑风暴→多智能体评审→可执行 触发：需要编排设计、避免过早实现与未评审高风险设计时 |
| `developer-growth-analysis` | 功能：分析 Claude Code 会话，识别模式与短板，推 HackerNews 学习资源，Slack 成长报告 触发：用户要成长分析、学习建议时 |
| `discord-bot-architect` | 功能：Discord 机器人：Discord.js/Pycord、网关、斜杠命令、限流、分片 触发：用户要做 Discord 机器人时 |
| `dispatching-parallel-agents` | 功能：派发 2+ 个无依赖、可并行的任务 触发：用户有多任务、无共享状态/顺序依赖时 |
| `doc-coauthoring` | 功能：协作写文档：提案、技术规格、决策文档，迭代与验证 触发：用户要 写文档、提案、规格、决策文档 时 |
| `docker-expert` | 功能：Docker：多阶段构建、镜像优化、安全、Compose、生产 触发：用户要 Dockerfile、容器、镜像、编排 时 |
| `documentation-templates` | 功能：文档模板：README、API 文档、注释、AI 友好文档 触发：用户写文档时 |
| `docx-official` | 功能：Word 文档：创建、编辑、修订、批注、格式保留、提取 触发：用户要处理 .docx 时 |
| `domain-name-brainstormer` | 功能：生成域名创意并检查多 TLD 可用性 触发：用户要起域名时 |
| `email-sequence` | 功能：邮件序列、 drip、自动化邮件、生命周期邮件 触发：用户提及 邮件序列、drip、欢迎邮件、再激活、邮件自动化 时 |
| `email-systems` | 功能：邮件系统：事务邮件、营销自动化、送达率、基础设施 触发：用户做邮件系统、营销邮件时 |
| `environment-setup-guide` | 功能：开发环境搭建：工具、依赖、配置 触发：用户要配环境时 |
| `ethical-hacking-methodology` | 功能：道德黑客与渗透测试方法论、侦察、扫描、利用、报告 触发：用户要 学渗透、渗透生命周期、写渗透报告 时 |
| `eval-harness` | 功能：评估与测试 harness 相关能力 触发：用户提及 eval harness、评估框架时 |
| `evaluation` | 功能：智能体评估、测试框架、LLM-as-judge、质量门控 触发：用户要 评估 agent、建测试框架、质量评估 时 |
| `exa-search` | 功能：Exa API：语义搜索、相似内容、结构化调研 触发：用户要做语义搜索、调研时 |
| `executing-plans` | 功能：在独立会话中执行已有实现计划，带评审检查点 触发：用户有书面计划要执行时 |
| `expo-api-routes` | 功能：Expo Router + EAS Hosting 下的 API 路由 触发：用户做 Expo API 路由时 |
| `expo-cicd-workflows` | 功能：EAS workflow YAML、CI/CD、构建与部署自动化 触发：用户提及 .eas/workflows、EAS CI/CD 时 |
| `expo-deployment` | 功能：Expo 上架 App Store / Play Store、Web、API 路由 触发：用户要发布 Expo 应用时 |
| `expo-dev-client` | 功能：构建与分发 Expo 开发版（本地或 TestFlight） 触发：用户要做 Expo 开发客户端时 |
| `expo-tailwind-setup` | 功能：Expo 中配置 Tailwind v4、react-native-css、NativeWind v5 触发：用户要在 Expo 用 Tailwind 时 |
| `file-organizer` | 功能：智能整理文件与目录：去重、建议结构 触发：用户要 整理目录、整理下载、去重、调整项目结构 时 |
| `file-path-traversal` | 功能：目录遍历、路径穿越、LFI 测试与利用 触发：用户要 测试目录遍历、LFI、读任意文件 时 |
| `file-uploads` | 功能：文件上传与云存储：S3、R2、预签名、分片、大文件 触发：用户要 文件上传、S3、R2、presigned、multipart 时 |
| `filesystem-context` | 功能：Context 卸载到文件、动态发现、文件型记忆、JIT 加载 触发：用户要 上下文落盘、agent 草稿、减 context 膨胀 时 |
| `find-skills` | 功能：发现与安装 agent 技能 触发：用户问「怎么做 X」「有没有 skill 可以…」时 |
| `finishing-a-development-branch` | 功能：功能完成、测试通过后，决定如何合并/PR/收尾 触发：用户完成开发要集成时 |
| `firebase` | 功能：Firebase：Auth、Firestore、Realtime、Functions、Hosting、安全规则 触发：用户做 Firebase 后端时 |
| `firecrawl-scraper` | 功能：Firecrawl：深度爬取、截图、PDF 解析、站 crawling 触发：用户要用 Firecrawl 爬站时 |
| `form-cro` | 功能：优化非注册类表单转化：线索、联系、演示、调查、结账等 触发：用户要优化 表单、线索转化、表单摩擦；注册见 signup-flow-cro |
| `free-tool-strategy` | 功能：规划、评估或搭建用于获客/SEO/品牌的免费工具 触发：用户提及 工程即营销、免费工具、营销工具、计算器、生成器、获客工具 |
| `frontend-design` | 功能：高水准前端：美学、工艺、非通用视觉 触发：用户构建/美化 Web UI、组件、仪表盘时 |
| `frontend-dev-guidelines` | 功能：React+TS 前端规范：Suspense、懒加载、MUI v7、TanStack Router 触发：用户做现代 React 前端时 |
| `frontend-patterns` | 功能：前端模式：React、Next、状态、性能、UI 实践 触发：用户做前端架构时 |
| `game-development` | 功能：游戏开发编排，按平台路由到对应技能 触发：用户做游戏开发时 |
| `gcp-cloud-run` | 功能：GCP 无服务：Cloud Run、Cloud Run Functions、Pub/Sub、冷启动 触发：用户做 GCP 无服务时 |
| `geo-fundamentals` | 功能：生成式引擎优化 GEO：ChatGPT、Claude、Perplexity 等 触发：用户做 AI 搜索引擎优化时 |
| `git-pushing` | 功能：git add/commit/push，Conventional Commits 触发：用户要 提交推送、push、保存并推送 时 |
| `github-workflow-automation` | 功能：GitHub 自动化：PR 评审、issue 分类、CI/CD、Git 操作 触发：用户要 自动化 GitHub、PR 评审、Actions、issue 分类 时 |
| `graphql` | 功能：GraphQL：Schema、resolver、DataLoader、联邦、Apollo 触发：用户做 GraphQL 时 |
| `hosted-agents` | 功能：托管/后台智能体、沙箱执行、多人在线 agent、Modal 等 触发：用户要 后台 agent、托管编码 agent、沙箱 时 |
| `html-injection-testing` | 功能：HTML 注入测试与利用 触发：用户要 测试 HTML 注入、篡改页面 时 |
| `hubspot-integration` | 功能：HubSpot CRM：OAuth、对象、关联、批操作、Webhook、Node/Python 触发：用户提及 hubspot、hubspot api、crm、contacts api |
| `i18n-localization` | 功能：国际化与本地化：硬编码检测、译文、locale、RTL 触发：用户做 i18n 时 |
| `idor-testing` | 功能：IDOR 测试：越权、枚举 ID、访问他人数据 触发：用户要 测 IDOR、越权、Broken AC 时 |
| `image-enhancer` | 功能：提升图片质量：分辨率、锐度、清晰度，适合截图、文档、社媒 触发：用户要增强截图/图片时 |
| `inngest` | 功能：Inngest：无服务优先后台任务、事件驱动、持久执行 触发：用户提及 inngest、serverless 后台、step function、durable execution |
| `interactive-portfolio` | 功能：作品集：能拿 offer/客户的开发/设计/创意作品站 触发：用户要 portfolio、个人站、展示作品 时 |
| `internal-comms` | 功能：内部沟通：周报、领导更新、 newsletters、FAQ、事故报告等 触发：用户要写内部沟通时 |
| `invoice-organizer` | 功能：自动整理发票/收据：读取、提取、重命名、分类，便于报税 触发：用户要整理发票收据时 |
| `javascript-mastery` | 功能：JS 精要：33+ 概念，从基础到 async/函数式 触发：用户要 讲 JS、调试 JS、教 JS 时 |
| `kaizen` | 功能：持续改进、防呆、标准化 触发：用户要 改进代码、重构、流程改进 时 |
| `langfuse` | 功能：Langfuse：LLM 可观测、追踪、提示管理、评估、LangChain/LlamaIndex 触发：用户提及 langfuse、llm 可观测、prompt 管理、llm 评估 |
| `langgraph` | 功能：LangGraph：有状态多角色 AI 应用、图、检查点、人机回环、ReAct 触发：用户提及 langgraph、多角色 agent、状态管理 |
| `langsmith-fetch` | 功能：从 LangSmith 拉取 LangChain/LangGraph 执行 trace 调试 触发：用户要 调试 agent、查 tool 调用、内存 时；需 langsmith-fetch CLI |
| `last30days` | 功能：Reddit + X + Web 近 30 天调研某话题，产出可直接用的 prompt 触发：用户要近期热点、某领域近期内容时 |
| `launch-strategy` | 功能：规划产品发布、功能公告或发布策略 触发：用户提及 发布、Product Hunt、功能发布、公告、GTM、Beta、早鸟、候补、产品更新 |
| `lead-research-assistant` | 功能：根据业务找高质量线索、目标公司、联系策略 触发：用户要 销售线索、BD、营销 时 |
| `lint-and-validate` | 功能：自动质量把关、lint、静态分析 触发：用户每次改代码后要 lint/format/check/validate 时 |
| `linux-privilege-escalation` | 功能：Linux 提权：sudo、SUID、cron、枚举 触发：用户要 Linux 提权、privesc、拿 root 时 |
| `linux-shell-scripting` | 功能：Bash 脚本：自动化、监控、备份、用户管理、生产脚本 触发：用户要 写 bash、自动化 Linux、运维脚本 时 |
| `llm-app-patterns` | 功能：LLM 应用模式：RAG、Agent、Prompt IDE、LLMOps 触发：用户要 设计 AI 应用、RAG、agent、可观测 时 |
| `loki-mode` | 功能：多智能体自主创业系统：Loki Mode 触发，100+ 智能体从 PRD 到上线创收 触发：用户说 Loki Mode 时 |
| `marketing-ideas` | 功能：面向 SaaS/软件的营销策略与增长思路 触发：用户要 营销点子、增长想法、如何推广、营销策略、推广方式 |
| `marketing-psychology` | 功能：心理、心智模型、行为科学应用于营销 触发：用户提及 心理学、心智模型、认知偏差、说服、消费者行为 |
| `mcp-builder` | 功能：构建高质量 MCP 服务：Python FastMCP、Node MCP SDK 触发：用户要 建 MCP、接外部 API 时 |
| `meeting-insights-analyzer` | 功能：分析会议实录：行为模式、沟通洞察、可执行反馈 触发：用户要改进沟通、领导力时 |
| `memory-systems` | 功能：智能体记忆：跨会话持久化、知识图谱、实体、向量库 触发：用户要 实现 agent 记忆、持久状态、知识图谱 时 |
| `metasploit-framework` | 功能：Metasploit：msfconsole、msfvenom、辅助模块、后渗透 触发：用户要 用 Metasploit 渗透、exploit、payload 时 |
| `micro-saas-launcher` | 功能：小微 SaaS 快速启动：验证、MVP、定价、发布、可持续收入 触发：用户提及 micro saas、indie hacker、side project、saas mvp |
| `mobile-design` | 功能：移动优先设计：触控、性能、平台惯例、离线、React Native/Flutter 触发：用户做移动端时 |
| `moodle-external-api-development` | 功能：Moodle 外部 Web 服务 API：课程、用户、测验、插件 触发：用户要做 Moodle 对接时 |
| `multi-agent-brainstorming` | 功能：多智能体顺序设计评审，降盲区、防过早收敛 触发：设计需更高置信度、降险或正式评审时 |
| `multi-agent-patterns` | 功能：多智能体模式：监督、集群、上下文隔离、交接、并行 触发：用户要 设计多智能体、supervisor、swarm、协调多 agent 时 |
| `native-data-fetching` | 功能：网络请求、API、数据获取：fetch、axios、React Query、SWR、缓存、离线 触发：用户要做 请求、API、数据获取 时 |
| `neon-postgres` | 功能：Neon 无服务 Postgres：分支、连接池、Prisma/Drizzle 触发：用户提及 neon、serverless postgres、database branching |
| `nestjs-expert` | 功能：Nest.js：模块、DI、中间件、守卫、拦截器、TypeORM、Passport 触发：用户做 Nest 应用、架构、测试、调试时 |
| `network-101` | 功能：Web 服务、HTTP/HTTPS、SNMP、SMB、渗透实验网络 触发：用户要 配 Web 服务、渗透实验网络 时 |
| `nextjs-best-practices` | 功能：Next.js App Router：Server Components、数据获取、路由 触发：用户做 Next 时 |
| `nextjs-supabase-auth` | 功能：Next.js + Supabase Auth：登录、中间件、受保护路由 触发：用户要 supabase auth、next 鉴权 时 |
| `nodejs-best-practices` | 功能：Node 开发：框架选择、异步、安全、架构 触发：用户做 Node 时 |
| `nosql-expert` | 功能：NoSQL：Cassandra、DynamoDB、建模、单表、热分区 触发：用户做分布式 NoSQL 时 |
| `notebooklm` | 功能：查询 Google NotebookLM 笔记本，基于文档、引用、Gemini 触发：用户要查 NotebookLM、文档问答时 |
| `notion-template-business` | 功能：Notion 模板生意：设计、定价、市场、营销、变现 触发：用户提及 notion template、卖模板、gumroad |
| `obsidian-clipper-template-creator` | 功能：Obsidian Web Clipper 模板：变量、格式 触发：用户要做 clipper 模板时 |
| `onboarding-cro` | 功能：优化注册后引导、激活、首次体验、实现价值时间 触发：用户提及 引导流程、激活率、首次体验、空状态、顿悟时刻、新用户体验 |
| `page-cro` | 功能：优化营销页转化：首页、落地页、定价页、功能页、博客 触发：用户提及 CRO、转化率优化、页面不转化、提升转化 |
| `paid-ads` | 功能：付费广告：Google、Meta、LinkedIn、X 等；PPC、创意、定向、优化 触发：用户提及 PPC、付费媒体、广告文案、ROAS、CPA、再营销、受众定向 |
| `parallel-agents` | 功能：多智能体编排：多领域并行、多视角分析 触发：用户有多任务、多视角需求时 |
| `paywall-upgrade-cro` | 功能：应用内付费墙、升级页、加推、功能门控、免费转付费 触发：用户提及 付费墙、升级、加推、功能门控、试用到期、限额、套餐升级 |
| `pdf-official` | 功能：PDF：提取文本/表格、创建、合并/拆分、表单 触发：用户要处理 PDF 时 |
| `pentest-checklist` | 功能：渗透测试计划、检查清单、范围、方法论 触发：用户要 规划渗透、安全评估清单、渗透范围 时 |
| `pentest-commands` | 功能：渗透命令：nmap、metasploit、hydra/john、nikto、枚举 触发：用户要 跑渗透命令、nmap 扫描、破解密码 时 |
| `performance-profiling` | 功能：性能剖析：测量、分析、优化 触发：用户要做性能剖析时 |
| `personal-tool-builder` | 功能：先解决自己问题的自用工具：原型、本地优先、CLI、脚本产品化 触发：用户要 做工具、自用工具、CLI、解决自己的问题 时 |
| `plaid-fintech` | 功能：Plaid：Link、交易同步、身份、ACH、余额、Webhook、合规 触发：用户提及 plaid、银行卡连接、ach、账户聚合 |
| `plan-writing` | 功能：结构化任务规划：拆分、依赖、验证标准 触发：用户做 功能、重构、多步工作 前要计划时 |
| `planning-with-files` | 功能：基于文件的规划：task_plan.md、findings.md、progress.md 触发：用户做复杂多步任务、调研、>5 次 tool 调用时 |
| `playwright-skill` | 功能：Playwright 浏览器自动化：测页面、填表、截图、响应式、登录、链接 触发：用户要 测站、自动化浏览器、验证 Web 时 |
| `popup-cro` | 功能：弹窗、模态框、滑入、横幅优化以提升转化 触发：用户提及 退出意图、弹窗转化、模态优化、线索弹窗、邮件弹窗、公告横幅 |
| `postgres-best-practices` | 功能：Postgres 性能与最佳实践（Supabase 等） 触发：用户写/审/优化 Postgres 查询、Schema、配置时 |
| `powershell-windows` | 功能：PowerShell：坑、运算符、错误处理 触发：用户在 Windows 用 PowerShell 时 |
| `pptx-official` | 功能：PPT：创建、编辑、版式、批注、备注 触发：用户要处理 .pptx 时 |
| `pricing-strategy` | 功能：定价、套餐与变现：价值、支付意愿、档位 触发：用户提及 定价、定价档、免费增值、免费试用、套餐、涨价、价值指标、变现 |
| `prisma-expert` | 功能：Prisma：Schema、迁移、查询优化、关系、连接 触发：用户做 Prisma、ORM 时 |
| `privilege-escalation-methods` | 功能：提权方法：Linux/Windows、sudo、SUID、Kerberoasting、token 冒充 触发：用户要 提权、拿 root、管理员、privesc 时 |
| `product-manager-toolkit` | 功能：产品工具：RICE、用户访谈、PRD、发现、GTM 触发：用户做 优先级、用研、需求、产品策略 时 |
| `product-marketing-context` | 功能：产品营销上下文文档，供其它营销技能引用 触发：用户要 产品/营销上下文、定位、避免重复填基础信息 时 |
| `production-code-audit` | 功能：全库深度扫描，理解架构与模式，系统升级为生产级 触发：用户要生产级代码审计时 |
| `programmatic-seo` | 功能：用模板与数据规模化做 SEO 页 触发：用户提及 程序化 SEO、模板页、目录/地域/对比/集成页、大量 SEO 页 |
| `project-development` | 功能：LLM 项目启动、批处理管道、任务-模型匹配、agent 项目结构 触发：用户要 启动 LLM 项目、管道设计、agent 项目 时 |
| `project-guidelines-example` | 功能：项目专属指南与约定 触发：在该项目相关工作中参考 |
| `prompt-caching` | 功能：Prompt 缓存：Anthropic 缓存、响应缓存、CAG 触发：用户要 prompt caching、cache prompt、cag 时 |
| `prompt-engineer` | 功能：提示设计：结构、上下文、输出格式、评估 触发：用户要 提示工程、system prompt、few-shot、CoT、提示设计 时 |
| `prompt-engineering` | 功能：提示工程模式、最佳实践、优化 触发：用户要 改进 prompt、学提示策略、调试 agent 时 |
| `prompt-library` | 功能：高质量 prompt 集合：角色、任务、精修 触发：用户要 prompt 模板、角色扮演、即用示例时 |
| `python-patterns` | 功能：Python 开发：框架、异步、类型、项目结构 触发：用户做 Python 时 |
| `raffle-winner-picker` | 功能：从列表/表格/Google Sheet 随机抽奖，公平透明 触发：用户要 抽奖、抽人、活动选人 时 |
| `rag-engineer` | 功能：RAG：嵌入、向量库、分块、检索优化 触发：用户要 做 RAG、向量搜索、语义搜索、文档检索 时 |
| `rag-implementation` | 功能：RAG 模式：分块、嵌入、向量库、检索优化 触发：用户提及 rag、retrieval augmented、vector search、embeddings |
| `ralph-loop` | 功能：自主开发循环：完成所有剩余任务 触发：用户说 全部完成、完成所有任务、finish all、complete everything 时 |
| `react-best-practices` | 功能：Vercel 的 React/Next 性能优化指南 触发：用户写/审/重构 React/Next 时 |
| `react-patterns` | 功能：现代 React：Hooks、组合、性能、TS 触发：用户做 React 时 |
| `react-ui-patterns` | 功能：React UI：加载、错误、数据获取 触发：用户做 UI 组件、异步数据、UI 状态时 |
| `receiving-code-review` | 功能：收到 Code Review 后，在落实前做技术严谨性与验证 触发：用户收到评审反馈、建议不清晰或存疑时 |
| `red-team-tactics` | 功能：红队战术：MITRE ATT&CK、攻击阶段、规避、报告 触发：用户做红队时 |
| `red-team-tools` | 功能：红队方法、漏洞赏金、自动化侦察、XSS、子域枚举 触发：用户要 红队、bug bounty、侦察、XSS、子域 时 |
| `referral-program` | 功能：推荐/联盟/口碑计划：设计、激励、增长优化 触发：用户提及 推荐、联盟、大使、口碑、病毒循环、邀请好友、合作伙伴 |
| `release-skills` | 功能：通用发布流程：版本文件、changelog；Node/Python/Rust/Plugin 触发：用户说 release、发布、new version、bump、推送 时 |
| `remotion-best-practices` | 功能：Remotion 视频创作最佳实践 触发：用户用 Remotion 做视频时 |
| `requesting-code-review` | 功能：完成开发/大功能后，合并前验证是否达标 触发：用户要 请求 Code Review、合并前验证 时 |
| `research-engineer` | 功能：学术研究工程师：严谨、批判、形式验证、最优实现 触发：用户要研究级实现时 |
| `salesforce-development` | 功能：Salesforce：LWC、Apex、REST/Bulk、Connected Apps、DX、2GP 触发：用户提及 salesforce、sfdc、apex、lwc |
| `scanning-tools` | 功能：漏洞扫描、端口扫描、Web 扫描、无线、恶意软件、云、合规 触发：用户要 漏洞扫描、扫端口、Web 安全、云安全 时 |
| `schema-markup` | 功能：Schema 与结构化数据：添加、修复、优化 触发：用户提及 schema、JSON-LD、富摘要、FAQ/产品/面包屑 schema |
| `scroll-experience` | 功能：滚动体验：视差、滚动动效、互动叙事、电影感站 触发：用户要 滚动动画、视差、滚动叙事、电影感网站 时 |
| `security-review` | 功能：安全检查：鉴权、用户输入、密钥、API、支付/敏感功能 触发：用户加鉴权、处理输入、密钥、API、支付时 |
| `segment-cdp` | 功能：Segment CDP：Analytics.js、服务端、Protocols、身份、数据治理 触发：用户提及 segment、analytics.js、cdp、tracking plan |
| `senior-architect` | 功能：全栈架构：React/Next/Node/RN/Swift/Kotlin/Flutter/Postgres/GraphQL/Go/Python 触发：用户要 设计架构、技术决策、画架构图 时 |
| `senior-fullstack` | 功能：全栈：React、Next、Node、GraphQL、Postgres；脚手架、质量、模式 触发：用户要 建项目、分析质量、设计模式、开发流程 时 |
| `seo-audit` | 功能：审计、诊断站点 SEO 问题 触发：用户提及 SEO 审计、技术 SEO、不排名、SEO 问题、站内 SEO、meta、SEO 健康 |
| `seo-fundamentals` | 功能：SEO 原理：E-E-A-T、Core Web Vitals、技术基础、内容质量 触发：用户要理解 SEO 为何有效时 |
| `server-management` | 功能：服务管理：进程、监控、扩容 触发：用户做服务管理决策时 |
| `shodan-reconnaissance` | 功能：Shodan 侦察：暴露设备、脆弱服务、IP 段、IoT、端口 触发：用户要 Shodan、互联网设备搜索、渗透侦察 时 |
| `shopify-apps` | 功能：Shopify 应用：Remix、App Bridge、Webhook、GraphQL、Polaris、计费 触发：用户提及 shopify app、embedded app、polaris、app bridge |
| `shopify-development` | 功能：Shopify 应用、扩展、主题：GraphQL、CLI、Polaris、Liquid、Webhook、计费 触发：用户提及 shopify、主题、liquid、graphql、webhook、metafields |
| `signup-flow-cro` | 功能：优化注册、开户、试用激活流程 触发：用户提及 注册转化、注册摩擦、注册优化、试用注册、开户流程 |
| `skill-creator` | 功能：创建或更新扩展 Claude 的技能 触发：用户要 建新 skill、更新 skill 时 |
| `skill-developer` | 功能：Claude Code 技能开发：Anthropic 实践、trigger、hooks、渐进披露 触发：用户要 建/改 skill、skill-rules、调试激活 时 |
| `skill-share` | 功能：创建技能并通过 Rube 自动分享到 Slack 触发：用户要团队共享技能时 |
| `slack-bot-builder` | 功能：Slack 应用：Bolt、Block Kit、斜杠命令、事件、OAuth、Workflow 触发：用户要 slack bot、slack app、bolt、block kit 时 |
| `slack-gif-creator` | 功能：Slack 用 GIF：约束、校验、动效创意 触发：用户要做 Slack GIF 时 |
| `smtp-penetration-testing` | 功能：SMTP 渗透：枚举用户、开放转发、banner、暴力破解、安全评估 触发：用户要 SMTP 渗透、邮件安全 时 |
| `social-content` | 功能：社媒内容：LinkedIn、X、Instagram、TikTok、Facebook；创作、排期、优化 触发：用户提及 LinkedIn 帖、推文串、社媒、内容日历、排期、互动、病毒内容 |
| `software-architecture` | 功能：质量导向的软件架构 触发：用户要 写代码、设计架构、分析代码、软件开发 时 |
| `spec-analyze` | 功能：对 spec.md / plan.md / tasks.md 做一致性、质量分析 触发：用户 /spec-analyze、分析规格、检查一致性 时 |
| `spec-checklist` | 功能：生成需求质量检查清单（非实现） 触发：用户 /spec-checklist、为某领域建清单 时 |
| `spec-clarify` | 功能：发现规格遗漏，最多 5 个澄清问题并写回 spec 触发：用户 /spec-clarify、澄清规格、/spec-specify 后 时 |
| `spec-constitution` | 功能：创建/更新项目宪章：原则与治理 触发：用户 /spec-constitution、建宪章、更新原则 时 |
| `spec-implement` | 功能：按 tasks.md 分阶段实现 触发：用户 /spec-implement、实现功能、/spec-tasks 后编码 时 |
| `spec-plan` | 功能：实现规划：research、data-model、contracts、quickstart 触发：用户 /spec-plan、做计划、/spec-specify 或 /spec-clarify 后 时 |
| `spec-specify` | 功能：从自然语言写出/更新功能规格（Spec 流程第一步） 触发：用户 /spec-specify、写规格、我要做… 时 |
| `spec-tasks` | 功能：生成按用户故事、依赖排序的 tasks.md 触发：用户 /spec-tasks、建任务、/spec-plan 后 时 |
| `spec-taskstoissues` | 功能：将 tasks.md 转为 GitHub issues（含依赖） 触发：用户 /spec-taskstoissues、建 issue、任务转 issue 时 |
| `specify-resources` | 功能：Spec 流程共用资源：脚本、模板；被 spec-* 依赖，不直接调用 触发：（被 spec-* 技能依赖） |
| `sql-injection-testing` | 功能：SQL 注入测试与利用 触发：用户要 测 SQLi、SQL 注入、认证绕过、脱库 时 |
| `sqlmap-database-pentesting` | 功能：SQLMap：自动化 SQLi、库结构枚举、脱库 触发：用户要 自动化 SQLi、sqlmap、脱库 时 |
| `ssh-penetration-testing` | 功能：SSH 渗透：配置枚举、暴力破解、漏洞、隧道、审计 触发：用户要 SSH 渗透、SSH 安全 时 |
| `strategic-compact` | 功能：在任务阶段节点建议手动压缩 context，避免随意自动压缩 触发：用户做长任务、多阶段时 |
| `stripe-integration` | 功能：Stripe：支付、订阅、计费门户、Webhook、按量、Connect 触发：用户要 stripe、支付、订阅、计费 时 |
| `subagent-driven-development` | 功能：当前会话中执行含独立任务的实现计划 触发：用户按计划执行多任务时 |
| `systematic-debugging` | 功能：遇到 bug、失败、异常时，先系统排查再修 触发：用户 遇到 bug、测试失败、异常行为 时 |
| `tailored-resume-generator` | 功能：根据 JD 生成定制简历，突出经历与技能 触发：用户要 改简历、投递 时 |
| `tailwind-patterns` | 功能：Tailwind v4：CSS 优先配置、容器查询、design tokens 触发：用户用 Tailwind 时 |
| `tavily-web` | 功能：Tavily API：搜索、抓取、爬取、调研 触发：用户要用 Tavily 搜索/调研时 |
| `tdd-workflow` | 功能：TDD：RED-GREEN-REFACTOR 触发：用户做 TDD 时 |
| `telegram-bot-builder` | 功能：Telegram 机器人：架构、Bot API、UX、变现、扩展 触发：用户要 telegram bot、tg bot、telegram 自动化 时 |
| `telegram-mini-app` | 功能：Telegram Mini App (TWA)：TON、Web App API、支付、鉴权 触发：用户要 telegram mini app、TWA、TON app 时 |
| `template-skill` | 功能：技能模板，需替换为具体描述与触发条件 触发：占位用 |
| `test-driven-development` | 功能：先写测试再实现 触发：用户 做功能/bugfix 前、要 TDD 时 |
| `test-fixing` | 功能：跑测试并系统修复失败用例，智能分组 触发：用户要 修失败测试、让测试过 时 |
| `testing-patterns` | 功能：Jest、工厂、mock、TDD 触发：用户 写单测、工厂、TDD 时 |
| `theme-factory` | 功能：制品主题化：幻灯片、文档、落地页等；10 套预设主题 触发：用户要给制品加主题时 |
| `tool-design` | 功能：Agent 工具设计：描述、降复杂度、MCP、命名 触发：用户要 设计 agent 工具、MCP 工具、工具描述 时 |
| `top-web-vulnerabilities` | 功能：Web 漏洞概览：注入、访问控制、配置、客户端、移动/IoT 触发：用户要 认漏洞、学注入、API 安全、配置问题 时 |
| `trigger-dev` | 功能：Trigger.dev：后台任务、AI 工作流、可靠异步、TS 优先 触发：用户提及 trigger.dev、background task、ai 后台、长任务 |
| `twilio-communications` | 功能：Twilio：短信、语音、WhatsApp、2FA 验证 触发：用户要 twilio、发短信、语音、验证码 时 |
| `typescript-expert` | 功能：TS/JS 专家：类型、性能、monorepo、迁移、工具 触发：用户做 TS/JS、类型、构建、调试、架构 时 |
| `ui-ux-pro-max` | 功能：UI/UX：50 风格、21 调色、50 字体、20 图表、9 技术栈 触发：用户 规划/实现/审查 UI、设计、重构 UI 时 |
| `unzip-crx` | 功能：解压 Chrome 扩展 .crx 触发：用户要 解压、提取 .crx 时 |
| `upgrading-expo` | 功能：Expo SDK 升级与依赖修复 触发：用户要升级 Expo 时 |
| `upstash-qstash` | 功能：Upstash QStash：无服务队列、定时任务、HTTP 投递 触发：用户提及 qstash、upstash queue、serverless cron、scheduled http |
| `use-dom` | 功能：Expo DOM：在 webview 跑 Web 代码，向原生渐进迁移 触发：用户要在 Expo 用 Web 代码时 |
| `using-git-worktrees` | 功能：功能隔离：git worktree，执行计划前建独立工作区 触发：用户 做独立功能、执行计划 前要隔离时 |
| `using-superpowers` | 功能：会话开始时确立如何发现与使用技能 触发：用户 开启会话、要用技能 时 |
| `vercel-composition-patterns` | 功能：React 组合模式：复合组件、render props、context、可扩展 API 触发：用户 重构组件、建组件库、设计 API 时 |
| `vercel-deployment` | 功能：Vercel + Next.js 部署 触发：用户要 vercel、部署、托管、生产 时 |
| `vercel-react-best-practices` | 功能：Vercel 的 React/Next 性能优化 触发：用户写/审/重构 React/Next 时 |
| `vercel-react-native-skills` | 功能：React Native / Expo 最佳实践：列表、动效、原生模块 触发：用户做 RN、Expo、移动性能、原生 API 时 |
| `verification-before-completion` | 功能：声称完成/修复/通过前，跑验证并确认输出 触发：用户 要交活、commit、建 PR 前 时 |
| `verification-loop` | 功能：功能/重大改动后的验证循环 触发：完成功能或重大代码变更、建 PR 前使用 |
| `video-downloader` | 功能：下载 YouTube：质量、格式、仅音频 MP3 触发：用户要 下载、保存 YouTube 视频 时 |
| `viral-generator-builder` | 功能：易传播生成器：起名、测验、头像、计算器等；分享心理与病毒机制 触发：用户要 生成器、测验、起名、头像、病毒工具 时 |
| `voice-agents` | 功能：语音智能体：语音识别/合成、低延迟对话、打断、噪声 触发：用户做 语音 agent、语音交互 时 |
| `voice-ai-development` | 功能：语音 AI：Realtime API、Vapi、Deepgram、ElevenLabs、LiveKit、WebRTC 触发：用户要 voice ai、语音 agent、STT、TTS、实时语音 时 |
| `voice-ai-engine-development` | 功能：实时语音引擎：异步管道、流式转写、LLM、TTS、打断、多提供商 触发：用户做 实时语音引擎 时 |
| `vulnerability-scanner` | 功能：漏洞分析：OWASP 2025、供应链、攻击面、风险排序 触发：用户做 漏洞分析、供应链安全 时 |
| `web-artifacts-builder` | 功能：多组件 claude.ai HTML 制品：React、Tailwind、shadcn 触发：复杂制品需状态、路由、shadcn 时 |
| `web-design-guidelines` | 功能：按 Web 界面指南审查 UI 触发：用户 审查 UI、无障碍、设计审计、UX 审查 时 |
| `web-performance-optimization` | 功能：Web 性能：加载、Core Web Vitals、体积、缓存、运行时 触发：用户要 优化性能、Core Web Vitals 时 |
| `webapp-testing` | 功能：Playwright 测本地 Web 应用：功能、截图、日志 触发：用户要 测本地 Web、前端验证 时 |
| `windows-privilege-escalation` | 功能：Windows 提权：枚举、配置滥用、后渗透 触发：用户要 Windows 提权、privesc 时 |
| `wireshark-analysis` | 功能：Wireshark：抓包、过滤、TCP/UDP 流、异常、协议分析 触发：用户要 Wireshark、抓包、分析流量 时 |
| `wordpress-penetration-testing` | 功能：WordPress 渗透：漏洞、用户/主题/插件枚举、WPScan 触发：用户要 WordPress 渗透、WPScan 时 |
| `workflow-automation` | 功能：工作流自动化：n8n、Temporal、Inngest；顺序/并行/编排-worker 触发：用户做 工作流、持久执行、支付流 时 |
| `writing-plans` | 功能：有规格或需求的多步任务，动代码前先写计划 触发：用户 有 spec/需求、多步任务 且未动代码时 |
| `writing-skills` | 功能：创建、编辑或验证技能 触发：用户 建技能、改技能、验证技能 时 |
| `xlsx-official` | 功能：Excel：创建、编辑、公式、格式、分析、可视化 触发：用户要处理 .xlsx/.csv 时 |
| `xss-html-injection` | 功能：XSS / HTML 注入测试与利用 触发：用户要 测 XSS、跨站、注入、偷 cookie、CSP 绕过 时 |
| `zapier-make-patterns` | 功能：Zapier / Make 无代码自动化：何时用、可靠构建、何时上代码 触发：用户做 Zapier、Make、无代码自动化 时 |

---

## 目录结构

```
~/.claude/skills/
├── skill-name/
│   ├── SKILL.md          # 主技能文件 (必需)
│   ├── references/       # 参考资料 (可选)
│   └── scripts/          # 辅助脚本 (可选)
└── ...
```

## 在 Claude Code 中使用

```bash
# 启动 Claude Code
claude

# 调用特定技能
/skill-name

# 查看可用技能
ls ~/.claude/skills/
```

## 其他 AI 工具集成

| 工具 | 配置位置 |
|------|---------|
| **Cursor** | `.cursor/rules/` |
| **Windsurf** | `.windsurfrules` |
| **VS Code + Copilot** | `.github/copilot-instructions.md` |
| **Aider** | `--read SKILL.md` |
| **Continue** | `.continue/config.json` |
| **Cline** | `.cline/` |

---

## 许可证

各 skill 可能有不同的许可证，请查看各 skill 目录下的 LICENSE.txt 文件。

## 贡献

欢迎提交 PR 添加新的 skill 或改进现有 skill！

---

## 联系方式

项目维护者: windy (xiaochangsheng@xichengtech.cn)
github: @xfstudio

---

> 📖 本文档最后更新: 2026-01-28
