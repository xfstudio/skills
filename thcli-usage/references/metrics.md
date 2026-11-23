# thcli usage · 数据源与呈现细节

## 两个数据源的区别

| 命令 | 底层接口 | 能力 | 局限 |
|---|---|---|---|
| `usage rank` / `export` | `DescribeUsageRankList` | 能按 model/apikey/endpoint 拆对象、排行 | 指标只有 4 个（tokens/search 相关） |
| `usage trend` | `GetMonitorData`（云监控 Barad） | 指标 14 个（TPM/缓存读写/平均 token 等） | 只有账号级，维度只有 uin，故不支持 `--dimension/--target` |

## rank 的响应结构（真实接口验证）

- `MetricKeys`：本次返回哪些指标，如 `[TotalToken, InputTotalToken, ...]`，第一个为主指标。
- `Timestamps`：时间轴（epoch 秒），与每个 Series 数组按下标对应。
- `TopList[]`：排行项，含 `Rank/Key/Name/Stats`（汇总）/`Series`（各指标时序，无数据点为 null）。Series 里的值后端返回的是 JSON 字符串而非真数组，CLI 已归一处理。
- `TotalStats`：全量汇总；`PageStats`：当前页汇总。

## 分页与"全量"的范围差异（重要）

`DescribeUsageRankList` 一次返回 10 条。CLI 的 `rank` 通过两次并发请求兼顾全貌与走势：

- `ShowAll=true`：返回全部对象做总表，但**不带 Series**（画不了走势）。
- 分页请求：返回本页 10 个的 Series，用于详细走势卡片。

因此：**总表/汇总是全量的，时序卡片只覆盖当前展示的对象**。量级可能差几千倍（实测某场景图表峰值 81.77K，而全量 434.60M）。CLI 已在标题/脚注显式标注范围，解读结果时注意区分"本页"与"全部"。

## 呈现方式

- **默认（无 --color）**：全量总表（占比条 + `▾` 标记有详细走势的项）+ 逐对象时序卡片（每张按自身峰值缩放，小对象波形也可见）。
- **--color**：堆叠分色图，一屏看构成与走势；超出配色容量的对象合并为"其它 N 个"。依赖终端色彩，故非默认。

## 非文本模型的处理

图片/视频/音频/3D 模型不产生 token，用 usage 查会是空图。`usage trend --model <非文本模型>` 会先查 `DescribeAIGCModelList` 识别模型类型，命中则提示改用 `thcli monitor vision`，避免把"用错命令"误判成"没有用量"。

## export 细节

- 强制 `ShowAll=true` 拿全量，不分页。
- `--metric-type` 仅支持 `tokens` / `search`。
- CSV 表头 = `Rank,Key,Name` + 动态 MetricKeys；Name 含逗号按 CSV 双引号转义。
- 未指定 `--output` 时文件名形如 `usage_<dimension>_<起>_<止>.csv`。
