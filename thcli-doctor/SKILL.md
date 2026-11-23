---
name: thcli-doctor
description: 用 thcli doctor 对腾讯云 TokenHub 做只读体检与排障——检查登录凭证/站点/云 API 连通/对话用的 Key、诊断某个 Key/接入点/模型/套餐为何调不通、查错误码含义。当用户报告"调不通""401""额度不对""接入点停了"或想做整体健康检查时使用。
---

# thcli doctor · 只读体检与诊断

`thcli doctor` 是纯只读的诊断工具，**不改任何资源**。用于回答"为什么调不通"。
执行前先遵循 **thcli-shared** 的认证前提与安全规则。

> **执行规则**：本 skill 的命令全部只读，可直接执行。但诊断结论若指向写操作修复
> （如"建议新建 Key""建议调额度""建议开通付费"），**只输出建议的命令文本给用户，
> 不调用工具执行**——即使用户接着说"那你帮我改吧"、即使已提问确认过参数。
> 诊断出问题不构成执行修复的授权。

## 何时用

- 想整体检查环境是否就绪（凭证/站点/云 API 连通/对话用的 Key）→ `doctor`（裸跑即体检，等同 `doctor all`）
- 某把 Key、某个接入点、某个模型、某个套餐"看着正常却调不通" → 对应的 `doctor key/endpoint/model/plan`
- 遇到错误码想知道原因和修复建议 → `doctor error <码>`（位置参数，不是 `--code`）

不适用：修改配置或资源（那属于写操作，不在本 skill 范围）。

## 命令

| 命令 | 作用 | 必填参数 |
|---|---|---|
| `thcli doctor` | 整体体检：凭证有效性/站点地域/云 API 连通/对话用的 Key（`doctor all` 同义） | 无 |
| `thcli doctor key --id <ak-xxx>` | 诊断某把 API Key：状态、绑定范围、额度、IP 白名单 | `--id` |
| `thcli doctor endpoint --id <ep-xxx>` | 诊断接入点：运行状态、停止原因与建议 | `--id` |
| `thcli doctor model --id <ModelId>` | 诊断模型：是否有活跃接入点 | `--id` |
| `thcli doctor plan --team-id <id>` | 诊断套餐：状态、额度余量、用量汇总 | `--team-id` |
| `thcli doctor error [code]` | 查错误码原因+修复建议；不给 code 则列出全部收录码 | 无（可选 code） |

## 典型排障路径

1. **先跑 `doctor`**：确认基础环境。凭证过期 → 重新 `thcli auth login`；云 API 不通 → 看报错信息。
2. **对话 401 / key 调不通** → `doctor key --id <ak-xxx>`：逐条看状态是否 enable、绑定资源是否在线、额度是否用尽、出口 IP 是否在白名单内。
   - 注意：IP 白名单检查会向第三方（ipify.org）请求本机出口公网 IP，命令会先提示再外发。
3. **接入点调不通** → `doctor endpoint --id <ep-xxx>`：非 ACTIVE/RUNNING 时给出停止原因与恢复建议。
4. **拿到一个错误码** → `doctor error <码>`：支持精确匹配与前缀匹配。管控面码输 `AuthFailure` 列出所有子码；
   数据面码输 `429` 列出 429001~429006。注意是位置参数，写 `--code` 会报 unknown option。

## 结果解读要点

- `doctor key` 的额度按周期（月/天）逐条比对"已用/总量"，用尽会明确标红提示。
- `doctor plan` 区分计价单位：企业版按积分（credit），轻享版按 token，别把单位看错当成额度算错。
- `doctor model` 只判断有无活跃接入点；"被哪些 Key 授权"不做反查。

## 错误码的两套体系

`doctor error` 的清单分两组打印，别混淆：

| | 形态 | 来自 | 典型场景 |
|---|---|---|---|
| 管控面 | 字母命名空间，如 `AuthFailure.TokenFailure` | 云 API | thcli 各查询/写操作命令报错 |
| 数据面 | 六位数字，如 `401008` | 网关业务码，与 HTTP 状态码独立 | `+chat` 与模型调用报错 |

数据面码段：`400xxx` 请求非法 / `401xxx` 认证与额度 / `403xxx` 权限与封禁 /
`410·413·429·451·499xxx` 各类拒绝 / `5xxxxx` 服务端。

用户贴来的报错里带 `"code":"401008"` 这类六位数字时，直接 `doctor error 401008`。
`+chat` 报错时若该码已收录，命令本身就会附上修复建议，不必再查一次。

未收录的码会走"未收录"分支并列出清单——**这是查不到，不是答错**，此时不要替它编原因，
按 message 原文和 request_id 走工单。

详见 `references/checks.md`。

## 参考

- 公共协议：**thcli-shared**
- 相关域：**thcli-key**（Key 查询）、**thcli-endpoint**（接入点查询）、**thcli-plan**（套餐查询）、**thcli-chat**（对话报错联动）
