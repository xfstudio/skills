# Claude Skills Collection

这是一个 Claude Code Skills 集合，为 AI 编程助手提供专业化的技能扩展。

**仓库地址**: `https://codeup.aliyun.com/6948c28bf7465fb3044334e2/bi/skills.git`

---

## 在各 AI Coding IDE/CLI 工具中使用本项目

### 通用克隆方式

```bash
# 克隆到 Claude Code 默认 skills 目录
git clone https://codeup.aliyun.com/6948c28bf7465fb3044334e2/bi/skills.git ~/.claude/skills

# 或克隆特定 skill (使用 sparse-checkout)
git clone --filter=blob:none --sparse https://codeup.aliyun.com/6948c28bf7465fb3044334e2/bi/skills.git ~/.claude/skills
cd ~/.claude/skills && git sparse-checkout set skill-name

# Windows 用户
git clone https://codeup.aliyun.com/6948c28bf7465fb3044334e2/bi/skills.git %USERPROFILE%\.claude\skills
```

---

### 🌍 国际主流工具配置说明

| 工具 | 厂商 | 配置位置 | 使用方式 |
|------|------|---------|---------|
| **Claude Code (CLI)** | Anthropic | `~/.claude/skills/` | 自动加载目录下所有 SKILL.md 文件，支持 `/skill-name` 命令调用 |
| **Cursor** | Anysphere | 项目 `.cursor/rules/` 或 Settings → Rules | 将 SKILL.md 内容复制到规则文件或全局规则 |
| **Windsurf** | Codeium | 项目 `.windsurfrules` 或 Cascade 设置 | 添加 skill 内容作为 Cascade Rules |
| **VS Code + Copilot** | Microsoft/GitHub | `.github/copilot-instructions.md` | 将 skill 内容作为项目指令，支持 @workspace 引用 |
| **Aider** | Paul Gauthier | `.aider.conf.yml` 或命令行 | `--read SKILL.md` 加载，或配置 `read:` 字段 |
| **Continue** | Continue.dev | `.continue/config.json` | 配置 `systemMessage` 或添加到 context providers |
| **Cline** | Saoud Rizwan | 扩展设置或项目 `.cline/` | 配置 Custom Instructions 或 Rules |
| **Roo Code** | Roo Code | 项目 `.roo/` 或全局设置 | 添加到 System Prompt 或 Custom Modes |
| **Zed** | Zed Industries | `.zed/settings.json` | 配置 `assistant.default_model.custom_instructions` |
| **JetBrains AI** | JetBrains | Settings → AI Assistant | 添加到 Custom Prompts 或 Project Instructions |
| **Tabnine** | Tabnine | Tabnine Hub → Personalization | 配置 Instruction Files 或 Global Instructions |
| **Sourcegraph Cody** | Sourcegraph | `.cody/` 或 VS Code 设置 | 配置 Custom Commands 或 Instructions |
| **OpenHands** | All-Hands AI | `config.toml` 或环境变量 | 设置 `custom_instructions` 或 agent prompts |
| **Devin** | Cognition | Playbook 或 Session Settings | 添加到 Playbook Instructions |
| **Replit Agent** | Replit | `.replit` 或 Agent Chat | 在 Agent 对话中引用或配置 |
| **Supermaven** | Supermaven | 扩展设置 | 添加到 Custom Context |

### 🚀 新兴 AI Coding 工具配置说明

| 工具 | 厂商 | 配置位置 | 使用方式 |
|------|------|---------|---------|
| **Kiro** | AWS | `.kiro/` 或 Spec 文件 | 配置 `specs/` 目录下的 Steering Files，或在 Agent Hooks 中引用 |
| **Augment Code** | Augment | `.augment/` 或 IDE 设置 | 配置 Memory 或 Instructions 文件，支持 @mention 引用 |
| **Trae** | ByteDance | `.trae/` 或插件设置 | 配置 Builder Mode Rules 或 Custom Instructions |
| **Qodo (原 Codium)** | Qodo AI | `.qodo/` 或扩展设置 | 配置 Custom Instructions 或 Test Generation Rules |
| **Amazon Q Developer** | AWS | `.amazonq/` 或 IDE 设置 | 添加到 Customization 或 Project Context |
| **Jules** | Google | `.jules/` 或 Workspace 设置 | 配置 Agent Instructions 或 Task Templates |
| **Gemini Code Assist** | Google | `.gemini/` 或 Cloud Workstations | 配置 Code Customization 或 Enterprise Rules |
| **Bolt.new** | StackBlitz | 项目 Prompt 或 Settings | 在创建项目时添加 System Instructions |
| **v0.dev** | Vercel | Chat Context | 在对话中粘贴 skill 内容作为上下文 |
| **Lovable** | Lovable | Project Settings | 配置 AI Instructions 或 Design System Rules |

### 🇨🇳 国内工具配置说明

| 工具 | 厂商 | 配置位置 | 使用方式 |
|------|------|---------|---------|
| **通义灵码** | 阿里云 | IDE 插件设置 → 偏好设置 | 配置「自定义指令」或项目级 `.lingma/` 目录 |
| **CodeGeeX** | 智谱 AI | 插件设置 → 提示词配置 | 添加到「系统提示词」或使用 @file 引用 |
| **文心快码 Comate** | 百度 | 插件设置 → 个性化配置 | 配置「开发规范」或项目指令 |
| **豆包 MarsCode** | 字节跳动 | 插件设置或 `.marscode/` | 配置 Custom Instructions 或项目规则 |
| **Trae (国内版)** | 字节跳动 | `.trae/` 或插件设置 | 配置 Builder 规则或 Chat 指令 |
| **Fitten Code** | 非十科技 | 插件设置 → 高级选项 | 配置「自定义系统提示」 |
| **腾讯云 AI 代码助手** | 腾讯云 | IDE 插件设置 | 配置「团队规范」或项目指令 |
| **华为 CodeArts Snap** | 华为云 | CodeArts IDE 设置 | 配置「编码规范」或项目级配置 |
| **讯飞星火代码助手** | 科大讯飞 | 插件设置 | 配置自定义提示词 |
| **商汤代码小浣熊** | 商汤科技 | 插件设置 → 偏好 | 添加到系统指令 |
| **百川智能代码助手** | 百川智能 | IDE 配置 | 项目级或全局自定义指令 |

### 通用集成方法

对于不直接支持 skills 的工具，可采用以下通用方法：

```bash
# 方法 1: 复制 skill 内容到剪贴板
cat ~/.claude/skills/skill-name/SKILL.md | pbcopy  # macOS
cat ~/.claude/skills/skill-name/SKILL.md | xclip   # Linux

# 方法 2: 创建符号链接到项目目录
ln -s ~/.claude/skills/skill-name/SKILL.md ./.ai-instructions/

# 方法 3: 使用环境变量
export AI_CUSTOM_INSTRUCTIONS="$(cat ~/.claude/skills/skill-name/SKILL.md)"
```

### IDE/编辑器支持情况

| 编辑器/IDE | 支持的 AI 工具 |
|-----------|---------------|
| **VS Code** | Copilot, Continue, Cline, Roo Code, Cursor (fork), Windsurf, Augment, 通义灵码, CodeGeeX, 文心快码, MarsCode, Trae, Fitten Code, Qodo |
| **JetBrains (IDEA/PyCharm等)** | JetBrains AI, Copilot, Continue, Augment, 通义灵码, CodeGeeX, 文心快码, Tabnine, Qodo |
| **Neovim/Vim** | Copilot, Codeium, Tabnine, Continue |
| **Zed** | Zed AI (内置), Supermaven |
| **Sublime Text** | Copilot, Tabnine, Codeium |
| **Xcode** | Copilot, 通义灵码 |
| **云 IDE** | Kiro (AWS), Replit Agent, Bolt.new, v0.dev, Lovable |
| **终端/CLI** | Claude Code, Aider, OpenHands, Codex CLI |
| **独立 IDE** | Cursor, Windsurf, Trae, Kiro |

---

## Skills 列表

### 🔐 安全与渗透测试

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `active-directory-attacks` | Active Directory 攻击技术，包括 Kerberoasting、DCSync、Pass-the-Hash 等 | 需要 AD 渗透、域攻击时使用 |
| `api-fuzzing-bug-bounty` | REST/GraphQL/SOAP API 安全测试与模糊测试 | 测试 API 安全、漏洞赏金猎人 |
| `aws-penetration-testing` | AWS 云环境渗透测试，IAM 枚举、权限提升 | 测试 AWS 安全、S3 桶测试 |
| `broken-authentication` | 身份认证与会话管理漏洞测试 | 测试登录安全、会话固定攻击 |
| `burp-suite-testing` | Burp Suite 工具使用指南 | HTTP 流量拦截、Web 漏洞扫描 |
| `cc-skill-security-review` | 安全审查检查清单与模式 | 添加认证、处理用户输入、API 端点安全 |
| `cloud-penetration-testing` | 多云平台 (AWS/Azure/GCP) 安全评估 | 云基础设施渗透测试 |
| `ethical-hacking-methodology` | 道德黑客完整方法论 | 学习渗透测试生命周期 |
| `file-path-traversal` | 目录遍历/LFI 漏洞测试 | 测试路径遍历漏洞 |
| `file-uploads` | 文件上传与云存储安全处理 | S3、R2、presigned URL、multipart 上传 |
| `html-injection-testing` | HTML 注入漏洞测试 | 内容注入、钓鱼测试 |
| `idor-testing` | 不安全直接对象引用 (IDOR) 测试 | 访问控制绕过测试 |
| `linux-privilege-escalation` | Linux 权限提升技术 | SUID、sudo 误配、cron 提权 |
| `linux-shell-scripting` | Linux Shell 脚本模板 | 系统管理自动化脚本 |
| `metasploit-framework` | Metasploit 框架使用指南 | 漏洞利用、payload 生成 |
| `network-101` | 网络服务配置基础 | HTTP/HTTPS/SMB/SNMP 配置 |
| `pentest-checklist` | 渗透测试检查清单 | 规划渗透测试流程 |
| `pentest-commands` | 渗透测试命令速查 | nmap、hydra、nikto 命令参考 |
| `privilege-escalation-methods` | 权限提升方法汇总 (Linux/Windows) | 提权向量发现与利用 |
| `red-team-tactics` | 红队战术原则 (MITRE ATT&CK) | 攻击阶段、检测规避、报告 |
| `red-team-tools` | 红队工具与方法论 | 自动化侦察、漏洞发现 |
| `scanning-tools` | 安全扫描工具指南 | 网络扫描、漏洞评估 |
| `shodan-reconnaissance` | Shodan 侦察与渗透测试 | 暴露设备搜索、IoT 发现 |
| `smtp-penetration-testing` | SMTP 服务安全测试 | 邮件服务器渗透测试 |
| `sql-injection-testing` | SQL 注入漏洞测试 | 数据库注入攻击测试 |
| `sqlmap-database-pentesting` | SQLMap 自动化数据库渗透 | 自动化 SQL 注入利用 |
| `ssh-penetration-testing` | SSH 服务安全测试 | SSH 暴力破解、隧道技术 |
| `top-web-vulnerabilities` | Top 100 Web 漏洞参考 | OWASP 对齐的漏洞分类 |
| `vulnerability-scanner` | 高级漏洞分析原则 | OWASP 2025、供应链安全、攻击面映射 |
| `webapp-testing` | Web 应用测试工具包 | Playwright 本地应用测试 |
| `windows-privilege-escalation` | Windows 权限提升技术 | 服务滥用、令牌模拟 |
| `wireshark-analysis` | Wireshark 网络流量分析 | 数据包捕获、协议分析 |
| `wordpress-penetration-testing` | WordPress 安全评估 | WPScan、插件漏洞测试 |
| `xss-html-injection` | XSS 与 HTML 注入测试 | 客户端注入漏洞测试 |

### 🤖 AI/LLM 开发

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `advanced-evaluation` | LLM-as-Judge 高级评估技术 | 模型输出比较、评估管道 |
| `agent-evaluation` | LLM Agent 测试与基准评估 | Agent 行为测试、可靠性指标、生产监控 |
| `agent-manager-skill` | 多 Agent 管理器 (tmux) | 通过 tmux 会话管理多个本地 CLI Agent |
| `agent-tool-builder` | Agent 工具设计与构建 | JSON Schema、工具描述、MCP 标准 |
| `ai-agents-architect` | 自主 AI Agent 设计专家 | 工具使用、记忆系统、多 Agent 编排 |
| `ai-product` | AI 产品开发模式 | LLM 集成、RAG 架构、AI UX、成本优化 |
| `ai-wrapper-product` | AI API 包装产品开发 | OpenAI/Anthropic 包装、提示工程、成本管理 |
| `autonomous-agent-patterns` | 自主编程 Agent 设计模式 | 构建 AI Agent、权限系统 |
| `bdi-mental-states` | BDI 心智状态建模 | 信念-期望-意图架构 |
| `blockrun` | 外部模型调用 | 图像生成、实时 X/Twitter 数据、Grok/GPT/DALL-E |
| `computer-use-agents` | 计算机使用 Agent | 屏幕控制、GUI 自动化、视觉 Agent |
| `context-window-management` | 上下文窗口管理策略 | 摘要、裁剪、路由、避免上下文腐烂 |
| `conversation-memory` | 对话记忆系统 | 短期/长期/实体记忆、聊天历史持久化 |
| `crewai` | CrewAI 多 Agent 框架 | 角色设计、任务定义、Crew 编排、流程类型 |
| `evaluation` | Agent 系统评估方法 | Agent 性能测试、质量门控 |
| `hosted-agents` | 托管 Agent 基础设施 | 后台 Agent、沙箱执行 |
| `langfuse` | Langfuse LLM 可观测性 | 追踪、提示管理、评估、数据集 |
| `langgraph` | LangGraph 状态化 Agent 框架 | 图构建、状态管理、检查点、ReAct 模式 |
| `llm-app-patterns` | LLM 应用开发模式 | RAG 管道、Agent 架构 |
| `loki-mode` | 多 Agent 自主创业系统 | PRD 到部署的完整自动化 |
| `mcp-builder` | MCP 服务器开发指南 | 构建 Model Context Protocol 服务器 |
| `memory-systems` | Agent 记忆系统设计 | 知识图谱、跨会话持久化 |
| `multi-agent-patterns` | 多 Agent 架构模式 | 监督模式、群体架构 |
| `parallel-agents` | 多 Agent 编排模式 | 多任务并行、多视角分析 |
| `project-development` | LLM 项目开发方法论 | 管道架构、成本估算 |
| `prompt-caching` | LLM 提示缓存策略 | Anthropic 缓存、响应缓存、CAG |
| `prompt-engineering` | 提示工程模式与最佳实践 | 优化提示、调试 Agent 行为 |
| `prompt-library` | 高质量提示模板库 | 角色扮演、任务特定提示 |
| `rag-engineer` | RAG 系统构建专家 | 嵌入模型、向量数据库、分块策略 |
| `rag-implementation` | RAG 实现模式 | 分块、嵌入、向量存储、检索优化 |
| `tool-design` | Agent 工具设计 | 工具描述、MCP 工具实现 |
| `voice-agents` | 语音 Agent 开发 | 语音到语音、STT→LLM→TTS、低延迟对话 |
| `voice-ai-development` | 语音 AI 应用开发 | OpenAI Realtime、Vapi、Deepgram、ElevenLabs |

### 📚 上下文工程

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `context-compression` | 上下文压缩策略 | 减少 token 用量、会话压缩 |
| `context-degradation` | 上下文退化诊断 | 诊断 lost-in-middle 问题 |
| `context-fundamentals` | 上下文工程基础 | 理解上下文窗口、注意力机制 |
| `context-optimization` | 上下文优化技术 | KV-cache 优化、上下文分区 |
| `filesystem-context` | 文件系统上下文工程 | 文件上下文管理、工具输出持久化 |

### 💻 代码开发与工程

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `api-patterns` | API 设计原则与决策 | REST vs GraphQL vs tRPC、响应格式、版本控制 |
| `app-builder` | 全栈应用构建编排器 | 从自然语言创建全栈应用、技术栈选择 |
| `architecture` | 架构决策框架 | 需求分析、权衡评估、ADR 文档 |
| `aws-serverless` | AWS 无服务器应用开发 | Lambda、API Gateway、DynamoDB、SAM/CDK |
| `azure-functions` | Azure Functions 开发模式 | 隔离工作模型、Durable Functions、冷启动优化 |
| `backend-dev-guidelines` | Node.js/Express/TypeScript 后端开发指南 | 微服务架构、Prisma、Zod |
| `bash-linux` | Bash/Linux 终端模式 | 关键命令、管道、错误处理、脚本 |
| `behavioral-modes` | AI 操作模式 | 头脑风暴、实现、调试、审查、教学、发布 |
| `browser-automation` | 浏览器自动化 | Playwright/Puppeteer、测试、爬虫、Agent 控制 |
| `browser-extension-builder` | 浏览器扩展开发 | Chrome/Firefox 扩展、Manifest V3、内容脚本 |
| `bullmq-specialist` | BullMQ 队列专家 | Redis 队列、后台任务、可靠异步执行 |
| `bun-development` | Bun 运行时现代 JS/TS 开发 | 从 Node.js 迁移到 Bun |
| `cc-skill-backend-patterns` | 后端架构模式 | API 设计、数据库优化、服务端最佳实践 |
| `cc-skill-clickhouse-io` | ClickHouse 数据库模式 | 查询优化、分析、高性能数据工程 |
| `cc-skill-coding-standards` | 通用编码标准 | TypeScript/JavaScript/React/Node.js 最佳实践 |
| `cc-skill-continuous-learning` | 持续学习技能 | 开发技能提升 |
| `cc-skill-frontend-patterns` | 前端开发模式 | React/Next.js、状态管理、性能优化 |
| `cc-skill-project-guidelines-example` | 项目指南示例 | 项目级配置示例 |
| `cc-skill-strategic-compact` | 战略紧凑技能 | 开发策略 |
| `clean-code` | 务实编码标准 | 简洁、直接、无过度工程 |
| `claude-code-guide` | Claude Code 使用大师指南 | 配置模板、调试技巧 |
| `code-review-checklist` | 代码审查检查清单 | 代码质量、安全、最佳实践 |
| `core-components` | 核心组件库与设计系统 | UI 构建、设计令牌 |
| `database-design` | 数据库设计原则 | Schema 设计、索引策略、ORM 选择 |
| `deployment-procedures` | 生产部署原则 | 安全部署、回滚策略、验证 |
| `docker-expert` | Docker 容器化专家 | 多阶段构建、镜像优化、安全加固 |
| `documentation-templates` | 文档模板与结构 | README、API 文档、代码注释 |
| `firebase` | Firebase 后端开发 | Auth、Firestore、Cloud Functions、安全规则 |
| `frontend-design` | 生产级前端界面设计 | 网页组件、落地页、仪表盘 |
| `frontend-dev-guidelines` | React/TypeScript 前端开发指南 | Suspense、TanStack Router |
| `game-development` | 游戏开发编排器 | 根据项目需求路由到平台特定技能 |
| `gcp-cloud-run` | GCP Cloud Run 无服务器开发 | 容器化服务、事件驱动、Pub/Sub |
| `graphql` | GraphQL 开发 | Schema 设计、Resolver、DataLoader、Federation |
| `inngest` | Inngest 无服务器后台任务 | 事件驱动工作流、持久执行 |
| `javascript-mastery` | JavaScript 核心概念精通 | 33+ 必知 JS 概念 |
| `kaizen` | 持续改进与标准化指南 | 代码质量、重构 |
| `lint-and-validate` | 自动质量控制 | 代码修改后的 lint、格式化、静态分析 |
| `moodle-external-api-development` | Moodle 外部 API 开发 | Web 服务、课程管理、用户追踪 |
| `neon-postgres` | Neon 无服务器 Postgres | 分支、连接池、Prisma/Drizzle 集成 |
| `nestjs-expert` | Nest.js 框架专家 | 模块架构、依赖注入、Guard、Interceptor |
| `nextjs-best-practices` | Next.js App Router 原则 | Server Components、数据获取、路由模式 |
| `nextjs-supabase-auth` | Next.js + Supabase Auth 集成 | 认证中间件、受保护路由 |
| `nodejs-best-practices` | Node.js 开发原则 | 框架选择、异步模式、安全、架构 |
| `performance-profiling` | 性能分析原则 | 测量、分析、优化技术 |
| `powershell-windows` | PowerShell Windows 模式 | 关键陷阱、操作符语法、错误处理 |
| `prisma-expert` | Prisma ORM 专家 | Schema 设计、迁移、查询优化、关系建模 |
| `python-patterns` | Python 开发模式 | Python 最佳实践 |
| `react-best-practices` | React/Next.js 性能优化 | Vercel 工程最佳实践 |
| `react-patterns` | 现代 React 模式 | Hooks、组合、性能、TypeScript |
| `react-ui-patterns` | React UI 模式 | 加载状态、错误处理 |
| `remotion-best-practices` | Remotion 视频创建最佳实践 | React 视频创建 |
| `research-engineer` | 学术研究工程师 | 科学严谨、形式验证、最优实现 |
| `senior-architect` | 高级软件架构设计 | 系统设计、技术决策 |
| `senior-fullstack` | 全栈开发工具包 | React、Next.js、GraphQL |
| `server-management` | 服务器管理原则 | 进程管理、监控策略、扩展决策 |
| `software-architecture` | 软件架构开发指南 | Clean Architecture、DDD |
| `systematic-debugging` | 系统化调试方法 | Bug 修复、测试失败分析 |
| `tailwind-patterns` | Tailwind CSS v4 原则 | CSS-first 配置、容器查询、设计令牌 |
| `test-driven-development` | 测试驱动开发 | 先写测试再实现 |
| `test-fixing` | 测试修复工具 | 智能错误分组修复 |
| `testing-patterns` | Jest 测试模式 | 工厂函数、Mock 策略 |
| `trigger-dev` | Trigger.dev 后台任务 | AI 工作流、长时间运行任务、TypeScript 优先 |
| `typescript-expert` | TypeScript 专家 | TypeScript 高级模式 |
| `vercel-deployment` | Vercel 部署专家 | Next.js 部署、托管、生产环境 |

### 📄 文档处理

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `docx-official` | Word 文档创建、编辑、分析 | 修订追踪、批注、格式保留 |
| `pdf-official` | PDF 处理工具包 | 表单填写、文本提取、合并拆分 |
| `pptx-official` | PowerPoint 演示文稿处理 | 创建、编辑、布局管理 |
| `xlsx-official` | Excel 电子表格处理 | 公式、格式化、数据分析 |

### 🎨 设计与 UI/UX

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `3d-web-experience` | 3D Web 体验架构师 | Three.js、React Three Fiber、WebGL、3D 产品配置器 |
| `algorithmic-art` | p5.js 算法艺术创作 | 生成艺术、流场、粒子系统 |
| `artifacts-builder` | Claude.ai HTML Artifact 构建器 | React、Tailwind、shadcn/ui |
| `brand-guidelines` | Anthropic 品牌样式指南 | 品牌色彩、排版 |
| `canvas-design` | 视觉艺术设计 (PNG/PDF) | 海报、静态设计作品 |
| `claude-d3js-skill` | D3.js 交互式数据可视化 | 自定义图表、网络图 |
| `i18n-localization` | 国际化与本地化模式 | 检测硬编码字符串、翻译管理、RTL 支持 |
| `interactive-portfolio` | 交互式作品集开发 | 开发者/设计师作品集、转化优化 |
| `mobile-design` | 移动优先设计思维 | iOS/Android 触摸交互、平台规范 |
| `scroll-experience` | 沉浸式滚动体验 | 视差、滚动动画、交互叙事 |
| `theme-factory` | 主题工厂工具包 | 10 种预设主题、配色方案 |
| `ui-ux-pro-max` | UI/UX 设计智能 | 50 种风格、97 种配色 |
| `web-artifacts-builder` | Web Artifact 构建器 | 复杂前端 Artifact |
| `web-design-guidelines` | Web 界面设计规范审查 | 可访问性、UX 审计 |

### 🔀 Git 与 GitHub 工作流

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `address-github-comments` | 处理 GitHub PR 评论 | 使用 gh CLI 处理反馈 |
| `changelog-generator` | 自动生成变更日志 | 从 git 提交生成用户友好日志 |
| `finishing-a-development-branch` | 完成开发分支工作流 | 合并、PR、清理选项 |
| `git-pushing` | Git 提交推送工作流 | 常规提交、推送到远程 |
| `github-workflow-automation` | GitHub 工作流自动化 | PR 审查、issue 分类、CI/CD |
| `using-git-worktrees` | Git Worktree 使用指南 | 隔离工作空间、多分支并行 |

### ✍️ 内容创作与写作

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `brainstorming` | 头脑风暴与设计探索 | 功能创建前的需求探索 |
| `content-creator` | SEO 优化营销内容创作 | 博客、社交媒体、品牌声音 |
| `content-research-writer` | 研究写作助手 | 引用、大纲、实时反馈 |
| `copy-editing` | 营销文案编辑 | 编辑、审查、改进现有文案 |
| `copywriting` | 营销文案写作 | 首页、落地页、定价页、CTA 文案 |
| `doc-coauthoring` | 文档协作工作流 | 提案、技术规格、决策文档 |
| `internal-comms` | 内部沟通模板 | 状态报告、3P 更新、FAQ |
| `social-content` | 社交媒体内容创作 | LinkedIn、Twitter、Instagram、TikTok 内容 |

### 📋 规格与计划

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `concise-planning` | 简洁计划生成 | 生成原子化可操作清单 |
| `dispatching-parallel-agents` | 并行 Agent 调度 | 多个独立任务并行处理 |
| `executing-plans` | 执行实现计划 | 按检查点执行计划 |
| `plan-writing` | 结构化任务规划 | 清晰分解、依赖关系、验证标准 |
| `planning-with-files` | 基于文件的计划 | Manus 风格文件规划 |
| `spec-analyze` | 规格一致性分析 | 检查 spec/plan/tasks 一致性 |
| `spec-checklist` | 规格质量检查清单 | 验证需求完整性 |
| `spec-clarify` | 规格澄清问答 | 减少规格歧义 |
| `spec-constitution` | 项目宪法创建 | 核心原则、治理规则 |
| `spec-implement` | 规格实现执行 | 按阶段实现 tasks.md |
| `spec-plan` | 实现计划生成 | 研究、数据模型、契约 |
| `spec-specify` | 特性规格创建 | 自然语言转规格 |
| `spec-tasks` | 任务列表生成 | 按用户故事组织任务 |
| `spec-taskstoissues` | 任务转 GitHub Issues | tasks.md 转 GitHub issue |
| `specify-resources` | 规格驱动开发资源 | 脚本、模板共享资源 |
| `subagent-driven-development` | 子 Agent 驱动开发 | 每任务派发 Agent |
| `writing-plans` | 编写实现计划 | 详细任务分解文档 |

### 🛠️ 实用工具

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `ab-test-setup` | A/B 测试规划与实现 | 分流测试、实验设计、假设验证 |
| `algolia-search` | Algolia 搜索实现 | 索引策略、React InstantSearch、相关性调优 |
| `analytics-tracking` | 分析追踪设置 | GA4、GTM、转化追踪、事件追踪 |
| `app-store-optimization` | 应用商店优化 (ASO) | App Store/Google Play 优化 |
| `clerk-auth` | Clerk 认证集成 | 中间件、组织、Webhook、用户同步 |
| `competitive-ads-extractor` | 竞品广告分析 | 提取分析竞争对手广告 |
| `competitor-alternatives` | 竞品对比页面创建 | 替代方案页、VS 页、竞品比较 |
| `connect` | 连接外部应用 | Gmail、Slack、GitHub 集成 (Composio) |
| `developer-growth-analysis` | 开发者成长分析 | 编码模式、学习资源 |
| `discord-bot-architect` | Discord 机器人开发 | Discord.js、Pycord、斜杠命令、分片 |
| `domain-name-brainstormer` | 域名创意与查询 | 域名头脑风暴、可用性检查 |
| `email-sequence` | 邮件序列优化 | 滴灌营销、欢迎序列、生命周期邮件 |
| `email-systems` | 邮件系统开发 | 事务邮件、营销自动化、送达率 |
| `file-organizer` | 智能文件整理 | 目录清理、重复检测 |
| `form-cro` | 表单转化优化 | 潜在客户表单、联系表单、申请表单 |
| `free-tool-strategy` | 免费工具营销策略 | 工程营销、潜在客户生成工具 |
| `geo-fundamentals` | 生成式引擎优化 (GEO) | AI 搜索引擎优化 (ChatGPT、Claude、Perplexity) |
| `hubspot-integration` | HubSpot CRM 集成 | OAuth、CRM 对象、Webhook、批量操作 |
| `image-enhancer` | 图片质量增强 | 截图清晰度提升 |
| `invoice-organizer` | 发票自动整理 | 税务准备、文件归档 |
| `langsmith-fetch` | LangSmith 跟踪调试 | LangChain/LangGraph 调试 |
| `launch-strategy` | 产品发布策略 | Product Hunt、功能发布、上市策略 |
| `lead-research-assistant` | 潜在客户研究 | 销售线索识别与筛选 |
| `marketing-ideas` | 营销创意库 | 140+ 营销策略与战术 |
| `marketing-psychology` | 营销心理学 | 70+ 心智模型、认知偏见、说服原则 |
| `meeting-insights-analyzer` | 会议洞察分析 | 沟通模式、行为分析 |
| `micro-saas-launcher` | Micro SaaS 快速启动 | 独立开发者、MVP 开发、快速发布 |
| `notebooklm` | NotebookLM 查询助手 | 源基础问答、引用 |
| `notion-template-business` | Notion 模板商业化 | 模板设计、定价、市场销售 |
| `onboarding-cro` | 用户激活优化 | 注册后引导、首次体验、Aha 时刻 |
| `page-cro` | 页面转化优化 | 首页、落地页、定价页转化提升 |
| `paid-ads` | 付费广告投放 | Google Ads、Meta、LinkedIn、PPC 策略 |
| `paywall-upgrade-cro` | 付费墙升级优化 | 应用内付费墙、升级弹窗、功能门控 |
| `personal-tool-builder` | 个人工具开发 | 解决自己问题的工具、CLI 工具、快速原型 |
| `plaid-fintech` | Plaid 金融科技集成 | 银行账户链接、交易同步、ACH |
| `playwright-skill` | Playwright 浏览器自动化 | 网站测试、表单填写 |
| `popup-cro` | 弹窗转化优化 | 退出意图、邮件弹窗、公告横幅 |
| `pricing-strategy` | 定价策略 | 定价研究、层级结构、打包策略 |
| `product-manager-toolkit` | 产品经理工具包 | RICE 优先级、PRD 模板 |
| `programmatic-seo` | 程序化 SEO | 模板页面、规模化 SEO 页面生成 |
| `raffle-winner-picker` | 抽奖随机选择器 | 公平抽奖、赠品活动 |
| `referral-program` | 推荐计划设计 | 推荐奖励、病毒循环、合作伙伴计划 |
| `salesforce-development` | Salesforce 平台开发 | LWC、Apex、REST API、Salesforce DX |
| `schema-markup` | Schema 结构化数据 | JSON-LD、富摘要、FAQ Schema |
| `segment-cdp` | Segment 客户数据平台 | Analytics.js、追踪计划、身份解析 |
| `seo-audit` | SEO 审计 | 技术 SEO、页面 SEO、排名诊断 |
| `seo-fundamentals` | SEO 基础 | E-E-A-T、Core Web Vitals、Google 算法 |
| `shopify-apps` | Shopify 应用开发 | Remix、App Bridge、Polaris、计费 |
| `shopify-development` | Shopify 开发 | Shopify 主题与应用开发 |
| `signup-flow-cro` | 注册流程优化 | 注册转化、试用激活、减少流失 |
| `skill-creator` | Skill 创建指南 | 创建新 skill |
| `skill-developer` | Skill 开发指南 | skill 结构、触发模式 |
| `skill-forge` | Skill 自动化工厂 | 从 GitHub/文档创建 skill |
| `skill-share` | Skill 分享工具 | 创建并分享到 Slack |
| `slack-bot-builder` | Slack 机器人开发 | Bolt 框架、Block Kit、斜杠命令 |
| `slack-gif-creator` | Slack GIF 创建器 | Slack 优化动画 GIF |
| `stripe-integration` | Stripe 支付集成 | 支付、订阅、计费门户、Webhook |
| `tailored-resume-generator` | 定制简历生成 | 职位描述分析、简历优化 |
| `telegram-bot-builder` | Telegram 机器人开发 | Bot API、用户体验、变现策略 |
| `telegram-mini-app` | Telegram Mini App 开发 | TWA、TON 生态、Web App API |
| `template-skill` | Skill 模板 | 新 skill 起始模板 |
| `twilio-communications` | Twilio 通信开发 | SMS、语音通话、WhatsApp、2FA 验证 |
| `upstash-qstash` | Upstash QStash 消息队列 | 无服务器队列、定时任务、HTTP 任务 |
| `video-downloader` | YouTube 视频下载 | 多质量/格式下载 |
| `viral-generator-builder` | 病毒式生成器工具 | 名字生成器、测验、头像创建器 |
| `workflow-automation` | 工作流自动化设计 | 多步骤自动化、API 集成 |
| `zapier-make-patterns` | Zapier/Make 自动化模式 | 无代码自动化、工作流构建 |

### 🔍 代码审查与验证

| Skill 名称 | 简述 | 用法/触发条件 |
|-----------|------|-------------|
| `receiving-code-review` | 接收代码审查 | 技术评估审查反馈 |
| `requesting-code-review` | 请求代码审查 | 完成任务后请求审查 |
| `using-superpowers` | 使用超能力技能 | 会话开始时技能发现 |
| `verification-before-completion` | 完成前验证 | 提交/PR 前运行验证 |
| `writing-skills` | 编写 Skills 指南 | 创建/编辑 skill |

---

## 目录结构

```
~/.claude/skills/
├── skill-name/
│   ├── SKILL.md          # 主技能文件 (必需)
│   ├── LICENSE.txt       # 许可证 (可选)
│   ├── references/       # 参考资料 (可选)
│   └── scripts/          # 辅助脚本 (可选)
└── ...
```

## 快速开始

```bash
# 1. 克隆仓库
git clone https://codeup.aliyun.com/6948c28bf7465fb3044334e2/bi/skills.git ~/.claude/skills

# 2. 在 Claude Code 中使用
claude  # 启动 Claude Code
# 输入 /skill-name 调用特定技能

# 3. 查看可用技能
ls ~/.claude/skills/

# 4. 更新技能库
cd ~/.claude/skills && git pull
```

## 许可证

各 skill 可能有不同的许可证，请查看各 skill 目录下的 LICENSE.txt 文件。

## 贡献

欢迎提交 PR 添加新的 skill 或改进现有 skill！

---

> 📖 本文档最后更新: 2026-01-24 (清理重复 skills)
