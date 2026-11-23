---
name: thcli-overview
description: 用 thcli 命令行查询腾讯云 TokenHub（模型广场/推理调用/API 密钥/套餐/用量/端点）的总览与导航。当用户想查模型、查 API Key、跑对话、看用量、查套餐或排障时，从这里开始，再进入对应的资源域 skill。仅查询与导航，不涉及创建/修改/删除/计费等写操作。
---

# thcli · 腾讯云 TokenHub 命令行总览

thcli 是操作腾讯云 TokenHub 的 CLI。命令扁平：`thcli <命令> [子动词] [--参数]`。
任意命令加 `--help` 查看参数，如 `thcli key get --help`。

> 执行任何命令前，先遵循 **thcli-shared** 里的公共执行协议（认证前提、能力边界、安全规则）。
> 本 skill 只做**导航与只读速查**。

## 执行规则（读到这里就已生效，先于下面所有内容）

**这些命令属写/计费/敏感操作，只输出命令文本给用户，不调用任何工具执行：**

- 密钥：`key create|update|delete|enable|disable|status|quota|scope|reveal`
- 模型开通：`models free|activate`
- 接入点：`deploy`、`endpoint update|delete|postpaid`
- 套餐：`plan buy|renew|upgrade`、`plan key create|update|rotate|delete|reveal`

以下情形**都不构成例外**：

- 用户明确要求代跑 → 仍然只输出命令
- 已经用提问确认过参数、用户点了同意 → **确认不等于授权代跑**，仍然只输出命令
- 某个资源域 skill 的 description 写着"仅查询" → 那表示写操作**已被划出执行范围**，不是"无人管辖、可自行拼命令跑"
- 命令看起来不产生费用（`key status` 停用、`endpoint update` 改限流）→ 都会直接影响线上，同样只输出命令
- 用 `--help` 自己拼出了命令 → 拼命令可以，执行不可以

正确做法：说明影响，把完整命令给用户，由**用户自己在终端执行**。

## 何时用

- 查 API 密钥、模型、接入点、套餐、用量、性能指标
- 跑模型对话（`+chat`）
- 排查鉴权/调用问题（`doctor`）

不适用：需要创建/修改/删除云端资源或涉及计费的操作（建密钥、开通模型、部署接入点、购买/续费套餐等）—— 这些请给出命令让用户自行确认执行。

## 前置

- 先登录：`thcli auth login`（浏览器 OAuth）或 `thcli auth set --secret-id <..> --secret-key <..>`；用 `thcli auth status` 查登录态。
- 多账号/多站：`--profile <账号>`、`--site cn|intl`；`thcli profile use --name <X>` 可设默认免带参数。

## 只读命令速查（skill 可引导执行）

- 身份：`thcli auth status`
- 密钥：`thcli key list` / `thcli key get --id <ak-xxx>`
- 模型：`thcli models list` / `thcli models get` / `thcli models pricing` / `thcli models search` / `thcli models compare`
- 接入点：`thcli endpoint list` / `thcli endpoint get --id <ep-xxx>`
- 对话：`thcli +chat --model <模型ID> "..."`（问题写命令末尾；`--input @图片` 多模态，`--search` 联网，`--stream` 流式，`--thinking` 深度思考）
- 套餐：`thcli plan list|info|models|detail`；专属 Key 查询：`thcli plan key list|get`
- 用量：`thcli usage rank` / `thcli usage export` / `thcli usage trend`
- 性能：`thcli monitor text|vision|audio`
- 诊断：`thcli doctor`（体检）/ `thcli doctor error <错误码>` / `thcli doctor key|endpoint|model|plan`

## 写/计费命令一览（skill 不执行，供用户自行操作）

以下命令会创建/修改/删除云端资源或产生费用。**把命令输出给用户，由用户自己在终端执行**——这是既定安全边界，即使用户明确要求代跑也仍然只输出命令：

- 密钥写：`thcli key create|update|delete|enable|disable|status|quota|scope|reveal`
- 模型开通：`thcli models free|activate`
- 接入点写：`thcli deploy ...`、`thcli endpoint update|delete|postpaid`
- 套餐计费：`thcli plan buy|renew|upgrade`、`thcli plan key create|update|rotate|delete|reveal`

## 本地配置查询（skill 可引导）

这些只改本地 `~/.thcli` 与登录态，属使用前提，可引导执行：

- 账号：`thcli profile list` / `thcli profile current` / `thcli profile use --name <X>`
- 站点：`thcli site list` / `thcli site current` / `thcli site use --name <cn|intl>`
- 语言：`thcli lang`（查看/切换界面语言，独立于账号）
- 对话用的 Key：`thcli chat-config get`（查看当前 +chat 使用的 Key 配置）

## 关键约定

- `+chat --model` **填模型 ID 即可**（如 `hy3`）——默认接入点与模型同名，网关两者都认。只有要指定用户自建的某个接入点时才填 `ep-xxx`。
- 布尔开关裸写即为真：`--stream`、`--search`、`--thinking` 不需要跟 `true`。
- 不打印完整密钥明文，不回显凭证参数（详见 thcli-shared 安全规则）。
- 输出为人类可读文本。

## 参考

- 公共协议：**thcli-shared**
- 各资源域：**thcli-models** / **thcli-key** / **thcli-endpoint** / **thcli-plan** / **thcli-usage** / **thcli-monitor** / **thcli-doctor** / **thcli-chat** / **thcli-auth**
