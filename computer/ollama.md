# Ollama 学习路径

## 阶段 1：安装与基础运行

**目标**：本地安装 Ollama，下载并运行第一个模型

**任务**：
1. 下载安装 Ollama（`curl -fsSL https://ollama.com/install.sh | sh`）
2. `ollama pull llama3.2` 下载基础模型
3. `ollama run llama3.2` 进入交互模式，测试对话
4. `ollama list` 查看已下载模型
5. 非交互模式：`ollama run llama3.2 "用中文解释递归"` > output.txt

**验收**：
- 能列出模型及大小
- 能用一条命令获取回答并保存
- 理解 `pull`（下载）与 `run`（运行）区别

---

## 阶段 2：API 调用与 Python 集成

**目标**：通过 HTTP API 调用模型，编写对话脚本

**任务**：
1. 确认服务运行：`curl http://localhost:11434/api/tags`
2. 用 `curl` 测试 `/api/generate` 接口
3. 用 `curl` 测试 `/api/chat` 接口（带历史消息）
4. 编写 Python 脚本 `chat_bot.py`，调用 `/api/chat`，实现多轮对话

**API 格式**：
```python
# /api/chat - 多轮对话
import requests
messages = [{"role": "user", "content": "你好"}]
r = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2", "messages": messages, "stream": False
})
print(r.json()["message"]["content"])
```

**验收**：
- Python 脚本能保持上下文连续对话
- 理解 `/api/generate`（单次生成）与 `/api/chat`（多轮对话）区别

---

## 阶段 3：Modelfile 与自定义模型

**目标**：用 Modelfile 创建自定义模型（修改系统提示词、参数）

**任务**：
1. 创建 `Modelfile`：
```dockerfile
FROM llama3.2
SYSTEM "你是一个专业的 Linux 运维助手，回答简洁实用"
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
```
2. `ollama create my-assistant -f Modelfile`
3. `ollama run my-assistant` 测试自定义模型
4. 尝试不同参数组合（temperature、num_ctx 等）

**验收**：
- 自定义模型在 `ollama list` 中可见
- 系统提示词生效（回复风格符合设定）

---

## 阶段 4：模型选择与场景适配

**目标**：根据任务选择合适模型，理解模型规格

**常用模型**：
| 模型 | 参数量 | 适用场景 |
|------|--------|----------|
| llama3.2 | 1B/3B | 轻量对话、嵌入式 |
| llama3.1 | 8B/70B | 通用对话 |
| qwen2.5 | 7B/72B | 中文优化 |
| codellama | 7B/13B | 代码生成 |
| mistral | 7B | 指令跟随 |
| phi3 | 3.8B | 轻量推理 |
| gemma2 | 2B/9B | 多语言 |

**模型大小选择**：
- 8GB 内存 → 3B 以下
- 16GB 内存 → 7B-8B
- 32GB 内存 → 13B
- 64GB+ → 70B+

**验收**：
- 能根据硬件和任务选择合适模型
- 理解 `ollama show <model>` 查看模型信息

---

## 阶段 5：进阶技巧与生产实践

**目标**：掌握高级功能，具备实际部署能力

**任务**：
1. 多模型管理：同时运行多个模型，切换使用
2. 环境变量配置（`OLLAMA_HOST`、`OLLAMA_MODELS`）
3. Docker 部署：`docker run -d -v ollama:/root/.ollama -p 11434:11434 ollama/ollama`
4. 与 Open WebUI 集成：`docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway ghcr.io/open-webui/open-webui`
5. 流式输出处理（`stream: true`）
6. 嵌入模型（`nomic-embed-text`）用于 RAG

**验收**：
- 能用 Docker 部署 Ollama + WebUI
- 能处理流式响应
- 理解 Ollama 在本地 AI 应用中的定位
