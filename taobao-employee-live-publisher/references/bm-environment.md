# BM 环境定位与只读兼容性演练

## 源码入口不等于运行实例

先在本 Skill 目录执行（将路径替换为用户指定的项目根）：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/bm_preflight.py --project-root /Users/a1111/Documents/dev/bm
```

也可显式传入 `/Users/a1111/Documents/dev/bm/bm-ai-octop`。脚本仅检查指定根及其 `bm-ai-octop` 子目录的文件存在性；不读配置、不导入项目、不访问网络、不装依赖、不写文件。JSON 的 `octop_root` 和 `sources` 是绝对路径或 `null`；`runtime_verified` 始终为 `false`。`ready` 仅表示三个源码文件齐全，退出码为 0；缺少全部来源为 `unavailable`，部分存在为 `partial`，两个候选均有来源为 `ambiguous`，均退出 2。歧义时不选根；无效显式路径不回退到当前目录。源码不齐仍可报告可见事实，不能宣称运行能力可用。

当前聚合仓库的 Octop 根为 `bm-ai-octop`，本 Skill 的源码路径都相对解析后的 Octop 根：

| 用途 | 相对路径 |
| --- | --- |
| BM 员工表单、平台状态与回查路由 | `bm-integration/deployment/single_database/management_routes.py` |
| 员工查询、版本与写操作契约 | `bm-integration/deployment/single_database/employee_contract.py` |
| 可信同步绑定与附件摘要核验 | `services/feishu-sop-oss-sync/verified_sources.py` |

同目录 `platform.py` 描述 Octop 进程内平台接入，源码标记服务端口为 50362。聚合根的 `bm-ai-taobao-topapi/services/employee-skill-api` 是另一个独立服务快照，其 README 示例默认 8019、test/LAN 模式；两者运行实例、鉴权和 API 能力不能互换。不能因目录存在就启动服务、使用 8019、套用免认证模式，或将旧端口当成当前实例证据。

## 只读兼容性 dry-run

用户只要求兼容性验证时，停留在下列步骤，报告已验证项、缺口和下一步，不进入创建、保存、关联、版本发布、飞书回填或同步操作：

1. 执行上述源码预检。浏览器操作前，先读取已安装 `ego-browser/SKILL.md`，执行 `ego-browser skill` 并遵循当前版本输出；使用自己的 taskSpace 和真实浏览器命令。沿用当前已登录账号，检查 BM 当前页面地址、账号、环境和目标员工身份；不抽取 Cookie、Token 或本地凭据，不另建登录态。仅在登录或验证码必须由用户完成时 handOff；完成后 finish 自己的 taskSpace，不关闭其他任务空间。
2. 从当前页面和实际能力响应确认运行入口，经现有 UI/应用请求链路核对 Octop 的 `GET /api/v2/bm/management/status`（账号权限、环境、configured、写开关、审批能力）与目标契约。现有审批和管理员权限仍是边界；预检成功、服务就绪或浏览器登录均不能证明 TOP 授权和发布能力。不要为验证而改配置、重启或安装依赖。页面登录态可能仍需应用的 Authorization，单独带浏览器 Cookie 的 GET 返回 401 不能证明退出登录或接口缺失；不提取 Token 来补请求。等待页面加载稳定后再判断按钮权限、空列表和授权范围，加载中的禁用或“暂无”不是最终结果。
3. 核对飞书来源、BM 本地对象与淘宝同账号的正式 worker_code、版本、依赖和完整渠道范围。飞书多维表格 canvas 用截图核对实际行和内容；没有可靠记录 ID 就报告未确定，不从行号或标题编造。读取或检索须限定本次对象，名称相似不能证明绑定。
4. 严格零本地业务状态写入时，不点 BM 的“回查平台资料和版本”：`GET /api/v2/bm/management/employees/{identifier}/platform` 调用 `refresh()`，会保存平台快照，GET 不能据此视为无副作用。改用经当前能力核实的直接平台只读查询 `GET /api/v1/digital-employees`、`GET /api/v1/digital-employees/{worker_code}/versions` 及指定版本详情，并限制页数和目标。读取失败或权限不足就报告，不能创建或重发来试探。

独立 TOP SDK 的只读测试脚本需要另外配置的应用凭据与平台权限；它验证该 SDK/应用上下文，不验证 Ego 浏览器已有登录态，也不能把浏览器会话转成 SDK 凭据。可信同步绑定若需要私有配置或数据库，只有已有明确授权才读取；本 dry-run 不会为了补齐证据读取它们。

2026-11-19 的只读浏览器观察：BM 页面实际位于 `http://192.168.110.121:50362/`，登录账号为 `official-admin`，员工列表加载完成后显示 55 个员工（初始只显示 24 个福客模板）；飞书员工表 canvas 可见 29 条记录及已有平台编码、线上版本列；淘宝开发者控制台账号为「成都福客」。BM 直接 Cookie 请求状态接口得到 `401 AUTH_FAILED`，而已登录 UI 可用；新建按钮由加载中禁用转为可用。未保存员工编辑器的“淘宝平台与版本”页要求先保存草稿再同步或关联，没有为测试保存或创建。淘宝某已有技能的授权列表加载完成后显示两店，最初的空态不能用作范围证据。

上述仅验证已登录 UI 与源码入口兼容；未核实运行时 platform mode、writesEnabled，未验证完整飞书/BM/平台映射、当前版本、发布结果或写操作，也未提交线上变更。这些是当时页面证据，不是默认目标或当前运行保证。BM 模板不能当作对应平台员工，飞书可见编码不能凭名称自动绑定，BM 浏览器账号不能当作 TOP 应用身份；实际操作仍逐对象核对。

进入真实操作后，仍按主流程保持既有审批、账号环境、版本隔离、渠道与商家范围。请求结果未知时先按同一对象和操作标识回查，不能重复创建或发布；飞书回填失败单独对账。
