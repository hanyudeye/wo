# QUESTIONS

## tmux 如何开启鼠标控制


To enable mouse control in tmux, you can use the following commands:

1. Start tmux: `tmux`
2. Enable mouse mode: `Ctrl+B` then `m` (or `C-m`)
3. Confirm that mouse mode is enabled by typing `~` to see the current pane status

Now you can use your mouse to interact with tmux panes and windows.

Alternatively, you can set the `mouse-select-pane` option to `on` in your tmux configuration file (`~/.tmux.conf`) to enable mouse control by default:

```
set-option -g mouse-select-pane on
```

## tmux 打开的 ssh 掉线了，如何重新打开

这是 `tmux` 的核心设计功能。当 SSH 连接断开时，由于您的工作进程是在远程服务器上的 `tmux` 会话中运行的，这些进程会继续在后台运行（不会受到本地网络波动影响）。

您只需要重新通过 SSH 登录到服务器，然后**重新挂载 (reattach)** 到那个仍然存活的 `tmux` 会话即可。

---

### 🎣 重连步骤

1. **SSH 回去**
   首先使用您的用户名和密码或密钥，重新连接到远程服务器：
   ```bash
   ssh user@your_server_ip
   ```

2. **查看会话列表 (可选)**
   执行以下命令确认您上次的工作会话仍在运行：
   ```bash
   tmux ls
   ```
   这会列出所有活动的 `tmux` 会话名称（例如：`session1: 1 windows (created)`）。

3. **重新挂载**
   使用 `-t` 参数指定您的会话名称，或者直接使用 `attach` 命令如果只有一个活动会话的话。
   ```bash
   # 如果您知道会话名，推荐用这个：
   tmux attach -t session_name 

   # 如果是唯一一个会话，可以直接用：
   tmux a 
   ```

您的工作环境和所有窗口（Panes/Windows）都会恢复到断开连接前的状态。

## 安装插件 

1. 在 tmux 里按 <prefix> + r（即先按 Ctrl+b，松开后再按 r）
2. 观察底部状态栏，应该会显示 "Installing tpm and plugins..." 等提示
3. 安装完成后底栏会显示 "Done installing tpm and plugins..."

如果 <prefix> + r 没反应，也可以直接退出所有 tmux 会话后执行：
tmux kill-server && tmux


## tmux 如何保存打开的窗口状态


1. tmux 自带：没有原生保存功能，但可以用脚本保存布局：

tmux list-windows -a -F "#{window_index} #{pane_index} #{pane_current_command}"
配合 tmux new-session + tmux send-keys 手动恢复。

2. 插件（推荐）：tmux-resurrect (https://github.com/tmux-plugins/tmux-resurrect)
- 保存：prefix + Ctrl-s
- 恢复：prefix + Ctrl-r
- 保存内容包含窗口、面板、路径、运行程序等

配合 tmux-continuum (https://github.com/tmux-plugins/tmux-continuum) 可实现自动每隔 15 分钟保存 + 开机自动恢复。

## key short

C-b C-b     Send the prefix key
C-b C-o     Rotate through the panes
C-b C-z     Suspend the current client
C-b Space   Select next layout
C-b !       Break pane to a new window
C-b #       List all paste buffers
C-b $       Rename current session
C-b &       Kill current window
C-b '       Prompt for window index to select
C-b (       Switch to previous client
C-b )       Switch to next client
C-b ,       Rename current window
C-b .       Move the current window
C-b /       Describe key binding
C-b 0       Select window 0
C-b 1       Select window 1
C-b 2       Select window 2
C-b 3       Select window 3
C-b 4       Select window 4
C-b 5       Select window 5
C-b 6       Select window 6
C-b 7       Select window 7
C-b 8       Select window 8
C-b 9       Select window 9
C-b :       Prompt for a command
C-b ;       Move to the previously active pane
C-b =       Choose a paste buffer from a list
C-b ?       List key bindings
C-b C       Customize options
C-b D       Choose and detach a client from a list
C-b E       Spread panes out evenly
C-b M       Clear the marked pane
C-b [       Enter copy mode
C-b ]       Paste the most recent paste buffer
C-b d       Detach the current client
C-b f       Search for a pane
C-b i       Display window information
C-b o       Select the next pane
C-b q       Display pane numbers
C-b s       Choose a session from a list
C-b t       Show a clock
C-b w       Choose a window from a list
C-b x       Kill the active pane
