---
---
# macOS

## 关闭开机自启软件

### 图形界面（macOS Sonoma 及之后）

1. 打开「系统设置」→「通用」→「登录项与扩展」
2. 「登录时打开」标签页：选中要移除的 App，点 `-` 或右键移除
3. 「允许在后台」标签页：关闭后台常驻 App（如微信、迅雷）的开关

macOS Ventura 及更早：系统偏好设置 → 用户与群组 → 登录项，选中后点 `-` 移除。

### 命令行

```bash
# 查看用户级 LaunchAgent
ls ~/Library/LaunchAgents
# 查看系统级 LaunchAgent / LaunchDaemon
ls /Library/LaunchAgents /Library/LaunchDaemons
# 移除自启（以某个 plist 为例）
launchctl unload ~/Library/LaunchAgents/com.example.foo.plist
rm ~/Library/LaunchAgents/com.example.foo.plist
```

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

## macbook 如何把某个窗口投屏到平板进行浏览

分两种情况：

### 1. 平板是 iPad（推荐用 Sidecar）
macOS 10.15+ 自带“随航”，把 iPad 变成 Mac 的第二块显示屏，可以把某个窗口直接拖过去浏览：

- Mac 和 iPad 登录同一个 Apple ID，打开 Wi‑Fi/蓝牙（也可用数据线连接）。
- 在 Mac：菜单栏点 **AirPlay 图标** → 选你的 iPad；或去 **系统设置 → 显示器 → 添加显示器**。
- iPad 显示桌面后，把要浏览的窗口从 Mac 屏幕拖到 iPad 上即可。

### 2. 平板是 Android 或任意设备
用 **Deskreen**（免费开源）：
- Mac 安装 Deskreen，平板浏览器打开电脑上显示的网址/二维码。
- 在 Deskreen 里选择 **Share a Window**（只共享某个窗口），然后选你想投射的 Mac 窗口。
- 平板浏览器里就能看到该窗口内容，适合单独浏览。

其它工具：**Spacedesk**（把平板变扩展屏）、**Duet Display**（有线/无线扩展屏），操作类似。

