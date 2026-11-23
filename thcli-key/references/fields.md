# thcli key · 查询字段与解读细节

## key get 输出字段

`key get --id <ak-xxx>`（或 `--api-key <明文>` 反查）对应接口 `DescribeApiKey`，展示：

- **基础**：ApiKeyId、名称、脱敏后的 Key、平台、Uin/SubUin、状态、BindType、是否可编辑（Editable）、创建/更新时间、备注。
- **IP 白名单**：为空显示"不限制"；否则列出允许的 IP/CIDR。
- **额度（QuotaSet）**：未配置时显示"无额度限制"；配置后逐条显示：
  - `已用/总量（百分比）`，按周期单位（月 m / 天 d）。
  - 额度记录 Status：1=正常、5=已用尽。
  - 周期起止时间（StartTime / ExpireTime）。
  - 顶层 `QuotaStatus=inactive` 表示额度整体停用（通常因用超）。
- **绑定资源（BindingItems）**：BindType 非 all 时列出，含 ResourceType / ResourceId / Status（在线状态）。

## 绑定范围（BindType）说明

- `all`：可访问全部资源。
- `model_custom_endpoint_custom`：按指定资源授权（CLI 对外简化为 `custom`）。
- 授权最终都落到 endpoint 上：给模型名等于授权其默认在线推理服务（模型级访问），给 `ep-` 开头的 ID 是服务级访问。

## key list 过滤

- `--status`（EXACT）、`--id`（EXACT）、`--bind-type`（EXACT）、`--name`（FUZZY 模糊）。
- `--order asc|desc` 按名称排序；`--limit`/`--offset` 分页。
- 列表的 APIKEY 列始终脱敏，不含完整明文。

## 与 doctor key 的分工

`key get` 是字段展示；`doctor key --id <ak-xxx>` 是诊断——在展示基础上判断状态是否 enable、绑定资源是否在线、额度是否用尽，并向 ipify.org 取出口 IP 判断是否命中白名单。排查"调不通"用 doctor，看配置用 key get。

## 为什么写/敏感操作不纳入 skill

- create/update/delete/enable/disable/status/quota：直接创建或修改云端密钥资源，属写操作。
- scope：改已创建密钥的可访问范围，属写操作。且是**全量覆盖**——未列出的目标立即失去访问权，误用会让线上调用当场鉴权失败，比多数写操作更需要用户亲自确认。
- reveal：输出密钥明文，属敏感读，出于安全边界不代为执行。

这些一律由用户手动执行，skill 只在需要时给出命令与参数。
