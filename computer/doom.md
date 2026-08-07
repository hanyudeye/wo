---
---
# Doom Emacs 基本用法

## 安装
```bash
git clone https://github.com/hlissner/doom-emacs ~/.emacs.d
~/.emacs.d/bin/doom install
```

## 核心命令 (`bin/doom`)

| 命令 | 用途 |
|------|------|
| `doom sync` | 同步配置（修改 `init.el` 或 `packages.el` 后运行） |
| `doom upgrade` | 升级 Doom 及所有包 |
| `doom doctor` | 诊断配置/系统问题 |
| `doom env` | 生成环境变量文件（macOS GUI 用户需要） |
| `doom purge` | 清理废弃包 |

## 配置目录 (`~/.doom.d/` 或 `~/.config/doom/`)

- **`init.el`** — `doom!` 块，控制启用哪些模块（约 160 个）
- **`config.el`** — 存放 99.99% 的个性化配置，在模块加载后执行
- **`packages.el`** — 声明要安装的包

## 模块与标志

```elisp
;; 启用/禁用模块，使用 +flag 启用可选特性
(doom! :completion
       (company +childframe)   ;; company 模块 + childframe 标志
       :lang
       python
       (org +jupyter))
```


**每次修改 `init.el` 后必须运行 `doom sync`。**

## 包管理

```elisp
;; 安装包（放入 packages.el）
(package! example)

;; 来自 GitHub 等外部源
(package! example :recipe (:host github :repo "user/repo"))

;; 禁用包
(package! irony :disable t)

;; 固定到特定提交
(package! evil :pin "e00626d9fd")
```

**不要在 packages.el 之外手动 `M-x package-install`，否则下次 `doom sync` 会被清理。**

## 配置包（在 config.el 中）

```elisp
(setq doom-font (font-spec :family "Fira Mono" :size 12))

(after! evil
  (setq evil-magic nil))

(add-hook! python-mode
  (setq python-shell-interpreter "bpython"))

(use-package! hl-todo
  :hook (prog-mode . hl-todo-mode)
  :config
  (setq hl-todo-highlight-punctuation ":"))
```

## 常用快捷键

- `SPC h d h` — 查看文档
- `SPC h d m` — 查看模块文档
- `SPC f` — 文件查找
- `SPC p` — 项目查找
- `SPC t` — 切换设置（行号、主题等）
- `doom/info` (或 `doom version`) — 查看版本信息

## 常用排查

- 配置不生效 → `doom sync`
- 找不到可执行文件 → `doom env` 重新生成环境变量
- 启动异常 → `doom doctor` 诊断
- 完全重置 → 删除 `~/.emacs.d/.local/straight` 再 `doom sync`
- 日志查看 → `C-h e` 查看 Emacs 消息日志
