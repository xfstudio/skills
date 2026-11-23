---
name: thcli-auth
description: 用 thcli auth 管理腾讯云 TokenHub 的登录与凭证——查看当前登录态、浏览器 OAuth 登录、手填永久密钥、登出。当用户"没登录/登录过期""想切换账号登录""查看当前用哪个账号"或任何命令报鉴权错误时使用。登录与本地凭证属使用前提，可引导执行。
---

# thcli auth · 登录与凭证

`thcli auth` 管理登录态与本地凭证。登录/登出/手填密钥只影响本地 `~/.thcli` 与登录态（非云端资源写），属**使用前提**，可引导执行。执行前先遵循 **thcli-shared**。

> **执行规则**：`auth status|login|set|logout` 只动本地凭证，可直接执行。
> 但**云端 API 密钥（`ak-`/`sk-`）的创建与管理不属于本 skill** —— 登录后若还需要
> 对话用的 Key，`key create` 等命令**只输出命令文本给用户，不调用工具执行**，
> 即使"为了把登录流程走完"、即使已提问确认过参数也不例外（**确认不等于授权代跑**）。
> 本地凭证与云端资源是两回事。

## 命令

| 命令 | 作用 |
|---|---|
| `thcli auth status` | 查看当前登录态：profile/site/凭证来源/类型/临时密钥有效期 |
| `thcli auth login` | 浏览器 OAuth 授权码登录（复用官方 app_id + 本地 loopback 回调） |
| `thcli auth set --secret-id <..> --secret-key <..>` | 手填永久密钥（type=static） |
| `thcli auth logout` | 删除当前 profile/site 的本地凭证 |

## 典型流程

1. **先查状态**：`thcli auth status`。退出码 0 表示凭证可用；非 0 表示未登录或已过期，见下方「故障态处置」。
2. **登录**：
   ```
   thcli auth login                    # 默认拉起浏览器
   thcli auth login --browser no       # 无图形环境（SSH/容器/CI）：显示 URL，手工粘贴凭据串
   thcli auth login --site intl        # 登录国际站
   ```
   登录成功后会自动备一把名为 `thcli-key` 的 API Key（供 `+chat` 用），正常无需手动配置。
3. **或手填永久密钥**（已有腾讯云 SecretId/SecretKey 时）：
   ```
   thcli auth set --secret-id <secret-id> --secret-key <secret-key>
   ```
4. **登出**：`thcli auth logout`（仅删本地凭证文件）。

## 故障态处置（照这里做，不要自行推断命令）

**`auth` 只有 `status` / `login` / `set` / `logout` 四个子命令。没有 `refresh`、没有 `renew`。**
凭证续期由 CLI 在调用云 API 前自动完成，不存在手动续期的命令——需要什么就查 `thcli auth --help`，
不要按其它 CLI 的惯例猜一个出来。

| 症状 | 处置 |
|---|---|
| `auth status` 显示已过期 / 来源 none | `thcli auth login`（这是唯一处置） |
| 任何命令报 `AuthFailure.TokenFailure` | `thcli auth login` 重新登录 |
| 报错但原因不明 | `thcli doctor` 定位后再决定 |

**判定是否可用要靠退出码，不要匹配文案**（文案随界面语言变化）：

```shell
thcli auth status >/dev/null 2>&1 && echo 可用 || echo 需要登录
```

退出码 1 覆盖两种情况：未登录、以及**凭证已过期**。二者的处置相同，都是重新 `login`。

关于自动续期：临时密钥有效期约 2 小时，但 CLI 每次调用前会检查、不足 5 分钟就自动换新，
所以**正常使用中不会因为"到点了"而失效**。若真的报了过期，说明 refreshToken 也失效了
（长期未使用、或在云控制台取消了授权），此时必须重新登录。不要向用户宣称"密钥 N 小时后
过期需重新登录"——那是误导。

## 多账号 / 多站点

- 登录/操作时用 `--profile <账号>`、`--site cn|intl` 临时指定。
- 设默认免带参数：`thcli profile use --name <X>`、`thcli site use --name <cn|intl>`（见 thcli-overview 的本地配置查询小节）。
- 每个 profile+site 组合各存一份凭证。

## 安全

- **复述命令时用占位符**（`<secret-id>`/`<secret-key>`），不要回显用户给出的真实密钥值。
- 凭证文件权限为 0600，仅本机当前用户可读。
- 遇到鉴权类报错，可配合 **thcli-doctor** 的 `doctor` 检查凭证有效性。

## 参考

- 公共协议：**thcli-shared**
- 环境体检：**thcli-doctor**
- 对话用的 Key（+chat 用）：**thcli-chat** / `thcli chat-config`
