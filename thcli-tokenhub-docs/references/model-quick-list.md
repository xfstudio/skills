# 常用模型速查表（区分国内站 / 国际站）

来源：国内站 [模型列表](https://cloud.tencent.com/document/product/1823/130051) / 国际站 [Model list](https://www.tencentcloud.com/document/product/1300/78934)。快照时间：2026-09-02。

**重要**：两站模型清单**不完全相同**。同一模型 ID 在两站可能都支持，但也存在只在一个站点提供的模型。使用前先确认用户所属站点（见 SKILL.md「能力零」），只在对应站点的表格里查找；查不到不要假设"另一站有所以这站也该有"，需重新 WebFetch 对应站点的模型列表页确认。**模型会持续上线/下线**，文档中标注"（YYYY-MM-DD下线）"的模型不要再推荐给用户新接入。

---

## 语言模型

| 常见叫法 | model（调用参数） | 国内站 | 国际站 | 备注 |
|---|---|---|---|---|
| 混元3 / Hy3 | `hy3` | ✓ | 国际站列表未见 | 国内站各接入文档默认示例模型；国际站接入文档默认示例已改用 `deepseek-v4-pro`（仅 Codex 文档国际站仍用 hy3 示例，需现场核实该模型是否已加入国际站） |
| 混元4预览版 | `hy4-preview` | ✓ | ✓ | 两站均支持，1M上下文 |
| 混元角色扮演 | `hy-role` / `hunyuan-role-latest` | ✓ | 国际站列表未见 | |
| 混元翻译 | `hy-mt2-pro` / `hy-mt2-plus` / `hy-mt2-lite` | ✓ | ✓ | 两站均支持 |
| DeepSeek V4 Pro | `deepseek-v4-pro` | ✓ | ✓ | 国际站各接入文档默认示例模型 |
| DeepSeek V4 Flash | `deepseek-v4-flash` | ✓ | ✓ | 两站均支持 |
| DeepSeek V3.2 | `deepseek-v3.2` | 国内站列表未见 | ✓ | **仅国际站**，国际站快速入门文档默认调用示例用的就是此模型 |
| GLM-5.3 / GLM-5.3-Flash / GLM-5.2 / GLM-5.1 / GLM-5-Turbo / GLM-5V-Turbo / GLM-5 | 同名小写 | ✓ | ✓ | 两站均支持 |
| Kimi K3 / K2.7 Code / K2.7 Code HighSpeed / K2.6 / K2.5 | 同名小写 | ✓ | 国际站未见 K2.7 Code HighSpeed 之外确认，需现场核实 | 建议接入前现场确认 |
| MiniMax-M3 | `minimax-m3` | ✓ | ✓ | 两站均支持 |
| MiniMax-M2.7 | `minimax-m2.7` | ✓ | ✓ | 两站均支持 |
| MiniMax-M2.5 | `minimax-m2.5` | 国内站列表未见 | ✓ | **仅国际站** |
| Qwen3.5-Flash（2026-09-08下线） | `qwen3.5-flash` | ✓ | 国际站列表未见 | **仅国内站**，且即将下线，不建议新接入 |
| Qwen3.5-Plus（2026-09-08下线） | `qwen3.5-plus` | ✓ | 国际站列表未见 | **仅国内站**，且即将下线，不建议新接入 |
| MiMo-V2.5-Pro | `mimo-v2.5-pro` | ✓ | ✓ | 两站均支持 |

## 视觉模型 - 图像生成

| 常见叫法 | model（调用参数） | 国内站 | 国际站 |
|---|---|---|---|
| 混元生图3.0 | `hy-image-v3` | ✓ | ✓ |
| Seedream 5.0 Pro / Lite | `Seedream-Image-v5.0-pro` / `-lite` | ✓ | ✓ |
| Vidu-Image-q2 | `vidu-image-q2` | ✓ | ✓ |
| Wand-Vega-Image 系列 | `wand-vega-image-*` | ✓ | 国际站列表未见 | **国内站图片生成模型种类明显多于国际站**，接入前建议现场核实 |

## 视觉模型 - 视频生成

| 常见叫法 | model（调用参数） | 国内站 | 国际站 |
|---|---|---|---|
| 可灵 V3 / V3-omni / V3-turbo | `kling-video-v3*` | ✓ | ✓ |
| MiniMax 视频 H3 | `minimax-video-h3` | ✓ | ✓ |
| PixVerse Video v6 / c1 | `pixverse-video-*` | ✓ | ✓ |
| 混元视频 1.5 | `hy-video-1.5` | ✓ | ✓ |
| MiniMax Video v2.3 系列、Vidu-Video 系列（q2/q3多档）、YT-Video 系列 | 各自 model 值 | ✓ | **国际站视频生成模型种类明显少于国内站**，仅保留部分主力型号，接入前必须现场核实目标模型是否在国际站可用 |

## 视觉模型 - 3D 生成

| 常见叫法 | model（调用参数） | 国内站 | 国际站 |
|---|---|---|---|
| 混元3D 全景图 / 3D场景 | `hy-world2-panorama` / `hy-world2-scene` | ✓ | ✓ |
| 混元3D 3.0/3.1/极速版/组件/格式转换/动作/拓扑/绑骨/纹理/UV 等全系列 | 各自 model 值 | ✓ | **国际站 3D 生成仅保留 2 个模型（全景图/3D场景），HY-3D 系列细分工具型模型（组件拆分/格式转换/绑骨蒙皮等）在国际站列表未见**，需现场核实 |
| Tripo-3D 系列 | `tripo-3d-*` | ✓ | 国际站列表未见 | 需现场核实 |

## 语音 / 多模态理解模型

| 常见叫法 | model（调用参数） | 国内站 | 国际站 |
|---|---|---|---|
| MiniMax 语音合成/音色复刻/音色设计 | `minimax-speech-*` / `minimax-voice-*` | ✓ | 国际站列表未见语音/多模态理解分类，**语言模型分类中部分带图片视频理解能力标签，未见独立的语音模型或多模态理解模型分类** |
| WAND ASR / AI配音 | `wand-*` | ✓ | 同上 |
| YT-VITA / HY-Vision 系列 | `youtu-vita` / `hy-vision-*` | ✓ | 同上 |

## 向量模型

| 常见叫法 | model（调用参数） | 国内站 | 国际站 |
|---|---|---|---|
| Kinfra 文本向量 0.6b / 4b | `kinfra-text-embedding-*` | ✓ | ✓ |
| Kinfra 多模态向量 2b / 8b | `kinfra-vl-embedding-*` | ✓ | ✓ |

---

## 使用说明

- 用户描述模型时可能用中文俗称、英文简称或不精确的版本号，需要先在对应站点的表里匹配，匹配不到再重新抓取该站点的模型列表文档确认。
- **接入编程类 AI 工具**（Claude Code/Cursor/CodeBuddy Code/Cline/Kilo Code/Roo Code/OpenCode/Codex）通常只用**语言模型**；如果用户想接入的是图片/视频/3D生成模型，这些编程工具插件形态一般不支持，需要向用户确认清楚场景。
- **国际站的视觉模型（图片/视频/3D）种类总体少于国内站**，接入前若用户目标模型属于视觉类，务必现场核实该模型是否在国际站列表中，不要假设国内站有的国际站也一定有。
- **国内站独有、即将下线的模型**（Qwen3.5-Flash/Plus，2026-09-08下线）不建议给任何用户新接入，无论站点。
- 每个模型的能力标签（深度思考/结构化输出/Function Calling/Cache缓存/图片视频理解）决定它能否在目标工具里开启对应功能，两站同名模型的能力标签基本一致（如两站的 `hy4-preview`、`glm-5.3` 系列能力描述相同）。
