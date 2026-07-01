# QUESTIONS

## emacs 如何查看光标所在字符的信息

| 需求                                    | 操作                              |
|-----------------------------------------|-----------------------------------|
| 快速看编码、行列位置                    | `C-x =`                           |
| 查生僻字/特殊符号完整 Unicode、字节编码 | `C-u C-x =` / `M-x describe-char` |
| Elisp 脚本获取字符编码数值              | `(following-char)`                |
| 想自动显示 Unicode 字符名称             | `(setq what-cursor-show-names t)` |

## emacs helm find file 怎么有些文件没有显示，是新创建的，但就是没显示

1. 目录缓存未刷新 — 在 Helm find files 里按 C-c C-u 强制刷新当前目录列表。

或者使用 C-x C-f，应该是缓存更新问题

## markdown 友好显示

markdown-toggle-markup-hiding
markdown-toggle-url-hiding


## 使用 emacs 编辑 web-page textarea

> 不好用

添加包
edit-server


;; (server-start)

(use-package edit-server
  :ensure t
  :commands edit-server-start
  :init (if after-init-time
            (edit-server-start)
          (add-hook 'after-init-hook
                    #'(lambda() (edit-server-start))))
  :config (setq edit-server-new-frame-alist
                '((name . "Edit with Emacs FRAME")
                  (top . 200)
                  (left . 200)
                  (width . 80)
                  (height . 25)
                  (minibuffer . t)
                  (menu-bar-lines . t)
                  (window-system . x))))

(setq edit-server-new-frame-alist `((window-system . nil)))


修正
(use-package edit-server
  :ensure t
  :commands edit-server-start
  :init (if after-init-time
            (edit-server-start)
          (add-hook 'after-init-hook
                    #'(lambda() (edit-server-start))))
  :config (setq edit-server-new-frame-alist
                '((name . "Edit with Emacs FRAME")
                  (top . 200)
                  (left . 200)
                  (width . 80)
                  (height . 25)
                  (minibuffer . t)
                  (menu-bar-lines . t)
                  (window-system . nil))))

## emacs 配置自己的初始化 emacs.d目录，并设置打开参数

### 自定义 init 目录

| 方式                | 说明                                       | 示例                                        |
|---------------------|--------------------------------------------|---------------------------------------------|
| `--init-directory`  | Emacs 27+ 原生支持，指定 `~/.emacs.d` 位置 | `emacs --init-directory ~/myconfig/emacs.d` |
| `HOME` 环境变量     | 修改 HOME 目录，间接改变 `.emacs.d` 位置   | `HOME=/opt/myapp emacs`                     |
| `EMACSDIR` 环境变量 | 部分构建支持，指定配置目录                 | 不通用，优先用 `--init-directory`           |
| `-q -l`             | 不加载默认 init，手动指定文件              | `emacs -q -l ~/myconfig/init.el`            |

### 常用启动参数

| 参数 | 作用 |
|------|------|
| `--init-directory DIR` | 指定 `~/.emacs.d` 目录（Emacs 27+） |
| `-q` / `--no-init-file` | 不加载 init.el |
| `-u USER` / `--user USER` | 加载指定用户的 init 文件 |
| `--debug-init` | init 报错时显示完整 backtrace |
| `-nw` | 不在 X 下启动 GUI，纯终端 |
| `--no-window-system` | 同 `-nw` |
| `-l FILE` / `--load FILE` | 启动后加载指定 elisp 文件 |
| `--eval EXPR` | 启动后求值 elisp 表达式 |
| `--batch` | 批处理模式（不交互，用于脚本） |
| `--script FILE` | 以脚本模式运行 FILE |
| `--daemon[=NAME]` | 启动 Emacs 守护进程 |
| `--fg-daemon[=NAME]` | 前台运行守护进程 |

### 实用 combo

```sh
# 使用自定义配置目录，调试初始化问题
emacs --init-directory ~/playground/emacs.d --debug-init

# 不加载任何配置，测试基线行为
emacs -q

# 终端模式 + 自定义目录
emacs -nw --init-directory ~/custom.d/emacs.d

# 仅加载某个文件启动（极简调试）
emacs -q -l /tmp/test.el
```

### shell alias 示例

```sh
alias myemacs='emacs --init-directory ~/myconfig/emacs.d'
alias vanillamacs='emacs -q'
```

alias myemacs='emacs --init-directory ~/me/config/emacs/emacs.d'

## spacemacs 里有什么好玩的社交应用

### 哪个 IRC 网络人最多

| 排名 | 网络 | 日均在线 |
|------|------|----------|
| 1 | **Libera.Chat** | ~30,000 |
| 2 | OFTC | ~17,000 |
| 3 | Undernet | ~15,000 |
| 4 | hackint | ~10,000 |

**Libera.Chat** 是当前最大的 IRC 网络，也是绝大多数 FOSS 项目（包括 Emacs）的大本营。#emacs、#spacemacs 都在这里。`irc.libera.chat:6697`（SSL）。

### IRC — ERC 层（推荐）

Spacemacs 官方 IRC 层，基于 Emacs 内置 ERC，最成熟、功能最全。

| 特性 | 说明 |
|------|------|
| 频道 | `+chat/erc`（官方，非社区） |
| 高亮 | nick 高亮、图片内联、YouTube 缩略图 |
| 认证 | SASL 认证、authinfo.gpg 加密 |
| 通知 | DBUS 通知 |
| 其他 | 日志、社交图谱 |

**启用**（`dotspacemacs-configuration-layers` 中）：

```elisp
(erc :variables
     erc-server-list '(("irc.libera.chat"
                        :port "6697" :ssl t
                        :nick "你的昵称")))
```

密码放 `~/.authinfo.gpg`，不要明文。启用后 `SPC a c i e` 启动。

> 另一个官方层是 `rcirc`（`+chat/rcirc`），更轻量。Circe **没有** 官方层（issue #4231 从未合并），需要自己配 private layer。
