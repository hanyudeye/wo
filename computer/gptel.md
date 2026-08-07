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

gptel 0.9.9+ 原生支持 DeepSeek,在 `dotspacemacs/user-config` 注册后端:

```elisp
(defun dotspacemacs/user-config ()
  ...
  ;; DeepSeek 后端,模型含 deepseek-reasoner / deepseek-chat / deepseek-v4-flash / deepseek-v4-pro
  (gptel-make-deepseek "DeepSeek"
    :stream t
    :key "你的 DeepSeek API Key")
  (setq gptel-model 'deepseek-reasoner
        gptel-backend (gptel-get-backend "DeepSeek")))
```

API key 也可放 `~/.authinfo`(推荐):

```
machine api.deepseek.com login apikey password sk-你的key
```

这样 `:key` 可省略,只写 `(gptel-make-deepseek "DeepSeek" :stream t)`。

## 常用操作（Spacemacs 键位）

| 按键 | 命令 | 说明 |
|------|------|------|
| `SPC $ g g` | gptel | 新开对话 |
| `SPC $ g s` | gptel-send | 发送消息 |
| `SPC $ g m` | gptel-menu | 打开 gptel 菜单 |
| `SPC $ g r` | gptel-rewrite | 重写/改写选中区域 |
| `SPC $ g c` | gptel-add | 把缓冲区加入上下文 |
| `SPC $ g f` | gptel-add-file | 加入文件到上下文 |
| `SPC $ g a` | gptel-agent | 开启 gptel-agent 对话 |
| `SPC $ e` | ellama-transient-main-menu | ellama 菜单 |

## 翻译（推荐用 ellama，无需模板）

你的 layer 已启用 `llm-client-enable-ellama`,ellama 内置翻译,不用配模板。

### 方式一：ellama 一键翻译（最方便）

- 选中要翻译的文本,按 `SPC $ e` 打开 ellama 菜单,按 **t** 进入翻译子菜单
  - **t** → 翻译选中区域/光标处单词
  - **b** → 翻译整个缓冲区
- 目标语言由 `ellama-language` 决定,默认为 `English`(英→中或中→英看方向)
- ellama 会弹窗让你选 provider(DeepSeek 需先配置)

ellama 用 DeepSeek 需在 `user-config` 设置 provider:

```elisp
;; ellama 依赖 llm.el,需先 require
(with-eval-after-load 'ellama
  (setq ellama-language "Chinese"
        ellama-provider (make-llm-deepseek :key "你的key"
                                           :chat-model "deepseek-chat")))
```

> `make-llm-deepseek` 来自 `llm-deepseek.el`,字段继承 `llm-openai-compatible`(`url` 默认 `https://api.deepseek.com`)。可选模型:`deepseek-chat`、`deepseek-reasoner`、`deepseek-v4-flash`。

### 方式二：gptel-rewrite 即时翻译

选中文字 → `SPC $ g r` → 输入"翻译成中文"回车。译文流式覆盖原文,可 diff/接受/拒绝。

### 方式三：gptel 预设（对应旧版模板）

gptel 0.9.9+ 里 `gptel-make-template` 已废弃,用 `gptel-make-preset`:

```elisp
(gptel-make-preset '英译中
  :system "你是专业译者,将用户输入翻译成通顺的简体中文,只输出译文,不要解释。")
(gptel-make-preset '中译英
  :system "You are a professional translator. Translate the user's text into natural English. Output only the translation.")
```

用法:对话中输入 `@英译中` 应用预设,或菜单里选。

## 其他实用功能

- **改写润色**:选中文本 `SPC $ g r`,输入"更口语化/更简洁/改写成商务语气"等
- **加上下文**:`SPC $ g c` 把当前文件内容附带到对话,模型能基于整份文档回答
- **代码审查**:gptel-agent(`SPC $ g a`)可拆解多步任务自动执行
- **保存会话**:gptel 对话可直接存成 Markdown/Org 文件,下次打开继续
- **gptel 菜单**:`SPC $ g m` 里可切换模型、后端、系统提示,检查 token 用量

## 注意

- gptel 0.9.9+ 系统提示变量为 `gptel-system-prompt`(旧 `gptel--system-message` 已废弃)
- 旧版教程里的 `gptel-make-template` 在新版本已不存在,用 `gptel-make-preset`
