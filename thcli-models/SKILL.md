---
name: thcli-models
description: 用 thcli models 查腾讯云 TokenHub 模型广场——列出模型、看单个模型详情与规格、查比价、按自然语言需求推荐模型、横向对比多个模型。当用户想"有哪些模型""这个模型多少钱""帮我找个能做 X 的模型""对比这几个模型"时使用。仅查询，不涉及开通付费/领取额度等写与计费操作。
---

# thcli models · 模型广场查询

`thcli models` 查询模型广场。以下均为只读命令。执行前先遵循 **thcli-shared**。

## 执行规则（读到这里就已生效，先于下面所有内容）

**这些命令属写/计费操作，只输出命令文本给用户，不调用任何工具执行：**

`models activate`（开按量付费） / `models free`（领免费额度）

以下情形**都不构成例外**：

- 用户明确要求"帮我开通按量付费/领一下额度" → 仍然只输出命令
- 已经用提问确认过参数、用户点了同意 → **确认不等于授权代跑**，仍然只输出命令
- 本 skill 的 description 写着"仅查询" → 那表示写操作**已被划出执行范围**，不是"无人管辖、可自行拼命令跑"
- `models free` 看起来是"免费"的 → 它同样是云端资源开通操作，只输出命令
- 用 `--help` 自己拼出了命令 → 拼命令可以，执行不可以

正确做法：说明该操作会开通资源或产生费用，把完整命令给用户，由**用户自己在终端执行**。

## 只读命令

| 命令 | 作用 |
|---|---|
| `thcli models list` | 列出模型（可按类型/标签/ID 过滤） |
| `thcli models get --id <ModelId>` | 单个模型详情：规格、计费、标签等 |
| `thcli models pricing` | 比价表（各模型的计费维度与单价） |
| `thcli models search [需求描述]` | 按自然语言需求推荐模型（软打分排序） |
| `thcli models compare <id1,id2,...>` | 横向对比多个模型（字段为行、模型为列） |

## list / pricing / get

```
thcli models list                          # 全部
thcli models list --type Text              # 按 ModelType 过滤
thcli models list --tags 深度思考           # 按标签
thcli models get --id <ModelId>            # 详情（含 ContextLength/MaxInput/MaxOutput/TPM/QPM 与计费明细）
thcli models pricing --type Text           # 比价
```

过滤参数：`--type`（ModelType，逗号分隔）/`--ids`/`--names`/`--tags`/`--limit`/`--offset`。

### 报价格时必须注意两件事

**一、很多模型是阶梯计价**，同一个维度（输入/输出/缓存）在不同区间有不同单价。表格里每档
前面标着 `[档位]`，`--json` 下 `ModelChargingInfo` 是按档分组的数组、每组有自己的 `Name`。

回答"这个模型多少钱"时要说清是哪一档，不要只报第一档就当成唯一价格：

```
[输入<16k]        输入 1.2 元/百万tokens
[16k<=输入<32k]   输入 1.6 元/百万tokens
[输入>=32k]       输入 2   元/百万tokens
```

**二、货币不统一**：部分模型按美元计价（如 `minimax-m3` 是 `美元/百万tokens`），多数按元。
单位就在 `PriceUnit` 里。**横向比价前先看单位**——把 `0.3 美元` 和 `1 元` 直接比会得出反的结论
（前者实际更贵）。单位不同时如实说明，不要自行换算汇率。

## search —— 需求驱动推荐

```
thcli models search "便宜的长文本模型"
thcli models search "混元的视频生成"
thcli models search "能看图识别文字的模型"
thcli models search --type 视觉理解 --max-input-price 5 --limit 5
```

- 底层无语义检索，search 是"需求词 → 分类维度翻译器"：把自然语言里的任务/厂商/规格词映射到真实的 Tags/Brand/ModelSpec 上打分排序，并给出命中理由。
- 任务词、厂商词命中时作为**硬过滤**（如"混元的视频生成"必须同时满足厂商=混元且标签含视频生成）；"便宜/长文本/长输出"等规格词作为**排序信号**。
- 结构化 flag（`--type/--brand/--status/--min-context/--max-input-price/--free-trial/--experience`）走硬过滤。
- 命中"函数调用/工具调用"这类运行时能力词时，会给出能力边界提示而非误匹配。
- 找支持联网搜索的模型用 `thcli models list --tags 联网搜索`（`models get` 的「标签」字段同样可见）。
- 词典与打分细节见 `references/search.md`。

## compare —— 横向对比

```
thcli models compare hy3,deepseek-v3,glm-4
```

- 一次最多 4 个（终端列宽限制）。以字段为行、模型为列转置展示，便于横向扫同一维度。
- 计费项按各模型的 PriceName 并集补行，能看出"某模型没有该计费维度"。

## 写/计费操作（skill 不执行，供用户自行操作）

以下会开通资源或产生费用：

- `thcli models free [models|all]`：领取模型免费额度。
- `thcli models activate [models|all]`：开启模型按量付费（会产生计费）。

**把命令输出给用户，由用户自己在终端执行**，并说明计费影响。这是既定安全边界——即使用户明确要求代跑，也仍然只输出命令。

## 参考

- 公共协议：**thcli-shared**
- 用模型跑对话：**thcli-chat**（`+chat --model` 直接填这里查到的模型 ID）
- 接入点：**thcli-endpoint**
