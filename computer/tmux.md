# tmux（Oh my tmux!）配置笔记

基于 gpakosz/Oh my tmux!（`~/.tmux`），自定义一律改 `.tmux.conf.local`，不改主配置文件。
按 `<prefix> e`（`C-a e` 或 `C-b e`）打开本地配置文件。

## 已开启的实用配置

```tmux
# -- clipboard
# 复制模式下选中内容同时复制到系统剪贴板（Linux 需 xsel/xclip/wl-copy）
tmux_conf_copy_to_os_clipboard=true

# 终端编辑模式，使用 ctrl+a [ 进入（vim 风格）
set -g status-keys vi
set -g mode-keys vi

# 新 pane 保留当前路径（默认已开）
tmux_conf_new_pane_retain_current_path=true

# TPM 插件启动/重载时自动更新
tmux_conf_update_plugins_on_launch=true
tmux_conf_update_plugins_on_reload=true

# Alt+Up / Alt+Down 模拟 PageUp / PageDown（对所有 tmux 内程序生效）
bind -n M-Up send-keys PPage
bind -n M-Down send-keys NPage
```

## 值得开启的配置

### 推荐开启

```tmux
# 高亮当前 pane，多窗格时一眼看清焦点（.tmux.conf.local:133）
tmux_conf_theme_highlight_focused_pane=true

# 新窗口保留当前目录，与 pane 行为保持一致（:41）
tmux_conf_new_window_retain_current_path=true

# 加大历史回滚行数，默认 2000 太少（:404）
set -g history-limit 5000
```

### 按需开启

```tmux
# 新 session 也保留当前路径（:32）
tmux_conf_new_session_retain_current_path=true

# 新窗口/新 pane 自动重连 SSH，常切换远程服务器时很实用（:47、:59）
tmux_conf_new_window_reconnect_ssh=true
tmux_conf_new_pane_reconnect_ssh=true

# Powerline 风格分隔符，字体支持时解开注释（:244-247）
tmux_conf_theme_left_separator_main='\uE0B0'
tmux_conf_theme_left_separator_sub='\uE0B1'
tmux_conf_theme_right_separator_main='\uE0B2'
tmux_conf_theme_right_separator_sub='\uE0B3'
```

### 会话持久化插件（TPM）

```tmux
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'
```

- 安装插件 `<prefix> I`，更新 `<prefix> u`，卸载 `<prefix> M-u`
- 不要手动加 `set -g @plugin 'tmux-plugins/tpm'` 和 `run '~/.tmux/plugins/tpm/tpm'`

### 自定义状态栏变量

在 `.tmux.conf.local` 底部的 `# EOF`…`# "$@"` 之间定义 POSIX shell 函数，
即可在 `tmux_conf_theme_status_left/right` 里用 `#{变量名}` 调用，例如天气、公网 IP。

## 常用按键速查

- `<prefix> +` 最大化当前 pane 到新窗口，再按一次还原
- `<prefix> m` 开关鼠标模式
- `C-l` 同时清屏并清除 tmux 历史
- `<prefix> C-c` 新建会话，`<prefix> BTab` 回到上个会话
- `<prefix> h/j/k/l` Vim 方式切换 pane，`H/J/K/L` 调整大小
- `<prefix> -` / `<prefix> _` 垂直/水平分割
- `<prefix> Tab` 回到上个窗口，`<prefix> C-h/C-l` 左右切换窗口
- `<prefix> b` 列出粘贴缓冲区，`<prefix> p` 粘贴，`<prefix> P` 选择粘贴

## 注意

- 主配置文件 `.tmux.conf` 不要直接改，改动会被更新覆盖
- 若某条设置被 Oh my tmux! 覆盖，在该行末尾加 `#!important`
- 状态栏对 Unicode 9 宽度符号敏感，旧 glibc（< 2.26）下可能显示错位