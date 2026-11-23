# thcli plan · 字段与命令细节

## plan list 字段

对应 `DescribeTokenPlanList`。列：TeamId / 名称 / ProductType / 状态 / KEYS（已用/上限 ApiKeyCount/ApiKeyMax）/ 创建时间。

## plan info 字段

对应 `DescribeTokenPlan`（结果裹在 Team 里）。展示：

- TeamId、名称、ProductType、状态（含 StopReason）、Key 数（已用/上限）、自动续费开关、创建/更新时间。
- PackageInfo：额度包信息（按产品类型选单位 credit/token）。
- TokenSummary：用量汇总。

## plan models

对应套餐的 PackageInfo.AllowedModels（或 Models）。列出该套餐允许调用的模型；为空会提示。

## plan detail

对应 `DescribeTokenPlanApiKeyUsageDetail`。按维度筛用量明细：`--id`（ApiKeyId）/`--name`（ApiKeyName）/`--model-name`/`--from`/`--to`/`--sort`/`--limit`。输出模型/Key 名/请求时间/输入/输出/合计。`ListOver=false` 时提示还有更多。

## available / cost

云 API 无"可购套餐列表""下单前询价"接口，这两个命令只打印说明并指向控制台，不发请求。属只读占位，可安全引导执行。

## plan key（专属 Key）三级命令

`plan key <verb>`。只读部分：

- `plan key list --team-id <id>`（`DescribeTokenPlanApiKeyList`）：APIKEY_ID/名称/脱敏 Key/状态/使用状态/创建时间。
- `plan key get --id <ak-xxx>`（`DescribeTokenPlanApiKey`）：Key ID/名称/脱敏 Key/TeamId/状态/允许模型/余额。

## 为什么写/计费/敏感操作不纳入 skill

- buy/renew/upgrade（`CreateTokenPlanTeamOrderAndBuy`/`RenewTokenPlanTeamOrder`/`UpgradeTokenPlanTeamOrder`）：真实扣款。且已知风险：调用返回错误但套餐可能已建成（不可退），失败必须先查状态再处理。
- plan key create/update/rotate/delete（`CreateTokenPlanApiKeys`/`ModifyTokenPlanApiKey`/`ModifyTokenPlanApiKeySecret`/`DeleteTokenPlanApiKey`）：创建/修改/轮换/删除专属 Key。
- plan key reveal（`DescribeTokenPlanApiKeySecret`）：输出明文，敏感读。

以上本期由用户手动执行，skill 只给命令与影响说明。
