# macOS

## iTerm2 弹出终端（Hotkey Window）

iTerm2 内置 Hotkey Window 功能，一键弹出/收起终端。

### 推荐快捷键

- `Option + Space`（Quake 风格，最常用）
- `Option + ` `` ``
- `Ctrl + ` `` ``
- `Cmd + ` `` ``

> `Option + Space` 最直观，注意不要和 Spotlight（`Cmd + Space`）冲突。

### 设置步骤

1. iTerm2 → Settings（`Cmd + ,`）
2. **Keys** → **Hotkey**
3. 勾选 **"Show/hide all windows with a system-wide hotkey"**
4. 点击 **"Create a Dedicated Hotkey Window"**，按你想设的快捷键
5. **Profiles** → **Window** 中可调：
   - **Style**: `Full Width`（占满屏幕宽度）
   - **Screen**: `Primary Screen`
   - **Transparency**: 透明度

### 建议

- **Window** 设置中勾选 **"Floating window"** 让热键窗口始终在最上面
- **Profiles** → **Window** → **Space** 选 **"All Spaces"**，所有桌面都能呼出
- 注意和 Raycast/Alfred 的快捷键不要冲突

## Karabiner-Elements — CapsLock 映射 Ctrl + 切换输入法

macOS 自带的 CapsLock → Ctrl 映射和输入法切换会冲突：按 Ctrl 组合键（如 `Ctrl+C`）时，macOS 先识别到 Ctrl 单按，触发输入法切换。

Karabiner-Elements 可以区分「轻按」和「长按」，解决这个冲突。

### 安装

```bash
brew install --cask karabiner-elements
```

或者去 https://karabiner-elements.pqrs.org/ 下载 `.dmg` 手动安装。

### 规则配置

在 `~/.config/karabiner/assets/complex_modifications/` 下创建规则文件：

```json
{
    "title": "CapsLock: 长按=Ctrl, 轻按=切换输入法",
    "rules": [
        {
            "description": "CapsLock held → left_control, CapsLock tapped → Ctrl+Space (切换输入源)",
            "manipulators": [
                {
                    "type": "basic",
                    "from": {
                        "key_code": "caps_lock",
                        "modifiers": { "optional": ["any"] }
                    },
                    "to": [
                        { "key_code": "left_control", "lazy": true }
                    ],
                    "to_if_alone": [
                        { "key_code": "spacebar", "modifiers": ["left_control"] }
                    ]
                }
            ]
        }
    ]
}
```

### 启用步骤

1. 打开 Karabiner-Elements → **Complex Modifications** → **Add rule** → 启用该规则
2. **系统设置 → 键盘 → 修饰键** → CapsLock 设为「无操作」（让 Karabiner 接管）
3. **系统设置 → 键盘 → 输入法** → 取消「使用 CapsLock 键切换中英文」

### 效果

- **轻按 CapsLock** → 切换输入法（发送 Ctrl+Space）
- **按住 CapsLock + 其他键** → 作为 Ctrl 修饰键（`Ctrl+C`、`Ctrl+A` 等正常工作）

> `to_if_alone` 中空格键的 key_code 是 `spacebar`（不是 `space`）。

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

| 快捷键 | 作用 |
|--------|------|
| `C-a \|` | 垂直分割 pane |
| `C-a -` | 水平分割 pane |
| `C-a h/j/k/l` | Vim 风格切换 pane |
| `C-a H/J/K/L` | 调整 pane 大小 |
| `C-a c` | 新建窗口 |
| `C-a d` | 分离会话（后台运行） |
| `C-a s` | 交互式选择会话 |
| `C-a z` | 放大/还原当前 pane |
| `C-a [` | 进入复制模式（Vim 键位） |
| `C-a r` | 重新加载配置 |
| `C-a ,` | 重命名当前窗口 |
| `C-a $` | 重命名当前会话 |

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
