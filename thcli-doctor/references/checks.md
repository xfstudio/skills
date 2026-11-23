# thcli doctor · 各诊断项细节

本文件补充 `thcli doctor` 各子命令的检查内容与输出解读，供需要深入排障时参考。

## doctor（= doctor all）—— 整体体检

裸跑 `thcli doctor` 即执行体检；`doctor all` 是它的显式同义写法。

依次检查四项，逐行输出结论：

1. **凭证（credential）**：来源（命令行/环境变量/凭证文件）、profile、site、脱敏后的 secretId、类型。OAuth 临时密钥会检查是否过期，过期则提示重新登录。来源为 none 表示尚未登录。
2. **站点地域（site/region）**：当前 site 是否合法（cn/intl），列出该站点可用地域。
3. **云 API 连通**：实际调一次 `DescribeApiKeyList`（Limit=1）验证 API 通路，失败会打印错误信息。
4. **对话用的 Key**：检查当前 profile/site/默认地域下是否存有 `th` 类型的 Key（`+chat` 用），缺失会提示。

## doctor key --id <ak-xxx> —— Key 诊断

对应接口 `DescribeApiKey`。逐项检查：

- **状态**：是否为 `enable`；非 enable 会指出当前状态。
- **绑定范围（BindType/BindingItems）**：
  - `all`：可访问全部资源。
  - 空绑定：提示范围为空可能调不通。
  - 有绑定：检查绑定的资源是否 `online`；有离线资源会单独列出（这是"Key 正常却调不通"的常见隐蔽原因）。
- **额度（QuotaSet）**：按周期逐条比对 `CycleUsed / CycleCredits`，给出百分比；用尽会明确标出。`QuotaStatus=inactive` 会额外提示。
- **IP 白名单（IpWhitelist）**：
  - 无白名单：放行所有 IP。
  - 有白名单：调用会先提示，再向 ipify.org 取本机出口公网 IP，然后判断是否命中（支持单 IP 与 IPv4 CIDR；IPv6 或异常格式按"无法确定"处理）。

## doctor endpoint --id <ep-xxx> —— 接入点诊断

对应接口 `DescribeEndpoint`。输出名称/ID/状态/计费类型/后付费开关。状态为 ACTIVE 或 RUNNING 即正常；否则给出 `StopReason` 与对应恢复建议（无匹配建议时给通用兜底话术）。

## doctor model --id <ModelId> —— 模型诊断

先 `DescribeModelList` 确认模型存在及状态，再 `DescribeModelEndpointList` 统计该模型的接入点：无接入点 / 有但无活跃 / 有活跃，分别给出结论。只看接入点活跃性，不反查"被哪些 Key 授权"。

## doctor plan --team-id <id> —— 套餐诊断

对应接口 `DescribeTokenPlan`。输出名称/ID/产品类型；状态 `enable` 且无异常 StopReason 即正常。额度按产品类型选单位（enterprise→积分，其他→token），余量超 80% 会预警、用尽会告警。附带 TokenSummary 明细。

## doctor error [code] —— 错误码查询

码是**位置参数**（`doctor error 401008`），写成 `--code` 会报 unknown option。

- 不给 code：分「管控面/数据面」两组列出全部收录码及简要原因。
- 精确命中：打印原因 + 修复建议（修复建议尽量给可直接执行的 thcli 命令）。
- 未精确命中但有前缀匹配：列出所有匹配子码。管控面输 `AuthFailure`、数据面输 `429` 都有效。
- 完全未命中：提示未收录，并附上完整清单便于自查。
