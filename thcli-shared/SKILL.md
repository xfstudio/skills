---
name: thcli-shared
description: thcli（腾讯云 TokenHub 命令行）所有 skill 的公共执行协议。定义认证前提、命令选择顺序、只读/写操作边界、输出与安全规则。任何 thcli-* skill 在执行命令前都应先遵循本协议。
---

# thcli · 公共执行协议

本 skill 是所有 `thcli-*` skill 的公共底座，定义**统一的执行规则**。在执行任何 thcli 命令前，先遵循这里的约定，再回到具体域 skill（models/key/endpoint/plan/usage/monitor/doctor/chat）查该命令的用法。

thcli 是操作腾讯云 TokenHub 的命令行：模型广场、推理调用、API 密钥、套餐、用量、接入点。命令扁平：`thcli <命令> [子动词] [--参数]`。任意命令加 `--help` 查看参数。

## 一、能力边界（重要）

**本期 skill 只引导「只读查询」与「不改动云端资源」的命令。**

允许 skill 主动执行的类别：
- **只读查询**：list / get / status / info / detail / pricing / rank / export / trend / doctor（体检诊断）等。
- **模型对话**：`+chat`（会消耗 token 产生费用，但不修改任何云端资源配置，视为核心可调用能力，允许执行）。
- **本地状态 / 使用前提**：登录与本地配置切换 —— `auth login|set|logout`、`profile use|current`、`site use|current`、`lang`、`chat-config`。这些只影响本地 `~/.thcli` 与登录态，不属于云端资源写。

**禁止 skill 主动执行的类别（云端资源创建/修改/删除/计费）：**
- 密钥写：`key create|update|delete|enable|disable|status|quota|scope|reveal`
- 模型开通/计费：`models free|activate`
- 接入点写：`deploy`、`endpoint update|delete|postpaid`
- 套餐计费：`plan buy|renew|upgrade`、`plan key create|update|rotate|delete|reveal`

> 说明：`key scope` 是**全量覆盖**——未列出的目标立即失去访问权，线上调用会当场鉴权失败，属高风险写操作。`reveal` 类命令会暴露密钥明文，同样排除。

遇到上述写/计费操作时：**只输出命令文本给用户，不调用任何工具执行**。

以下情形**都不构成例外**：

- 用户明确要求代跑 → 仍然只输出命令
- 已经用提问确认过参数、用户点了同意 → **确认不等于授权代跑**，仍然只输出命令
- 某个资源域 skill 的 description 写着"仅查询" → 那表示写操作**已被划出执行范围**，不是"无人管辖、可自行拼命令跑"
- 命令看起来不产生费用（`key status` 停用、`endpoint update` 改限流）→ 都会直接影响线上，同样只输出命令
- 用 `--help` 自己拼出了命令 → 拼命令可以，执行不可以
- CLI 没有弹二次确认就跑通了 → 部分写命令确实没有确认环节，**这不代表允许执行**

正确做法：说明该操作会创建/修改/删除云端资源或产生费用，把完整命令与参数给用户，由**用户自己在终端执行**。

## 二、认证与前提检查

执行任何需要云端数据的命令前，先确认已登录：

1. 用 `thcli auth status` 检查当前登录态与生效 profile/site。
2. 未登录时，可引导执行 `thcli auth login`（浏览器 OAuth 授权码登录）；或用户已有永久密钥时 `thcli auth set --secret-id <..> --secret-key <..>`。
3. 多账号 / 多站点：用 `--profile <账号>`、`--site cn|intl` 临时指定；或 `thcli profile use --name <X>` / `thcli site use --name <cn|intl>` 设默认，之后免带参数。

`+chat` 额外需要一把对话用的 API Key（与登录凭证是两回事）：**登录时会自动备好一把 `thcli-key`，正常无需手动配置**。用 `thcli chat-config get` 确认——输出里有 `default = sk-x****xxxx` 就表示已配好（`****` 是脱敏，不是未配置）。详见 **thcli-chat**。

## 三、命令选择顺序

面对一个查询需求，按此顺序决策：

1. **先定位资源域** → 去对应 skill：
   - 模型信息/价格/对比 → `thcli-models`
   - API 密钥查询 → `thcli-key`
   - 接入点（Endpoint）查询 → `thcli-endpoint`
   - 套餐/额度查询 → `thcli-plan`
   - 用量统计/导出 → `thcli-usage`
   - 性能/健康度指标 → `thcli-monitor`
   - 跑对话/多模态 → `thcli-chat`
   - 排障/体检 → `thcli-doctor`
2. **优先用最精确的只读命令**：能 `get <id>` 就不要 `list` 全量再筛。
3. **拿不准 ID 时先 list 再 get**：如不确定模型 ID，先 `thcli models list` 查。
4. **报错先体检**：命令报错且原因不明时，用 `thcli doctor` 或 `thcli doctor error <错误码>` 定位（error 的码是位置参数）。

## 四、关键约定

- `+chat --model` **填模型 ID 即可**（如 `hy3`）——默认接入点与模型同名，网关两者都认。只有要指定用户自建的某个接入点时才填 `ep-xxx`。
- 布尔开关**裸写即为真**：`--stream`、`--search`、`--thinking` 都不需要跟 `true`。
- 全局参数在任意子命令上都可用：`--profile`、`--site`、`--region`、`--secret-id`、`--secret-key`、`--lang`、`--json`。
- **要解析结果就加 `--json`**（所有命令都支持）。默认输出是给人看的表格与图表，列宽随中英文混排变化，
  按空格拆列会错位——不要用 `awk`/`cut` 解析默认输出，那样读到的字段可能是错的。

  ```shell
  thcli models list --json
  thcli key list --json      # 密钥字段仍是打码值
  ```

  `--json` 给的是云 API 的原始响应结构（字段名为驼峰），信息比表格完整：例如模型的
  `ModelChargingInfo` 是**按档位分组的数组**，阶梯计价的每一档带自己的 `Name` 与价格单位，
  而表格里只能看到拼好的文本。
- **价格单位随模型而变**，`PriceUnit` 里就带着货币（如 `元/百万tokens`、`美元/百万tokens`）。
  横向比价前先确认单位一致，不要把不同货币的数值直接排序。

## 五、安全与输出规则

- **绝不打印完整密钥明文**：不代为执行 `key reveal` / `plan key reveal`；如用户确需查看，提示其自行执行并注意保管。
- **不回显凭证**：`--secret-id` / `--secret-key` / `--api-key` 等敏感参数，复述命令时用占位符（如 `<secret-id>`），不要把用户给出的真实值再打印出来。
- **非交互场景**：在自动化/管道中执行时，只跑只读命令；一旦命中写/计费命令，停止并向用户报告需要手动确认。
- **日志位置**：调用日志在 `~/.thcli/log/`，只记录 action / trace_id / 耗时，不含参数与响应体。排查网关问题时可让用户提供其中的 request_id。

## 六、参考

具体命令用法见各资源域 skill：`thcli-overview`（总览导航）、`thcli-models`、`thcli-key`、`thcli-endpoint`、`thcli-plan`、`thcli-usage`、`thcli-monitor`、`thcli-doctor`、`thcli-chat`、`thcli-auth`。
