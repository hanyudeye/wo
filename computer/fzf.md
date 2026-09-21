---
---
# fzf 教程

fzf（fuzzy finder，模糊查找器）是一个交互式命令行工具：读取输入流，让你用键盘模糊过滤、选中一行，选中的内容输出到 stdout，供其他命令继续使用。

检查是否安装：
```bash
fzf --version
# 0.67.0 (debian)
```

> 本文基于本机 Debian 包 0.67.0。

## 基本用法

```bash
fzf                    # 浏览当前目录及子目录的所有文件（交互式选择）
echo aaa bbb ccc | fzf # 过滤任意文本行
ls | fzf               # 过滤 ls 输出
```

交互界面操作：
| 按键 | 作用 |
|---|---|
| 输入关键字 | 模糊过滤（用空格分隔可多关键字） |
| `↑` `↓` / `Ctrl+K` `Ctrl+J` | 移动选择 |
| `Enter` | 确认选中 |
| `Esc` / `Ctrl+C` | 取消 |
| `Tab` | 多选标记（需 `-m`） |
| `Ctrl-R` | 切换拼音/正则过滤模式（0.67 版） |

## Shell 快捷键（默认已绑定）

| 快捷键 | 作用 |
|---|---|
| `Ctrl+T` | 选文件/目录，路径插入命令行 |
| `Ctrl+R` | 模糊搜索命令历史 |
| `Alt+C` | 快速跳转目录 |

## 常用搭配

```bash
vim $(fzf)                                  # 打开选中的文件
kill -9 $(ps aux | fzf | awk '{print $2}')  # 结束选中的进程
history | fzf                               # 搜索历史命令
git branch -a | fzf                         # 切换 git 分支
docker ps -a | fzf                          # 选容器
killall -9 $(docker ps -a | fzf | awk '{print $1}')
```

## 常用选项

```bash
fzf --height 40%                        # 以 40% 窗口高度展示，而非全屏
fzf --preview 'cat {}'                  # 右侧实时预览选中文件
fzf --preview 'bat --color=always {}'   # 用 bat 高亮预览（若已安装）
fzf -m                                  # 多选（Tab 标记，Enter 输出全部）
fzf --query "关键字"                     # 启动时自带关键字
fzf --reverse                           # 提示符在底部（默认集中于顶部）
fzf --layout=reverse                    # 同上，但方向键逻辑翻转
fzf --tac                               # 倒序显示（最新在最上）
```

## 配合 find / fd 使用

```bash
find . -type f | fzf                     # 只找文件
fd -t f | fzf --preview 'cat {}'         # fd 更快的文件搜索 + 预览
```

## 配置别名（~/.bashrc 或 ~/.zshrc）

```bash
alias fz="fzf --height 40% --preview 'cat {}'"
alias vf='vim $(fzf --preview "cat {}")'   # 选文件并 vim 打开
```

## 常见问题

**Q: 提示符位置不习惯？**
- 用 `--layout=reverse`，输入在底部。

**Q: fzf 快捷键没生效？**
- 需要在 shell 启动时加载补全：Bash 用户在 `~/.bashrc` 加 `eval "$(fzf --bash)"`，Zsh 用户加 `source <(fzf --zsh)`。