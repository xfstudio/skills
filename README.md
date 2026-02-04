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

## Skills 分类目录 (698 个)

### 主要分类概览

| 分类 | 数量 | 主要内容 |
|------|------|---------|
| 🤖 AI 与智能代理 | 51 | LLM 应用、RAG、代理架构、提示工程 |
| 🏗️ 架构与设计 | 35 | 系统架构、微服务、事件驱动、DDD |
| 🔐 安全与渗透测试 | 50 | 漏洞扫描、渗透测试、安全审计 |
| 💾 数据库与数据工程 | 24 | SQL/NoSQL、数据管道、向量数据库 |
| 🎨 前端开发 | 34 | React、Next.js、UI/UX、组件库 |
| ⚙️ 后端开发 | 36 | API 设计、微服务、认证、消息队列 |
| 📱 移动开发 | 8 | React Native、Flutter、iOS/Android |
| ☁️ 云与 DevOps | 39 | K8s、CI/CD、监控、IaC、GitOps |
| 🧪 测试与质量 | 41 | TDD、E2E、代码审查、性能测试 |
| 📊 数据与可视化 | 12 | 数据可视化、BI、ML、量化分析 |
| 🎮 游戏开发 | 11 | Unity、Unreal、Godot、ECS |
| 📝 文档与内容 | 25 | 技术写作、API 文档、营销文案 |
| 🔧 工具与自动化 | 50 | CLI、脚本、爬虫、文件处理 |
| 🌐 Web3 区块链 | 3 | 智能合约、DeFi、NFT |
| 💼 产品与营销 | 37 | 产品管理、增长、定价、SEO |
| 🎓 学习与知识 | 9 | 研究工具、笔记系统 |
| 🔍 搜索与 SEO | 7 | 搜索优化、关键词、内容策略 |
| 💬 通信与社交 | 10 | 聊天机器人、社交媒体自动化 |
| 🖼️ 图像与创意 | 25 | AI 绘画、图像处理、设计 |
| 📦 编程语言 | 28 | Python、Rust、Go、TypeScript |
| 🔄 其他专业 | 163 | HR、法律、财务、行业特定 |

**总计：698 个专业技能**

---

## 📚 详细技能清单

### 🤖 AI 与智能代理 (51个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `agent-evaluation` | Testing and benchmarking LLM agents including behavioral ... | agent testing, agent evaluation, benchmark agents, agent ... |
| `agent-manager-skill` | Manage multiple local CLI agents via tmux sessions (start... |  |
| `agent-memory-mcp` | A hybrid memory system that provides persistent, searchab... |  |
| `agent-memory-systems` | Memory is the cornerstone of intelligent agents. Without ... |  |
| `agent-orchestration-improve-agent` | Systematic improvement of existing agents through perform... |  |
| `agent-orchestration-multi-agent-optimize` | Optimize multi-agent systems with coordinated profiling, ... | improving agent performance, throughput, or reliability |
| `agent-tool-builder` | Tools are how AI agents interact with the world. A well-d... |  |
| `ai-agents-architect` | Expert in designing and building autonomous AI agents. Ma... | build agent, AI agent, autonomous agent, tool use, functi... |
| `ai-engineer` | Build production-ready LLM applications, advanced RAG sys... |  |
| `ai-product` | Every product will be AI-powered. The question is whether... | keywords, file_patterns, code_patterns |
| `ai-wrapper-product` | Expert in building products that wrap AI APIs (OpenAI, An... | AI wrapper, GPT product, AI tool, wrap AI, AI SaaS |
| `autonomous-agent-patterns` | Design patterns for building autonomous coding agents. Co... | building AI agents, designing tool APIs, implementing per... |
| `autonomous-agents` | Autonomous agents are AI systems that can independently d... |  |
| `bullmq-specialist` | BullMQ expert for Redis-backed job queues, background pro... | bullmq, bull queue, redis queue, background job, job queue |
| `code-review-ai-ai-review` | You are an expert AI-powered code review specialist combi... |  |
| `computer-use-agents` | Build AI agents that interact with computers like humans ... | computer use, desktop automation agent, screen control AI... |
| `conversation-memory` | Persistent memory systems for LLM conversations including... | conversation memory, remember, memory persistence, long-t... |
| `crewai` | Expert in CrewAI - the leading role-based multi-agent fra... | crewai, multi-agent team, agent roles, crew of agents, ro... |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked o... | facing 2+ independent tasks that can be worked on without... |
| `embedding-strategies` | Select and optimize embedding models for semantic search ... | choosing embedding models, implementing chunking strategi... |
| `error-debugging-multi-agent-review` | Use when working with error debugging multi agent review | working with error debugging multi agent review |
| `fp-ts-pragmatic` | A practical, jargon-free guide to fp-ts functional progra... | writing TypeScript with fp-ts library |
| `hosted-agents` | This skill should be used when the user asks to "build ba... | the user asks to "build background agent", "create hosted... |
| `langchain-architecture` | Design LLM applications using the LangChain framework wit... | building LangChain applications, implementing AI agents, ... |
| `langgraph` | Expert in LangGraph - the production-grade framework for ... | langgraph, langchain agent, stateful agent, agent graph, ... |
| `llm-app-patterns` | Production-ready patterns for building LLM applications. ... | designing AI applications, implementing RAG, building age... |
| `llm-application-dev-ai-assistant` | You are an AI assistant development expert specializing i... |  |
| `llm-application-dev-langchain-agent` | You are an expert LangChain agent developer specializing ... |  |
| `llm-application-dev-prompt-optimize` | You are an expert prompt engineer specializing in craftin... |  |
| `llm-evaluation` | Implement comprehensive evaluation strategies for LLM app... | testing LLM performance, measuring AI application quality... |
| `memory-forensics` | Master memory forensics techniques including memory acqui... | analyzing memory dumps, investigating incidents, or perfo... |
| `memory-safety-patterns` | Implement memory-safe programming with RAII, ownership, s... | writing safe systems code, managing resources, or prevent... |
| `memory-systems` | Design short-term, long-term, and graph-based memory arch... |  |
| `multi-agent-brainstorming` | > |  |
| `multi-agent-patterns` | Master orchestrator, peer-to-peer, and hierarchical multi... |  |
| `parallel-agents` | Multi-agent orchestration patterns. Use when multiple ind... | multiple independent tasks can run with different domain ... |
| `performance-testing-review-ai-review` | You are an expert AI-powered code review specialist combi... |  |
| `performance-testing-review-multi-agent-review` | Use when working with performance testing review multi ag... | working with performance testing review multi agent review |
| `prompt-caching` | Caching strategies for LLM prompts including Anthropic pr... | prompt caching, cache prompt, response cache, cag, cache ... |
| `prompt-engineer` | Expert prompt engineer specializing in advanced prompting |  |
| `prompt-engineering` | Expert guide on prompt engineering patterns, best practic... | user wants to improve prompts, learn prompting strategies... |
| `prompt-engineering-patterns` | Master advanced prompt engineering techniques to maximize... | optimizing prompts, improving LLM outputs, or designing p... |
| `prompt-library` | Curated collection of high-quality prompts for various us... | user needs prompt templates, role-play prompts, or ready-... |
| `rag-engineer` | Expert in building Retrieval-Augmented Generation systems... | building RAG, vector search, embeddings, semantic search,... |
| `rag-implementation` | Build Retrieval-Augmented Generation (RAG) systems for LL... | implementing knowledge-grounded AI, building document Q&A... |
| `subagent-driven-development` | Use when executing implementation plans with independent ... | executing implementation plans with independent tasks in ... |
| `vector-database-engineer` | Expert in vector databases, embedding strategies, and sem... |  |
| `vector-index-tuning` | Optimize vector index performance for latency, recall, an... | tuning HNSW parameters, selecting quantization strategies... |
| `voice-agents` | Voice agents represent the frontier of AI interaction - h... |  |
| `voice-ai-development` | Expert in building voice AI applications - from real-time... | voice ai, voice agent, speech to text, text to speech, re... |
| `voice-ai-engine-development` | Build real-time conversational AI voice engines using asy... |  |

### 🏗️ 架构与设计 (35个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `api-design-principles` | Master REST and GraphQL API design principles to build in... | designing new APIs, reviewing API specifications, or esta... |
| `architect-review` | Master software architect specializing in modern architec... |  |
| `architecture` | Architectural decision-making framework. Requirements ana... | making architecture decisions or analyzing system design |
| `architecture-decision-records` | Write and maintain Architecture Decision Records (ADRs) f... | documenting significant technical decisions, reviewing pa... |
| `architecture-patterns` | Implement proven backend architecture patterns including ... | architecting complex backend systems or refactoring exist... |
| `backend-architect` | Expert backend architect specializing in scalable API des... |  |
| `c4-architecture-c4-architecture` | Generate comprehensive C4 architecture documentation for ... |  |
| `c4-code` | Expert C4 Code-level documentation specialist. Analyzes code |  |
| `c4-component` | Expert C4 Component-level documentation specialist. Synth... |  |
| `c4-container` | Expert C4 Container-level documentation specialist. Synth... |  |
| `c4-context` | Expert C4 Context-level documentation specialist. Creates |  |
| `cloud-architect` | Expert cloud architect specializing in AWS/Azure/GCP mult... |  |
| `cqrs-implementation` | Implement Command Query Responsibility Segregation for sc... | separating read and write models, optimizing query perfor... |
| `database-architect` | Expert database architect specializing in data layer desi... |  |
| `design-md` | Analyze Stitch projects and synthesize a semantic design ... |  |
| `design-orchestration` | > |  |
| `discord-bot-architect` | Specialized skill for building production-ready Discord b... |  |
| `docs-architect` | Creates comprehensive technical documentation from existing |  |
| `dotnet-architect` | Expert .NET backend architect specializing in C#, ASP.NET... |  |
| `event-sourcing-architect` | Expert in event sourcing, CQRS, and event-driven architec... |  |
| `graphql-architect` | Master modern GraphQL with federation, performance optimi... |  |
| `hybrid-cloud-architect` | Expert hybrid cloud architect specializing in complex mul... |  |
| `kubernetes-architect` | Expert Kubernetes architect specializing in cloud-native |  |
| `microservices-patterns` | Design microservices architectures with service boundarie... | building distributed systems, decomposing monoliths, or i... |
| `monorepo-architect` | Expert in monorepo architecture, build systems, and depen... |  |
| `monorepo-management` | Master monorepo management with Turborepo, Nx, and pnpm w... | setting up monorepos, optimizing builds, or managing shar... |
| `multi-cloud-architecture` | Design multi-cloud architectures using a decision framewo... | building multi-cloud systems, avoiding vendor lock-in, or... |
| `radix-ui-design-system` | Build accessible design systems with Radix UI primitives.... |  |
| `react-native-architecture` | Build production React Native apps with Expo, navigation,... | developing mobile apps, implementing native integrations,... |
| `saga-orchestration` | Implement saga patterns for distributed transactions and ... | coordinating multi-step business processes, handling comp... |
| `senior-architect` | Comprehensive software architecture skill for designing s... | designing system architecture, making technical decisions... |
| `seo-structure-architect` | Analyzes and optimizes content structure including header |  |
| `software-architecture` | Guide for quality focused software architecture. This ski... | users want to write code, design architecture, analyze co... |
| `tailwind-design-system` | Build scalable design systems with Tailwind CSS, design t... | creating component libraries, implementing design systems... |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. U... | asked to "review my UI", "check accessibility", "audit de... |

### 🔐 安全与渗透测试 (50个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `active-directory-attacks` | This skill should be used when the user asks to "attack A... | the user asks to "attack Active Directory", "exploit AD",... |
| `api-fuzzing-bug-bounty` | This skill should be used when the user asks to "test API... | the user asks to "test API security", "fuzz APIs", "find ... |
| `api-security-best-practices` | Implement secure API design patterns including authentica... |  |
| `attack-tree-construction` | Build comprehensive attack trees to visualize threat path... | mapping attack scenarios, identifying defense gaps, or co... |
| `aws-penetration-testing` | This skill should be used when the user asks to "pentest ... | the user asks to "pentest AWS", "test AWS security", "enu... |
| `backend-security-coder` | Expert in secure backend coding practices specializing in... |  |
| `broken-authentication` | This skill should be used when the user asks to "test for... | the user asks to "test for broken authentication vulnerab... |
| `burp-suite-testing` | This skill should be used when the user asks to "intercep... | the user asks to "intercept HTTP traffic", "modify web re... |
| `cc-skill-security-review` | Use this skill when adding authentication, handling user ... |  |
| `ciphey` | Automatic decryption and decoding tool using AI. Use when... | user says "解密", "decrypt", "decode", "crack", "破解密码", or ... |
| `cloud-penetration-testing` | This skill should be used when the user asks to "perform ... | the user asks to "perform cloud penetration testing", "as... |
| `ethical-hacking-methodology` | This skill should be used when the user asks to "learn et... | the user asks to "learn ethical hacking", "understand pen... |
| `ffuf-claude-skill` | Web fuzzing with ffuf |  |
| `file-path-traversal` | This skill should be used when the user asks to "test for... | the user asks to "test for directory traversal", "exploit... |
| `frontend-mobile-security-xss-scan` | You are a frontend security specialist focusing on Cross-... |  |
| `frontend-security-coder` | Expert in secure frontend coding practices specializing i... |  |
| `html-injection-testing` | This skill should be used when the user asks to "test for... | the user asks to "test for HTML injection", "inject HTML ... |
| `idor-testing` | This skill should be used when the user asks to "test for... | the user asks to "test for insecure direct object referen... |
| `k8s-security-policies` | Implement Kubernetes security policies including NetworkP... | securing Kubernetes clusters, implementing network isolat... |
| `linux-privilege-escalation` | This skill should be used when the user asks to "escalate... | the user asks to "escalate privileges on Linux", "find pr... |
| `malware-analyst` | Expert malware analyst specializing in defensive malware ... |  |
| `metasploit-framework` | This skill should be used when the user asks to "use Meta... | the user asks to "use Metasploit for penetration testing"... |
| `mobile-security-coder` | Expert in secure mobile coding practices specializing in ... |  |
| `pentest-checklist` | This skill should be used when the user asks to "plan a p... | the user asks to "plan a penetration test", "create a sec... |
| `pentest-commands` | This skill should be used when the user asks to "run pent... | the user asks to "run pentest commands", "scan with nmap"... |
| `privilege-escalation-methods` | This skill should be used when the user asks to "escalate... | the user asks to "escalate privileges", "get root access"... |
| `red-team-tactics` | Red team tactics principles based on MITRE ATT&CK. Attack... |  |
| `red-team-tools` | This skill should be used when the user asks to "follow r... | the user asks to "follow red team methodology", "perform ... |
| `scanning-tools` | This skill should be used when the user asks to "perform ... | the user asks to "perform vulnerability scanning", "scan ... |
| `security-auditor` | Expert security auditor specializing in DevSecOps, compre... |  |
| `security-bluebook-builder` | Build security Blue Books for sensitive apps |  |
| `security-compliance-compliance-check` | You are a compliance expert specializing in regulatory re... |  |
| `security-requirement-extraction` | Derive security requirements from threat models and busin... | translating threats into actionable requirements, creatin... |
| `security-review` | Use this skill when adding authentication, handling user ... |  |
| `security-scanning-security-dependencies` | You are a security expert specializing in dependency vuln... |  |
| `security-scanning-security-hardening` | Coordinate multi-layer security scanning and hardening ac... |  |
| `security-scanning-security-sast` | Static Application Security Testing (SAST) for code vulne... |  |
| `shodan-reconnaissance` | This skill should be used when the user asks to "search f... | the user asks to "search for exposed devices on the inter... |
| `smtp-penetration-testing` | This skill should be used when the user asks to "perform ... | the user asks to "perform SMTP penetration testing", "enu... |
| `solidity-security` | Master smart contract security best practices to prevent ... | writing smart contracts, auditing existing contracts, or ... |
| `sql-injection-testing` | This skill should be used when the user asks to "test for... | the user asks to "test for SQL injection vulnerabilities"... |
| `sqlmap-database-pentesting` | This skill should be used when the user asks to "automate... | the user asks to "automate SQL injection testing," "enume... |
| `ssh-penetration-testing` | This skill should be used when the user asks to "pentest ... | the user asks to "pentest SSH services", "enumerate SSH c... |
| `threat-mitigation-mapping` | Map identified threats to appropriate security controls a... | prioritizing security investments, creating remediation p... |
| `threat-modeling-expert` | Expert in threat modeling methodologies, security archite... |  |
| `vulnerability-scanner` | Advanced vulnerability analysis principles. OWASP 2025, S... |  |
| `windows-privilege-escalation` | This skill should be used when the user asks to "escalate... | the user asks to "escalate privileges on Windows," "find ... |
| `wireshark-analysis` | This skill should be used when the user asks to "analyze ... | the user asks to "analyze network traffic with Wireshark"... |
| `wordpress-penetration-testing` | This skill should be used when the user asks to "pentest ... | the user asks to "pentest WordPress sites", "scan WordPre... |
| `xss-html-injection` | This skill should be used when the user asks to "test for... | the user asks to "test for XSS vulnerabilities", "perform... |

### 💾 数据库与数据工程 (24个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `airflow-dag-patterns` | Build production Apache Airflow DAGs with best practices ... | creating data pipelines, orchestrating workflows, or sche... |
| `cc-skill-clickhouse-io` | ClickHouse database patterns, query optimization, analyti... |  |
| `clickhouse-io` | ClickHouse database patterns, query optimization, analyti... |  |
| `data-engineer` | Build scalable data pipelines, modern data warehouses, and |  |
| `data-engineering-data-driven-feature` | Build features guided by data insights, A/B testing, and ... |  |
| `data-engineering-data-pipeline` | You are a data pipeline architecture expert specializing ... |  |
| `data-quality-frameworks` | Implement data quality validation with Great Expectations... | building data quality pipelines, implementing validation ... |
| `database-admin` | Expert database administrator specializing in modern cloud |  |
| `database-cloud-optimization-cost-optimize` | You are a cloud cost optimization expert specializing in ... |  |
| `database-design` | Database design principles and decision-making. Schema de... |  |
| `database-migration` | Execute database migrations across ORMs and platforms wit... | migrating databases, changing schemas, performing data tr... |
| `database-migrations-migration-observability` | Migration monitoring, CDC, and observability infrastructure |  |
| `database-migrations-sql-migrations` | SQL database migrations with zero-downtime strategies for |  |
| `database-optimizer` | Expert database optimizer specializing in modern performance |  |
| `dbt-transformation-patterns` | Master dbt (data build tool) for analytics engineering wi... | building data transformations, creating data models, or i... |
| `neon-postgres` | Expert patterns for Neon serverless Postgres, branching, ... | neon database, serverless postgres, database branching, n... |
| `nosql-expert` | Expert guidance for distributed NoSQL databases (Cassandr... |  |
| `postgres-best-practices` | Postgres performance optimization and best practices from... |  |
| `postgresql` | Design a PostgreSQL-specific schema. Covers best-practice... |  |
| `prisma-expert` | Prisma ORM expert for schema design, migrations, query op... |  |
| `spark-optimization` | Optimize Apache Spark jobs with partitioning, caching, sh... | improving Spark performance, debugging slow jobs, or scal... |
| `sql-optimization-patterns` | Master SQL query optimization, indexing strategies, and E... | debugging slow queries, designing database schemas, or op... |
| `sql-pro` | Master modern SQL with cloud-native databases, OLTP/OLAP |  |
| `using-neon` | Guides and best practices for working with Neon Serverles... |  |

### 🎨 前端开发 (34个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `a2ui-embed` | Write HTML visualizations to the A2UI panel or embed runn... |  |
| `angular` | >- |  |
| `angular-best-practices` | Angular performance optimization and best practices guide... | writing, reviewing, or refactoring Angular code for optim... |
| `angular-migration` | Migrate from AngularJS to Angular using hybrid mode, incr... | upgrading AngularJS applications, planning framework migr... |
| `angular-state-management` | Master modern Angular state management with Signals, NgRx... | setting up global state, managing component stores, choos... |
| `angular-ui-patterns` | Modern Angular UI patterns for loading states, error hand... | building UI components, handling async data, or managing ... |
| `cc-skill-frontend-patterns` | Frontend development patterns for React, Next.js, state m... |  |
| `core-components` | Core component library and design system patterns. Use wh... | building UI, using design tokens, or working with the com... |
| `expo-tailwind-setup` | Set up Tailwind CSS v4 in Expo with react-native-css and ... |  |
| `frontend-design` | Create distinctive, production-grade frontend interfaces ... | building or styling web UIs, components, pages, dashboard... |
| `frontend-dev-guidelines` | Opinionated frontend development standards for modern Rea... |  |
| `frontend-developer` | Build React components, implement responsive layouts, and... |  |
| `frontend-mobile-development-component-scaffold` | You are a React component architecture expert specializin... |  |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state m... |  |
| `frontend-slides` | Create stunning, animation-rich HTML presentations from s... | the user wants to build a presentation, convert a PPT/PPT... |
| `linux-shell-scripting` | This skill should be used when the user asks to "create b... | the user asks to "create bash scripts", "automate Linux t... |
| `nextjs-app-router-patterns` | Master Next.js 14+ App Router with Server Components, str... | building Next |
| `nextjs-best-practices` | Next.js App Router principles. Server Components, data fe... |  |
| `nextjs-supabase-auth` | Expert integration of Supabase Auth with Next.js App Rout... | supabase auth next, authentication next |
| `react-best-practices` | React and Next.js performance optimization guidelines fro... | writing, reviewing, or refactoring React/Next |
| `react-modernization` | Upgrade React applications to latest versions, migrate fr... | modernizing React codebases, migrating to React Hooks, or... |
| `react-patterns` | Modern React patterns and principles. Hooks, composition,... |  |
| `react-state-management` | Master modern React state management with Redux Toolkit, ... | setting up global state, managing server state, or choosi... |
| `react-ui-patterns` | Modern React UI patterns for loading states, error handli... | building UI components, handling async data, or managing ... |
| `scroll-experience` | Expert in building immersive scroll-driven experiences - ... | scroll animation, parallax, scroll storytelling, interact... |
| `stitch-ui-design` | Expert guide for creating effective prompts for Google St... | user wants to design UI/UX in Stitch, create app interfac... |
| `swiftui-expert-skill` | Write, review, or improve SwiftUI code following best pra... | building new SwiftUI features, refactoring existing views... |
| `tailwind-patterns` | Tailwind CSS v4 principles. CSS-first configuration, cont... |  |
| `ui-skills` | Opinionated, evolving constraints to guide agents when bu... |  |
| `ui-ux-designer` | Create interface designs, wireframes, and design systems.... |  |
| `ui-ux-pro-max` | UI/UX design intelligence. 50 styles, 21 palettes, 50 fon... |  |
| `ui-visual-validator` | Rigorous visual validation expert specializing in UI test... |  |
| `vercel-react-best-practices` | React and Next.js performance optimization guidelines fro... | writing, reviewing, or refactoring React/Next |
| `vercel-react-native-skills` | React Native and Expo best practices for building perform... |  |

### ⚙️ 后端开发 (36个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `api-documentation-generator` | Generate comprehensive, developer-friendly API documentat... |  |
| `api-documenter` | Master API documentation with OpenAPI 3.1, AI-powered too... |  |
| `api-patterns` | API design principles and decision-making. REST vs GraphQ... |  |
| `api-testing-observability-api-mock` | You are an API mocking expert specializing in realistic m... |  |
| `auth-implementation-patterns` | Master authentication and authorization patterns includin... | implementing auth systems, securing APIs, or debugging se... |
| `backend-dev-guidelines` | Opinionated backend development standards for Node.js + E... |  |
| `backend-development-feature-development` | Orchestrate end-to-end backend feature development from r... | coordinating multi-phase feature delivery across teams an... |
| `backend-patterns` | Backend architecture patterns, API design, database optim... |  |
| `billing-automation` | Build automated billing systems for recurring payments, i... | implementing subscription billing, automating invoicing, ... |
| `cc-skill-backend-patterns` | Backend architecture patterns, API design, database optim... |  |
| `clerk-auth` | Expert patterns for Clerk auth implementation, middleware... | adding authentication, clerk auth, user authentication, s... |
| `django-pro` | Master Django 5.x with async views, DRF, Celery, and Django |  |
| `dotnet-backend-patterns` | Master C#/.NET backend development patterns for building ... | developing |
| `expo-api-routes` | Guidelines for creating API routes in Expo Router with EA... |  |
| `fastapi-pro` | Build high-performance async APIs with FastAPI, SQLAlchem... |  |
| `fastapi-templates` | Create production-ready FastAPI projects with async patte... | building new FastAPI applications or setting up backend A... |
| `firebase` | Firebase gives you a complete backend in minutes - auth, ... |  |
| `graphql` | GraphQL gives clients exactly the data they need - no mor... |  |
| `hubspot-integration` | Expert patterns for HubSpot CRM integration including OAu... | hubspot, hubspot api, hubspot crm, hubspot integration, c... |
| `inngest` | Inngest expert for serverless-first background jobs, even... | inngest, serverless background job, event-driven workflow... |
| `moodle-external-api-development` | Create custom external web service APIs for Moodle LMS. U... | implementing web services for course management, user tra... |
| `nestjs-expert` | Nest.js framework expert specializing in module architect... |  |
| `nodejs-backend-patterns` | Build production-ready Node.js backend services with Expr... | creating Node |
| `nodejs-best-practices` | Node.js development principles and decision-making. Frame... |  |
| `openapi-spec-generation` | Generate and maintain OpenAPI 3.1 specifications from cod... | creating API documentation, generating SDKs, or ensuring ... |
| `payment-integration` | Integrate Stripe, PayPal, and payment processors. Handles... |  |
| `paypal-integration` | Integrate PayPal payment processing with support for expr... | implementing PayPal payments, processing online transacti... |
| `plaid-fintech` | Expert patterns for Plaid API integration including Link ... | plaid, bank account linking, bank connection, ach, accoun... |
| `salesforce-development` | Expert patterns for Salesforce platform development inclu... | salesforce, sfdc, apex, lwc, lightning web components |
| `segment-cdp` | Expert patterns for Segment Customer Data Platform includ... | segment, analytics |
| `shopify-apps` | Expert patterns for Shopify app development including Rem... | shopify app, shopify, embedded app, polaris, app bridge |
| `shopify-development` | \| |  |
| `stripe-integration` | Implement Stripe payment processing for robust, PCI-compl... | integrating Stripe payments, building subscription system... |
| `temporal-python-pro` | Master Temporal workflow orchestration with Python SDK. I... |  |
| `temporal-python-testing` | Test Temporal workflows with pytest, time-skipping, and m... | implementing Temporal workflow tests or debugging test fa... |
| `trigger-dev` | Trigger.dev expert for background jobs, AI workflows, and... | trigger |

### 📱 移动开发 (8个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `app-store-optimization` | Complete App Store Optimization (ASO) toolkit for researc... |  |
| `expo-cicd-workflows` | Helps understand and write EAS workflow YAML files for Ex... |  |
| `expo-deployment` | Deploy Expo apps to production |  |
| `expo-dev-client` | Build and distribute Expo development clients locally or ... |  |
| `flutter-expert` | Master Flutter development with Dart 3, advanced widgets,... |  |
| `ios-developer` | Develop native iOS applications with Swift/SwiftUI. Maste... |  |
| `mobile-design` | Mobile-first design and engineering doctrine for iOS and ... |  |
| `mobile-developer` | Develop React Native, Flutter, or native mobile apps with... |  |

### ☁️ 云与 DevOps (39个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `aws-serverless` | Specialized skill for building production-ready serverles... |  |
| `aws-skills` | AWS development with infrastructure automation and cloud ... |  |
| `azure-functions` | Expert patterns for Azure Functions development including... | azure function, azure functions, durable functions, azure... |
| `cicd-automation-workflow-automate` | You are a workflow automation expert specializing in crea... |  |
| `cost-optimization` | Optimize cloud costs through resource rightsizing, taggin... | reducing cloud expenses, analyzing infrastructure costs, ... |
| `deployment-engineer` | Expert deployment engineer specializing in modern CI/CD p... |  |
| `deployment-pipeline-design` | Design multi-stage CI/CD pipelines with approval gates, s... | architecting deployment workflows, setting up continuous ... |
| `deployment-procedures` | Production deployment principles and decision-making. Saf... |  |
| `deployment-validation-config-validate` | You are a configuration management expert specializing in... |  |
| `devops-troubleshooter` | Expert DevOps troubleshooter specializing in rapid incident |  |
| `docker-expert` | Docker containerization expert with deep knowledge of mul... |  |
| `gcp-cloud-run` | Specialized skill for building production-ready serverles... |  |
| `github-actions-templates` | Create production-ready GitHub Actions workflows for auto... | setting up CI/CD with GitHub Actions, automating developm... |
| `gitlab-ci-patterns` | Build GitLab CI/CD pipelines with multi-stage workflows, ... | implementing GitLab CI/CD, optimizing pipeline performanc... |
| `gitops-workflow` | Implement GitOps workflows with ArgoCD and Flux for autom... | implementing GitOps practices, automating Kubernetes depl... |
| `grafana-dashboards` | Create and manage production Grafana dashboards for real-... | building monitoring dashboards, visualizing metrics, or c... |
| `helm-chart-scaffolding` | Design, organize, and manage Helm charts for templating a... | creating Helm charts, packaging Kubernetes applications, ... |
| `hybrid-cloud-networking` | Configure secure, high-performance connectivity between o... | building hybrid cloud architectures, connecting data cent... |
| `incident-responder` | Expert SRE incident responder specializing in rapid problem |  |
| `incident-response-incident-response` | Use when working with incident response incident response | working with incident response incident response |
| `incident-response-smart-fix` | [Extended thinking: This workflow implements a sophistica... |  |
| `incident-runbook-templates` | Create structured incident response runbooks with step-by... | building runbooks, responding to incidents, or establishi... |
| `istio-traffic-management` | Configure Istio traffic management including routing, loa... | implementing service mesh traffic policies, progressive d... |
| `k8s-manifest-generator` | Create production-ready Kubernetes manifests for Deployme... | generating Kubernetes YAML manifests, creating K8s resour... |
| `linkerd-patterns` | Implement Linkerd service mesh patterns for lightweight, ... | setting up Linkerd, configuring traffic policies, or impl... |
| `mtls-configuration` | Configure mutual TLS (mTLS) for zero-trust service-to-ser... | implementing zero-trust networking, certificate managemen... |
| `observability-engineer` | Build production-ready monitoring, logging, and tracing s... |  |
| `observability-monitoring-monitor-setup` | You are a monitoring and observability expert specializin... |  |
| `observability-monitoring-slo-implement` | You are an SLO (Service Level Objective) expert specializ... |  |
| `on-call-handoff-patterns` | Master on-call shift handoffs with context transfer, esca... | transitioning on-call responsibilities, documenting shift... |
| `prometheus-configuration` | Set up Prometheus for comprehensive metric collection, st... | implementing metrics collection, setting up monitoring in... |
| `secrets-management` | Implement secure secrets management for CI/CD pipelines u... | handling sensitive credentials, rotating secrets, or secu... |
| `service-mesh-expert` | Expert service mesh architect specializing in Istio, Link... |  |
| `service-mesh-observability` | Implement comprehensive observability for service meshes ... | setting up mesh monitoring, debugging latency issues, or ... |
| `slo-implementation` | Define and implement Service Level Indicators (SLIs) and ... | establishing reliability targets, implementing SRE practi... |
| `terraform-module-library` | Build reusable Terraform modules for AWS, Azure, and GCP ... | creating infrastructure modules, standardizing cloud prov... |
| `terraform-skill` | Terraform infrastructure as code best practices |  |
| `terraform-specialist` | Expert Terraform/OpenTofu specialist mastering advanced IaC |  |
| `vercel-deployment` | Expert knowledge for deploying to Vercel with Next.js Use... | vercel, deploy, deployment, hosting, production |

### 🧪 测试与质量 (41个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `ab-test-setup` | Structured guide for setting up A/B tests with mandatory ... |  |
| `accessibility-compliance-accessibility-audit` | You are an accessibility expert specializing in WCAG comp... |  |
| `backtesting-frameworks` | Build robust backtesting systems for trading strategies w... | developing trading algorithms, validating strategies, or ... |
| `bats-testing-patterns` | Master Bash Automated Testing System (Bats) for comprehen... | writing tests for shell scripts, CI/CD pipelines, or requ... |
| `code-review-checklist` | Comprehensive checklist for conducting thorough code revi... |  |
| `code-review-excellence` | Master effective code review practices to provide constru... | reviewing pull requests, establishing review standards, o... |
| `code-reviewer` | Elite code review expert specializing in modern AI-powere... |  |
| `debugger` | Debugging specialist for errors, test failures, and unexp... |  |
| `debugging-strategies` | Master systematic debugging techniques, profiling tools, ... | investigating bugs, performance issues, or unexpected beh... |
| `debugging-toolkit-smart-debug` | Use when working with debugging toolkit smart debug | working with debugging toolkit smart debug |
| `distributed-debugging-debug-trace` | You are a debugging expert specializing in setting up com... |  |
| `e2e-testing-patterns` | Master end-to-end testing with Playwright and Cypress to ... | implementing E2E tests, debugging flaky tests, or establi... |
| `error-debugging-error-analysis` | You are an expert error analysis specialist with deep exp... |  |
| `error-debugging-error-trace` | You are an error tracking and observability expert specia... |  |
| `error-diagnostics-smart-debug` | Use when working with error diagnostics smart debug | working with error diagnostics smart debug |
| `javascript-testing-patterns` | Implement comprehensive testing strategies using Jest, Vi... | writing JavaScript/TypeScript tests, setting up test infr... |
| `lint-and-validate` | Automatic quality control, linting, and static analysis p... |  |
| `playwright-skill` | Complete browser automation with Playwright. Auto-detects... | user wants to test websites, automate browser interaction... |
| `python-testing-patterns` | Implement comprehensive testing strategies with pytest, f... | writing Python tests, setting up test suites, or implemen... |
| `receiving-code-review` | Use when receiving code review feedback, before implement... | receiving code review feedback, before implementing sugge... |
| `requesting-code-review` | Use when completing tasks, implementing major features, o... | completing tasks, implementing major features, or before ... |
| `sast-configuration` | Configure Static Application Security Testing (SAST) tool... | setting up security scanning, implementing DevSecOps prac... |
| `screen-reader-testing` | Test web applications with screen readers including Voice... | validating screen reader compatibility, debugging accessi... |
| `shellcheck-configuration` | Master ShellCheck static analysis configuration and usage... | setting up linting infrastructure, fixing code issues, or... |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpecte... | encountering any bug, test failure, or unexpected behavio... |
| `tdd-orchestrator` | Master TDD orchestrator specializing in red-green-refactor |  |
| `tdd-workflow` | Test-Driven Development workflow principles. RED-GREEN-RE... |  |
| `tdd-workflows-tdd-cycle` | Use when working with tdd workflows tdd cycle | working with tdd workflows tdd cycle |
| `tdd-workflows-tdd-green` | Implement the minimal code needed to make failing tests p... |  |
| `tdd-workflows-tdd-red` | Generate failing tests for the TDD red phase to define ex... |  |
| `tdd-workflows-tdd-refactor` | Use when working with tdd workflows tdd refactor | working with tdd workflows tdd refactor |
| `test-automator` | Master AI-powered test automation with modern frameworks, |  |
| `test-driven-development` | Use when implementing any feature or bugfix, before writi... | implementing any feature or bugfix, before writing implem... |
| `test-fixing` | Run tests and systematically fix all failing tests using ... | user asks to fix failing tests, mentions test failures, r... |
| `testing-patterns` | Jest testing patterns, factory functions, mocking strateg... | writing unit tests, creating test factories, or following... |
| `unit-testing-test-generate` | Generate comprehensive, maintainable unit tests across la... |  |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passi... | about to claim work is complete, fixed, or passing, befor... |
| `verification-loop` |  |  |
| `wcag-audit-patterns` | Conduct WCAG 2.2 accessibility audits with automated test... | auditing websites for accessibility, fixing WCAG violatio... |
| `web3-testing` | Test smart contracts comprehensively using Hardhat and Fo... | testing Solidity contracts, setting up blockchain test su... |
| `webapp-testing` | Toolkit for interacting with and testing local web applic... |  |

### 📊 数据与可视化 (12个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `analytics-tracking` | > |  |
| `d3-viz` | Creating interactive data visualisations using d3.js. Thi... | creating custom charts, graphs, network diagrams, geograp... |
| `data-scientist` | Expert data scientist for advanced analytics, machine lea... |  |
| `data-storytelling` | Transform data into compelling narratives using visualiza... | presenting analytics to stakeholders, creating data repor... |
| `kpi-dashboard-design` | Design effective KPI dashboards with metrics selection, v... | building business dashboards, selecting metrics, or desig... |
| `machine-learning-ops-ml-pipeline` | Design and implement a complete ML pipeline for: $ARGUMENTS |  |
| `ml-engineer` | Build production ML systems with PyTorch 2.x, TensorFlow,... |  |
| `ml-pipeline-workflow` | Build end-to-end MLOps pipelines from data preparation th... | creating ML pipelines, implementing MLOps practices, or a... |
| `mlops-engineer` | Build comprehensive ML pipelines, experiment tracking, an... |  |
| `quant-analyst` | Build financial models, backtest trading strategies, and ... |  |
| `risk-manager` | Monitor portfolio risk, R-multiples, and position limits.... |  |
| `risk-metrics-calculation` | Calculate portfolio risk metrics including VaR, CVaR, Sha... | measuring portfolio risk, implementing risk limits, or bu... |

### 🎮 游戏开发 (11个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `3d-web-experience` | Expert in building 3D experiences for the web - Three.js,... | 3D website, three |
| `brand-guidelines-community` | Applies Anthropic's official brand colors and typography ... |  |
| `game-development` | Game development orchestrator. Routes to platform-specifi... |  |
| `godot-gdscript-patterns` | Master Godot 4 GDScript patterns including signals, scene... | building Godot games, implementing game systems, or learn... |
| `internal-comms-community` | A set of resources to help me write all kinds of internal... |  |
| `minecraft-bukkit-pro` | Master Minecraft server plugin development with Bukkit, S... |  |
| `startup-business-analyst-market-opportunity` | Generate comprehensive market opportunity analysis with T... |  |
| `threejs-skills` | Three.js skills for creating 3D elements and interactive ... |  |
| `unity-developer` | Build Unity games with optimized C# scripts, efficient re... |  |
| `unity-ecs-patterns` | Master Unity ECS (Entity Component System) with DOTS, Job... | building data-oriented games, optimizing performance, or ... |
| `unreal-engine-cpp-pro` | Expert guide for Unreal Engine 5.x C++ development, cover... |  |

### 📝 文档与内容 (25个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `beautiful-prose` | Hard-edged writing style contract for timeless, forceful ... |  |
| `changelog-automation` | Automate changelog generation from commits, PRs, and rele... | setting up release workflows, generating release notes, o... |
| `changelog-generator` | Automatically creates user-facing changelogs from git com... |  |
| `code-documentation-code-explain` | You are a code education expert specializing in explainin... |  |
| `code-documentation-doc-generate` | You are a documentation expert specializing in creating c... |  |
| `content-creator` | Create SEO-optimized marketing content with consistent br... | writing blog posts, creating social media content, analyz... |
| `content-marketer` | Elite content marketing strategist specializing in AI-pow... |  |
| `content-research-writer` | Assists in writing high-quality content by conducting res... |  |
| `content-strategy` | When the user wants to plan a content strategy, decide wh... | the user mentions "content strategy," "what should I writ... |
| `copy-editing` | When the user wants to edit, review, or improve existing ... | the user mentions 'edit this copy,' 'review my copy,' 'co... |
| `copywriting` | > |  |
| `doc-coauthoring` | Guide users through a structured workflow for co-authorin... | user wants to write documentation, proposals, technical s... |
| `documentation-generation-doc-generate` | You are a documentation expert specializing in creating c... |  |
| `documentation-templates` | Documentation templates and structure guidelines. README,... |  |
| `docx-official` | Comprehensive document creation, editing, and analysis wi... |  |
| `plan-writing` | Structured task planning with clear breakdowns, dependenc... | implementing features, refactoring, or any multi-step work |
| `postmortem-writing` | Write effective blameless postmortems with root cause ana... | conducting incident reviews, writing postmortem documents... |
| `reference-builder` | Creates exhaustive technical references and API documenta... |  |
| `seo-content-auditor` | Analyzes provided content for quality, E-E-A-T signals, a... |  |
| `seo-content-planner` | Creates comprehensive content outlines and topic clusters... |  |
| `seo-content-refresher` | Identifies outdated elements in provided content and sugg... |  |
| `seo-content-writer` | Writes SEO-optimized content based on provided keywords a... |  |
| `tutorial-engineer` | Creates step-by-step tutorials and educational content fr... |  |
| `writing-plans` | Use when you have a spec or requirements for a multi-step... | you have a spec or requirements for a multi-step task, be... |
| `writing-skills` | Use when creating, updating, or improving agent skills. | creating, updating, or improving agent skills |

### 🔧 工具与自动化 (50个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `automate-whatsapp` | Build WhatsApp automations with Kapso workflows: configur... | automating WhatsApp conversations and event handling |
| `browser-automation` | Browser automation powers web testing, scraping, and AI a... |  |
| `browser-extension-builder` | Expert in building browser extensions that solve real pro... | browser extension, chrome extension, firefox addon, exten... |
| `cc-skill-coding-standards` | Universal coding standards, best practices, and patterns ... |  |
| `cc-skill-continuous-learning` | Development skill from everything-claude-code |  |
| `cc-skill-project-guidelines-example` | Project Guidelines Skill (Example) |  |
| `cc-skill-strategic-compact` | Development skill from everything-claude-code |  |
| `email-sequence` | When the user wants to create or optimize an email sequen... | the user mentions "email sequence," "drip campaign," "nur... |
| `email-systems` | Email has the highest ROI of any marketing channel. $36 f... | keywords, file_patterns, code_patterns |
| `file-organizer` | Intelligently organizes files and folders by understandin... | user wants to clean up directories, organize downloads, r... |
| `file-uploads` | Expert at handling file uploads and cloud storage. Covers... | file upload, S3, R2, presigned URL, multipart |
| `firecrawl-scraper` | Deep web scraping, screenshots, PDF parsing, and website ... |  |
| `free-tool-strategy` | When the user wants to plan, evaluate, or build a free to... | the user mentions "engineering as marketing," "free tool,... |
| `github-workflow-automation` | Automate GitHub workflows with AI assistance. Includes PR... | automating GitHub workflows, setting up PR review automat... |
| `hugging-face-cli` | Execute Hugging Face Hub operations using the `hf` CLI. U... | the user needs to download models/datasets/spaces, upload... |
| `invoice-organizer` | Automatically organizes invoices and receipts for tax pre... |  |
| `javascript-mastery` | Comprehensive JavaScript reference covering 33+ essential... | explaining JS concepts, debugging JavaScript issues, or t... |
| `javascript-pro` | Master modern JavaScript with ES6+, async patterns, and N... |  |
| `javascript-typescript-typescript-scaffold` | You are a TypeScript project architecture expert speciali... |  |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protoc... | building MCP servers to integrate external APIs or servic... |
| `modern-javascript-patterns` | Master ES6+ features including async/await, destructuring... | refactoring legacy code, implementing modern patterns, or... |
| `n8n-code-python` | Write Python code in n8n Code nodes. Use when writing Pyt... | writing Python in n8n, using _input/_json/_node syntax, w... |
| `n8n-mcp-tools-expert` | Expert guide for using n8n-mcp MCP tools effectively. Use... | searching for nodes, validating configurations, accessing... |
| `n8n-node-configuration` | Operation-aware node configuration guidance. Use when con... | configuring nodes, understanding property dependencies, d... |
| `obsidian-clipper-template-creator` | Guide for creating templates for the Obsidian Web Clipper... | you want to create a new clipping template, understand av... |
| `pdf-official` | Comprehensive PDF manipulation toolkit for extracting tex... |  |
| `personal-tool-builder` | Expert in building custom tools that solve your own probl... | build a tool, personal tool, scratch my itch, solve my pr... |
| `pptx-official` | Presentation creation, editing, and analysis. When Claude... |  |
| `raffle-winner-picker` | Picks random winners from lists, spreadsheets, or Google ... |  |
| `sales-automator` | Draft cold emails, follow-ups, and proposal templates. Cr... |  |
| `skill-creator` | Guide for creating effective skills. This skill should be... | users want to create a new skill (or update an existing s... |
| `skill-developer` | Create and manage Claude Code skills following Anthropic ... | creating new skills, modifying skill-rules |
| `skill-rails-upgrade` | Analyze Rails apps and provide upgrade assessments |  |
| `skill-seekers` | -Automatically convert documentation websites, GitHub rep... |  |
| `slack-bot-builder` | Build Slack apps using the Bolt framework across Python, ... | slack bot, slack app, bolt framework, block kit, slash co... |
| `slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimi... | users request animated GIFs for Slack like "make me a GIF... |
| `telegram-bot-builder` | Expert in building Telegram bots that solve real problems... | telegram bot, bot api, telegram automation, chat bot tele... |
| `telegram-mini-app` | Expert in building Telegram Mini Apps (TWA) - web apps th... | telegram mini app, TWA, telegram web app, TON app, mini app |
| `tool-design` | Build tools that agents can use effectively, including ar... |  |
| `typescript-advanced-types` | Master TypeScript's advanced type system including generi... | implementing complex type logic, creating reusable type u... |
| `typescript-expert` | >- |  |
| `typescript-pro` | Master TypeScript with advanced types, generics, and stri... |  |
| `unzip-crx` | Extract Chrome extension (.crx) files. Use when user need... | user needs to unzip, extract, or decompress a |
| `video-downloader` | Downloads videos from YouTube and other platforms for off... |  |
| `workflow-automation` | Workflow automation is the infrastructure that makes AI a... |  |
| `workflow-orchestration-patterns` | Design durable workflows with Temporal for distributed sy... | building long-running processes, distributed transactions... |
| `workflow-patterns` | Use this skill when implementing tasks according to Condu... |  |
| `xlsx-official` | Comprehensive spreadsheet creation, editing, and analysis... |  |
| `youtube-transcript` | Download YouTube video transcripts when user provides a Y... | user wants to transcribe or get captions/subtitles from a... |
| `zapier-make-patterns` | No-code automation democratizes workflow building. Zapier... |  |

### 🌐 Web3 区块链 (3个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `blockchain-developer` | Build production-ready Web3 applications, smart contracts... |  |
| `defi-protocol-templates` | Implement DeFi protocols with production-ready templates ... | building decentralized finance applications or smart cont... |
| `nft-standards` | Implement NFT standards (ERC-721, ERC-1155) with proper m... | creating NFT contracts, building NFT marketplaces, or imp... |

### 💼 产品与营销 (37个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `brand-guidelines` | Applies Anthropic's official brand colors and typography ... |  |
| `brand-guidelines-anthropic` | Applies Anthropic's official brand colors and typography ... |  |
| `business-analyst` | Master modern business analysis with AI-powered analytics, |  |
| `competitive-ads-extractor` | Extracts and analyzes competitors' ads from ad libraries ... |  |
| `competitor-alternatives` | When the user wants to create competitor comparison or al... | the user mentions 'alternative page,' 'vs page,' 'competi... |
| `form-cro` | > |  |
| `launch-strategy` | When the user wants to plan a product launch, feature ann... | the user mentions 'launch,' 'Product Hunt,' 'feature rele... |
| `lead-research-assistant` | Identifies high-quality leads for your product or service... |  |
| `market-sizing-analysis` | This skill should be used when the user asks to "calculat... | the user asks to "calculate TAM", |
| `marketing-ideas` | Provide proven marketing strategies and growth ideas for ... |  |
| `marketing-psychology` | Apply behavioral science and mental models to marketing d... |  |
| `micro-saas-launcher` | Expert in launching small, focused SaaS products fast - t... | micro saas, indie hacker, small saas, side project, saas mvp |
| `notion-template-business` | Expert in building and selling Notion templates as a busi... | notion template, sell templates, digital product, notion ... |
| `onboarding-cro` | When the user wants to optimize post-signup onboarding, u... | the user mentions "onboarding flow," "activation rate," "... |
| `page-cro` | > |  |
| `paid-ads` | When the user wants help with paid advertising campaigns ... | the user mentions 'PPC,' 'paid media,' 'ad copy,' 'ad cre... |
| `paywall-upgrade-cro` | When the user wants to create or optimize in-app paywalls... | the user mentions "paywall," "upgrade screen," "upgrade m... |
| `popup-cro` | Create and optimize popups, modals, overlays, slide-ins, ... |  |
| `pricing-strategy` | Design pricing, packaging, and monetization strategies ba... |  |
| `product-manager-toolkit` | Comprehensive toolkit for product managers including RICE... |  |
| `product-marketing-context` | When the user wants to create or update their product mar... | the user mentions 'product context,' 'marketing context,'... |
| `production-code-audit` | Autonomously deep-scan entire codebase line-by-line, unde... |  |
| `referral-program` | When the user wants to create, optimize, or analyze a ref... | the user mentions 'referral,' 'affiliate,' 'ambassador,' ... |
| `seo-audit` | > |  |
| `seo-authority-builder` | Analyzes content for E-E-A-T signals and suggests improve... |  |
| `seo-cannibalization-detector` | Analyzes multiple provided pages to identify keyword over... |  |
| `seo-fundamentals` | > |  |
| `seo-keyword-strategist` | Analyzes keyword usage in provided content, calculates de... |  |
| `seo-meta-optimizer` | Creates optimized meta titles, descriptions, and URL sugg... |  |
| `seo-snippet-hunter` | Formats content to be eligible for featured snippets and ... |  |
| `signup-flow-cro` | When the user wants to optimize signup, registration, acc... | the user mentions "signup conversions," "registration fri... |
| `startup-analyst` | Expert startup business analyst specializing in market si... |  |
| `startup-business-analyst-business-case` | Generate comprehensive investor-ready business case docum... |  |
| `startup-business-analyst-financial-projections` | Create detailed 3-5 year financial model with revenue, co... |  |
| `startup-financial-modeling` | This skill should be used when the user asks to "create f... | the user asks to "create financial |
| `startup-metrics-framework` | This skill should be used when the user asks about "key s... | the user asks about "key startup |
| `viral-generator-builder` | Expert in building shareable generator tools that go vira... | generator tool, quiz maker, name generator, avatar creato... |

### 🎓 学习与知识 (9个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `context7-auto-research` | Automatically fetch latest library/framework documentatio... |  |
| `continuous-learning` | Automatically extract reusable patterns from Claude Code ... |  |
| `deep-research` | Execute autonomous multi-step research using Google Gemin... |  |
| `exa-search` | Semantic search, similar content discovery, and structure... |  |
| `infinite-gratitude` | Multi-agent research skill for parallel research executio... |  |
| `last30days` | Research a topic from the last 30 days on Reddit + X + We... |  |
| `notebooklm` | Use this skill to query your Google NotebookLM notebooks ... |  |
| `research-engineer` | An uncompromising Academic Research Engineer. Operates wi... |  |
| `tavily-web` | Web search, content extraction, crawling, and research ca... |  |

### 🔍 搜索与 SEO (7个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `algolia-search` | Expert patterns for Algolia search implementation, indexi... | adding search to, algolia, instantsearch, search api, sea... |
| `geo-fundamentals` | Generative Engine Optimization for AI search engines (Cha... |  |
| `hybrid-search-implementation` | Combine vector and keyword search for improved retrieval.... | implementing RAG systems, building search engines, or whe... |
| `programmatic-seo` | > |  |
| `schema-markup` | > |  |
| `search-specialist` | Expert web researcher using advanced search techniques and |  |
| `similarity-search-patterns` | Implement efficient similarity search with vector databas... | building semantic search, implementing nearest neighbor q... |

### 💬 通信与社交 (10个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `baoyu-post-to-wechat` | Posts content to WeChat Official Account (微信公众号) via Chro... | user mentions "发布公众号", "post to wechat", "微信公众号", or "图文/文章" |
| `baoyu-post-to-x` | Posts content and articles to X (Twitter). Supports regul... | user asks to "post to X", "tweet", "publish to Twitter", ... |
| `customer-support` | Elite AI-powered customer support specialist mastering |  |
| `daily-news-report` | Scrapes content based on a preset URL list, filters high-... |  |
| `internal-comms` | A set of resources to help me write all kinds of internal... |  |
| `internal-comms-anthropic` | A set of resources to help me write all kinds of internal... |  |
| `meeting-insights-analyzer` | Analyzes meeting transcripts and recordings to uncover be... |  |
| `observe-whatsapp` | Observe and troubleshoot WhatsApp in Kapso: debug message... | investigating production issues, message failures, or web... |
| `social-content` | When the user wants help creating, scheduling, or optimiz... | the user mentions 'LinkedIn post,' 'Twitter thread,' 'soc... |
| `x-article-publisher-skill` | Publish articles to X/Twitter |  |

### 🖼️ 图像与创意 (25个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `algorithmic-art` | Creating algorithmic art using p5.js with seeded randomne... |  |
| `artifacts-builder` | Suite of tools for creating elaborate, multi-component cl... |  |
| `baoyu-article-illustrator` | Analyzes article structure, identifies positions requirin... | user asks to "illustrate article", "add images", "generat... |
| `baoyu-comic` | Knowledge comic creator supporting multiple art styles an... | user asks to create "知识漫画", "教育漫画", "biography comic", "t... |
| `baoyu-compress-image` | Compresses images to WebP (default) or PNG with automatic... | user asks to "compress image", "optimize image", "convert... |
| `baoyu-cover-image` | Generates article cover images with 5 dimensions (type, p... | user asks to "generate cover image", "create article cove... |
| `baoyu-danger-gemini-web` | Generates images and text via reverse-engineered Gemini W... | other skills need image generation backend, or when user ... |
| `baoyu-danger-x-to-markdown` | Converts X (Twitter) tweets and articles to markdown with... | user mentions "X to markdown", "tweet to markdown", "save... |
| `baoyu-image-gen` | AI image generation with OpenAI and Google APIs. Supports... | user asks to generate, create, or draw images |
| `baoyu-infographic` | Generates professional infographics with 20 layout types ... | user asks to create "infographic", "信息图", "visual summary... |
| `baoyu-slide-deck` | Generates professional slide deck images from content. Cr... | user asks to "create slides", "make a presentation", "gen... |
| `baoyu-url-to-markdown` | Fetch any URL and convert to markdown using Chrome CDP. S... | user wants to save a webpage as markdown |
| `baoyu-xhs-images` | Generates Xiaohongshu (Little Red Book) infographic serie... | user mentions "小红书图片", "XHS images", "RedNote infographic... |
| `canvas-design` | Create beautiful visual art in .png and .pdf documents us... |  |
| `fal-audio` | Text-to-speech and speech-to-text using fal.ai audio models |  |
| `fal-generate` | Generate images and videos using fal.ai AI models |  |
| `fal-image-edit` | AI-powered image editing with style transfer and object r... |  |
| `fal-platform` | Platform APIs for model management, pricing, and usage tr... |  |
| `fal-upscale` | Upscale and enhance image and video resolution using AI |  |
| `fal-workflow` | Generate workflow JSON files for chaining AI models |  |
| `image-enhancer` | Improves the quality of images, especially screenshots, b... |  |
| `imagen` | \| |  |
| `nanobanana-ppt-skills` | AI-powered PPT generation with document analysis and styl... |  |
| `theme-factory` | Toolkit for styling artifacts with a theme. These artifac... |  |
| `web-artifacts-builder` | Suite of tools for creating elaborate, multi-component cl... |  |

### 📦 编程语言 (28个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `async-python-patterns` | Master Python asyncio, concurrent programming, and async/... | building async APIs, concurrent systems, or I/O-bound app... |
| `bash-defensive-patterns` | Master defensive Bash programming techniques for producti... | writing robust shell scripts, CI/CD pipelines, or system ... |
| `bash-linux` | Bash/Linux terminal patterns. Critical commands, piping, ... | working on macOS or Linux systems |
| `bash-pro` | Master of defensive Bash scripting for production automat... |  |
| `bun-development` | Modern JavaScript/TypeScript development with Bun runtime... | working with Bun, optimizing JS/TS development speed, or ... |
| `c-pro` | Write efficient C code with proper memory management, poi... |  |
| `cpp-pro` | Write idiomatic C++ code with modern features, RAII, smart |  |
| `csharp-pro` | Write modern C# code with advanced features like records,... |  |
| `elixir-pro` | Write idiomatic Elixir code with OTP patterns, supervisio... |  |
| `go-concurrency-patterns` | Master Go concurrency with goroutines, channels, sync pri... | building concurrent Go applications, implementing worker ... |
| `golang-pro` | Master Go 1.21+ with modern patterns, advanced concurrency, |  |
| `haskell-pro` | Expert Haskell engineer specializing in advanced type sys... |  |
| `hr-pro` | Professional, ethical HR partner for hiring, |  |
| `java-pro` | Master Java 21+ with modern features like virtual threads... |  |
| `julia-pro` | Master Julia 1.10+ with modern features, performance opti... |  |
| `performance-profiling` | Performance profiling principles. Measurement, analysis, ... |  |
| `php-pro` | Write idiomatic PHP code with generators, iterators, SPL ... |  |
| `posix-shell-pro` | Expert in strict POSIX sh scripting for maximum portabili... |  |
| `powershell-windows` | PowerShell Windows patterns. Critical pitfalls, operator ... |  |
| `python-packaging` | Create distributable Python packages with proper project ... | packaging Python libraries, creating CLI tools, or distri... |
| `python-patterns` | Python development principles and decision-making. Framew... |  |
| `python-performance-optimization` | Profile and optimize Python code using cProfile, memory p... | debugging slow Python code, optimizing bottlenecks, or im... |
| `python-pro` | Master Python 3.12+ with modern features, async programming, |  |
| `ruby-pro` | Write idiomatic Ruby code with metaprogramming, Rails pat... |  |
| `rust-async-patterns` | Master Rust async programming with Tokio, async traits, e... | building async Rust applications, implementing concurrent... |
| `rust-pro` | Master Rust 1.75+ with modern async patterns, advanced ty... |  |
| `scala-pro` | Master enterprise-grade Scala development with functional |  |
| `systems-programming-rust-project` | You are a Rust project architecture expert specializing i... |  |

### 🔄 其他专业 (163个)

| 技能名称 | 功能简述 | 触发条件 |
|----------|----------|----------|
| `a2ui` | Generate A2UI 0.8 protocol compliant UI code. Use when bu... | building agent-driven interfaces, generating JSONL messag... |
| `address-github-comments` | Use when you need to address review or issue comments on ... | you need to address review or issue comments on an open G... |
| `advanced-evaluation` | This skill should be used when the user asks to "implemen... | the user asks to "implement LLM-as-judge", "compare model... |
| `anti-reversing-techniques` | Understand anti-reversing, obfuscation, and protection te... | analyzing protected binaries, bypassing anti-debugging fo... |
| `app-builder` | Main application building orchestrator. Creates full-stac... |  |
| `application-performance-performance-optimization` | Optimize end-to-end application performance with profilin... | coordinating performance optimization across the stack |
| `arm-cortex-expert` | > |  |
| `avalonia-layout-zafiro` | Guidelines for modern Avalonia UI layout using Zafiro.Ava... |  |
| `avalonia-viewmodels-zafiro` | Optimal ViewModel and Wizard creation patterns for Avalon... |  |
| `avalonia-zafiro-development` | Mandatory skills, conventions, and behavioral rules for A... |  |
| `bazel-build-optimization` | Optimize Bazel builds for large-scale monorepos. Use when... | configuring Bazel, implementing remote execution, or opti... |
| `bdi-mental-states` | This skill should be used when the user asks to "model ag... | the user asks to "model agent mental states", "implement ... |
| `behavioral-modes` | AI operational modes (brainstorm, implement, debug, revie... |  |
| `binary-analysis-patterns` | Master binary analysis patterns including disassembly, de... | analyzing executables, understanding compiled code, or pe... |
| `blockrun` | Use when user needs capabilities Claude lacks (image gene... | user needs capabilities Claude lacks (image generation, r... |
| `brainstorming` | > |  |
| `building-native-ui` | Complete guide for building beautiful apps with Expo Rout... |  |
| `busybox-on-windows` | How to use a Win32 build of BusyBox to run many of the st... |  |
| `clarity-gate` | Pre-ingestion verification for epistemic quality in RAG s... |  |
| `claude-ally-health` | A health assistant skill for medical information analysis... |  |
| `claude-code-guide` | Master guide for using Claude Code effectively. Includes ... |  |
| `claude-d3js-skill` | Creating interactive data visualisations using d3.js. Thi... | creating custom charts, graphs, network diagrams, geograp... |
| `claude-scientific-skills` | Scientific research and analysis skills |  |
| `claude-speed-reader` | -Speed read Claude's responses at 600+ WPM using RSVP wit... |  |
| `claude-win11-speckit-update-skill` | Windows 11 system management |  |
| `clean-code` | Pragmatic coding standards - concise, direct, no over-eng... |  |
| `code-refactoring-context-restore` | Use when working with code refactoring context restore | working with code refactoring context restore |
| `code-refactoring-refactor-clean` | You are a code refactoring expert specializing in clean c... |  |
| `code-refactoring-tech-debt` | You are a technical debt expert specializing in identifyi... |  |
| `codebase-cleanup-deps-audit` | You are a dependency security expert specializing in vuln... |  |
| `codebase-cleanup-refactor-clean` | You are a code refactoring expert specializing in clean c... |  |
| `codebase-cleanup-tech-debt` | You are a technical debt expert specializing in identifyi... |  |
| `codex-review` | Professional code review with auto CHANGELOG generation, ... |  |
| `coding-standards` | Universal coding standards, best practices, and patterns ... |  |
| `commit` | Create commit messages following Sentry conventions. Use ... | committing code changes, writing commit messages, or form... |
| `competitive-landscape` | This skill should be used when the user asks to "analyze | the user asks to "analyze |
| `comprehensive-review-full-review` | Use when working with comprehensive review full review | working with comprehensive review full review |
| `comprehensive-review-pr-enhance` | You are a PR optimization expert specializing in creating... |  |
| `computer-vision-expert` | SOTA Computer Vision Expert (2026). Specialized in YOLO26... |  |
| `concise-planning` | Use when a user asks for a plan for a coding task, to gen... | a user asks for a plan for a coding task, to generate a c... |
| `conductor-implement` | Execute tasks from a track's implementation plan followin... |  |
| `conductor-manage` | Manage track lifecycle: archive, restore, delete, rename,... |  |
| `conductor-new-track` | Create a new track with specification and phased implemen... |  |
| `conductor-revert` | Git-aware undo by logical work unit (track, phase, or task) |  |
| `conductor-setup` | Initialize project with Conductor artifacts (product defi... |  |
| `conductor-status` | Display project status, active tracks, and next actions |  |
| `conductor-validator` | Validates Conductor project artifacts for completeness, |  |
| `connect` | Connect Claude to any app. Send emails, create issues, po... |  |
| `context-compression` | Design and evaluate compression strategies for long-runni... |  |
| `context-degradation` | Recognize patterns of context failure: lost-in-middle, po... |  |
| `context-driven-development` | Use this skill when working with Conductor's context-driven |  |
| `context-extract` | Append conversation context to cumulative project history... |  |
| `context-fundamentals` | Understand what context is, why it matters, and the anato... |  |
| `context-management-context-restore` | Use when working with context management context restore | working with context management context restore |
| `context-management-context-save` | Use when working with context management context save | working with context management context save |
| `context-manager` | Elite AI context engineering specialist mastering dynamic... |  |
| `context-optimization` | Apply compaction, masking, and caching strategies |  |
| `context-window-management` | Strategies for managing LLM context windows including sum... | context window, token limit, context management, context ... |
| `create-pr` | Create pull requests following Sentry conventions. Use wh... | opening PRs, writing PR descriptions, or preparing change... |
| `culture-index` | Index and search culture documentation |  |
| `dependency-management-deps-audit` | You are a dependency security expert specializing in vuln... |  |
| `dependency-upgrade` | Manage major dependency version upgrades with compatibili... | upgrading framework versions, updating major dependencies... |
| `developer-growth-analysis` | Analyzes your recent Claude Code chat history to identify... |  |
| `distributed-tracing` | Implement distributed tracing with Jaeger and Tempo to tr... | debugging microservices, analyzing request flows, or impl... |
| `domain-name-brainstormer` | Generates creative domain name ideas for your project and... |  |
| `dx-optimizer` | Developer Experience specialist. Improves tooling, setup,... |  |
| `employment-contract-templates` | Create employment contracts, offer letters, and HR policy... | drafting employment agreements, creating HR policies, or ... |
| `environment-setup-guide` | Guide developers through setting up development environme... |  |
| `error-detective` | Search logs and codebases for error patterns, stack trace... |  |
| `error-diagnostics-error-analysis` | You are an expert error analysis specialist with deep exp... |  |
| `error-diagnostics-error-trace` | You are an error tracking and observability expert specia... |  |
| `error-handling-patterns` | Master error handling patterns across languages including... | implementing error handling, designing APIs, or improving... |
| `eval-harness` |  |  |
| `evaluation` | Build evaluation frameworks for agent systems |  |
| `event-store-design` | Design and implement event stores for event-sourced syste... | building event sourcing infrastructure, choosing event st... |
| `executing-plans` | Use when you have a written implementation plan to execut... | you have a written implementation plan to execute in a se... |
| `filesystem-context` | This skill should be used when the user asks to "offload ... | the user asks to "offload context to files", "implement d... |
| `find-bugs` | Find bugs, security vulnerabilities, and code quality iss... | asked to review changes, find bugs, security review, or a... |
| `find-skills` | Helps users discover and install agent skills when they a... | the user is looking for functionality that might exist as... |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and ... | implementation is complete, all tests pass, and you need ... |
| `firmware-analyst` | Expert firmware analyst specializing in embedded systems,... |  |
| `fix-review` | Verify fix commits address audit findings without new bugs |  |
| `fp-ts-errors` | Handle errors as values using fp-ts Either and TaskEither... | implementing error handling patterns with fp-ts |
| `fp-ts-react` | Practical patterns for using fp-ts with React - hooks, st... | building React apps with functional programming patterns |
| `framework-migration-code-migrate` | You are a code migration expert specializing in transitio... |  |
| `framework-migration-deps-upgrade` | You are a dependency management expert specializing in sa... |  |
| `framework-migration-legacy-modernize` | Orchestrate a comprehensive legacy system modernization u... |  |
| `full-stack-orchestration-full-stack-feature` | Use when working with full stack orchestration full stack... | working with full stack orchestration full stack feature |
| `gdpr-data-handling` | Implement GDPR-compliant data handling with consent manag... | building systems that process EU personal data, implement... |
| `git-advanced-workflows` | Master advanced Git workflows including rebasing, cherry-... | managing complex Git histories, collaborating on feature ... |
| `git-pr-workflows-git-workflow` | Orchestrate a comprehensive git workflow from code review... |  |
| `git-pr-workflows-onboard` | You are an **expert onboarding specialist and knowledge t... |  |
| `git-pr-workflows-pr-enhance` | You are a PR optimization expert specializing in creating... |  |
| `git-pushing` | Stage, commit, and push git changes with conventional com... | user wants to commit and push changes, mentions pushing t... |
| `hugging-face-jobs` | This skill should be used when users want to run any work... | users want to run any workload on Hugging Face Jobs infra... |
| `i18n-localization` | Internationalization and localization patterns. Detecting... |  |
| `interactive-portfolio` | Expert in building portfolios that actually land jobs and... | portfolio, personal website, showcase work, developer por... |
| `iterate-pr` | Iterate on a PR until CI passes. Use when you need to fix... | you need to fix CI failures, address review feedback, or ... |
| `kaizen` | Guide for continuous improvement, error proofing, and sta... |  |
| `langfuse` | Expert in Langfuse - the open-source LLM observability pl... | langfuse, llm observability, llm tracing, prompt manageme... |
| `langsmith-fetch` | Debug LangChain and LangGraph agents by fetching executio... | debugging agent behavior, investigating errors, analyzing... |
| `legacy-modernizer` | Refactor legacy codebases, migrate outdated frameworks, and |  |
| `legal-advisor` | Draft privacy policies, terms of service, disclaimers, an... |  |
| `linear-claude-skill` | Manage Linear issues, projects, and teams |  |
| `loki-mode` | Multi-agent autonomous startup system for Claude Code. Tr... |  |
| `makepad-skills` | Makepad UI development skills for Rust apps: setup, patte... |  |
| `mermaid-expert` | Create Mermaid diagrams for flowcharts, sequences, ERDs, and |  |
| `multi-platform-apps-multi-platform` | Build and deploy the same feature consistently across web... |  |
| `native-data-fetching` | Use when implementing or debugging ANY network request, A... | implementing or debugging ANY network request, API call, ... |
| `network-101` | This skill should be used when the user asks to "set up a... | the user asks to "set up a web server", "configure HTTP o... |
| `network-engineer` | Expert network engineer specializing in modern cloud netw... |  |
| `nx-workspace-patterns` | Configure and optimize Nx monorepo workspaces. Use when s... | setting up Nx, configuring project boundaries, optimizing... |
| `pci-compliance` | Implement PCI DSS compliance requirements for secure hand... | securing payment processing, achieving PCI compliance, or... |
| `performance-engineer` | Expert performance engineer specializing in modern observ... |  |
| `planning-with-files` | Implements Manus-style file-based planning for complex ta... | starting complex multi-step tasks, research projects, or ... |
| `project-development` | This skill should be used when the user asks to "start an... | the user asks to "start an LLM project", "design batch pi... |
| `project-guidelines-example` |  |  |
| `projection-patterns` | Build read models and projections from event streams. Use... | implementing CQRS read sides, building materialized views... |
| `protocol-reverse-engineering` | Master network protocol reverse engineering including pac... | analyzing network traffic, understanding proprietary prot... |
| `pypict-skill` | Pairwise test generation |  |
| `python-development-python-scaffold` | You are a Python project architecture expert specializing... |  |
| `ralph-loop` | Autonomous development loop for completing all remaining ... | user says "全部完成", "完成所有任务", "finish all", "complete every... |
| `readme` | When the user wants to create or update a README.md file ... | the user says 'write readme,' 'create readme,' 'document ... |
| `release-skills` | Universal release workflow. Auto-detects version files an... | user says "release", "发布", "new version", "bump version",... |
| `remotion-best-practices` | Best practices for Remotion - Video creation in React |  |
| `reverse-engineer` | Expert reverse engineer specializing in binary analysis, |  |
| `screenshots` | Generate marketing screenshots of your app using Playwrig... | the user wants to create screenshots for Product Hunt, so... |
| `senior-fullstack` | Comprehensive fullstack development skill for building co... | building new projects, analyzing code quality, implementi... |
| `server-management` | Server management principles and decision-making. Process... |  |
| `sharp-edges` | Identify error-prone APIs and dangerous configurations |  |
| `spec-analyze` | Perform non-destructive cross-artifact consistency and qu... | user says "/spec-analyze", "analyze the spec", "check con... |
| `spec-checklist` | Generate custom quality checklists that validate REQUIREM... | user says "/spec-checklist", "create checklist for [domai... |
| `spec-clarify` | Identify underspecified areas in a feature spec by asking... | user says "/spec-clarify", "clarify the spec", or after /... |
| `spec-constitution` | Create or update the project constitution with core princ... | user says "/spec-constitution", "create constitution", "u... |
| `spec-implement` | Execute implementation by processing tasks defined in tas... | user says "/spec-implement", "implement the feature", "st... |
| `spec-plan` | Execute implementation planning workflow to generate desi... | user says "/spec-plan", "create a plan", "plan the implem... |
| `spec-specify` | Create or update a feature specification from a natural l... | user says "/spec-specify", "create a spec", "write a spec... |
| `spec-tasks` | Generate actionable, dependency-ordered tasks.md organize... | user says "/spec-tasks", "create tasks", "generate task l... |
| `spec-taskstoissues` | Convert tasks.md into GitHub issues with proper dependenc... | user says "/spec-taskstoissues", "create GitHub issues", ... |
| `specify-resources` | Shared resources (scripts, templates) for Spec-Driven Dev... |  |
| `strategic-compact` | Suggests manual context compaction at logical intervals t... |  |
| `stride-analysis-patterns` | Apply STRIDE methodology to systematically identify threa... | analyzing system security, conducting threat modeling ses... |
| `superpowers-lab` | Lab environment for Claude superpowers |  |
| `tailored-resume-generator` | Analyzes job descriptions and generates tailored resumes ... |  |
| `team-collaboration-issue` | You are a GitHub issue resolution expert specializing in ... |  |
| `team-collaboration-standup-notes` | You are an expert team communication specialist focused o... |  |
| `team-composition-analysis` | This skill should be used when the user asks to "plan team | the user asks to "plan team |
| `template-skill` | Replace with description of the skill and when Claude sho... |  |
| `top-web-vulnerabilities` | This skill should be used when the user asks to "identify... | the user asks to "identify web application vulnerabilitie... |
| `track-management` | Use this skill when creating, managing, or working with C... |  |
| `turborepo-caching` | Configure Turborepo for efficient monorepo builds with lo... | setting up Turborepo, optimizing build pipelines, or impl... |
| `twilio-communications` | Build communication features with Twilio: SMS messaging, ... | twilio, send SMS, text message, voice call, phone verific... |
| `upgrading-expo` | Upgrade Expo SDK versions |  |
| `upstash-qstash` | Upstash QStash expert for serverless message queues, sche... | qstash, upstash queue, serverless cron, scheduled http, m... |
| `use-dom` | Use Expo DOM components to run web code in a webview on n... |  |
| `using-git-worktrees` | Use when starting feature work that needs isolation from ... | starting feature work that needs isolation from current w... |
| `using-superpowers` | Use when starting any conversation - establishes how to f... | starting any conversation - establishes how to find and u... |
| `uv-package-manager` | Master the uv package manager for fast Python dependency ... | setting up Python projects, managing dependencies, or opt... |
| `varlock-claude-skill` | Secure environment variable management ensuring secrets a... |  |
| `vercel-composition-patterns` | React composition patterns that scale. Use when refactori... | refactoring components with |
| `vercel-deploy-claimable` | Deploy applications and websites to Vercel. Use this skil... |  |
| `vexor` | Vector-powered CLI for semantic file search with a Claude... |  |
| `web-performance-optimization` | Optimize website and web application performance includin... |  |

---

## 🚀 快速开始指南

### 热门使用场景

**场景 1: 构建 AI 应用**
```
推荐技能：ai-agents-architect, rag-implementation, langchain-architecture
触发方式：提及 "AI 代理"、"RAG 系统"、"LangChain"
```

**场景 2: 系统架构设计**
```
推荐技能：architecture, microservices-patterns, event-sourcing-architect
触发方式：提及 "架构设计"、"微服务"、"事件驱动"
```

**场景 3: 安全审计**
```
推荐技能：security-review, vulnerability-scanner, api-security-best-practices
触发方式：提及 "安全审计"、"漏洞扫描"、"渗透测试"
```

**场景 4: 前端开发**
```
推荐技能：react-best-practices, nextjs-app-router-patterns, tailwind-design-system
触发方式：提及 "React"、"Next.js"、"前端优化"
```

**场景 5: DevOps 运维**
```
推荐技能：kubernetes-architect, github-actions-templates, observability-engineer
触发方式：提及 "K8s"、"CI/CD"、"监控部署"
```

---

## 💡 使用方法

### 在 Claude Code 中使用

技能会根据对话内容自动激活：

```bash
# 启动 Claude Code
claude

# 技能自动激活示例：
用户: "帮我设计一个 RAG 系统"
→ 自动加载 rag-implementation 技能

用户: "审查这段代码的安全问题"  
→ 触发 security-review 技能

用户: "优化这个 React 组件的性能"
→ 激活 react-best-practices 技能
```

### 在其他 AI 工具中使用

| 工具 | 配置位置 | 使用方法 |
|------|---------|---------|
| **Cursor** | `.cursor/rules/` | 复制 SKILL.md 到 rules 目录 |
| **Windsurf** | `.windsurf/rules` | 复制技能文件到 rules 目录 |
| **VS Code + Copilot** | `.github/copilot-instructions.md` | 合并相关技能内容 |
| **Aider** | `--read SKILL.md` | 使用 --read 参数加载技能 |
| **Continue** | `.continue/config.json` | 在配置中引用技能文件路径 |
| **Cline** | `.cline/` | 复制技能到 Cline 目录 |

---

## 📁 目录结构

```
~/.agents/skills/
├── skill-name/
│   ├── SKILL.md          # 主技能文件（必需）
│   ├── references/       # 参考资料（可选）
│   ├── scripts/          # 辅助脚本（可选）
│   └── examples/         # 示例代码（可选）
├── another-skill/
│   └── SKILL.md
└── README.md             # 本文件
```

---

## 🤝 贡献指南

欢迎贡献新技能或改进现有技能！

### 如何贡献

1. **Fork 本仓库**
2. **创建新技能目录**
   ```bash
   mkdir your-skill-name
   cd your-skill-name
   ```
3. **创建 SKILL.md 文件**（参考现有技能格式）
4. **更新 README.md**（添加到相应分类）
5. **提交 Pull Request**

### 技能质量标准

- ✅ 清晰的功能说明和使用场景
- ✅ 明确的触发关键词
- ✅ 实用的示例代码和最佳实践
- ✅ 相关文档和资源链接
- ✅ 适当的引用和参考资料

### 技能命名规范

- 使用小写字母和连字符
- 名称简洁且描述性强
- 避免过于通用的名称
- 例如：`react-best-practices`、`api-security-best-practices`

---

## 📄 许可证

本项目采用 MIT 许可证。各技能可能有不同的许可证，请查看各技能目录下的 LICENSE 文件。

---

## 📬 联系方式

- **项目维护者**: windy  
- **邮箱**: xiaochangsheng@xichengtech.cn
- **GitHub**: [@xfstudio](https://github.com/xfstudio)
- **项目仓库**: [github.com/xfstudio/skills](https://github.com/xfstudio/skills)

---

## 🔄 更新日志

### 2026-02-04
- 📊 更新技能清单格式，新增触发条件列
- 🔢 当前技能总数：698 个

### 历史版本
- 查看完整更新历史请访问 [CHANGELOG.md](./CHANGELOG.md)

---

## 🌟 Star History

如果这个项目对你有帮助，请给个 Star ⭐️ 支持一下！

---

## 📚 相关资源

- [Claude AI 官方文档](https://docs.anthropic.com/)
- [Claude Code 使用指南](https://docs.anthropic.com/claude/docs)
- [技能开发最佳实践](./docs/skill-development-guide.md)
- [社区贡献指南](./CONTRIBUTING.md)

---

> 📖 文档最后更新: 2026-02-04
> 
> 💡 **提示**: 建议定期运行 `npx skills update xfstudio/skills` 获取最新技能