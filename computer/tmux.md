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
