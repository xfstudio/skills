# AI 工具接入配置模板

**重要：先确定用户是国内站还是国际站用户（见 SKILL.md「能力零」），再选用对应小节内的配置。两站域名、部分字段格式不同，不能混用。**

所有工具接入前提：已在对应站点的 API Key 管理页面创建好 API Key（若访问范围选"限定范围"，务必勾选本次要用的模型）：
- 国内站：`https://console.cloud.tencent.com/tokenhub/apikey`
- 国际站：`https://console.tencentcloud.com/tokenhub/apikey`

以下各小节的示例均以官方文档默认示例模型演示（国内站文档多用 `hy3`，国际站文档多用 `deepseek-v4-pro`），实际使用时将模型 ID 替换为用户要接入的真实模型（模型 ID 速查见 `model-quick-list.md`，或到对应站点的模型列表文档核实最新值）。

---

## WorkBuddy
类型：GUI 设置界面

### 国内站
文档：https://cloud.tencent.com/document/product/1823/131902
1. 启动 WorkBuddy → 左下角账户 → **设置**
2. 左侧导航选择**模型** → 自定义模型 → **添加模型**
3. 提供商选择 **自定义 / Custom**，填写：
   - **接口地址**：`https://tokenhub.tencentmaas.com/v1/chat/completions`
   - **API Key**：<用户的国内站 API Key>
   - **模型名称**：<模型ID，如 `hy3`>
   - **高级工具**（选填，建议勾选）：工具调用、图片输入、推理模式

### 国际站
文档：https://www.tencentcloud.com/document/product/1300/80640
步骤同国内站，字段差异：
   - **接口地址**：`https://tokenhub-intl.tencentcloudmaas.com/v1/chat/completions`
   - **API Key**：<用户的国际站 API Key>
   - **模型名称**：<模型ID，如 `deepseek-v4-pro`>
   - **高级工具**：建议勾选：工具调用、图片格式、推理模式

保存后在模型选择框中选中该模型即可对话（两站一致）。

---

## Claude Code
类型：配置文件（`settings.json`，环境变量）

配置文件路径（两站一致）：
- macOS/Linux：`~/.claude/settings.json`
- Windows：`用户目录\.claude\settings.json`（国际站文档写作 `%USERPROFILE%\.claude\settings.json`，等价）

不存在时创建：
```bash
# macOS/Linux
mkdir -p ~/.claude && touch ~/.claude/settings.json
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$HOME\.claude" | Out-Null; New-Item -ItemType File -Force -Path "$HOME\.claude\settings.json" | Out-Null
```

### 国内站
文档：https://cloud.tencent.com/document/product/1823/131903
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://tokenhub.tencentmaas.com",
    "ANTHROPIC_AUTH_TOKEN": "<用户的国内站 API Key>",
    "ANTHROPIC_MODEL": "<模型ID，如 hy3>",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "<同上模型ID>",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "<同上模型ID>",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "<同上模型ID>",
    "CLAUDE_CODE_SUBAGENT_MODEL": "<同上模型ID>",
    "ENABLE_TOOL_SEARCH": false
  }
}
```
验证：`/status` 确认 `API Endpoint` 为 `https://tokenhub.tencentmaas.com`。

### 国际站
文档：https://www.tencentcloud.com/document/product/1300/80641
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://tokenhub-intl.tencentcloudmaas.com",
    "ANTHROPIC_AUTH_TOKEN": "<用户的国际站 API Key>",
    "ANTHROPIC_MODEL": "<模型ID，如 deepseek-v4-pro>",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "<同上模型ID>",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "<同上模型ID>",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "<同上模型ID>",
    "CLAUDE_CODE_SUBAGENT_MODEL": "<同上模型ID>",
    "ENABLE_TOOL_SEARCH": false
  }
}
```
验证：`/status` 确认 `API Endpoint` 为 `https://tokenhub-intl.tencentcloudmaas.com`。

**两站共同注意**：`ANTHROPIC_BASE_URL` 均不带 `/v1`（Claude Code 自己会拼接路径），这是与其他工具的共同例外。`ENABLE_TOOL_SEARCH` 必须为 `false`（Claude Code 禁止第三方模型用内置 web search）。保存后**必须打开新终端窗口**才能加载生效。开启深度思考：`/config` → Thinking mode 设为 `true`（默认 `no_think`）。

---

## Cursor
类型：GUI 设置界面（需 Cursor Pro 及以上套餐才支持自定义模型）

步骤（两站一致）：`Cmd/Ctrl + Shift + P` → 输入 Cursor Settings → 左侧菜单 **Models**：

### 国内站
文档：https://cloud.tencent.com/document/product/1823/130933
   - **OpenAI API Key**：<用户的国内站 API Key>
   - **Override OpenAI Base URL**：`https://tokenhub.tencentmaas.com/v1`
   - **Add Custom model**：<模型ID，如 `hy3`>

### 国际站
文档：https://www.tencentcloud.com/document/product/1300/80646
   - **OpenAI API Key**：<用户的国际站 API Key>
   - **Override OpenAI Base URL**：`https://tokenhub-intl.tencentcloudmaas.com/v1`
   - **Add Custom model**：<模型ID，如 `deepseek-v4-pro`>

对话窗口找到该模型即可使用。

---

## CodeBuddy Code
类型：配置文件（`models.json`）

配置文件路径（两站一致）：
- macOS/Linux：`~/.codebuddy/models.json`
- Windows：`C:\Users\<用户名>\.codebuddy\models.json`

### 国内站
文档：https://cloud.tencent.com/document/product/1823/131901
```json
{
  "models": [
    {
      "id": "<模型ID，如 hy3>",
      "name": "<模型ID，如 hy3>",
      "vendor": "Tencent Cloud",
      "apiKey": "<用户的国内站 API Key>",
      "url": "https://tokenhub.tencentmaas.com/v1"
    }
  ],
  "availableModels": ["<模型ID，如 hy3>"]
}
```

### 国际站
文档：https://www.tencentcloud.com/document/product/1300/80639
```json
{
  "models": [
    {
      "id": "<模型ID，如 deepseek-v4-pro>",
      "name": "<模型ID，如 deepseek-v4-pro>",
      "vendor": "Tencent Cloud",
      "apiKey": "<用户的国际站 API Key>",
      "url": "https://tokenhub-intl.tencentcloudmaas.com/v1"
    }
  ],
  "availableModels": ["<模型ID，如 deepseek-v4-pro>"]
}
```

若文件已存在，仅在 `models`、`availableModels` 数组中追加，不要覆盖已有条目（两站一致）。启动 `codebuddy`，首次需选择信任目录、登录方式（Chinese Site / International Site / Enterprise Domain / iOA —— **注意此登录方式与上面的国内/国际站文档配置是两件事**：登录方式决定 CodeBuddy Code 工具本身用哪个账号体系登录，不影响你在 models.json 里配的腾讯云 TokenHub 模型该用哪个域名）。登录后输入 `/model` 选择刚配置的模型。

---

## OpenCode
类型：GUI（桌面端）或配置文件（终端 CLI 版）

### 桌面端（GUI，两站步骤一致，仅域名不同）
模型列表 → 管理模型/model settings → "+链接提供商"/"+" → 自定义 OpenAI 兼容提供商，填写：
- **提供商 ID**：`tencent`
- **显示名称**：`Tencent`
- **基础 URL**：国内站 `https://tokenhub.tencentmaas.com/v1` ｜ 国际站 `https://tokenhub-intl.tencentcloudmaas.com/v1`
- **API 密钥**：对应站点的 API Key
- **模型 ID**：<如 `deepseek-v4-pro`>
- **模型显示名称**：<自定义显示名>

国内站文档：https://cloud.tencent.com/document/product/1823/130936　国际站文档：https://www.tencentcloud.com/document/product/1300/80644

### 终端 CLI 版
配置文件路径（两站一致）：`~/.config/opencode/opencode.json`
```bash
mkdir -p ~/.config/opencode && open -e ~/.config/opencode/opencode.json
```

**国内站**配置内容：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "tencent": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Tencent",
      "options": { "baseURL": "https://tokenhub.tencentmaas.com/v1" },
      "models": { "<模型ID，如 deepseek-v4-pro>": { "name": "<自定义显示名>" } }
    }
  }
}
```

**国际站**配置内容：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "tencent": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Tencent",
      "options": { "baseURL": "https://tokenhub-intl.tencentcloudmaas.com/v1" },
      "models": { "<模型ID，如 deepseek-v4-pro>": { "name": "<自定义显示名>" } }
    }
  }
}
```

运行 `opencode` → `/connect` → 选择 **Tencent** → 粘贴对应站点的 API Key → `/models` 选择目标模型。

---

## Cline
类型：GUI 设置界面（VSCode 插件）

安装后选择 **Bring my own API key**，配置：
- **API Provider**：`OpenAI Compatible`（两站一致）
- **Base URL**：国内站 `https://tokenhub.tencentmaas.com/v1` ｜ 国际站 `https://tokenhub-intl.tencentcloudmaas.com/v1`
- **OpenAI Compatible API Key**：对应站点的 API Key
- **Model ID**：<模型ID，如 `hy3` / `deepseek-v4-pro`>

国内站文档：https://cloud.tencent.com/document/product/1823/130932　国际站文档：https://www.tencentcloud.com/document/product/1300/80645

---

## OpenClaw
类型：终端交互式向导

### 交互式接入（两站流程基本一致，域名/模型名差异见下）
```bash
openclaw onboard --auth-choice tokenhub-api-key
```
终端提示 → 填写：
- "personal-by-default..." → `Yes`
- Setup mode → `QuickStart`（已有配置则按需选 `Reset` 换模型 或 `Use existing values` 沿用）
- "Enter Tencent TokenHub API key" → 对应站点的 API Key
- "Default model" → `tencent-tokenhub/<模型ID>`（国内站文档示例 `tencent-tokenhub/hy3`，国际站文档示例 `tencent-tokenhub/deepseek-v4-pro`——**注意：无论哪个站点，这个字段前缀都固定是 `tencent-tokenhub/`，只是后面替换成目标站点支持的模型 ID**）
- "Select channel" → `Skip for now`
- "Configure skills now?" → `No`
- "Enable hooks?" → 国内站文档建议首次 `Skip for now`；国际站文档描述为按空格勾选后回车进入下一步（细节以实际终端交互为准）
- "How do you want to hatch your agent/bot?" → 国内站选项文案为 `Hatch in Terminal`，国际站为 `Hatch in TUI`（同义，按实际终端选项选择）

验证：`openclaw models list --provider tencent-tokenhub`

国内站文档：https://cloud.tencent.com/document/product/1823/130935　国际站文档：https://www.tencentcloud.com/document/product/1300/80642

### 非交互式快速接入（目前仅在国内站文档中明确给出，国际站若需要建议先按交互式流程操作，或重新核实是否有等价的非交互参数）
```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice tokenhub-api-key \
  --tokenhub-api-key "<用户的 API Key>" \
  --skip-health \
  --accept-risk
```
（Windows 用户去掉行尾 `\`，写成一行或用 `^` 续行）

思考模式：Hy3 系模型支持 `reasoning_effort`，OpenClaw 的 `off/minimal/low/medium` 映射到 `low`（或不传参），`high/xhigh` 映射到 `high`。聊天中用 `/think low` 或 `/think high` 切换。

---

## Hermes Agent
类型：终端交互式向导

```bash
hermes setup
```
首次运行：国内站文档写选择 `Full setup`；国际站文档写选择 `Quick setup — provider, model & messaging (recommended)`（版本迭代导致文案略有差异，按实际终端显示选择"首次完整设置"类选项即可）。

Provider 选择：国内站文档描述为在列表中选 **Tencent TokenHub (Hy3 via tokenhub.tencentmaas.com)**；国际站文档描述为滚动到底部选 **Custom endpoint**，然后手动填写以下字段：
- **API base URL**：国内站 `https://tokenhub.tencentmaas.com/v1` ｜ 国际站 `https://tokenhub-intl.tencentcloudmaas.com/v1`
- **API key**：对应站点的 API Key
- （国际站额外提示）**API compatibility mode** → 选 `Chat Completions`；**Model name** → 填模型ID；**Context length** → 按模型上下文窗口填（如 `256000`）；**Display name** → 同模型ID；**Terminal backend** → 本地安装选 `Local`

完成后执行 `hermes` 启动对话。注意：暂不支持切换思考模式（固定极速响应）。

国内站文档：https://cloud.tencent.com/document/product/1823/131927　国际站文档：https://www.tencentcloud.com/document/product/1300/80643

---

## Kilo Code
类型：GUI 设置界面（VSCode/JetBrains 插件）

Kilo Settings → 提供商 → 自定义提供商 → "+ 连接"：
- **提供商 ID**：如 `tencent`
- **提供商显示名称**：国内站文档示例填 `Hy`；国际站文档示例填 `tencent`（自定义，无强制要求）
- **基础 URL**：国内站 `https://tokenhub.tencentmaas.com/v1` ｜ 国际站 `https://tokenhub-intl.tencentcloudmaas.com/v1`
- **API 密钥**：对应站点的 API Key
- **模型 ID**：<如 `hy3` / `deepseek-v4-pro`>
- **模型显示名称**：<自定义>

思考档位映射：low/medium → `low`；High → `high`（两站一致）。

若需强制 no_think：编辑 `kilo.jsonc`（macOS/Linux: `~/.config/kilo/kilo.jsonc`；Windows: `用户目录\.config\kilo\kilo.jsonc`），设置 `"reasoning": false`，重启 VS Code 生效（国际站文档未单独提及此项，按国内站文档操作即可，两站客户端行为一致）。

排障：提示 "Not Connected to CLI Backend" 需先 `npm install -g @kilocode/cli`（Node.js ≥ v18），再重启 VS Code。

国内站文档：https://cloud.tencent.com/document/product/1823/131904　国际站文档：https://www.tencentcloud.com/document/product/1300/80647

---

## Roo Code
类型：GUI 设置界面（VSCode 插件）

左侧边栏 Roo Code 图标 → 第三方供应商：
- **API 提供商**：`OpenAI Compatible`（两站一致）
- **OpenAI 基础 URL**：国内站 `https://tokenhub.tencentmaas.com/v1` ｜ 国际站 `https://tokenhub-intl.tencentcloudmaas.com/v1`
- **API 密钥**：对应站点的 API Key
- **模型**：自定义填写 <模型ID>

国内站文档：https://cloud.tencent.com/document/product/1823/131905　国际站文档：https://www.tencentcloud.com/document/product/1300/80648

---

## Codex
类型：配置文件（`config.toml`）+ 环境变量注入 API Key

打开 Codex → **设置** → **配置** → **打开 config.toml**，在顶部写入以下内容（若已有其他内容，追加到文件开头，不要整体覆盖）：

### 国内站
文档：https://cloud.tencent.com/document/product/1823/133532
```toml
model_provider = "hy3-tokenhub"
model = "hy3"
disable_response_storage = true

[model_providers.hy3-tokenhub]
name = "Hy3 via tokenhub"
base_url = "https://tokenhub.tencentmaas.com/v1"
env_key = "HY3_API_KEY"
wire_api = "responses"
```

### 国际站
文档：https://www.tencentcloud.com/document/product/1300/82454
```toml
model_provider = "hy3-tokenhub"
model = "hy3"
disable_response_storage = true

[model_providers.hy3-tokenhub]
name = "Hy3 via tokenhub"
base_url = "https://tokenhub-intl.tencentcloudmaas.com"
env_key = "HY3_API_KEY"
wire_api = "responses"
```

**关键差异，务必注意**：国内站 `base_url` **带** `/v1` 后缀，国际站**不带** `/v1`（与前面几个工具"国内站不带 /v1、国际站也不带"的规律不同，Codex 是个例外，两站都要对照原文档确认，不要凑规律）。

若用户要接入的模型不是 `hy3`（示例模型），将 `model = "hy3"`、`[model_providers.hy3-tokenhub]` 中的 `hy3-tokenhub`、`name` 里的 `Hy3`、`env_key` 里的 `HY3_API_KEY` 相应替换为目标模型名，保持三处命名前缀一致即可，避免必须叫 `hy3-tokenhub` 的误解。

注入 API Key（把 `HY3_API_KEY` 换成 `config.toml` 里 `env_key` 实际设置的值）：
```bash
# macOS
launchctl setenv HY3_API_KEY "用户的 API Key"
# Windows
setx HY3_API_KEY "用户的 API Key"
```

验证：**完全退出 Codex（仅关闭窗口无效）后重新启动**，输入测试消息，模型正常返回即成功。

---

## 未收录工具的处理方式

若用户要接入的工具不在以上列表中，不要凭空编造配置格式。应：
1. 先确认站点（国内站 vs 国际站，见 SKILL.md「能力零」）；
2. 用 `WebFetch` 抓取对应站点的文档目录页确认该工具是否有官方接入文档：
   - 国内站：`https://cloud.tencent.com/document/product/1823`（找"接入 AI 工具"分类）
   - 国际站：`https://www.tencentcloud.com/document/product/1300`（找"AI Tools Integration"分类）
3. 找到后按文档实际内容操作，找不到则明确告知用户该工具在该站点暂无官方接入文档（可能另一个站点有，但不能因此假设配置内容通用）。
