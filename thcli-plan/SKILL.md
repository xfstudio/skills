---
name: thcli-plan
description: 用 thcli plan 查询腾讯云 TokenHub 的套餐（TokenPlan，企业版/轻享版）与专属 Key——列出套餐、看套餐详情与额度、看套餐可用模型、看用量明细、列出与查看专属 Key。当用户想"有哪些套餐""套餐额度还剩多少""这个套餐能用哪些模型""专属 Key 列表"时使用。仅查询，不涉及购买/续费/升配等计费操作。
---

# thcli plan · 套餐与专属 Key 查询

`thcli plan` 管理套餐（TokenPlan）与其专属 Key。**本 skill 只引导只读查询**。执行前先遵循 **thcli-shared**。

## 执行规则（读到这里就已生效，先于下面所有内容）

**这些命令属写/计费/敏感操作，只输出命令文本给用户，不调用任何工具执行：**

`plan buy` / `plan renew` / `plan upgrade` / `plan key create` / `plan key update` / `plan key rotate` / `plan key delete` / `plan key reveal`

以下情形**都不构成例外**：

- 用户明确要求"帮我买个套餐/续个费/建几把 Key" → 仍然只输出命令
- 已经用提问确认过参数、用户点了同意 → **确认不等于授权代跑**，仍然只输出命令
- 本 skill 的 description 写着"仅查询" → 那表示写操作**已被划出执行范围**，不是"无人管辖、可自行拼命令跑"
- 用 `--help` 自己拼出了命令 → 拼命令可以，执行不可以

**套餐计费操作尤其不可代跑**：`plan buy` 若返回错误，套餐**可能已实际创建成功且不可退**——盲目重试会重复扣费。这类判断必须由用户在终端亲自把握。

正确做法：说明该操作会产生费用、修改资源或暴露明文，把完整命令给用户，由**用户自己在终端执行**。

## 只读命令（skill 可引导执行）

| 命令 | 作用 |
|---|---|
| `thcli plan list` | 列出套餐（TeamId/名称/类型/状态/Key 数/创建时间） |
| `thcli plan info --team-id <id>` | 套餐详情：状态、额度余量、自动续费、用量汇总 |
| `thcli plan models --team-id <id>` | 套餐可用的模型清单 |
| `thcli plan detail --team-id <id>` | 按 Key/模型/时间的用量明细（逐次请求，含 RequestId） |
| `thcli plan available` | 说明可购套餐去控制台（无查询接口，仅打印指引） |
| `thcli plan cost` | 说明询价去控制台（无查询接口，仅打印指引） |
| `thcli plan key list --team-id <id>` | 列出套餐的专属 Key（Key 明文脱敏） |
| `thcli plan key get --id <ak-xxx>` | 单个专属 Key 详情：状态、允许模型、余额 |

```
thcli plan list
thcli plan info --team-id tp-xxxx
thcli plan models --team-id tp-xxxx
thcli plan detail --team-id tp-xxxx --from 2026-08-01T00:00:00+08:00 --to 2026-08-25T23:59:59+08:00
thcli plan key list --team-id tp-xxxx
thcli plan key get --id ak-xxxx
```

`--from` / `--to` **必须是完整 RFC3339 且带时区**，`2026-08-01` 这种只有日期的写法会被
直接拒绝（报 `时间格式不对`）。`Z` 与 `+08:00` 两种都收。都不传时默认最近 15 分钟——
窗口很窄，查不到数据先确认是不是时间窗的问题，而不是没有用量。

## 结果解读

- 计价单位随产品类型：enterprise 按积分（credit），其他按 token，别看错单位。
- `detail` 的**列集合随产品类型变**，与控制台一致：enterprise（专业版）有 4 个积分列
  （`IN_CR_MISS` 未命中缓存 / `IN_CR_HIT` 命中缓存 / `OUT_CR` / `TOTAL_CR`），token 列序是
  输入→输出→缓存→总；其余（轻享版 enterprise-auto 等）**没有积分列**，token 列序是
  输入→缓存→输出→总。两者 token 列序不同不是笔误。
- `detail` 的 `REQUEST_TIME` 是 **UTC**（`Z` 结尾），不是本地时间——东八区看到的
  `03:40` 其实是本地 `11:40`。用于跟服务端日志按 `REQUEST_ID` 对账。
- `detail` 的 `APIKEY_ID` 列是缩写（`ak-tp-…59e0b5`），要完整 ID 加 `--json`。
- `detail` 一次只返回一页。输出末尾若出现 `下一页：--context xxx`，把该值原样传给
  `--context` 取下一页，**其余筛选条件必须保持一致**（游标只在同一组条件下有效）。
- `info` 的额度汇总（PackageInfo/TokenSummary）显示总量/已用/余量。
- 专属 Key 列表的 APIKEY 列已脱敏。
- 套餐为什么不可用，可用 **thcli-doctor** 的 `doctor plan --team-id <id>` 进一步诊断。

## 写 / 计费 / 敏感操作（skill 不执行，供用户自行操作）

以下会产生费用、修改资源或暴露明文。**把命令输出给用户，由用户自己在终端执行**，并说明影响——这是既定安全边界，即使用户明确要求代跑也仍然只输出命令：

- 套餐计费：`thcli plan buy`（购买/重订）、`thcli plan renew`（续费）、`thcli plan upgrade`（升配）
  - 注意：计费操作若返回错误，套餐**可能已实际创建成功**（不可退），务必先 `plan list`/`plan info` 查状态再决定是否重试，切勿盲目重跑。
- 专属 Key 写：`thcli plan key create`（批量创建）、`thcli plan key update`（改额度/允许模型/状态）、`thcli plan key rotate`（轮换密钥）、`thcli plan key delete`（删除）
- 明文查看：`thcli plan key reveal`（输出专属 Key 明文，出于安全不代为执行；如用户确需查看，提示其自行执行并妥善保管）

## 参考

- 公共协议：**thcli-shared**
- 套餐排障：**thcli-doctor**（`doctor plan`）
- 普通 API 密钥（非专属）：**thcli-key**
