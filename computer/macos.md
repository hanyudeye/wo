# macOS

## tmux 配置与使用

### 安装

```bash
brew install tmux
```

### 推荐设置：改用 `Ctrl+A` 作为前缀

```tmux
# .tmux.conf
unbind C-b
set -g prefix C-a
bind C-a send-prefix
```

### 常用快捷键

| 快捷键        | 作用                     |
|---------------|--------------------------|
| `C-a \|`      | 垂直分割 pane            |
| `C-a -`       | 水平分割 pane            |
| `C-a h/j/k/l` | Vim 风格切换 pane        |
| `C-a H/J/K/L` | 调整 pane 大小           |
| `C-a c`       | 新建窗口                 |
| `C-a d`       | 分离会话（后台运行）     |
| `C-a s`       | 交互式选择会话           |
| `C-a z`       | 放大/还原当前 pane       |
| `C-a [`       | 进入复制模式（Vim 键位） |
| `C-a r`       | 重新加载配置             |
| `C-a ,`       | 重命名当前窗口           |
| `C-a $`       | 重命名当前会话           |

### 会话管理

```bash
tmux                        # 新建匿名会话
tmux new -s dev             # 新建名为 dev 的会话
tmux ls                     # 列出所有会话
tmux attach -t dev          # 附加到 dev 会话
tmux attach                 # 附加到上一个会话
tmux kill-session -t dev    # 杀死 dev 会话
```

### 推荐插件（TPM）

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

在 `.tmux.conf` 中添加：

```tmux
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-yank'          # 系统剪贴板集成
set -g @plugin 'tmux-plugins/tmux-resurrect'     # 会话保存/恢复
set -g @plugin 'tmux-plugins/tmux-continuum'     # 每15分钟自动保存
set -g @plugin 'christoomey/vim-tmux-navigator'  # 无缝导航 nvim pane
set -g @plugin 'tmux-plugins/tmux-cpu'           # CPU 监控
set -g @plugin 'tmux-plugins/tmux-battery'       # 电池状态

run '~/.tmux/plugins/tpm/tpm'
```

在 tmux 内按 `C-a I` 安装插件。

### macOS 专用优化

```tmux
set -g default-terminal "screen-256color"
set -as terminal-overrides ",*:Tc"       # 开启真彩色
set -g escape-time 10                     # 响应更快
set -g history-limit 50000                # 增大滚动缓冲区
set -g mouse on                            # 启用鼠标支持
set -g set-clipboard on                    # 系统剪贴板
```

### 实用别名

```bash
alias ta='tmux attach'
alias tls='tmux list-sessions'
alias tns='tmux new-session -s'
alias tks='tmux kill-session -t'
```

### 开机自启 tmux（在 .zshrc 中添加）

```bash
# 如果不在 tmux 中，自动附加或创建会话
if [[ -z "$TMUX" ]] && [[ -z "$NVIM" ]]; then
  if tmux has-session 2>/dev/null; then
    tmux attach
  else
    tmux new-session -s main
  fi
fi
```

### 进阶工具

- **[sesh](https://github.com/joshmedeski/sesh)** — 智能 tmux 会话管理器，按项目自动创建布局
- **[devmux](https://github.com/arach/devmux)** — 声明式 tmux 会话配置，有 macOS 菜单栏 App
- **[tmuxinator](https://github.com/tmuxinator/tmuxinator)** — 用 YAML 文件定义项目 tmux 布局

