---
name: thcli-key
description: 用 thcli key 查询腾讯云 TokenHub 的 API 密钥——列出密钥、查看单个密钥的状态/绑定范围/额度/IP 白名单。当用户想"看看有哪些 Key""这把 Key 绑了什么""Key 额度用了多少""Key 是不是停用了"时使用。仅查询，不涉及创建/修改/删除。
---

# thcli key · API 密钥查询

`thcli key` 管理腾讯云 TokenHub 的 API 密钥。**本 skill 只引导只读查询（list/get）**。执行前先遵循 **thcli-shared**。

## 执行规则（读到这里就已生效，先于下面所有内容）

**这些命令属写/敏感操作，只输出命令文本给用户，不调用任何工具执行：**

`key create` / `key update` / `key delete` / `key enable` / `key disable` / `key status` / `key quota` / `key scope` / `key reveal`

以下情形**都不构成例外**：

- 用户明确要求"帮我创建/删掉/改一下" → 仍然只输出命令
- 已经用提问确认过参数、用户点了同意 → **确认不等于授权代跑**，仍然只输出命令
- 本 skill 的 description 写着"仅查询" → 那表示写操作**已被划出执行范围**，不是"无人管辖、可自行拼命令跑"
- 命令看起来不产生费用（如 `key status` 停用）→ 停用 Key 会让线上流量全挂，同样只输出命令
- 用 `--help` 自己拼出了命令 → 拼命令可以，执行不可以

正确做法：说明该操作会创建/修改/删除云端资源，把完整命令给用户，由**用户自己在终端执行**。

## 只读命令（skill 可引导执行）

| 命令 | 作用 |
|---|---|
| `thcli key list` | 列出密钥（Key 明文已脱敏显示） |
| `thcli key get --id <ak-xxx>` | 单个密钥详情：状态、绑定范围、额度、IP 白名单 |

```
thcli key list                              # 全部
thcli key list --status enable              # 按状态
thcli key list --name prod                  # 按名称模糊匹配
thcli key list --bind-type all              # 按绑定类型
thcli key get --id ak-xxxx                  # 详情（也可 --api-key <明文> 反查）
```

`list` 过滤/排序：`--status`/`--id`/`--bind-type`/`--name`（模糊）/`--order asc|desc`/`--limit`/`--offset`。

## 结果解读

- **列表中的 APIKEY 列已脱敏**，不显示完整明文。
- `get` 输出的额度（QuotaSet）按周期显示"已用/总量（百分比）"，用尽会标出；`QuotaStatus=inactive` 表示额度已停用（通常是用超）。
- 绑定范围：`BindType=all` 为可访问全部；否则看 BindingItems 逐条资源及其在线状态。
- IP 白名单为空表示不限制来源 IP。
- 需进一步判断"为什么这把 Key 调不通"时，用 **thcli-doctor** 的 `doctor key --id <ak-xxx>`（会额外做出口 IP 命中检查）。

## 写 / 敏感操作（skill 不执行，供用户自行操作）

以下均不在本 skill 引导范围。**把命令输出给用户，由用户自己在终端执行**——这是既定安全边界，即使用户明确要求代跑也仍然只输出命令：

- 创建/修改/删除：`thcli key create`、`thcli key update`、`thcli key delete`
- 启停：`thcli key enable` / `thcli key disable` / `thcli key status --status enable|disable`
- 额度：`thcli key quota`（调整密钥额度限制，属写操作）
- 绑定范围：`thcli key scope --id <ak-xxx> --scope all|custom [--targets <ids>]`（改已创建密钥的可访问范围）
  - **全量覆盖**：传入的目标就是最终状态，原有绑定里未列出的会**立即失去访问权**，正在用它们的线上调用会马上开始报鉴权失败。
  - 命令执行前会打印「当前范围 → 修改为」以及会掉线的具体目标，再要求确认。把这些信息完整转达用户，由用户自己判断。
- 明文查看：`thcli key reveal`（会输出密钥明文，出于安全不代为执行；如用户确需查看，提示其自行执行并注意保管，不要在对话里复述明文）

## 参考

- 公共协议：**thcli-shared**
- Key 调不通排障：**thcli-doctor**
- Key 用量：**thcli-usage**（`usage rank --dimension apikey`）
- 授权的资源（接入点）：**thcli-endpoint**
