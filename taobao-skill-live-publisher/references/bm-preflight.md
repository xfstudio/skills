# BM/Codex 本地发现与只读预检

在当前 Codex 会话中采用用户指定的项目根；未指定时从工作区附加目录确定 BM 或 Octop 根。不要把技能安装目录当项目根，也不要在显式路径缺失时改用 cwd。

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /absolute/path/to/taobao-skill-live-publisher/scripts/bm_preflight.py --project-root /absolute/path/to/bm
```

脚本仅检查指定根本身和其 `bm-ai-octop` 子目录中的文件是否存在；不读取内容、配置或凭据，不导入项目模块，不访问网络，不安装依赖，不写文件。JSON 的 `sources` 给出存在文件的绝对路径或 null，`octop_root` 为唯一候选根或 null；`runtime_verified` 始终为 false。三个必需文件全在时 `ready`/退出 0；部分存在为 `partial`，均不存在或根不可用为 `unavailable`，两个候选都含相关源码时为 `ambiguous`，后三者均退出 2。歧义时停止，明确根后重跑，不自行择一。`ready` 只证明文件存在，不证明源码版本、部署、登录、权限或发布能力。

## 当前源码定位

相对 `octop_root`：

| 用途 | 路径 |
| --- | --- |
| Octop 管理端身份、表单与淘宝批次契约 | `bm-integration/deployment/single_database/management_routes.py` |
| Octop 内嵌员工 HTTP 契约 | `bm-integration/deployment/single_database/employee_contract.py` |
| 飞书同步可信绑定核对 | `services/feishu-sop-oss-sync/verified_sources.py` |
| 需配置和网络的同步来源核验程序 | `services/feishu-sop-oss-sync/codex_source_preflight.py` |

先发现路径，再按任务读取公开源码核对实际契约，不能为“检查能否导入”运行项目代码。BM 聚合工作区另有 `bm-ai-taobao-topapi/services/employee-skill-api` 独立组件；其源码存在不证明 Octop 内嵌服务已部署，更不能将其端口、配置、账号、数据库或认证与 Octop 混用。分别标明来源与部署，优先核对用户当前所指的 Octop 页面及内嵌契约。员工接口仅作依赖/契约核对，不因此启动员工创建或发布。

## 只读 dry-run

- 从已知会话和现有登录页面核对目标账号、来源记录、包摘要、平台编码、版本和授权范围，列出缺项及来源证据。浏览器可查看现有记录，不触发创建、保存、上传或平台变更；批次创建和预览类 POST 也不当作只读请求。
- 文件发现不等于可信包核验。继续遵守 [飞书来源与回填](feishu-source-and-writeback.md) 的记录、附件指纹、可信绑定、OSS SHA256、包修订号和前后来源一致性检查。缺少可信库或配置权限时报告“来源未验证”，不因 dry-run 去下载密钥或获取额外凭据。
- `codex_source_preflight.py` 会读取配置、查询飞书和可信库并回读 OSS；它与本技能纯文件发现脚本不同，只在已有获准的服务端环境和访问范围下另行使用。不要在本地为 dry-run 自动安装其依赖或执行它。
- 输出已观察事实、源码存在性、尚未验证的运行时/包身份/权限，以及真实发布前待满足的条件。未知状态保持未知；dry-run 的可行性结论不是平台回执或写入授权。

## Ego 当前会话流程

浏览器操作前读取可用 `ego-browser/SKILL.md`，执行 `ego-browser skill` 并读到结尾标记。按该版本指南开始/恢复 `taskSpace`，记录 space ID，同一目标跨回复沿用；不新建任务空间绕过错误或人工接管。使用已登录网站，不导出 cookies、token 或 profile，也不把会话复制到 shell 请求。

需要登录、验证码、协议或其他人工操作时调用 `task.handOff()` 后结束本轮，等用户确认后按指南 `takeOverTaskSpace` 恢复。正常完成且已观察结果后，在单独最后脚本中调用一次 `task.finish({ keep: [...] })`，保留页仅按指南确有用户需要时选择；交接或错误停止时不调用 `finish()`。SDK 命令以本次 `ego-browser skill` 输出为准。
