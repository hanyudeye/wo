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
