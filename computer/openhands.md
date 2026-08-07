---
---
# OpenHands 项目简介

## 概述
OpenHands 是一个开源的 AI 驱动软件开发平台，MIT 许可。

## 核心产品

### SDK
可组合的 Python 库，包含所有 agentic 技术，可本地运行或云端扩展至 1000+ agent。
- 文档：https://docs.openhands.dev/sdk
- 源码：https://github.com/OpenHands/software-agent-sdk/

### CLI
命令行界面，支持 Claude/GPT 等 LLM，类似 Claude Code 体验。
- 文档：https://docs.openhands.dev/openhands/usage/run-openhands/cli-mode
- 源码：https://github.com/OpenHands/OpenHands-CLI

### Local GUI
REST API + React 单页应用，可本地运行 agent，类似 Devin/Jules 体验。
- 文档：https://docs.openhands.dev/openhands/usage/run-openhands/local-setup

### Cloud
托管部署版本，支持：
- Slack、Jira、Linear 集成
- 多用户支持
- RBAC 和权限管理
- 协作功能（对话共享）
- 免费试用：https://app.all-hands.dev

### Enterprise
企业版，支持 Kubernetes 自托管（Polyform 许可）。
- 网站：https://openhands.dev/enterprise

## 技术栈
| 组件 | 技术 |
|------|------|
| 后端 | Python（`openhands/` 目录） |
| 前端 | React（`frontend/` 目录） |
| 运行时 | Docker 容器化 |
| 测试基准 | SWE-Bench 得分 77.6% |

## 生态项目
- [评估框架](https://github.com/OpenHands/benchmarks)
- [Chrome 扩展](https://github.com/OpenHands/openhands-chrome-extension/)
- [Theory-of-Mind 模块](https://github.com/OpenHands/ToM-SWE)

## 许可
核心 `openhands` 和 `agent-server` Docker 镜像为 MIT 许可，`enterprise/` 目录除外（Polyform 许可）。

## 社区
- Slack：https://dub.sh/openhands
- GitHub Issues：https://github.com/OpenHands/OpenHands/issues
- 产品路线图：https://github.com/orgs/openhands/projects/1
