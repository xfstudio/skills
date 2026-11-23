# thcli endpoint · 查询字段与解读细节

## endpoint list 字段

对应接口 `DescribeModelEndpointList`。列：EndpointId / ModelId / ModelName / Status / ChargeType / Payment（后付费 on/off）。

注意 `ModelName` 与 `ModelId` 是两个不同字段：ModelId 可能是英文全称，ModelName 是缩写；`--model-name` 过滤的是 ModelName（模糊），`--model-id` 过滤 ModelId（精确）。

`--id`（EndpointId 精确）与 `--endpoint-name`（模糊）虽然官方 Filters 未显式声明，但后端实际支持。

## endpoint get 字段

对应接口 `DescribeEndpoint`。展示：

- 服务名与 EndpointId、关联模型名与 ModelId。
- 状态（Status）。
- 计费类型（ChargeType）。
- 后付费开关（PaymentEnabled）。
- 停止原因（StopReason，若非运行态）：附带对应恢复建议。
- 免费额度（从 ChargeDetail 的 FreeQuota 解析，若有）：显示"已用/总量（百分比）"。

## 常见停止原因

- `FREE_QUOTA_EXHAUSTED`：免费额度用尽。恢复需开后付费（写操作，`endpoint postpaid on`，由用户执行）。
- 其他原因（欠费、无免费包等）：开后付费也未必能恢复，`get`/`doctor endpoint` 会给出针对性建议。

## 与 +chat 的关系

`+chat --model` 填模型 ID 即可（默认接入点同名）。要指定自建接入点时，用 `endpoint list` 找状态为 ACTIVE/RUNNING 的 `ep-xxx`。

## 为什么写/计费操作不纳入 skill

- `deploy`（CreateEndpoint）：创建新接入点。
- `endpoint update`（ModifyEndpoint）：改限流/名称/计费方式/自动调额。
- `endpoint delete`（DeleteEndpoint）：删除接入点。
- `endpoint postpaid on|off`（ModifyPaymentState）：开关后付费，`on` 会产生计费并领取未领免费包。

以上均改动云端资源或影响计费，本期由用户手动执行，skill 只给命令与影响说明。
