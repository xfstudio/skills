---
name: thcli-usage
description: 用 thcli usage 查腾讯云 TokenHub 的 token 用量——按模型/接入点/API Key 维度的用量排行（终端图表）、账号整体用量走势、导出 CSV。当用户想知道"谁用得最多""这个月用了多少 token""用量趋势""导出用量报表"时使用。纯只读统计，不涉及任何云端资源写或计费操作。
---

# thcli usage · 用量查询

`thcli usage` 回答"用了多少 token"。纯只读。执行前先遵循 **thcli-shared**。

> **执行规则**：本 skill 的命令全部只读，可直接执行。若用量结论引出写操作
> （如"这把 Key 超额了，要不要调额度""这个模型没开通，帮我开一下"），
> **只输出命令文本给用户，不调用工具执行**——即使用户明确要求、即使已提问确认过参数。

与 **thcli-monitor** 的分工：usage 看"用量"（token 数、排行、趋势）；monitor 看"健康度"（请求量、错误率、延迟）。

## 命令

| 命令 | 作用 |
|---|---|
| `thcli usage rank` | 用量排行：按维度列出 Top 对象，带终端时序图表 |
| `thcli usage trend` | 账号整体用量走势（走云监控接口，指标更丰富，但只有账号级） |
| `thcli usage export` | 导出全量排行到 CSV |

## usage rank —— 用量排行

```
thcli usage rank --dimension model      # 按模型（默认）
thcli usage rank --dimension endpoint   # 按接入点
thcli usage rank --dimension apikey     # 按 API Key
thcli usage rank --color                # 堆叠分色图（一屏看构成，依赖终端色彩）
```

- `--dimension`：`model`（默认）/ `endpoint` / `apikey`。
- `--metric-type`：`tokens`（默认）/ `search`。
- `--start-time` / `--end-time`：默认最近 24 小时；`--period <秒>`：聚合粒度，默认 3600。
- 默认视图：先一张全量总表（占比条 + `▾` 标出下方有详细走势的项），再逐对象平铺时序卡片。
- 汇总（TotalStats）始终是全量的，与总表范围一致。

## usage trend —— 整体走势

```
thcli usage trend                       # 账号整体，缺省核心指标
thcli usage trend --model <ModelId>     # 下钻到某模型
thcli usage trend --all                 # 全部指标
thcli usage trend --list-metrics        # 列出可选指标
```

- 指标比 rank 丰富（TPM/缓存读写/平均 token 等 14 个），但只有账号级；可按 `--model/--endpoint/--apikey` 下钻单个对象。
- `--metric <keys>`：逗号分隔选指标；不传用缺省核心指标。
- 注意：指定的模型若是**非文本模型**（图片/视频/音频/3D，不产生 token），trend 会提示改用 `thcli monitor vision`，而不是给出误导性的空图。

## usage export —— 导出 CSV

```
thcli usage export --dimension model --metric-type tokens
thcli usage export --output my_report.csv
```

- 导出全量（不分页）。`--metric-type` 仅支持 `tokens` / `search`。
- 不指定 `--output` 时按维度与时间范围自动命名。
- 列随返回的指标动态生成；名称含逗号会按 CSV 规则转义。

## 参考

- 公共协议：**thcli-shared**
- 健康度指标（错误率/延迟/非文本模型产出）：**thcli-monitor**
- 细节（响应结构、分页与全量的范围差异、非文本模型处理）见 `references/metrics.md`
