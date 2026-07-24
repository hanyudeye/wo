# Emacs

## 快捷键速查

| 操作 | 快捷键 |
|------|--------|
| 打开文件 | `C-x C-f` |
| 保存 | `C-x C-s` |
| 另存为 | `C-x C-w` |
| 搜索 | `C-s` / `C-r` |
| 替换 | `M-%` |
| 撤销 | `C-/` |
| 复制行 | `C-a M-w` |
| 剪切行 | `C-a C-k` |
| 粘贴 | `C-y` |
| 分屏 | `C-x 2`（水平）/ `C-x 3`（垂直） |
| 切换窗口 | `C-x o` |
| 关闭窗口 | `C-x 0` |
| 查看字符信息 | `C-u C-x =` |

## 配置

### 自定义 init 目录

```sh
# Emacs 27+ 原生支持
emacs --init-directory ~/myconfig/emacs.d

# 调试模式
emacs --init-directory ~/myconfig/emacs.d --debug-init

# 不加载任何配置
emacs -q
```

### 常用启动参数

| 参数 | 作用 |
|------|------|
| `--init-directory DIR` | 指定配置目录（Emacs 27+） |
| `-q` | 不加载 init.el |
| `--debug-init` | init 报错时显示 backtrace |
| `-nw` | 终端模式 |
| `-l FILE` | 启动后加载指定文件 |
| `--daemon` | 启动守护进程 |

## 常见问题

### Helm 找不到新文件

目录缓存未刷新，按 `C-c C-u` 强制刷新。

### Markdown 友好显示

```elisp
M-x markdown-toggle-markup-hiding
M-x markdown-toggle-url-hiding
```

### 编辑网页 textarea

安装 `edit-server` 包，配置：

```elisp
(use-package edit-server
  :ensure t
  :commands edit-server-start
  :init (if after-init-time
            (edit-server-start)
          (add-hook 'after-init-hook
                    #'(lambda() (edit-server-start)))))
```

### 查看光标字符信息

| 需求 | 操作 |
|------|------|
| 快速看编码、行列位置 | `C-x =` |
| 查完整 Unicode、字节编码 | `C-u C-x =` |
| 自动显示字符名称 | `(setq what-cursor-show-names t)` |

## 扩展

### Org mode

- 大纲：`*` 标题，`TAB` 折叠
- TODO：`C-c C-t` 切换状态
- 时间戳：`C-c C-s` 开始，`C-c C-d` 截止
- 导出：`C-c C-e`

### Org Agenda（Spacemacs）

#### 配置

在 `dotspacemacs/user-config` 中：

```elisp
(setq org-agenda-files '("~/org/" "~/org/todo.org"))

(setq org-agenda-custom-commands
      '(("w" "Weekly Review"
         agenda ""
         ((org-agenda-span 'week)))))
```

#### 快捷键

| 按键 | 作用 |
|------|------|
| `SPC a o o` | 打开 Org Agenda 主视图 |
| `SPC a o a` | 当天 Agenda |

Agenda 视图内：

| 按键 | 作用 |
|------|------|
| `d` | 日视图 |
| `w` | 周视图 |
| `t` | 只显示 TODO |
| `T` | 按标签过滤 |
| `f` / `b` | 前/后一天 |
| `g r` | 刷新 |
| `q` | 退出 |
| `RET` | 跳转到源条目 |
| `B` | 按日期排序 |

#### Org 文件中标记时间

```org
* TODO 学习 Python
  SCHEDULED: <2026-07-25 周六 05:00>

* TODO AI项目
  DEADLINE: <2026-07-26 周日>
```

#### 时间统计（Clock）

Agenda 视图内：

| 按键 | 作用 |
|------|------|
| `tr` | Clock Report — 显示时钟汇总表 |
| `tl` | Log Mode — 显示已完成条目和时钟历史 |

在 org 文件中操作时钟：

| 按键 | 作用 |
|------|------|
| `SPC m C i` | 开始计时（clock-in） |
| `SPC m C o` | 停止计时（clock-out） |
| `SPC m C d` | 临时显示当前文件的时钟时间 |
| `SPC m C R` | 插入时钟报告表格 |

在 org 文件中手动记录：

```org
* TODO 学习 Python
  CLOCK: [2026-07-24 周四 05:00] → [2026-07-24 周四 06:00] => 1:00
```

插入 clocktable 汇总：

```org
#+BEGIN: clocktable :scope file :block today
#+END:
```

### Magit（Git）

| 操作 | 快捷键 |
|------|--------|
| 状态 | `C-x g` |
| 暂存文件 | `s` |
| 提交 | `c c` |
| 推送 | `P u` |
| 日志 | `l l` |
| 创建分支 | `b c` |

### ERC（IRC）

最大网络 Libera.Chat（~30,000人），启用：

```elisp
(erc :variables
     erc-server-list '(("irc.libera.chat"
                        :port "6697" :ssl t
                        :nick "昵称")))
```

密码放 `~/.authinfo.gpg`，启用后 `SPC a c i e` 启动。

### browse-url 使用 eww

全局使用 Emacs 内置浏览器：

```elisp
(setq browse-url-browser-function 'eww-browse-url)
```

仅 elfeed 文章用 eww（其他场景仍用外部浏览器）：

```elisp
(add-hook 'elfeed-show-mode-map
          (kbd "b") (lambda () (interactive)
                      (eww-browse-url (elfeed-entry-link elfeed-show-entry))))
```
