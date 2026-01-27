# Claude Skills Collection

这是一个 Claude Code Skills 集合，为 AI 编程助手提供专业化的技能扩展。

---

## 快速安装

```bash
# 一键安装所有 skills
npx add-skill xfstudio/skills

# 安装单个 skill
npx add-skill xfstudio/skills --skill skill-name

# 更新已安装的 skills
npx add-skill xfstudio/skills --update
```

---

## Skills 列表 (256 个)

### 🔐 安全与渗透测试 (32)

| Skill | 简述 |
|-------|------|
| `active-directory-attacks` | AD 攻击技术 (Kerberoasting, DCSync, Pass-the-Hash) |
| `api-fuzzing-bug-bounty` | REST/GraphQL/SOAP API 安全测试 |
| `aws-penetration-testing` | AWS 云环境渗透测试 |
| `broken-authentication` | 身份认证漏洞测试 |
| `burp-suite-testing` | Burp Suite 使用指南 |
| `cc-skill-security-review` | 安全审查检查清单 |
| `ciphey` | 自动密码破解工具 (50+ 加密类型) |
| `cloud-penetration-testing` | 多云平台安全评估 |
| `ethical-hacking-methodology` | 道德黑客方法论 |
| `file-path-traversal` | 目录遍历漏洞测试 |
| `file-uploads` | 文件上传安全处理 |
| `html-injection-testing` | HTML 注入测试 |
| `idor-testing` | IDOR 漏洞测试 |
| `linux-privilege-escalation` | Linux 提权技术 |
| `linux-shell-scripting` | Shell 脚本模板 |
| `metasploit-framework` | Metasploit 使用指南 |
| `network-101` | 网络服务配置基础 |
| `pentest-checklist` | 渗透测试检查清单 |
| `pentest-commands` | 渗透测试命令速查 |
| `privilege-escalation-methods` | 提权方法汇总 |
| `red-team-tactics` | 红队战术 (MITRE ATT&CK) |
| `red-team-tools` | 红队工具与方法论 |
| `scanning-tools` | 安全扫描工具 |
| `shodan-reconnaissance` | Shodan 侦察 |
| `smtp-penetration-testing` | SMTP 安全测试 |
| `sql-injection-testing` | SQL 注入测试 |
| `sqlmap-database-pentesting` | SQLMap 自动化渗透 |
| `ssh-penetration-testing` | SSH 安全测试 |
| `top-web-vulnerabilities` | Top 100 Web 漏洞 |
| `vulnerability-scanner` | 高级漏洞分析 |
| `windows-privilege-escalation` | Windows 提权技术 |
| `wireshark-analysis` | Wireshark 流量分析 |
| `wordpress-penetration-testing` | WordPress 安全评估 |
| `xss-html-injection` | XSS 注入测试 |

### 🤖 AI/LLM 开发 (38)

| Skill | 简述 |
|-------|------|
| `advanced-evaluation` | LLM-as-Judge 评估技术 |
| `agent-evaluation` | Agent 测试与基准评估 |
| `agent-manager-skill` | 多 Agent 管理器 (tmux) |
| `agent-tool-builder` | Agent 工具设计 |
| `ai-agents-architect` | 自主 AI Agent 设计 |
| `ai-product` | AI 产品开发模式 |
| `ai-wrapper-product` | AI API 包装产品 |
| `autonomous-agent-patterns` | 自主 Agent 设计模式 |
| `bdi-mental-states` | BDI 心智状态建模 |
| `blockrun` | 外部模型调用 (Grok/GPT/DALL-E) |
| `computer-use-agents` | 计算机使用 Agent |
| `context-window-management` | 上下文窗口管理 |
| `conversation-memory` | 对话记忆系统 |
| `crewai` | CrewAI 多 Agent 框架 |
| `evaluation` | Agent 系统评估 |
| `hosted-agents` | 托管 Agent 基础设施 |
| `langfuse` | Langfuse LLM 可观测性 |
| `langgraph` | LangGraph 状态化 Agent |
| `llm-app-patterns` | LLM 应用开发模式 |
| `loki-mode` | 多 Agent 自主创业系统 |
| `mcp-builder` | MCP 服务器开发 |
| `memory-systems` | Agent 记忆系统设计 |
| `multi-agent-patterns` | 多 Agent 架构模式 |
| `parallel-agents` | 多 Agent 编排 |
| `project-development` | LLM 项目开发方法论 |
| `prompt-caching` | 提示缓存策略 |
| `prompt-engineering` | 提示工程最佳实践 |
| `prompt-library` | 高质量提示模板库 |
| `rag-engineer` | RAG 系统构建 |
| `rag-implementation` | RAG 实现模式 |
| `ralph-loop` | 自主开发循环 |
| `tool-design` | Agent 工具设计 |
| `voice-agents` | 语音 Agent 开发 |
| `voice-ai-development` | 语音 AI 应用开发 |

### 📚 上下文工程 (5)

| Skill | 简述 |
|-------|------|
| `context-compression` | 上下文压缩策略 |
| `context-degradation` | 上下文退化诊断 |
| `context-fundamentals` | 上下文工程基础 |
| `context-optimization` | 上下文优化技术 |
| `filesystem-context` | 文件系统上下文工程 |

### 💻 代码开发与工程 (75)

| Skill | 简述 |
|-------|------|
| `api-patterns` | API 设计原则 |
| `app-builder` | 全栈应用构建编排器 |
| `architecture` | 架构决策框架 |
| `aws-serverless` | AWS 无服务器开发 |
| `azure-functions` | Azure Functions 开发 |
| `backend-dev-guidelines` | Node.js/Express 后端指南 |
| `backend-patterns` | 后端架构模式 |
| `bash-linux` | Bash/Linux 终端模式 |
| `behavioral-modes` | AI 操作模式 |
| `browser-automation` | 浏览器自动化 |
| `browser-extension-builder` | 浏览器扩展开发 |
| `bullmq-specialist` | BullMQ 队列专家 |
| `bun-development` | Bun 运行时开发 |
| `cc-skill-backend-patterns` | 后端架构模式 |
| `cc-skill-clickhouse-io` | ClickHouse 数据库 |
| `cc-skill-coding-standards` | 通用编码标准 |
| `cc-skill-continuous-learning` | 持续学习技能 |
| `cc-skill-frontend-patterns` | 前端开发模式 |
| `cc-skill-project-guidelines-example` | 项目指南示例 |
| `cc-skill-strategic-compact` | 战略紧凑技能 |
| `clean-code` | 务实编码标准 |
| `claude-code-guide` | Claude Code 使用指南 |
| `clickhouse-io` | ClickHouse 数据库 |
| `code-review-checklist` | 代码审查检查清单 |
| `coding-standards` | 编码标准 |
| `continuous-learning` | 持续学习 |
| `core-components` | 核心组件库 |
| `database-design` | 数据库设计原则 |
| `deployment-procedures` | 生产部署原则 |
| `docker-expert` | Docker 容器化专家 |
| `documentation-templates` | 文档模板 |
| `firebase` | Firebase 后端开发 |
| `frontend-design` | 前端界面设计 |
| `frontend-dev-guidelines` | React/TypeScript 前端指南 |
| `frontend-patterns` | 前端开发模式 |
| `game-development` | 游戏开发编排器 |
| `gcp-cloud-run` | GCP Cloud Run 开发 |
| `graphql` | GraphQL 开发 |
| `inngest` | Inngest 后台任务 |
| `javascript-mastery` | JavaScript 核心概念 |
| `kaizen` | 持续改进指南 |
| `lint-and-validate` | 自动质量控制 |
| `moodle-external-api-development` | Moodle API 开发 |
| `neon-postgres` | Neon 无服务器 Postgres |
| `nestjs-expert` | Nest.js 框架专家 |
| `nextjs-best-practices` | Next.js App Router |
| `nextjs-supabase-auth` | Next.js + Supabase Auth |
| `nodejs-best-practices` | Node.js 开发原则 |
| `performance-profiling` | 性能分析原则 |
| `powershell-windows` | PowerShell Windows |
| `prisma-expert` | Prisma ORM 专家 |
| `python-patterns` | Python 开发模式 |
| `react-best-practices` | React 性能优化 |
| `react-patterns` | 现代 React 模式 |
| `react-ui-patterns` | React UI 模式 |
| `remotion-best-practices` | Remotion 视频创建 |
| `research-engineer` | 学术研究工程师 |
| `security-review` | 安全审查 |
| `senior-architect` | 高级软件架构 |
| `senior-fullstack` | 全栈开发工具包 |
| `server-management` | 服务器管理原则 |
| `software-architecture` | 软件架构指南 |
| `strategic-compact` | 战略紧凑 |
| `systematic-debugging` | 系统化调试 |
| `tailwind-patterns` | Tailwind CSS v4 |
| `test-driven-development` | 测试驱动开发 |
| `test-fixing` | 测试修复工具 |
| `testing-patterns` | Jest 测试模式 |
| `trigger-dev` | Trigger.dev 后台任务 |
| `typescript-expert` | TypeScript 专家 |
| `unzip-crx` | Chrome 扩展解压 |
| `vercel-deployment` | Vercel 部署专家 |
| `webapp-testing` | Web 应用测试 |

### 📄 文档处理 (8)

| Skill | 简述 |
|-------|------|
| `docx` | Word 文档处理 |
| `docx-official` | Word 文档 (官方版) |
| `pdf` | PDF 处理 |
| `pdf-official` | PDF 处理 (官方版) |
| `pptx` | PowerPoint 处理 |
| `pptx-official` | PowerPoint (官方版) |
| `xlsx` | Excel 处理 |
| `xlsx-official` | Excel (官方版) |

### 🎨 设计与 UI/UX (20)

| Skill | 简述 |
|-------|------|
| `3d-web-experience` | 3D Web 体验 (Three.js) |
| `algorithmic-art` | p5.js 算法艺术 |
| `artifacts-builder` | Claude.ai Artifact 构建器 |
| `baoyu-article-illustrator` | 文章配图生成 |
| `baoyu-comic` | 知识漫画创作 |
| `baoyu-cover-image` | 封面图生成 |
| `baoyu-image-gen` | 图像生成 |
| `baoyu-infographic` | 信息图生成 |
| `baoyu-slide-deck` | 幻灯片生成 |
| `baoyu-xhs-images` | 小红书图片生成 |
| `brand-guidelines` | 品牌样式指南 |
| `canvas-design` | 视觉艺术设计 |
| `claude-d3js-skill` | D3.js 数据可视化 |
| `i18n-localization` | 国际化与本地化 |
| `interactive-portfolio` | 交互式作品集 |
| `mobile-design` | 移动优先设计 |
| `scroll-experience` | 沉浸式滚动体验 |
| `theme-factory` | 主题工厂工具包 |
| `ui-ux-pro-max` | UI/UX 设计智能 |
| `web-artifacts-builder` | Web Artifact 构建器 |
| `web-design-guidelines` | Web 设计规范 |

### 🔀 Git 与 GitHub (6)

| Skill | 简述 |
|-------|------|
| `address-github-comments` | 处理 GitHub PR 评论 |
| `changelog-generator` | 自动生成变更日志 |
| `finishing-a-development-branch` | 完成开发分支 |
| `git-pushing` | Git 提交推送 |
| `github-workflow-automation` | GitHub 工作流自动化 |
| `using-git-worktrees` | Git Worktree 使用 |

### ✍️ 内容创作 (10)

| Skill | 简述 |
|-------|------|
| `brainstorming` | 头脑风暴与设计探索 |
| `content-creator` | SEO 营销内容创作 |
| `content-research-writer` | 研究写作助手 |
| `copy-editing` | 营销文案编辑 |
| `copywriting` | 营销文案写作 |
| `doc-coauthoring` | 文档协作工作流 |
| `internal-comms` | 内部沟通模板 |
| `social-content` | 社交媒体内容 |

### 📋 规格与计划 (18)

| Skill | 简述 |
|-------|------|
| `concise-planning` | 简洁计划生成 |
| `dispatching-parallel-agents` | 并行 Agent 调度 |
| `executing-plans` | 执行实现计划 |
| `plan-writing` | 结构化任务规划 |
| `planning-with-files` | 基于文件的计划 |
| `spec-analyze` | 规格一致性分析 |
| `spec-checklist` | 规格质量检查 |
| `spec-clarify` | 规格澄清问答 |
| `spec-constitution` | 项目宪法创建 |
| `spec-implement` | 规格实现执行 |
| `spec-plan` | 实现计划生成 |
| `spec-specify` | 特性规格创建 |
| `spec-tasks` | 任务列表生成 |
| `spec-taskstoissues` | 任务转 GitHub Issues |
| `specify-resources` | 规格驱动开发资源 |
| `subagent-driven-development` | 子 Agent 驱动开发 |
| `writing-plans` | 编写实现计划 |

### 🛠️ 实用工具 (70+)

| Skill | 简述 |
|-------|------|
| `ab-test-setup` | A/B 测试规划 |
| `algolia-search` | Algolia 搜索实现 |
| `analytics-tracking` | 分析追踪设置 |
| `app-store-optimization` | 应用商店优化 |
| `baoyu-compress-image` | 图片压缩 |
| `baoyu-danger-gemini-web` | Gemini Web 工具 |
| `baoyu-danger-x-to-markdown` | X/Twitter 转 Markdown |
| `baoyu-post-to-wechat` | 发布到微信 |
| `baoyu-post-to-x` | 发布到 X/Twitter |
| `baoyu-url-to-markdown` | URL 转 Markdown |
| `clerk-auth` | Clerk 认证集成 |
| `competitive-ads-extractor` | 竞品广告分析 |
| `competitor-alternatives` | 竞品对比页面 |
| `connect` | 连接外部应用 |
| `developer-growth-analysis` | 开发者成长分析 |
| `discord-bot-architect` | Discord 机器人 |
| `domain-name-brainstormer` | 域名创意 |
| `email-sequence` | 邮件序列优化 |
| `email-systems` | 邮件系统开发 |
| `file-organizer` | 智能文件整理 |
| `find-skills` | 技能搜索 |
| `form-cro` | 表单转化优化 |
| `free-tool-strategy` | 免费工具营销 |
| `geo-fundamentals` | 生成式引擎优化 |
| `hubspot-integration` | HubSpot CRM 集成 |
| `image-enhancer` | 图片质量增强 |
| `invoice-organizer` | 发票自动整理 |
| `langsmith-fetch` | LangSmith 调试 |
| `launch-strategy` | 产品发布策略 |
| `lead-research-assistant` | 潜在客户研究 |
| `marketing-ideas` | 营销创意库 |
| `marketing-psychology` | 营销心理学 |
| `meeting-insights-analyzer` | 会议洞察分析 |
| `micro-saas-launcher` | Micro SaaS 启动 |
| `notebooklm` | NotebookLM 助手 |
| `notion-template-business` | Notion 模板商业化 |
| `onboarding-cro` | 用户激活优化 |
| `page-cro` | 页面转化优化 |
| `paid-ads` | 付费广告投放 |
| `paywall-upgrade-cro` | 付费墙升级优化 |
| `personal-tool-builder` | 个人工具开发 |
| `plaid-fintech` | Plaid 金融科技 |
| `playwright-skill` | Playwright 自动化 |
| `popup-cro` | 弹窗转化优化 |
| `pricing-strategy` | 定价策略 |
| `product-manager-toolkit` | 产品经理工具包 |
| `programmatic-seo` | 程序化 SEO |
| `raffle-winner-picker` | 抽奖选择器 |
| `referral-program` | 推荐计划设计 |
| `release-skills` | 技能发布 |
| `salesforce-development` | Salesforce 开发 |
| `schema-markup` | Schema 结构化数据 |
| `segment-cdp` | Segment CDP |
| `seo-audit` | SEO 审计 |
| `seo-fundamentals` | SEO 基础 |
| `shopify-apps` | Shopify 应用开发 |
| `shopify-development` | Shopify 开发 |
| `signup-flow-cro` | 注册流程优化 |
| `skill-creator` | Skill 创建指南 |
| `skill-developer` | Skill 开发指南 |
| `skill-forge` | Skill 自动化工厂 |
| `skill-share` | Skill 分享工具 |
| `slack-bot-builder` | Slack 机器人 |
| `slack-gif-creator` | Slack GIF 创建 |
| `stripe-integration` | Stripe 支付集成 |
| `tailored-resume-generator` | 定制简历生成 |
| `telegram-bot-builder` | Telegram 机器人 |
| `telegram-mini-app` | Telegram Mini App |
| `template-skill` | Skill 模板 |
| `twilio-communications` | Twilio 通信开发 |
| `upstash-qstash` | Upstash QStash |
| `video-downloader` | YouTube 视频下载 |
| `viral-generator-builder` | 病毒式生成器 |
| `workflow-automation` | 工作流自动化 |
| `zapier-make-patterns` | Zapier/Make 自动化 |

### 🔍 代码审查与验证 (5)

| Skill | 简述 |
|-------|------|
| `receiving-code-review` | 接收代码审查 |
| `requesting-code-review` | 请求代码审查 |
| `using-superpowers` | 使用超能力技能 |
| `verification-before-completion` | 完成前验证 |
| `writing-skills` | 编写 Skills 指南 |

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

> 📖 本文档最后更新: 2026-01-27
