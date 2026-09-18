# opencode 精选 Issues 备忘（值得看清单）

> 整理自 github.com/anomalyco/opencode 上讨论最多、最有价值的 issues（按评论数筛选）。
> 目的：新用户快速了解 opencode 的坑、已知问题与设计方向，少走弯路。
> 数据截至 2026-09，状态以仓库为准。

---

## 一、最值得看的前几名

### 1. #20695 Memory Megathread —— 内存问题总入口（144 评论，closed）
- 官方把所有散落的内存/卡顿问题集中到这一个 issue 处理，收敛了很多报告。
- **关键收获**：排查内存泄漏的官方流程——
  - 手动：`opencode` 跑到内存升到 1–2GB → 按 `ctrl+p` → 选 heap snapshot → 上传给官方分析。
  - 自动：`OPENCODE_AUTO_HEAP_SNAPSHOT=1 opencode`，内存超过 ~2GB 会自动写 `.heapsnapshot` 到日志目录。
- 教训：**别让 LLM 猜内存问题的原因，官方要的是堆快照这类实据。**

### 2. #8030 Copilot 授权把大量请求算成 "user" 狂吃配额（225 评论，closed）
- 现象：早上用 Copilot 的 Opus 几次操作，就消耗了半个月配额——因为工具调用产生的消息被计为 "user" 类型从而消耗 premium 配额。
- 本质：`opencode-copilot-auth` 收紧了对 `X-Initiator: agent` 头的发放，导致 opencode 合成的"工具附件"消息被算作真用户请求，统统扣 premium 额度。
- **启示**：用 Copilot + opencode 时注意配额消耗，agent 自动触发的请求与真正用户请求的计费边界需要留意。

### 3. #631 Windows Support —— Windows 支持总开关（207 评论，closed）
- 一个"超级 issue"，汇集所有 Windows 上报的问题（曾经支持不完善）。
- 现在 Windows 支持已大幅改善，但这个 issue 是了解历史问题清单的好地方。

### 4. #2242 Is there a way to sandbox the agent?（90 评论，open）
- 问：能不能限制 agent 访问当前目录以外的文件？gemini-cli / codex-cli 在 macOS 用 seatbelt 沙箱。
- 官方当时没有等价的沙箱，安全边界靠权限系统（permission）实现，而不是 OS 级沙箱。
- **启示**：不信任时，用 permission 白名单 + 只读模式 + git 兜底，别指望 OS 级隔离。

### 5. #10416 OpenCode 默认不够"纯本地"？（60 评论，closed）
- 现象：用本地自建 LLM 时，**会话标题的生成居然发生在你的网络之外**；用 nftables 挡住外联后，自动命名功能才失效。
- 官方回应处理方向：标题生成这类功能要有明确开关 / 尽量走本地。
- **启示**：在意隐私 + 想全本地跑的人，要检查遥测/云功能的开关，光断网会出现功能悄悄失效。

---

## 二、常见故障类（遇到相似问题先来这里）

### 6. #18267 Claude Code OAuth 登录炸了？（154 评论，closed）
- 现象：`opencode` 用 Claude Code 授权，不断报 429、登录后无 token。
- 是 Claude Code 端认证波动引起，等官方修复/重试即可，很多人同批中招。
- **启示**：429 / OAuth token 丢失，先确认不是自己配置问题，很可能是一波通用的服务端故障。

### 7. #4283 Copy To Clipboard is not working（133 评论，open）
- 现象：选中回复文本提示"已复制"，但粘贴出来的是旧内容。
- Ubuntu 24.04 默认终端 + VS Code 终端均复现，报了一大堆，**至今仍 open**（复制到剪贴板是个顽固坑）。
- **启示**：剪贴板失效可改用 opencode 内置 `/copy` 或输出重定向，别依赖终端选择的"假复制"。

### 8. #29079 GPT Models takes too long to respond（119 评论，closed）
- 现象：简单 prompt 有时秒回、有时几分钟甚至十分钟（GPT 5.4 xhigh 等）。
- 与模型端负载/网络、reasoning effort 有关，不是 opencode 本身 bug。
- **启示**：用 GPT 高 reasoning 档位时，把等待预期放长；太久可先 `/compact` 或重启会话。

### 9. #811 Text rendering is VERY slow（84 评论，closed）
- 现象：assistant 消息/ diff / 工具结果渲染极慢，CPU 占用高甚至空闲也高。
- 曾导致时间戳比墙钟慢几分钟——渲染是瓶颈，不是模型慢。
- 老版本问题，新版已改善；若仍复现可配合 heap snapshot（见 #20695）报给官方。

### 10. #3936 Github Enterprise authorization（58 评论，closed）
- 现象：GitHub Copilot + GitHub Enterprise 登录时 `Failed to initiate device authorization`。
- 是 `opencode-copilot-auth` 对 GitHub Enterprise 设备授权流程的兼容问题，后来已修。
- **启示**：企业部署 (SSO/GHE) 用户注意 copilot-auth 相关版本更新。

---

## 三、功能与设计方向（值得关注的新东西）

### 11. #4773 隐藏子代理（subagents）（63 评论，closed）
- 新增 `hidden` 和 `permission.task`:子代理可以从 `@` 菜单隐藏，还能控制"哪个 agent 能调用哪些子代理"(allow/deny/ask + glob)。
- 用处：编排式架构里，内部助手子代理只允许被主 agent 程序化调用，用户不能直接 @ 出来。
- 已在 dev 分支，属于"被更多人用上的高阶玩法"。

### 12. #27167 原生会话目标 `/goal`（78 评论，open）
- 提议给会话加"目标"概念，让模型一直记得该 session 要完成什么（比反复粘贴任务描述更结构化、省 token）。
- 方向处于 open，若你在意"会话漂移"，值得关注进展。

### 13. #33742 Windows：v1.17.10 Bun 段错误崩溃（60 评论，open）
- 具体版本在 Windows 上 Bun 段错误，v1.17.9 稳定——**升级前注意版本回退**。

---

## 四、一句话清单（快速扫）

| # | 标题 | 状态 | 评论 | 一句话 |
|---|---|---|---|---|
| 20695 | Memory Megathread | closed | 144 | 内存排查：堆快照是官方要的证据 |
| 8030 | Copilot 配额被工具消息狂吃 | closed | 225 | 小心 agent 请求消耗 premium 额度 |
| 631 | Windows Support | closed | 207 | Windows 问题历史总集 |
| 2242 | 给 agent 上沙箱? | open | 90 | 目前无 OS 级沙箱，靠权限+只读兜底 |
| 10416 | 默认不够本地/隐私 | closed | 60 | 会话标题生成也会联网，注意开关 |
| 18267 | Claude OAuth 429 | closed | 154 | 一波流认证故障，重试/等修 |
| 4283 | 复制到剪贴板失效 | open | 133 | 老大难坑，用 /copy 替代 |
| 29079 | GPT 模型响应慢 | closed | 119 | 主要怪模型/网络，不是 opencode |
| 811 | 文本渲染慢+CPU 高 | closed | 84 | 老版渲染瓶颈，新版已好转 |
| 3936 | GHE 设备授权失败 | closed | 58 | copilot-auth 兼容问题，已修 |
| 4773 | 隐藏子代理 | closed | 63 | hidden + permission.task 新特性 |
| 27167 | 原生 /goal 目标 | open | 78 | 会话目标概念，值得观望 |
| 33742 | Win Bun 段错误 | open | 60 | v1.17.10 崩，v1.17.9 稳 |

---

## 给新用户的行动建议

1. **遇到奇怪卡顿/内存**：直接走 #20695 的堆快照流程给官方，比自己猜强。
2. **在意隐私**：审查遥测、标题生成等云端功能开关；用本地模型时留意"悄悄联网"。
3. **用 Copilot 当 provider**：留意配额消耗曲线（#8030），版本更新注意 copilot-auth 兼容（#3936）。
4. **安全第一**：别把 agent 当沙箱（#2242），上只读 + permission 白名单 + git 仓库做兜底。
5. **常用功能坑**：剪贴板复制（#4283）、GPT 高推理档慢（#29079）都是已知的，别当是自己配错了。