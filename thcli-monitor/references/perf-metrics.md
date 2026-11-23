# thcli monitor · 指标与模态细节

## 数据源

- `monitor text`：走云监控接口（`GetMonitorData`），指标集为 `PERF_METRICS`（13 个），默认账号整体，可按 model/endpoint/apikey 下钻。
- `monitor vision/audio`：先 `DescribeAIGCModelList` 拿模型清单与其 `UsageDisplayStrategy`，再按模型类型取对应指标集。

## text 指标下钻规则

- 维度键：`model` / `endpoint` / `apikey`，任一给值即下钻到该对象，都不给则账号整体。
- 部分指标是 `uinOnly`（仅账号级），即使传了下钻参数也不生效，卡片会标注"该指标仅账号级（uin）"。
- `--list-metrics` 会用 `*` 标出默认项，并标注每个指标是"可下钻"还是"仅账号级"。
- 监控接口仅支持单指标拉取，CLI 对多指标并发请求后逐张渲染卡片。

## vision / audio 的模态分组

依据 `DescribeAIGCModelList` 的 `ModelType` 划分（实测非文本模型全部落在这两组）：

- `vision` = `Image` + `Video`（含 3D 模型 hy-world2-*，其 ModelType 归为 Image/Video）
- `audio` = `Audio` + `ASR` + `TTS`

拆两个子命令的收益是 `--list-models` 各自的清单更短，找模型时不必在图片里翻语音。

## multimodal_usage 的含义随模型而变

vision/audio 共用五项指标（rpm / total_token / multimodal_usage / error_ratio / duration），其中 `multimodal_usage` 的量纲由模型 `UsageDisplayStrategy` 决定：

- 视频模型 → 时长（秒）
- 图片模型 → 张数（Count）
- TTS → 输入字符数

因此必须先查清模型策略才能正确标注量纲，CLI 已据此处理，不会张冠李戴。

## 数值格式

- 百分比指标显示为 `85.00%`，不套 K/M 单位。
- 毫秒/秒指标按可读性缩放（≥1000 显示为 k），不强套 K/M。
- 其他计数类走通用 human 格式（K/M/B）。

## 图表呈现

每个指标一张纵向柱状图卡片（带 Y 轴刻度、时间轴、最大/最小/平均与峰值时刻），与 `usage trend` 的卡片形式一致。null 表示该时间点无数据（与 0 不同），统计时排除以免拉低平均值。
