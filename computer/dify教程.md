# Dify 详细教程

> 基于 Dify 1.x（2026）。界面细节可能随版本微调，但概念和流程稳定。官方文档：https://docs.dify.ai

## 一、Dify 是什么

开源的 LLM 应用开发平台，一个界面里完成：**接模型 → 编排提示词/工作流 → 挂知识库 → 调 Agent 工具 → 发布成 Web/API**。

五种应用类型：

| 类型 | 适合场景 |
|---|---|
| 聊天助手 Chatbot | 客服、问答、陪聊 |
| 文本生成 Completion | 单次输入输出：写作、翻译、摘要 |
| Agent | 自主规划、多步调用工具 |
| 工作流 Workflow | 复杂固定流程，可视化编排 |
| Chatflow | 带对话记忆的工作流 |

## 二、安装部署

### 方式 A：本地 Docker Compose（推荐入门）

要求：CPU ≥ 2 核、内存 ≥ 4G（建议 8G），Docker + Compose ≥ 2.24。

```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env

# 新版 agent sandbox 需要 token
openssl rand -base64 32
# 把输出填到 .env 的 DIFY_AGENT_LOCAL_SANDBOX_AUTH_TOKEN

docker compose up -d
docker compose ps        # init_permissions 退出是正常的
```

访问 `http://localhost/install` 初始化管理员账号，然后登录 `http://localhost`。

- Windows 用 WSL2，代码和数据放 Linux 文件系统，别放 `/mnt/c`。
- 改端口：编辑 `.env` 里的 `EXPOSE_NGINX_PORT`（默认 80）。
- 国内拉镜像慢，先配 Docker 镜像加速器。
- 默认会起：api、worker、web、plugin_daemon、agent_backend、postgres、redis、weaviate、nginx、sandbox 等容器。

### 方式 B：云版（最快体验）

注册 https://cloud.dify.ai ，有免费额度，不折腾服务器。适合先验证想法。

### 方式 C：服务器生产部署

4C8G 云服务器起步，装 Docker，步骤同 A；再加：

- 域名 + Nginx/Caddy 反向代理 + HTTPS
- 改默认管理员密码、限制 80/443 外网、关掉不需要的端口
- 定期备份 `docker/volumes`（postgres、redis、weaviate、storage）
- **商用务必读 license**：Dify 是「Apache 2.0 + 附加条件」，不能直接拿去做多租户 SaaS 售卖

## 三、第一步：接入模型

右上角头像 → **设置 → 模型供应商**。支持 OpenAI、Anthropic、DeepSeek、通义千问、智谱、Ollama、以及任何 OpenAI 兼容 API。

- 填 `API Key`，兼容服务再填 `Base URL`
- 到 **系统模型设置** 指定默认的 LLM、Embedding、Rerank 模型
- **Embedding 模型直接决定知识库检索质量**，别随便选

本地 Ollama 接法：Base URL 填 `http://host.docker.internal:11434`（Mac/Windows）。Linux 上 `host.docker.internal` 不一定解析，用宿主机 IP 或 `172.17.0.1`。

填完点「检查」测试连通，再保存。

## 四、实战一：知识库问答（RAG）

### 4.1 建知识库

**知识库 → 创建知识库**，上传 PDF / Word / PPT / Markdown / TXT / 网页 / Notion 内容。

关键设置：

- **分段**：通用分段（固定长度+重叠）适合普通文档；父子分段适合长文，检索用子块、喂给模型用父块
- **分段长度/重叠**：中文一般 500~800 字，重叠 50~100
- **索引方式**：高质量（向量化，需 Embedding，效果好）/ 经济（关键词，省钱）
- **检索设置**：向量检索、全文检索、混合检索；TopK（取几条）、Score 阈值、是否挂 Rerank

上传后等索引完成，点「召回测试」，输入问题看命中的分段对不对。

### 4.2 建聊天助手并挂知识库

**创建应用 → 聊天助手**：

1. **添加上下文** → 选择知识库
2. 写系统提示词，例如：
   ```
   你是 XX 公司的客服。只根据提供的知识库内容回答。
   知识库里没有的信息，直接说“这个问题我需要转人工”，不要编造。
   回答简洁，用中文。
   ```
3. 右侧调试窗口直接提问，看回答和引用的文档片段
4. 调提示词、调 TopK，直到命中稳定

### 4.3 发布

右上角 **发布**：

- **Web App**：公开链接，可直接分享
- **嵌入网站**：iframe / script 代码贴到自己网站
- **API**：应用 → 「API 访问」→ 创建 API Key，供程序调用

## 五、实战二：工作流

**创建应用 → 工作流**。画布上从左到右连线。

常用节点：

- **开始**：定义输入变量
- **LLM**：调模型，可挂知识库
- **知识检索**：单独检索节点
- **条件分支**：if/else 分流
- **代码**：跑 Python/JS 处理数据
- **HTTP 请求**：调外部 API
- **变量聚合 / 迭代 / 循环**
- **结束**：定义输出

变量用 `{{#节点ID.变量名#}}` 引用。典型例子：客服工单 → LLM 判断类别 → 条件分支 → 不同处理 → 结束输出。画完点「运行」用测试数据调试。

## 六、Agent 与工具

选 **Agent** 类型应用，给它加工具：

- 内置工具：网页搜索、网页抓取、代码执行、时间等
- **自定义工具**：用 OpenAPI/Swagger 描述你的接口，导入即可
- **MCP**：接入 MCP Server 的工具
- **Dify Marketplace**：现成插件市场

Agent 会自主决定调哪个工具、调几次。适合开放式任务；流程固定的业务优先用工作流，更可控。

## 七、API 集成

应用 → **API 访问** → 创建 Key（形如 `app-xxxx`）。

```bash
curl -X POST 'http://localhost/v1/chat-messages' \
-H 'Authorization: Bearer app-xxxx' \
-H 'Content-Type: application/json' \
-d '{
  "inputs": {},
  "query": "你们的退款政策是什么？",
  "response_mode": "streaming",
  "conversation_id": "",
  "user": "user-123"
}'
```

主要接口：

- `POST /v1/chat-messages` —— 聊天助手 / Agent / Chatflow
- `POST /v1/completion-messages` —— 文本生成
- `POST /v1/workflows/run` —— 工作流
- `POST /v1/files/upload` —— 先传文件再引用

Python 示例：

```python
import requests

url = "http://localhost/v1/chat-messages"
headers = {"Authorization": "Bearer app-xxxx"}
payload = {
    "inputs": {},
    "query": "退货要多久到账？",
    "response_mode": "blocking",
    "conversation_id": "",
    "user": "user-123",
}
print(requests.post(url, json=payload, headers=headers).json())
```

`conversation_id` 传上一轮返回的值，就实现多轮对话；`response_mode=streaming` 走 SSE 流式输出。

## 八、运维与优化

- **日志与标注**：应用 → 日志，看真实对话、用户反馈，标注好/坏回答，反过来改提示词和知识库
- **提升 RAG 命中**：文档清洗去页眉页脚、合理分段、挂 Rerank、开 Query 改写、调 TopK 和阈值
- **控成本**：便宜模型做路由/分类，贵模型只做最终回答；Embedding 批量处理；开缓存
- **备份**：整个 `docker/volumes` 目录
- **升级**：拉新版本后对比 `.env.example` 与 `.env` 的新增变量；改了 `docker-compose.yaml` 要重新套用

## 九、常见问题

| 现象 | 排查 |
|---|---|
| 打开是 502/空白 | `docker compose ps` 看容器是否 healthy，看 nginx/api 日志 |
| 模型连接失败 | Base URL 在容器里能否访问；Linux 用宿主机 IP 不是 localhost |
| 文档上传失败 | storage 目录权限、插件是否启用、文件大小限制 |
| 检索答非所问 | 换 Embedding、调分段、加 Rerank、补文档 |
| 中文分段差 | 缩短分段长度、加大重叠、手动清理文档格式 |
| 想换向量库 | `docker/envs/vectorstores/` 下有 milvus/qdrant/pgvector 模板，复制去 `.example` 后重启 |

## 十、学习与落地路径

1. 云版注册，跑通「知识库问答」
2. 本地 Docker 部署，接自己的模型
3. 做一个真实场景的知识库客服（公司手册、产品文档）
4. 学工作流，把重复业务自动化
5. 用 API 接到自己的网站/小程序/企业微信
6. 对外交付：企业私有化部署 + 知识库 + 工作流，注意 license 合规
