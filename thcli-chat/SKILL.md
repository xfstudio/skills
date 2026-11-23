---
name: thcli-chat
description: 用 thcli +chat 跑腾讯云 TokenHub 模型对话（文本/图片多模态/联网搜索/深度思考/流式）。当用户想让某个腾讯云 TokenHub 模型回答问题、理解图片、读文本文件内容时使用。会消耗 token 产生费用，但不修改任何云端资源配置，可引导执行。
---

# thcli +chat · 模型对话

`thcli +chat --model <模型ID> "<问题>"`

问题直接写在命令末尾（位置参数），**没有 `--message` 选项**。

+chat 会消耗 token（产生费用）但不修改任何云端资源配置，作为核心可调用能力可引导执行。执行前先遵循 **thcli-shared**（登录与对话 Key 前提）。

> **执行规则**：`+chat` 本身可直接执行。但对话跑不通时若需写操作修复
> （如"这个模型没开通，要 `models activate`""需要新建一把对话用的 Key"），
> **只输出命令文本给用户，不调用工具执行**——即使用户说"那你先帮我开通"、
> 即使已提问确认过参数。"为了让对话跑通"不构成执行写操作的授权。

## 参数

- `--model`：**填模型 ID 即可**（如 `hy3`）——每个模型都有一个同名的默认接入点，网关两者都认。
  只有用户自建了额外接入点、且要指定其中某一个时，才需要填 `ep-xxx`（用 `thcli endpoint list` 查）。
- **问题文本**：位置参数，写在命令末尾（与 `--input` 至少给一个）。含空格时建议加引号。
- `--input @<路径>`：附带文件输入。
  - **图片**（png/jpg/jpeg/gif/webp/bmp）→ 走视觉通道（image_url），图文混合理解。
  - **文本类文件**（txt/md/json/csv/log/xml/yaml/html 及常见源码后缀）→ 内容内联进提问。
  - **其它二进制**（pdf/docx 等）→ 网关不支持，命令会直接报错，不会发无效请求。
- `--search`：开联网搜索（走 responses 通道，返回带引用来源）。**要用带「联网搜索」标签的模型** —— 用 `thcli models list --tags 联网搜索` 查，不要靠猜或试错。
- `--stream`：流式输出。
- `--thinking` / `--no-thinking`：开/关深度思考（复杂推理/数学）；不传用模型默认。
- `--responses`：改用 Responses API 的 body 结构。
- `--plan tp-ep|tp`：走 TokenPlan 企业版/个人版通道。**只在 `cn/gz` 与 `intl/sg` 两个组合上有服务**，其它组合会直接报错。
- `--anthropic`：套餐通道改用 Anthropic 兼容协议（`/plan/anthropic/v1/messages`）。**必须与 `--plan` 同用**，单独给会报错。`tp` 与 `tp-ep` 都支持。
- `--max-tokens <n>`：最大输出 token 数。**仅 `--anthropic` 时有效** —— 该协议要求必填，不给则用默认 4096；OpenAI 协议侧不读这个参数。
- `--site cn|intl` / `--area gz|sg|..`：站点/地域。
- `--api-key sk-..`：临时指定 key（不落盘）。
- `--alias <别名>`：选用某个已配置的 key 别名。

布尔开关裸写即为真，不用跟 `true`。

## 通道路由（了解即可）

- `--plan` 优先级最高：给了就锁定套餐通道，不受 `--responses/--search` 影响。
- body 结构：给了 `--responses` 或 `--search` 用 responses 结构（input），否则用 chat 结构（messages）。
- **例外**：`--anthropic` 时 body 跟着 URL 走 Anthropic 结构（`messages` + 必填 `max_tokens`），不看 `--responses/--search`。
- 是否挂搜索工具只看 `--search`。

## 前置：对话用的 Key

`+chat` 需要一把 API Key（与登录凭证是两回事）。**`thcli auth login` 时会自动备好一把名为 `thcli-key` 的，正常无需任何手动配置。**

用 `thcli chat-config get` 确认：

```
[profile=default site=cn area=gz] th 共 1 个 alias：
  default = sk-2****BMuB
```

**看到 `default = sk-x****xxxx` 就表示已配好** —— 中间的 `****` 是明文脱敏显示，不是占位符、不是未配置。此时直接跑 `+chat`，不要去 `key list` 找 Key、更不要建新的。

只有这两种情况才需要处理：

- `chat-config get` 输出"未设置"/无任何 alias
- `+chat` 明确报 `未找到 API Key（site=.. area=.. type=th ..）`

此时**先看账号里是否已有 `thcli-key`**（`thcli key list --name thcli-key`），有就说明只是本地没配上，把 `thcli chat-config set --type th --value <sk-..> --area gz` 给用户执行（明文需用户自己 `key reveal` 取，那是敏感操作）。**不要直接建新 Key** —— `key create` 是写操作，见上方执行规则。

## 示例

```
thcli +chat --model hy3 "你好"
thcli +chat --model hy3 --input @photo.png "描述这张图"
thcli +chat --model hy3 --input @notes.md "总结这份文档"
thcli +chat --model hy3-preview "今天新闻" --search    # 先用 models list --tags 联网搜索 确认模型
thcli +chat --model hy3 "证明勾股定理" --thinking --stream
thcli +chat --plan tp --model glm-5.2 "你好"                        # 套餐通道（OpenAI 协议）
thcli +chat --plan tp --anthropic --model glm-5.2 "你好"            # 套餐通道（Anthropic 协议）
thcli +chat --plan tp --anthropic --max-tokens 8192 --model glm-5.2 "写篇长文"
```

## 排查

- `400 ... 不支持所请求的协议或能力 Responses API` → 这个模型不支持 `--search`/`--responses` 走的通道。用 `thcli models list --tags 联网搜索` 查一个支持的换上，**不要去查 Key 或额度**（这个错与鉴权无关）。
- `未找到 API Key（site=.. area=.. type=th ..）` → 本地没配对话用的 Key，见上方「前置」。注意 `chat-config get` 显示 `sk-x****xxxx` 表示**已配好**。
- 401 → `thcli doctor`（见 thcli-doctor）。
- 报错体里的 `"code":"401008"` 这类**六位数字**是网关业务码。已收录的码 +chat 会直接在报错后附上
  修复建议；想单独查用 `thcli doctor error <码>`（如 `401008` 免费额度耗尽、`403005` IP 不在白名单、
  `429003` TPM 超限）。这类码与 HTTP 状态码独立，别拿 HTTP 状态去查。
- 报错带 request_id → 反馈给网关侧排查（日志在 `~/.thcli/log/{profile}.{site}.*.log`，只记 action/trace_id/耗时，不含内容）。
- 接入点选择/状态问题 → thcli-endpoint。

## 参考

- 公共协议：**thcli-shared**
- 找 EndpointId：**thcli-endpoint**
- 环境体检：**thcli-doctor**
