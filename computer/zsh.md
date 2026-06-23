# QAQ
# zsh 哪个插件 可以使用 j 跳转到历史某个目录

在 Oh My Zsh 中，能够通过按 `j` 跳转到历史目录的插件是 **`autojump`**（需先安装 autojump 软件）。

- 启用方法：在 `~/.zshrc` 的 `plugins` 列表中加入 `autojump`，并确保已通过包管理器（如 `brew install autojump` 或 `apt install autojump`）安装 autojump。  
- 常用命令：`j <目录关键词>` 即可跳转。

如果你不想额外安装软件，Oh My Zsh 自带的 **`z`** 插件功能类似，但命令是 `z`。你可以通过别名 `alias j='z'` 实现同样的 `j` 快捷键效果。



