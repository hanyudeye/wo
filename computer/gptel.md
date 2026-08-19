---
---

# gptel / llm-client 使用笔记

Spacemacs 中通过 `llm-client` layer 使用 gptel 与 DeepSeek 交互。

## 已启用配置

`~/.spacemacs` 的 `dotspacemacs-configuration-layers`:

```elisp
(llm-client :variables llm-client-enable-gptel t
            llm-client-enable-gptel-agent t
            llm-client-enable-ellama t)
```

## DeepSeek 后端配置

gptel 0.9.9+ 原生支持 DeepSeek，在 `dotspacemacs/user-config` 注册:

```elisp
(gptel-make-deepseek "DeepSeek" :stream t)
(setq gptel-model 'deepseek-v4-flash
      gptel-backend (gptel-get-backend "DeepSeek"))
```

> 注意：0.9.9.6-pre 起 `deepseek-chat` / `deepseek-reasoner` 已从默认模型列表移除，改用 `deepseek-v4-flash` / `deepseek-v4-pro`。旧模型可手动加回：
> `(push 'deepseek-chat (gptel-backend-models (gptel-get-backend "DeepSeek")))`

API key 放 `~/.authinfo`（推荐，`:key` 可省略）:

```
machine api.deepseek.com login apikey password sk-你的key
```

## 常用操作（Spacemacs 键位）

| 按键 | 命令 | 说明 |
|------|------|------|
| `SPC $ g g` | gptel | 新开对话 |
| `SPC $ g s` | gptel-send | 发送消息 |
| `SPC $ g m` | gptel-menu | 菜单：模型/后端/系统提示/token 用量 |
| `SPC $ g r` | gptel-rewrite | 重写/改写选中区域 |
| `SPC $ g c` | gptel-add | 把缓冲区/区域加入上下文 |
| `SPC $ g f` | gptel-add-file | 加入文件到上下文 |
| `SPC $ g a` | gptel-agent | gptel-agent 对话 |
| `SPC $ e` | ellama-transient-main-menu | ellama 菜单 |

## 翻译

### 方式一：ellama 一键翻译（最方便）

- 选中文本 → `SPC $ e` → **t** 翻译选中区域（**b** 翻译整个缓冲区）
- 目标语言由 `ellama-language` 决定

```elisp
(with-eval-after-load 'ellama
  (setq ellama-language "Chinese"
        ellama-provider (make-llm-deepseek :key "你的key"
                                           :chat-model "deepseek-v4-flash")))
```

### 方式二：gptel-rewrite

选中文字 → `SPC $ g r` → 输入"翻译成中文"。译文流式覆盖原文，可 diff/接受/拒绝。

### 方式三：gptel 预设（旧版模板已废弃）

```elisp
(gptel-make-preset '英译中
  :system "你是专业译者,将用户输入翻译成通顺的简体中文,只输出译文,不要解释。")
(gptel-make-preset '中译英
  :system "You are a professional translator. Translate the user's text into natural English. Output only the translation.")
```

用法：对话中输入 `@英译中` 应用预设，或菜单里选（新命令 `gptel-preset` 可应用/保存预设）。

## 高级功能

- **工具调用**：`gptel-make-tool` 定义 elisp 工具（`:name` `:function` `:description` `:args`），工具结果默认插入 buffer。可装 `gptel-agent`、`llm-tool-collection` 等现成集合
- **MCP 集成**：装 `mcp.el` 后需 `(require 'gptel-integrations)`，再用 `gptel-mcp-connect` 注册 MCP 工具
- **加上下文**：`SPC $ g c` 附上当前文件，模型基于整份文档回答；配置里可用 `gptel-context` 变量直接指定文件/buffer
- **多模态**：`gptel-track-media` 开启后，buffer 里的文件/图片链接会被标注并随请求发送
- **思考内容**：`gptel-include-reasoning` 默认 `ignore`（显示但不回传，省上下文），可改为包含或重定向到其他 buffer
- **保存会话**：对话可直接存成 Markdown/Org 文件，打开后启用 `gptel-mode` 继续

## 注意

- 需要 Transient 0.7.8+（内置包默认不更新，需设 `package-install-upgrade-built-in` 为 t）
- 系统提示变量为 `gptel-system-prompt`（旧 `gptel--system-message` 已废弃）
- `gptel-request` 已独立成库，可用 `:schema` 做 JSON 结构化输出（`gptel-send` 暂不支持）
- gptel 不自带工具/模型列表，无后端配置时 `gptel-send` 会自动现场创建 ChatGPT 后端

## 翻译提示词

你是一名专业英语翻译。

任务：
- 英译中
- 保留原文语气
- 给出自然中文表达
- 对难句分析语法
- 对专业词汇补充解释

输出格式：

原文：
...

翻译：
...

重点词汇：
...

语法解析：
...

https://www.chatgpt.com/?q={query}
