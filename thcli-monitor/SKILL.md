---
name: thcli-monitor
description: 用 thcli monitor 查腾讯云 TokenHub 的服务健康度——文本模型的请求量/错误率/延迟/TPM 等指标，以及非文本模型（图片/视频/音频/3D）的产出量与质量。当用户想知道"服务稳不稳""错误率高不高""延迟多少""视频生成了多少时长""图片生成量"时使用。纯只读观测，不涉及任何云端资源写或计费操作。
---

# thcli monitor · 服务健康度观测

`thcli monitor` 回答"用得好不好"——请求量、错误率、延迟，以及非文本模型的产出量。纯只读。执行前先遵循 **thcli-shared**。

> **执行规则**：本 skill 的命令全部只读，可直接执行。若指标结论引出写操作
> （如"错误率高，建议调限流""这个接入点该停了"），**只输出命令文本给用户，
> 不调用工具执行**——即使用户明确要求、即使已提问确认过参数。

与 **thcli-usage** 的分工：usage 看 token 用量；monitor 看健康度指标与非文本模型产出。

## 命令

| 命令 | 面向 | 说明 |
|---|---|---|
| `thcli monitor text` | 文本模型 | 健康度指标（请求量/错误率/延迟/TPM 等）；默认账号整体，可下钻 |
| `thcli monitor vision --model <ModelId>` | 图片/视频/3D 模型 | 产出量与质量（张数/时长等） |
| `thcli monitor audio --model <ModelId>` | 语音模型（ASR/TTS/Audio） | 产出量与质量（字符数/时长等） |

## monitor text —— 文本模型健康度

```
thcli monitor text                      # 账号整体，缺省核心指标
thcli monitor text --model <ModelId>    # 下钻到某模型
thcli monitor text --endpoint <ep-xxx>  # 下钻到某接入点
thcli monitor text --apikey <ak-xxx>    # 下钻到某 Key
thcli monitor text --all                # 全部指标
thcli monitor text --list-metrics       # 列出可选指标（含 * 标默认项、可下钻/仅账号级标注）
```

- `--metric <keys>`：逗号分隔选指标；不传用缺省核心指标。
- 部分指标仅账号级（uinOnly），下钻参数对它们无效，输出会标注"该指标仅账号级"。
- `--start-time/--end-time`：默认最近 24 小时；`--period <秒>`：默认 3600。

## monitor vision / audio —— 非文本模型产出

```
thcli monitor vision --list-models      # 列出可查的图片/视频模型（按类型分组）
thcli monitor vision --model <ModelId>  # 查指定模型
thcli monitor audio  --list-models      # 列出语音模型
thcli monitor audio  --model <ModelId>  # 查指定模型
```

- 必须指定 `--model`；不给会提示先用 `--list-models` 找模型。
- vision 与 audio 指标结构相同（rpm/total_token/multimodal_usage/error_ratio/duration 五项），差别在 `multimodal_usage` 的含义：视频=时长、图片=张数、TTS=输入字符数（由模型的 UsageDisplayStrategy 决定）。
- 若把模型传给了错误的子命令（如语音模型传给 vision），会提示改用另一个子命令；若模型根本不是非文本模型，会提示改用 `thcli usage trend`。

## 参考

- 公共协议：**thcli-shared**
- token 用量与排行：**thcli-usage**
- 指标分组依据与下钻规则见 `references/perf-metrics.md`
