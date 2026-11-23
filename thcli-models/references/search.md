# thcli models search · 需求解析与打分细节

`models search` 无语义检索，它把自然语言需求翻译成真实的分类维度（Tags/Brand/ModelSpec）后打分排序。理解这套映射有助于写出更精准的 query 或改用结构化 flag。

## 解析流程

1. 拉全量模型（分页，一次 100）。
2. 结构化 flag 做硬过滤（见下）。
3. 有 query 时按词典解析 query → 硬过滤（任务/厂商/规格）+ 软打分 → 排序取 Top N（默认 10）。
4. 无 query 时按结构化过滤结果，按 RecommendWeight 排序。

## 任务词典（需求词 → Tags，硬过滤）

命中即要求模型带对应标签。示例映射：

| 需求词（部分） | 命中标签 |
|---|---|
| 深度思考/推理/数学/证明/逻辑/代码 | 深度思考 |
| 看图/识图/视觉/图片理解/ocr/文字识别 | 视觉理解 |
| 画图/文生图/生成图片/绘图 | 图片生成 |
| 视频/文生视频/图生视频 | 视频生成 |
| 语音转文字/语音识别/asr/转写 | 语音识别 |
| 配音/文字转语音/tts/语音合成 | 语音合成、AI配音 |
| 音乐/作曲/歌曲/bgm/配乐 | 音乐生成 |
| 3d/三维/建模/立体 | 3D生成 |
| 向量/检索/embedding/相似度 | 文本向量、多模态向量 |
| 翻译/中译英/英译中 | 翻译 |
| 角色扮演/人设/扮演 | 角色扮演 |
| 写作/对话/聊天/问答/文案 | 文本生成 |

注意：不含裸"文本"一词，避免"长文本""多模态文本"里的"文本"误触发生成任务。

## 厂商词典（需求词 → Brand，硬过滤）

混元/hunyuan/腾讯→混元；minimax→MiniMax；deepseek/深度求索→DeepSeek；可灵/kling→可灵；vidu→Vidu；智谱/glm/zhipu→智谱 AI；月之暗面/kimi/moonshot→月之暗面；通义/千问/qwen/阿里→通义千问；优图/youtu→优图；pixverse→pixverse；tripo→Tripo。

只放品牌名，不放模型 ID 前缀（如 hy3、hy- 走文本模糊匹配精确命中单个模型，不当厂商过滤）。

## 规格排序信号（软打分）

- cheap（便宜/低价/省钱/性价比/实惠）：按输入价归一化，越便宜分越高；同时要求模型有价格。
- longContext（长文本/长上下文/大窗口/长文档）：按 ContextLength 归一化；要求 >0。
- longOutput（长输出/写长文/长回答）：按 MaxOutputToken 归一化；要求 >0。
- highThroughput（高并发/高吞吐/高tpm/高qps）：有 TPM 时加分。

"免费"不算价格低——它对应 FreeTrialInfo（状态词 free），另行加分。

## 状态词（软打分）

- free（免费/试用/白嫖/领取）：有 FreeTrialInfo 时加分。
- experience（体验）：SupportExperience 时加分。

## 运行时能力词（给提示，不硬匹配）

"联网/搜索/上网""函数调用/工具调用/function/tool/插件"这类被当作网关层运行时能力，命中时给能力边界提示与下一步建议，而不是误匹配到不准的标签或返回空。

其中「联网搜索」有对应的模型标签，用 `thcli models list --tags 联网搜索` 可精确筛出支持的模型。

## 打分权重（近似）

- 任务标签命中：+10（每个命中标签）
- 厂商命中：+8
- 文本 token 命中（模型名/系列/ID 含 query 的 ASCII 词）：+5
- 规格归一化：各最多 +5（cheap/longContext/longOutput）
- highThroughput/free/experience：+3

最终按分数降序，同分按 RecommendWeight。分数为 0 的不进结果。

## 结构化 flag（硬过滤，可与 query 组合）

`--type`（ModelType 精确值或中文任务词）/`--brand`/`--status`/`--min-context`（如 128k）/`--max-input-price`/`--free-trial`/`--experience`/`--limit`。

## 规格字符串解析

`256k`→256000，`1m`→1000000，`2b`→2000000000。输入价优先取 Input 维度，3D 等只有 Output 的模型回退取第一个有价格的维度。
