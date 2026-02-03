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

## Skills 分类目录 (604 个)

### 主要分类概览

| 分类 | 数量 | 主要内容 |
|------|------|---------|
| 🤖 AI 与智能代理 | 47 | LLM 应用、RAG、代理架构、提示工程 |
| 🏗️ 架构与设计 | 36 | 系统架构、微服务、事件驱动、DDD |
| 🔐 安全与渗透测试 | 47 | 漏洞扫描、渗透测试、安全审计 |
| 💾 数据库与数据工程 | 17 | SQL/NoSQL、数据管道、向量数据库 |
| 🎨 前端开发 | 28 | React、Next.js、UI/UX、组件库 |
| ⚙️ 后端开发 | 32 | API 设计、微服务、认证、消息队列 |
| 📱 移动开发 | 8 | React Native、Flutter、iOS/Android |
| ☁️ 云与 DevOps | 33 | K8s、CI/CD、监控、IaC、GitOps |
| 🧪 测试与质量 | 35 | TDD、E2E、代码审查、性能测试 |
| 📊 数据与可视化 | 12 | 数据可视化、BI、ML、量化分析 |
| 🎮 游戏开发 | 8 | Unity、Unreal、Godot、ECS |
| 📝 文档与内容 | 22 | 技术写作、API 文档、营销文案 |
| 🔧 工具与自动化 | 37 | CLI、脚本、爬虫、文件处理 |
| 🌐 Web3 区块链 | 3 | 智能合约、DeFi、NFT |
| 💼 产品与营销 | 32 | 产品管理、增长、定价、SEO |
| 🎓 学习与知识 | 9 | 研究工具、笔记系统 |
| 🔍 搜索与 SEO | 6 | 搜索优化、关键词、内容策略 |
| 💬 通信与社交 | 8 | 聊天机器人、社交媒体自动化 |
| 🖼️ 图像与创意 | 24 | AI 绘画、图像处理、设计 |
| 📦 编程语言 | 25 | Python、Rust、Go、TypeScript |
| 🔄 其他专业 | 135 | HR、法律、财务、行业特定 |

**总计：604 个专业技能**

---

## 📚 详细技能清单

### 🤖 AI 与智能代理 (47个)

| 名称 | 功能简述 |
|------|----------|
| `advanced-evaluation` | This skill should be used when the user asks to "implement L |
| `agent-evaluation` | Testing and benchmarking LLM agents including behavioral tes |
| `agent-manager-skill` | Manage multiple local CLI agents via tmux sessions (start/st |
| `agent-memory-mcp` | A hybrid memory system that provides persistent, searchable  |
| `agent-memory-systems` | Memory is the cornerstone of intelligent agents. Without it, |
| `agent-tool-builder` | Tools are how AI agents interact with the world. A well-desi |
| `ai-agents-architect` | Expert in designing and building autonomous AI agents. Maste |
| `ai-engineer` | Build production-ready LLM applications, advanced RAG system |
| `ai-product` | Every product will be AI-powered. The question is whether yo |
| `ai-wrapper-product` | Expert in building products that wrap AI APIs (OpenAI, Anthr |
| `autonomous-agent-patterns` | Design patterns for building autonomous coding agents. Cover |
| `bullmq-specialist` | BullMQ expert for Redis-backed job queues, background proces |
| `computer-use-agents` | Build AI agents that interact with computers like humans do  |
| `context-compression` | Design and evaluate compression strategies for long-running  |
| `context-degradation` | Recognize patterns of context failure: lost-in-middle, poiso |
| `context-driven-development` | Use this skill when working with Conductor's context-driven |
| `context-extract` | Append conversation context to cumulative project history -  |
| `context-fundamentals` | Understand what context is, why it matters, and the anatomy  |
| `context-manager` | Elite AI context engineering specialist mastering dynamic co |
| `context-optimization` | Apply compaction, masking, and caching strategies |
| `context-window-management` | Strategies for managing LLM context windows including summar |
| `crewai` | Expert in CrewAI - the leading role-based multi-agent framew |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on w |
| `embedding-strategies` | Select and optimize embedding models for semantic search and |
| `evaluation` | Build evaluation frameworks for agent systems |
| `fp-ts-pragmatic` | A practical, jargon-free guide to fp-ts functional programmi |
| `hosted-agents` | This skill should be used when the user asks to "build backg |
| `langchain-architecture` | Design LLM applications using the LangChain framework with a |
| `langfuse` | Expert in Langfuse - the open-source LLM observability platf |
| `langgraph` | Expert in LangGraph - the production-grade framework for bui |
| `langsmith-fetch` | Debug LangChain and LangGraph agents by fetching execution t |
| `llm-app-patterns` | Production-ready patterns for building LLM applications. Cov |
| `llm-evaluation` | Implement comprehensive evaluation strategies for LLM applic |
| `memory-systems` | Design short-term, long-term, and graph-based memory archite |
| `multi-agent-brainstorming` | > |
| `multi-agent-patterns` | Master orchestrator, peer-to-peer, and hierarchical multi-ag |
| `parallel-agents` | Multi-agent orchestration patterns. Use when multiple indepe |
| `prompt-caching` | Caching strategies for LLM prompts including Anthropic promp |
| `prompt-engineering` | Expert guide on prompt engineering patterns, best practices, |
| `prompt-library` | Curated collection of high-quality prompts for various use c |
| `rag-engineer` | Expert in building Retrieval-Augmented Generation systems. M |
| `rag-implementation` | Build Retrieval-Augmented Generation (RAG) systems for LLM a |
| `subagent-driven-development` | Use when executing implementation plans with independent tas |
| `vector-database-engineer` | Expert in vector databases, embedding strategies, and semant |
| `voice-agents` | Voice agents represent the frontier of AI interaction - huma |
| `voice-ai-development` | Expert in building voice AI applications - from real-time vo |
| `voice-ai-engine-development` | Build real-time conversational AI voice engines using async  |

### 🏗️ 架构与设计 (36个)

| 名称 | 功能简述 |
|------|----------|
| `api-design-principles` | Master REST and GraphQL API design principles to build intui |
| `architect-review` | Master software architect specializing in modern architectur |
| `architecture` | Architectural decision-making framework. Requirements analys |
| `architecture-decision-records` | Write and maintain Architecture Decision Records (ADRs) foll |
| `architecture-patterns` | Implement proven backend architecture patterns including Cle |
| `backend-architect` | Expert backend architect specializing in scalable API design |
| `c4-architecture-c4-architecture` | Generate comprehensive C4 architecture documentation for an  |
| `c4-code` | Expert C4 Code-level documentation specialist. Analyzes code |
| `c4-component` | Expert C4 Component-level documentation specialist. Synthesi |
| `c4-container` | Expert C4 Container-level documentation specialist. Synthesi |
| `c4-context` | Expert C4 Context-level documentation specialist. Creates |
| `cloud-architect` | Expert cloud architect specializing in AWS/Azure/GCP multi-c |
| `cqrs-implementation` | Implement Command Query Responsibility Segregation for scala |
| `database-architect` | Expert database architect specializing in data layer design  |
| `design-md` | Analyze Stitch projects and synthesize a semantic design sys |
| `design-orchestration` | > |
| `discord-bot-architect` | Specialized skill for building production-ready Discord bots |
| `docs-architect` | Creates comprehensive technical documentation from existing |
| `dotnet-architect` | Expert .NET backend architect specializing in C#, ASP.NET Co |
| `event-sourcing-architect` | Expert in event sourcing, CQRS, and event-driven architectur |
| `graphql-architect` | Master modern GraphQL with federation, performance optimizat |
| `hybrid-cloud-architect` | Expert hybrid cloud architect specializing in complex multi- |
| `kubernetes-architect` | Expert Kubernetes architect specializing in cloud-native |
| `microservices-patterns` | Design microservices architectures with service boundaries,  |
| `monorepo-architect` | Expert in monorepo architecture, build systems, and dependen |
| `monorepo-management` | Master monorepo management with Turborepo, Nx, and pnpm work |
| `multi-cloud-architecture` | Design multi-cloud architectures using a decision framework  |
| `projection-patterns` | Build read models and projections from event streams. Use wh |
| `radix-ui-design-system` | Build accessible design systems with Radix UI primitives. He |
| `react-native-architecture` | Build production React Native apps with Expo, navigation, na |
| `saga-orchestration` | Implement saga patterns for distributed transactions and cro |
| `senior-architect` | Comprehensive software architecture skill for designing scal |
| `seo-structure-architect` | Analyzes and optimizes content structure including header |
| `software-architecture` | Guide for quality focused software architecture. This skill  |
| `tailwind-design-system` | Build scalable design systems with Tailwind CSS, design toke |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. Use  |

### 🔐 安全与渗透测试 (47个)

| 名称 | 功能简述 |
|------|----------|
| `active-directory-attacks` | This skill should be used when the user asks to "attack Acti |
| `anti-reversing-techniques` | Understand anti-reversing, obfuscation, and protection techn |
| `api-fuzzing-bug-bounty` | This skill should be used when the user asks to "test API se |
| `api-security-best-practices` | Implement secure API design patterns including authenticatio |
| `attack-tree-construction` | Build comprehensive attack trees to visualize threat paths.  |
| `aws-penetration-testing` | This skill should be used when the user asks to "pentest AWS |
| `backend-security-coder` | Expert in secure backend coding practices specializing in in |
| `broken-authentication` | This skill should be used when the user asks to "test for br |
| `burp-suite-testing` | This skill should be used when the user asks to "intercept H |
| `ciphey` | Automatic decryption and decoding tool using AI. Use when us |
| `cloud-penetration-testing` | This skill should be used when the user asks to "perform clo |
| `ethical-hacking-methodology` | This skill should be used when the user asks to "learn ethic |
| `ffuf-claude-skill` | Web fuzzing with ffuf |
| `file-path-traversal` | This skill should be used when the user asks to "test for di |
| `frontend-security-coder` | Expert in secure frontend coding practices specializing in X |
| `html-injection-testing` | This skill should be used when the user asks to "test for HT |
| `idor-testing` | This skill should be used when the user asks to "test for in |
| `k8s-security-policies` | Implement Kubernetes security policies including NetworkPoli |
| `linux-privilege-escalation` | This skill should be used when the user asks to "escalate pr |
| `malware-analyst` | Expert malware analyst specializing in defensive malware res |
| `memory-forensics` | Master memory forensics techniques including memory acquisit |
| `metasploit-framework` | This skill should be used when the user asks to "use Metaspl |
| `mobile-security-coder` | Expert in secure mobile coding practices specializing in inp |
| `pentest-checklist` | This skill should be used when the user asks to "plan a pene |
| `pentest-commands` | This skill should be used when the user asks to "run pentest |
| `privilege-escalation-methods` | This skill should be used when the user asks to "escalate pr |
| `red-team-tactics` | Red team tactics principles based on MITRE ATT&CK. Attack ph |
| `red-team-tools` | This skill should be used when the user asks to "follow red  |
| `scanning-tools` | This skill should be used when the user asks to "perform vul |
| `security-auditor` | Expert security auditor specializing in DevSecOps, comprehen |
| `security-bluebook-builder` | Build security Blue Books for sensitive apps |
| `security-requirement-extraction` | Derive security requirements from threat models and business |
| `security-review` | Use this skill when adding authentication, handling user inp |
| `shodan-reconnaissance` | This skill should be used when the user asks to "search for  |
| `smtp-penetration-testing` | This skill should be used when the user asks to "perform SMT |
| `solidity-security` | Master smart contract security best practices to prevent com |
| `sql-injection-testing` | This skill should be used when the user asks to "test for SQ |
| `sqlmap-database-pentesting` | This skill should be used when the user asks to "automate SQ |
| `ssh-penetration-testing` | This skill should be used when the user asks to "pentest SSH |
| `threat-mitigation-mapping` | Map identified threats to appropriate security controls and  |
| `threat-modeling-expert` | Expert in threat modeling methodologies, security architectu |
| `top-web-vulnerabilities` | This skill should be used when the user asks to "identify we |
| `vulnerability-scanner` | Advanced vulnerability analysis principles. OWASP 2025, Supp |
| `windows-privilege-escalation` | This skill should be used when the user asks to "escalate pr |
| `wireshark-analysis` | This skill should be used when the user asks to "analyze net |
| `wordpress-penetration-testing` | This skill should be used when the user asks to "pentest Wor |
| `xss-html-injection` | This skill should be used when the user asks to "test for XS |

### 💾 数据库与数据工程 (17个)

| 名称 | 功能简述 |
|------|----------|
| `airflow-dag-patterns` | Build production Apache Airflow DAGs with best practices for |
| `angular-migration` | Migrate from AngularJS to Angular using hybrid mode, increme |
| `clickhouse-io` | ClickHouse database patterns, query optimization, analytics, |
| `data-engineer` | Build scalable data pipelines, modern data warehouses, and |
| `data-quality-frameworks` | Implement data quality validation with Great Expectations, d |
| `database-admin` | Expert database administrator specializing in modern cloud |
| `database-design` | Database design principles and decision-making. Schema desig |
| `database-migration` | Execute database migrations across ORMs and platforms with z |
| `database-optimizer` | Expert database optimizer specializing in modern performance |
| `dbt-transformation-patterns` | Master dbt (data build tool) for analytics engineering with  |
| `neon-postgres` | Expert patterns for Neon serverless Postgres, branching, con |
| `nosql-expert` | Expert guidance for distributed NoSQL databases (Cassandra,  |
| `postgres-best-practices` | Postgres performance optimization and best practices from Su |
| `postgresql` | Design a PostgreSQL-specific schema. Covers best-practices,  |
| `spark-optimization` | Optimize Apache Spark jobs with partitioning, caching, shuff |
| `sql-optimization-patterns` | Master SQL query optimization, indexing strategies, and EXPL |
| `sql-pro` | Master modern SQL with cloud-native databases, OLTP/OLAP |

### 🎨 前端开发 (28个)

| 名称 | 功能简述 |
|------|----------|
| `a2ui-embed` | Write HTML visualizations to the A2UI panel or embed running |
| `core-components` | Core component library and design system patterns. Use when  |
| `expo-tailwind-setup` | Set up Tailwind CSS v4 in Expo with react-native-css and Nat |
| `fp-ts-react` | Practical patterns for using fp-ts with React - hooks, state |
| `frontend-design` | Create distinctive, production-grade frontend interfaces wit |
| `frontend-dev-guidelines` | Opinionated frontend development standards for modern React  |
| `frontend-developer` | Build React components, implement responsive layouts, and ha |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state mana |
| `frontend-slides` | Create stunning, animation-rich HTML presentations from scra |
| `nextjs-app-router-patterns` | Master Next.js 14+ App Router with Server Components, stream |
| `nextjs-best-practices` | Next.js App Router principles. Server Components, data fetch |
| `nextjs-supabase-auth` | Expert integration of Supabase Auth with Next.js App Router  |
| `react-best-practices` | React and Next.js performance optimization guidelines from V |
| `react-modernization` | Upgrade React applications to latest versions, migrate from  |
| `react-patterns` | Modern React patterns and principles. Hooks, composition, pe |
| `react-state-management` | Master modern React state management with Redux Toolkit, Zus |
| `react-ui-patterns` | Modern React UI patterns for loading states, error handling, |
| `scroll-experience` | Expert in building immersive scroll-driven experiences - par |
| `stitch-ui-design` | Expert guide for creating effective prompts for Google Stitc |
| `swiftui-expert-skill` | Write, review, or improve SwiftUI code following best practi |
| `tailwind-patterns` | Tailwind CSS v4 principles. CSS-first configuration, contain |
| `ui-skills` | Opinionated, evolving constraints to guide agents when build |
| `ui-ux-designer` | Create interface designs, wireframes, and design systems. Ma |
| `ui-ux-pro-max` | UI/UX design intelligence. 50 styles, 21 palettes, 50 font p |
| `ui-visual-validator` | Rigorous visual validation expert specializing in UI testing |
| `vercel-react-best-practices` | React and Next.js performance optimization guidelines from V |
| `vercel-react-native-skills` |  |
| `web-performance-optimization` | Optimize website and web application performance including l |

### ⚙️ 后端开发 (32个)

| 名称 | 功能简述 |
|------|----------|
| `api-documentation-generator` | Generate comprehensive, developer-friendly API documentation |
| `api-patterns` | API design principles and decision-making. REST vs GraphQL v |
| `auth-implementation-patterns` | Master authentication and authorization patterns including J |
| `backend-dev-guidelines` | Opinionated backend development standards for Node.js + Expr |
| `backend-patterns` | Backend architecture patterns, API design, database optimiza |
| `billing-automation` | Build automated billing systems for recurring payments, invo |
| `clerk-auth` | Expert patterns for Clerk auth implementation, middleware, o |
| `django-pro` | Master Django 5.x with async views, DRF, Celery, and Django |
| `dotnet-backend-patterns` | Master C#/.NET backend development patterns for building rob |
| `expo-api-routes` | Guidelines for creating API routes in Expo Router with EAS H |
| `fastapi-pro` | Build high-performance async APIs with FastAPI, SQLAlchemy 2 |
| `fastapi-templates` | Create production-ready FastAPI projects with async patterns |
| `firebase` | Firebase gives you a complete backend in minutes - auth, dat |
| `graphql` | GraphQL gives clients exactly the data they need - no more,  |
| `hubspot-integration` | Expert patterns for HubSpot CRM integration including OAuth  |
| `inngest` | Inngest expert for serverless-first background jobs, event-d |
| `moodle-external-api-development` | Create custom external web service APIs for Moodle LMS. Use  |
| `nestjs-expert` | Nest.js framework expert specializing in module architecture |
| `nodejs-backend-patterns` | Build production-ready Node.js backend services with Express |
| `nodejs-best-practices` | Node.js development principles and decision-making. Framewor |
| `openapi-spec-generation` | Generate and maintain OpenAPI 3.1 specifications from code,  |
| `payment-integration` | Integrate Stripe, PayPal, and payment processors. Handles ch |
| `paypal-integration` | Integrate PayPal payment processing with support for express |
| `plaid-fintech` | Expert patterns for Plaid API integration including Link tok |
| `salesforce-development` | Expert patterns for Salesforce platform development includin |
| `segment-cdp` | Expert patterns for Segment Customer Data Platform including |
| `shopify-apps` | Expert patterns for Shopify app development including Remix/ |
| `shopify-development` | - |
| `stripe-integration` | Implement Stripe payment processing for robust, PCI-complian |
| `temporal-python-pro` | Master Temporal workflow orchestration with Python SDK. Impl |
| `temporal-python-testing` | Test Temporal workflows with pytest, time-skipping, and mock |
| `trigger-dev` | Trigger.dev expert for background jobs, AI workflows, and re |

### 📱 移动开发 (8个)

| 名称 | 功能简述 |
|------|----------|
| `app-store-optimization` | Complete App Store Optimization (ASO) toolkit for researchin |
| `expo-cicd-workflows` | Helps understand and write EAS workflow YAML files for Expo  |
| `expo-deployment` | Deploy Expo apps to production |
| `expo-dev-client` | Build and distribute Expo development clients locally or via |
| `flutter-expert` | Master Flutter development with Dart 3, advanced widgets, an |
| `ios-developer` | Develop native iOS applications with Swift/SwiftUI. Masters  |
| `mobile-design` | Mobile-first design and engineering doctrine for iOS and And |
| `mobile-developer` | Develop React Native, Flutter, or native mobile apps with mo |

### ☁️ 云与 DevOps (33个)

| 名称 | 功能简述 |
|------|----------|
| `aws-serverless` | Specialized skill for building production-ready serverless a |
| `aws-skills` | AWS development with infrastructure automation and cloud arc |
| `azure-functions` | Expert patterns for Azure Functions development including is |
| `cost-optimization` | Optimize cloud costs through resource rightsizing, tagging s |
| `deployment-engineer` | Expert deployment engineer specializing in modern CI/CD pipe |
| `deployment-pipeline-design` | Design multi-stage CI/CD pipelines with approval gates, secu |
| `deployment-procedures` | Production deployment principles and decision-making. Safe d |
| `devops-troubleshooter` | Expert DevOps troubleshooter specializing in rapid incident |
| `docker-expert` | Docker containerization expert with deep knowledge of multi- |
| `gcp-cloud-run` | Specialized skill for building production-ready serverless a |
| `github-actions-templates` | Create production-ready GitHub Actions workflows for automat |
| `gitlab-ci-patterns` | Build GitLab CI/CD pipelines with multi-stage workflows, cac |
| `gitops-workflow` | Implement GitOps workflows with ArgoCD and Flux for automate |
| `grafana-dashboards` | Create and manage production Grafana dashboards for real-tim |
| `helm-chart-scaffolding` | Design, organize, and manage Helm charts for templating and  |
| `hybrid-cloud-networking` | Configure secure, high-performance connectivity between on-p |
| `incident-responder` | Expert SRE incident responder specializing in rapid problem |
| `incident-runbook-templates` | Create structured incident response runbooks with step-by-st |
| `istio-traffic-management` | Configure Istio traffic management including routing, load b |
| `k8s-manifest-generator` | Create production-ready Kubernetes manifests for Deployments |
| `linkerd-patterns` | Implement Linkerd service mesh patterns for lightweight, sec |
| `mtls-configuration` | Configure mutual TLS (mTLS) for zero-trust service-to-servic |
| `observability-engineer` | Build production-ready monitoring, logging, and tracing syst |
| `on-call-handoff-patterns` | Master on-call shift handoffs with context transfer, escalat |
| `prometheus-configuration` | Set up Prometheus for comprehensive metric collection, stora |
| `secrets-management` | Implement secure secrets management for CI/CD pipelines usin |
| `service-mesh-expert` | Expert service mesh architect specializing in Istio, Linkerd |
| `service-mesh-observability` | Implement comprehensive observability for service meshes inc |
| `slo-implementation` | Define and implement Service Level Indicators (SLIs) and Ser |
| `terraform-module-library` | Build reusable Terraform modules for AWS, Azure, and GCP inf |
| `terraform-skill` | Terraform infrastructure as code best practices |
| `terraform-specialist` | Expert Terraform/OpenTofu specialist mastering advanced IaC |
| `vercel-deployment` | Expert knowledge for deploying to Vercel with Next.js Use wh |

### 🧪 测试与质量 (35个)

| 名称 | 功能简述 |
|------|----------|
| `ab-test-setup` | Structured guide for setting up A/B tests with mandatory gat |
| `backtesting-frameworks` | Build robust backtesting systems for trading strategies with |
| `bats-testing-patterns` | Master Bash Automated Testing System (Bats) for comprehensiv |
| `code-review-checklist` | Comprehensive checklist for conducting thorough code reviews |
| `code-review-excellence` | Master effective code review practices to provide constructi |
| `code-reviewer` | Elite code review expert specializing in modern AI-powered c |
| `debugging-strategies` | Master systematic debugging techniques, profiling tools, and |
| `debugging-toolkit-smart-debug` | Use when working with debugging toolkit smart debug |
| `e2e-testing-patterns` | Master end-to-end testing with Playwright and Cypress to bui |
| `error-detective` | Search logs and codebases for error patterns, stack traces,  |
| `error-handling-patterns` | Master error handling patterns across languages including ex |
| `find-bugs` | Find bugs, security vulnerabilities, and code quality issues |
| `fix-review` | Verify fix commits address audit findings without new bugs |
| `javascript-testing-patterns` | Implement comprehensive testing strategies using Jest, Vites |
| `lint-and-validate` | Automatic quality control, linting, and static analysis proc |
| `playwright-skill` | Complete browser automation with Playwright. Auto-detects de |
| `python-testing-patterns` | Implement comprehensive testing strategies with pytest, fixt |
| `receiving-code-review` | Use when receiving code review feedback, before implementing |
| `requesting-code-review` | Use when completing tasks, implementing major features, or b |
| `sast-configuration` | Configure Static Application Security Testing (SAST) tools f |
| `screen-reader-testing` | Test web applications with screen readers including VoiceOve |
| `shellcheck-configuration` | Master ShellCheck static analysis configuration and usage fo |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected b |
| `tdd-orchestrator` | Master TDD orchestrator specializing in red-green-refactor |
| `tdd-workflow` | Test-Driven Development workflow principles. RED-GREEN-REFAC |
| `test-automator` | Master AI-powered test automation with modern frameworks, |
| `test-driven-development` | Use when implementing any feature or bugfix, before writing  |
| `test-fixing` | Run tests and systematically fix all failing tests using sma |
| `testing-patterns` | Jest testing patterns, factory functions, mocking strategies |
| `unit-testing-test-generate` | Generate comprehensive, maintainable unit tests across langu |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, |
| `verification-loop` |  |
| `wcag-audit-patterns` | Conduct WCAG 2.2 accessibility audits with automated testing |
| `web3-testing` | Test smart contracts comprehensively using Hardhat and Found |
| `webapp-testing` | Toolkit for interacting with and testing local web applicati |

### 📊 数据与可视化 (12个)

| 名称 | 功能简述 |
|------|----------|
| `analytics-tracking` | > |
| `claude-d3js-skill` | Creating interactive data visualisations using d3.js. This s |
| `d3-viz` | Creating interactive data visualisations using d3.js. This s |
| `data-scientist` | Expert data scientist for advanced analytics, machine learni |
| `data-storytelling` | Transform data into compelling narratives using visualizatio |
| `kpi-dashboard-design` | Design effective KPI dashboards with metrics selection, visu |
| `ml-engineer` | Build production ML systems with PyTorch 2.x, TensorFlow, an |
| `ml-pipeline-workflow` | Build end-to-end MLOps pipelines from data preparation throu |
| `mlops-engineer` | Build comprehensive ML pipelines, experiment tracking, and m |
| `quant-analyst` | Build financial models, backtest trading strategies, and ana |
| `risk-manager` | Monitor portfolio risk, R-multiples, and position limits. Cr |
| `risk-metrics-calculation` | Calculate portfolio risk metrics including VaR, CVaR, Sharpe |

### 🎮 游戏开发 (8个)

| 名称 | 功能简述 |
|------|----------|
| `3d-web-experience` | Expert in building 3D experiences for the web - Three.js, Re |
| `game-development` | Game development orchestrator. Routes to platform-specific s |
| `godot-gdscript-patterns` | Master Godot 4 GDScript patterns including signals, scenes,  |
| `minecraft-bukkit-pro` | Master Minecraft server plugin development with Bukkit, Spig |
| `threejs-skills` | Three.js skills for creating 3D elements and interactive exp |
| `unity-developer` | Build Unity games with optimized C# scripts, efficient rende |
| `unity-ecs-patterns` | Master Unity ECS (Entity Component System) with DOTS, Jobs,  |
| `unreal-engine-cpp-pro` | Expert guide for Unreal Engine 5.x C++ development, covering |

### 📝 文档与内容 (22个)

| 名称 | 功能简述 |
|------|----------|
| `beautiful-prose` | Hard-edged writing style contract for timeless, forceful Eng |
| `changelog-automation` | Automate changelog generation from commits, PRs, and release |
| `changelog-generator` | Automatically creates user-facing changelogs from git commit |
| `content-creator` | Create SEO-optimized marketing content with consistent brand |
| `content-marketer` | Elite content marketing strategist specializing in AI-powere |
| `content-research-writer` | Assists in writing high-quality content by conducting resear |
| `content-strategy` | When the user wants to plan a content strategy, decide what  |
| `copy-editing` | When the user wants to edit, review, or improve existing mar |
| `copywriting` | > |
| `doc-coauthoring` | Guide users through a structured workflow for co-authoring d |
| `documentation-templates` | Documentation templates and structure guidelines. README, AP |
| `docx-official` | Comprehensive document creation, editing, and analysis with  |
| `plan-writing` | Structured task planning with clear breakdowns, dependencies |
| `postmortem-writing` | Write effective blameless postmortems with root cause analys |
| `reference-builder` | Creates exhaustive technical references and API documentatio |
| `seo-content-auditor` | Analyzes provided content for quality, E-E-A-T signals, and  |
| `seo-content-planner` | Creates comprehensive content outlines and topic clusters fo |
| `seo-content-refresher` | Identifies outdated elements in provided content and suggest |
| `seo-content-writer` | Writes SEO-optimized content based on provided keywords and  |
| `tutorial-engineer` | Creates step-by-step tutorials and educational content from  |
| `writing-plans` | Use when you have a spec or requirements for a multi-step ta |
| `writing-skills` | Use when creating, updating, or improving agent skills. |

### 🔧 工具与自动化 (37个)

| 名称 | 功能简述 |
|------|----------|
| `.spec-workflow` |  |
| `automate-whatsapp` | Build WhatsApp automations with Kapso workflows: configure W |
| `browser-automation` | Browser automation powers web testing, scraping, and AI agen |
| `browser-extension-builder` | Expert in building browser extensions that solve real proble |
| `connect` | Connect Claude to any app. Send emails, create issues, post  |
| `connect-apps-plugin` |  |
| `email-sequence` | When the user wants to create or optimize an email sequence, |
| `email-systems` | Email has the highest ROI of any marketing channel. $36 for  |
| `fal-workflow` | Generate workflow JSON files for chaining AI models |
| `file-organizer` | Intelligently organizes files and folders by understanding c |
| `firecrawl-scraper` | Deep web scraping, screenshots, PDF parsing, and website cra |
| `git-advanced-workflows` | Master advanced Git workflows including rebasing, cherry-pic |
| `github-workflow-automation` | Automate GitHub workflows with AI assistance. Includes PR re |
| `invoice-organizer` | Automatically organizes invoices and receipts for tax prepar |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) |
| `n8n-code-python` | Write Python code in n8n Code nodes. Use when writing Python |
| `n8n-mcp-tools-expert` | Expert guide for using n8n-mcp MCP tools effectively. Use wh |
| `n8n-node-configuration` | Operation-aware node configuration guidance. Use when config |
| `observe-whatsapp` | Observe and troubleshoot WhatsApp in Kapso: debug message de |
| `pdf-official` | Comprehensive PDF manipulation toolkit for extracting text a |
| `personal-tool-builder` | Expert in building custom tools that solve your own problems |
| `pptx-official` | Presentation creation, editing, and analysis. When Claude ne |
| `raffle-winner-picker` | Picks random winners from lists, spreadsheets, or Google She |
| `sales-automator` | Draft cold emails, follow-ups, and proposal templates. Creat |
| `skill-forge` |  |
| `skill-rails-upgrade` | Analyze Rails apps and provide upgrade assessments |
| `slack-bot-builder` | Build Slack apps using the Bolt framework across Python, Jav |
| `slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimized |
| `telegram-bot-builder` | Expert in building Telegram bots that solve real problems -  |
| `telegram-mini-app` | Expert in building Telegram Mini Apps (TWA) - web apps that  |
| `tool-design` | Build tools that agents can use effectively, including archi |
| `unzip-crx` | Extract Chrome extension (.crx) files. Use when user needs t |
| `video-downloader` | Downloads videos from YouTube and other platforms for offlin |
| `workflow-automation` | Workflow automation is the infrastructure that makes AI agen |
| `workflow-patterns` | Use this skill when implementing tasks according to Conducto |
| `xlsx-official` | Comprehensive spreadsheet creation, editing, and analysis wi |
| `zapier-make-patterns` | No-code automation democratizes workflow building. Zapier an |

### 🌐 Web3 区块链 (3个)

| 名称 | 功能简述 |
|------|----------|
| `blockchain-developer` | Build production-ready Web3 applications, smart contracts, a |
| `defi-protocol-templates` | Implement DeFi protocols with production-ready templates for |
| `nft-standards` | Implement NFT standards (ERC-721, ERC-1155) with proper meta |

### 💼 产品与营销 (32个)

| 名称 | 功能简述 |
|------|----------|
| `brand-guidelines` | Applies Anthropic's official brand colors and typography to  |
| `business-analyst` | Master modern business analysis with AI-powered analytics, |
| `competitor-alternatives` | When the user wants to create competitor comparison or alter |
| `form-cro` | > |
| `free-tool-strategy` | When the user wants to plan, evaluate, or build a free tool  |
| `launch-strategy` | When the user wants to plan a product launch, feature announ |
| `lead-research-assistant` | Identifies high-quality leads for your product or service by |
| `market-sizing-analysis` | This skill should be used when the user asks to "calculate T |
| `marketing-ideas` | Provide proven marketing strategies and growth ideas for Saa |
| `marketing-psychology` | Apply behavioral science and mental models to marketing deci |
| `micro-saas-launcher` | Expert in launching small, focused SaaS products fast - the  |
| `onboarding-cro` | When the user wants to optimize post-signup onboarding, user |
| `page-cro` | > |
| `paid-ads` | When the user wants help with paid advertising campaigns on  |
| `paywall-upgrade-cro` | When the user wants to create or optimize in-app paywalls, u |
| `popup-cro` | Create and optimize popups, modals, overlays, slide-ins, and |
| `pricing-strategy` | Design pricing, packaging, and monetization strategies based |
| `product-manager-toolkit` | Comprehensive toolkit for product managers including RICE pr |
| `product-marketing-context` | When the user wants to create or update their product market |
| `referral-program` | When the user wants to create, optimize, or analyze a referr |
| `seo-audit` | > |
| `seo-authority-builder` | Analyzes content for E-E-A-T signals and suggests improvemen |
| `seo-cannibalization-detector` | Analyzes multiple provided pages to identify keyword overlap |
| `seo-fundamentals` | > |
| `seo-keyword-strategist` | Analyzes keyword usage in provided content, calculates densi |
| `seo-meta-optimizer` | Creates optimized meta titles, descriptions, and URL suggest |
| `seo-snippet-hunter` | Formats content to be eligible for featured snippets and SER |
| `signup-flow-cro` | When the user wants to optimize signup, registration, accoun |
| `startup-analyst` | Expert startup business analyst specializing in market sizin |
| `startup-financial-modeling` | This skill should be used when the user asks to "create fina |
| `startup-metrics-framework` | This skill should be used when the user asks about "key star |
| `viral-generator-builder` | Expert in building shareable generator tools that go viral - |

### 🎓 学习与知识 (9个)

| 名称 | 功能简述 |
|------|----------|
| `context7-auto-research` | Automatically fetch latest library/framework documentation f |
| `deep-research` | Execute autonomous multi-step research using Google Gemini D |
| `exa-search` | Semantic search, similar content discovery, and structured r |
| `infinite-gratitude` | Multi-agent research skill for parallel research execution ( |
| `last30days` | Research a topic from the last 30 days on Reddit + X + Web,  |
| `notebooklm` | Use this skill to query your Google NotebookLM notebooks dir |
| `research-engineer` | An uncompromising Academic Research Engineer. Operates with  |
| `search-specialist` | Expert web researcher using advanced search techniques and |
| `tavily-web` | Web search, content extraction, crawling, and research capab |

### 🔍 搜索与 SEO (6个)

| 名称 | 功能简述 |
|------|----------|
| `algolia-search` | Expert patterns for Algolia search implementation, indexing  |
| `geo-fundamentals` | Generative Engine Optimization for AI search engines (ChatGP |
| `hybrid-search-implementation` | Combine vector and keyword search for improved retrieval. Us |
| `programmatic-seo` | > |
| `schema-markup` | > |
| `similarity-search-patterns` | Implement efficient similarity search with vector databases. |

### 💬 通信与社交 (8个)

| 名称 | 功能简述 |
|------|----------|
| `baoyu-post-to-wechat` | Posts content to WeChat Official Account (微信公众号) via Chrome  |
| `baoyu-post-to-x` | Posts content and articles to X (Twitter). Supports regular  |
| `customer-support` | Elite AI-powered customer support specialist mastering |
| `daily-news-report` | Scrapes content based on a preset URL list, filters high-qua |
| `internal-comms` | A set of resources to help me write all kinds of internal co |
| `meeting-insights-analyzer` | Analyzes meeting transcripts and recordings to uncover behav |
| `social-content` | When the user wants help creating, scheduling, or optimizing |
| `x-article-publisher-skill` | Publish articles to X/Twitter |

### 🖼️ 图像与创意 (24个)

| 名称 | 功能简述 |
|------|----------|
| `algorithmic-art` | Creating algorithmic art using p5.js with seeded randomness  |
| `artifacts-builder` | Suite of tools for creating elaborate, multi-component claud |
| `baoyu-article-illustrator` | Analyzes article structure, identifies positions requiring v |
| `baoyu-comic` | Knowledge comic creator supporting multiple art styles and t |
| `baoyu-compress-image` | Compresses images to WebP (default) or PNG with automatic to |
| `baoyu-cover-image` | Generates article cover images with 5 dimensions (type, pale |
| `baoyu-danger-gemini-web` | Generates images and text via reverse-engineered Gemini Web  |
| `baoyu-danger-x-to-markdown` | Converts X (Twitter) tweets and articles to markdown with YA |
| `baoyu-image-gen` | AI image generation with OpenAI and Google APIs. Supports te |
| `baoyu-infographic` | Generates professional infographics with 20 layout types and |
| `baoyu-slide-deck` | Generates professional slide deck images from content. Creat |
| `baoyu-url-to-markdown` | Fetch any URL and convert to markdown using Chrome CDP. Supp |
| `baoyu-xhs-images` | Generates Xiaohongshu (Little Red Book) infographic series w |
| `canvas-design` | Create beautiful visual art in .png and .pdf documents using |
| `fal-audio` | Text-to-speech and speech-to-text using fal.ai audio models |
| `fal-generate` | Generate images and videos using fal.ai AI models |
| `fal-image-edit` | AI-powered image editing with style transfer and object remo |
| `fal-platform` | Platform APIs for model management, pricing, and usage track |
| `fal-upscale` | Upscale and enhance image and video resolution using AI |
| `image-enhancer` | Improves the quality of images, especially screenshots, by e |
| `imagen` | - |
| `nanobanana-ppt-skills` | AI-powered PPT generation with document analysis and styled  |
| `theme-factory` | Toolkit for styling artifacts with a theme. These artifacts  |
| `web-artifacts-builder` | Suite of tools for creating elaborate, multi-component claud |

### 📦 编程语言 (25个)

| 名称 | 功能简述 |
|------|----------|
| `bash-defensive-patterns` | Master defensive Bash programming techniques for production- |
| `bash-linux` | Bash/Linux terminal patterns. Critical commands, piping, err |
| `bash-pro` | Master of defensive Bash scripting for production automation |
| `busybox-on-windows` | How to use a Win32 build of BusyBox to run many of the stand |
| `c-pro` | Write efficient C code with proper memory management, pointe |
| `cpp-pro` | Write idiomatic C++ code with modern features, RAII, smart |
| `csharp-pro` | Write modern C# code with advanced features like records, pa |
| `elixir-pro` | Write idiomatic Elixir code with OTP patterns, supervision t |
| `golang-pro` | Master Go 1.21+ with modern patterns, advanced concurrency, |
| `haskell-pro` | Expert Haskell engineer specializing in advanced type system |
| `hr-pro` | Professional, ethical HR partner for hiring, |
| `java-pro` | Master Java 21+ with modern features like virtual threads, p |
| `javascript-pro` | Master modern JavaScript with ES6+, async patterns, and Node |
| `julia-pro` | Master Julia 1.10+ with modern features, performance optimiz |
| `performance-profiling` | Performance profiling principles. Measurement, analysis, and |
| `php-pro` | Write idiomatic PHP code with generators, iterators, SPL dat |
| `posix-shell-pro` | Expert in strict POSIX sh scripting for maximum portability  |
| `powershell-windows` | PowerShell Windows patterns. Critical pitfalls, operator syn |
| `python-pro` | Master Python 3.12+ with modern features, async programming, |
| `ruby-pro` | Write idiomatic Ruby code with metaprogramming, Rails patter |
| `rust-pro` | Master Rust 1.75+ with modern async patterns, advanced type  |
| `scala-pro` | Master enterprise-grade Scala development with functional |
| `typescript-advanced-types` | Master TypeScript's advanced type system including generics, |
| `typescript-expert` | >- |
| `typescript-pro` | Master TypeScript with advanced types, generics, and strict  |

### 🔄 其他专业 (135个)

| 名称 | 功能简述 |
|------|----------|
| `.git` |  |
| `SPDD` |  |
| `a2ui` | Generate A2UI 0.8 protocol compliant UI code. Use when build |
| `address-github-comments` | Use when you need to address review or issue comments on an  |
| `app-builder` | Main application building orchestrator. Creates full-stack a |
| `arm-cortex-expert` | > |
| `async-python-patterns` | Master Python asyncio, concurrent programming, and async/awa |
| `avalonia-layout-zafiro` | Guidelines for modern Avalonia UI layout using Zafiro.Avalon |
| `avalonia-viewmodels-zafiro` | Optimal ViewModel and Wizard creation patterns for Avalonia  |
| `avalonia-zafiro-development` | Mandatory skills, conventions, and behavioral rules for Aval |
| `bazel-build-optimization` | Optimize Bazel builds for large-scale monorepos. Use when co |
| `bdi-mental-states` | This skill should be used when the user asks to "model agent |
| `behavioral-modes` | AI operational modes (brainstorm, implement, debug, review,  |
| `binary-analysis-patterns` | Master binary analysis patterns including disassembly, decom |
| `blockrun` | Use when user needs capabilities Claude lacks (image generat |
| `brainstorming` | > |
| `building-native-ui` | Complete guide for building beautiful apps with Expo Router. |
| `bun-development` | Modern JavaScript/TypeScript development with Bun runtime. C |
| `clarity-gate` | Pre-ingestion verification for epistemic quality in RAG syst |
| `claude-ally-health` | A health assistant skill for medical information analysis, s |
| `claude-code-guide` | Master guide for using Claude Code effectively. Includes con |
| `claude-scientific-skills` | Scientific research and analysis skills |
| `claude-speed-reader` | -Speed read Claude's responses at 600+ WPM using RSVP with S |
| `claude-win11-speckit-update-skill` | Windows 11 system management |
| `clean-code` | Pragmatic coding standards - concise, direct, no over-engine |
| `codex-review` | Professional code review with auto CHANGELOG generation, int |
| `coding-standards` | Universal coding standards, best practices, and patterns for |
| `commit` | Create commit messages following Sentry conventions. Use whe |
| `competitive-ads-extractor` | Extracts and analyzes competitors' ads from ad libraries (Fa |
| `competitive-landscape` | This skill should be used when the user asks to "analyze |
| `concise-planning` | Use when a user asks for a plan for a coding task, to genera |
| `conductor-implement` | Execute tasks from a track's implementation plan following T |
| `conductor-manage` | Manage track lifecycle: archive, restore, delete, rename, an |
| `conductor-new-track` | Create a new track with specification and phased implementat |
| `conductor-revert` | Git-aware undo by logical work unit (track, phase, or task) |
| `conductor-setup` | Initialize project with Conductor artifacts (product definit |
| `conductor-status` | Display project status, active tracks, and next actions |
| `conductor-validator` | Validates Conductor project artifacts for completeness, |
| `continuous-learning` | Automatically extract reusable patterns from Claude Code ses |
| `conversation-memory` | Persistent memory systems for LLM conversations including sh |
| `create-pr` | Create pull requests following Sentry conventions. Use when  |
| `culture-index` | Index and search culture documentation |
| `debugger` | Debugging specialist for errors, test failures, and unexpect |
| `dependency-upgrade` | Manage major dependency version upgrades with compatibility  |
| `developer-growth-analysis` | Analyzes your recent Claude Code chat history to identify co |
| `distributed-tracing` | Implement distributed tracing with Jaeger and Tempo to track |
| `domain-name-brainstormer` | Generates creative domain name ideas for your project and ch |
| `dx-optimizer` | Developer Experience specialist. Improves tooling, setup, an |
| `employment-contract-templates` | Create employment contracts, offer letters, and HR policy do |
| `environment-setup-guide` | Guide developers through setting up development environments |
| `eval-harness` |  |
| `event-store-design` | Design and implement event stores for event-sourced systems. |
| `executing-plans` | Use when you have a written implementation plan to execute i |
| `file-uploads` | Expert at handling file uploads and cloud storage. Covers S3 |
| `filesystem-context` | This skill should be used when the user asks to "offload con |
| `find-skills` | Helps users discover and install agent skills when they ask  |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you |
| `firmware-analyst` | Expert firmware analyst specializing in embedded systems, Io |
| `fp-ts-errors` | Handle errors as values using fp-ts Either and TaskEither fo |
| `gdpr-data-handling` | Implement GDPR-compliant data handling with consent manageme |
| `git-pushing` | Stage, commit, and push git changes with conventional commit |
| `go-concurrency-patterns` | Master Go concurrency with goroutines, channels, sync primit |
| `hugging-face-cli` | Execute Hugging Face Hub operations using the `hf` CLI. Use  |
| `hugging-face-jobs` | This skill should be used when users want to run any workloa |
| `i18n-localization` | Internationalization and localization patterns. Detecting ha |
| `interactive-portfolio` | Expert in building portfolios that actually land jobs and cl |
| `iterate-pr` | Iterate on a PR until CI passes. Use when you need to fix CI |
| `kaizen` | Guide for continuous improvement, error proofing, and standa |
| `legacy-modernizer` | Refactor legacy codebases, migrate outdated frameworks, and |
| `legal-advisor` | Draft privacy policies, terms of service, disclaimers, and l |
| `linear-claude-skill` | Manage Linear issues, projects, and teams |
| `linux-shell-scripting` | This skill should be used when the user asks to "create bash |
| `loki-mode` | Multi-agent autonomous startup system for Claude Code. Trigg |
| `makepad-skills` | Makepad UI development skills for Rust apps: setup, patterns |
| `memory-safety-patterns` | Implement memory-safe programming with RAII, ownership, smar |
| `mermaid-expert` | Create Mermaid diagrams for flowcharts, sequences, ERDs, and |
| `modern-javascript-patterns` | Master ES6+ features including async/await, destructuring, s |
| `native-data-fetching` | Use when implementing or debugging ANY network request, API  |
| `network-101` | This skill should be used when the user asks to "set up a we |
| `network-engineer` | Expert network engineer specializing in modern cloud network |
| `notion-template-business` | Expert in building and selling Notion templates as a busines |
| `nx-workspace-patterns` | Configure and optimize Nx monorepo workspaces. Use when sett |
| `obsidian-clipper-template-creator` | Guide for creating templates for the Obsidian Web Clipper. U |
| `pci-compliance` | Implement PCI DSS compliance requirements for secure handlin |
| `performance-engineer` | Expert performance engineer specializing in modern observabi |
| `planning-with-files` | Implements Manus-style file-based planning for complex tasks |
| `prisma-expert` | Prisma ORM expert for schema design, migrations, query optim |
| `production-code-audit` | Autonomously deep-scan entire codebase line-by-line, underst |
| `project-development` | This skill should be used when the user asks to "start an LL |
| `project-guidelines-example` |  |
| `protocol-reverse-engineering` | Master network protocol reverse engineering including packet |
| `pypict-skill` | Pairwise test generation |
| `python-packaging` | Create distributable Python packages with proper project str |
| `python-patterns` | Python development principles and decision-making. Framework |
| `python-performance-optimization` | Profile and optimize Python code using cProfile, memory prof |
| `ralph-loop` | Autonomous development loop for completing all remaining tas |
| `release-skills` | Universal release workflow. Auto-detects version files and c |
| `remotion-best-practices` | Best practices for Remotion - Video creation in React |
| `reverse-engineer` | Expert reverse engineer specializing in binary analysis, |
| `rust-async-patterns` | Master Rust async programming with Tokio, async traits, erro |
| `senior-fullstack` | Comprehensive fullstack development skill for building compl |
| `server-management` | Server management principles and decision-making. Process ma |
| `sharp-edges` | Identify error-prone APIs and dangerous configurations |
| `spec-analyze` | Perform non-destructive cross-artifact consistency and quali |
| `spec-checklist` | Generate custom quality checklists that validate REQUIREMENT |
| `spec-clarify` | Identify underspecified areas in a feature spec by asking up |
| `spec-constitution` | Create or update the project constitution with core principl |
| `spec-implement` | Execute implementation by processing tasks defined in tasks. |
| `spec-plan` | Execute implementation planning workflow to generate design  |
| `spec-specify` | Create or update a feature specification from a natural lang |
| `spec-tasks` | Generate actionable, dependency-ordered tasks.md organized b |
| `spec-taskstoissues` | Convert tasks.md into GitHub issues with proper dependencies |
| `specify-resources` | Shared resources (scripts, templates) for Spec-Driven Develo |
| `strategic-compact` | Suggests manual context compaction at logical intervals to p |
| `stride-analysis-patterns` | Apply STRIDE methodology to systematically identify threats. |
| `superpowers-lab` | Lab environment for Claude superpowers |
| `tailored-resume-generator` | Analyzes job descriptions and generates tailored resumes tha |
| `team-composition-analysis` | This skill should be used when the user asks to "plan team |
| `template-skill` | Replace with description of the skill and when Claude should |
| `track-management` | Use this skill when creating, managing, or working with Cond |
| `turborepo-caching` | Configure Turborepo for efficient monorepo builds with local |
| `twilio-communications` | Build communication features with Twilio: SMS messaging, voi |
| `upgrading-expo` | Upgrade Expo SDK versions |
| `upstash-qstash` | Upstash QStash expert for serverless message queues, schedul |
| `use-dom` | Use Expo DOM components to run web code in a webview on nati |
| `using-git-worktrees` | Use when starting feature work that needs isolation from cur |
| `using-neon` | Guides and best practices for working with Neon Serverless P |
| `using-superpowers` | Use when starting any conversation - establishes how to find |
| `uv-package-manager` | Master the uv package manager for fast Python dependency man |
| `varlock-claude-skill` | Secure environment variable management ensuring secrets are  |
| `vector-index-tuning` | Optimize vector index performance for latency, recall, and m |
| `vercel-composition-patterns` |  |
| `vercel-deploy-claimable` | Deploy applications and websites to Vercel. Use this skill w |
| `vexor` | Vector-powered CLI for semantic file search with a Claude/Co |
| `youtube-transcript` | Download YouTube video transcripts when user provides a YouT |

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
- 🧹 清理重复技能，从 695 个精简至 604 个
- 📊 重新整理分类，更新技能清单

### 2026-02-03
- ✨ 重新组织 README 结构，提升可读性
- 📊 将技能按 21 个分类整理
- 🔍 添加快速查找索引和场景导航

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
