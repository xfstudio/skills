---
name: thcli-endpoint
description: 用 thcli endpoint 查询腾讯云 TokenHub 的推理接入点（Endpoint）——列出接入点、查看单个接入点的状态/计费/免费额度/停止原因。当用户想"有哪些接入点""这个 ep-xxx 什么状态""接入点为什么停了"时使用。仅查询，不涉及部署/修改/删除。
---

# thcli endpoint · 接入点查询

`thcli endpoint` 管理推理接入点（Endpoint）。**本 skill 只引导只读查询（list/get）**。执行前先遵循 **thcli-shared**。

## 执行规则（读到这里就已生效，先于下面所有内容）

**这些命令属写/计费操作，只输出命令文本给用户，不调用任何工具执行：**

`thcli deploy`（部署新接入点） / `endpoint update` / `endpoint delete` / `endpoint postpaid`

以下情形**都不构成例外**：

- 用户明确要求"帮我部署/改限流/删掉" → 仍然只输出命令
- 已经用提问确认过参数、用户点了同意 → **确认不等于授权代跑**，仍然只输出命令
- 本 skill 的 description 写着"仅查询" → 那表示写操作**已被划出执行范围**，不是"无人管辖、可自行拼命令跑"
- 命令看起来不产生费用（如 `endpoint update` 调限流）→ 改限流会直接影响线上服务，同样只输出命令
- 用 `--help` 自己拼出了命令 → 拼命令可以，执行不可以

正确做法：说明该操作会创建/修改/删除云端资源或影响计费，把完整命令给用户，由**用户自己在终端执行**。

## 只读命令（skill 可引导执行）

| 命令 | 作用 |
|---|---|
| `thcli endpoint list` | 列出接入点（含状态、计费类型、后付费开关） |
| `thcli endpoint get --id <ep-xxx>` | 单个接入点详情：状态、计费、免费额度、停止原因与建议 |

```
thcli endpoint list                         # 全部
thcli endpoint list --status ACTIVE         # 按状态
thcli endpoint list --model-id <ModelId>    # 某模型的接入点
thcli endpoint list --model-name hy3        # 按模型名模糊
thcli endpoint list --payment-enabled true  # 已开后付费的
thcli endpoint get --id ep-xxxx             # 详情
```

`list` 过滤/排序：`--id`/`--endpoint-name`（模糊）/`--status`/`--charge-type`/`--request-source`/`--model-id`/`--model-name`（模糊）/`--payment-enabled`/`--order-by created|updated`/`--order asc|desc`/`--limit`/`--offset`。

## 结果解读

- **`+chat --model` 通常直接填模型 ID 就行**（默认接入点与模型同名）。只有要指定自建接入点时，才用这里查到的 `ep-xxx`。
- 状态非 ACTIVE/RUNNING 时，`get` 会给出 StopReason 与恢复建议（如 `FREE_QUOTA_EXHAUSTED` 表示免费额度用尽）。
- 免费额度信息（若有）显示"已用/总量（百分比）"。
- 深入排障某个接入点用 **thcli-doctor** 的 `doctor endpoint --id <ep-xxx>`。

## 写 / 计费操作（skill 不执行，供用户自行操作）

以下会创建/修改/删除资源或影响计费。**把命令输出给用户，由用户自己在终端执行**，并说明影响——这是既定安全边界，即使用户明确要求代跑也仍然只输出命令：

- 部署新接入点：`thcli deploy --model-id <ModelId> --name <名称> --charge-type <类型>`
- 修改配置/限流：`thcli endpoint update --id <ep-xxx> [--rpm/--tpm/--qpm/--name/--charge-type/--auto-adjust-quota]`
- 删除：`thcli endpoint delete --id <ep-xxx>`
- 后付费开关：`thcli endpoint postpaid on|off [--endpoint <ids>|--all]`（开后付费会产生计费，`on` 还会顺带领取该服务未领的免费包）

## 参考

- 公共协议：**thcli-shared**
- 用接入点跑对话：**thcli-chat**
- 接入点排障：**thcli-doctor**
- 模型信息：**thcli-models**
- 接入点用量：**thcli-usage**（`usage rank --dimension endpoint`）
