
## 安全删除文件

brew install trash  或 sudo apt install trash-cli
alias rm='trash' 或  lias rm='trash-put'

``` sh
trash-put test.txt    # 移入回收站，也可以直接简写 trash test.txt
trash-list            # 列出回收站（带删除时间、原始路径）
trash-restore         # 交互式选择恢复文件
trash-empty           # 清空全部回收站
trash-rm test.txt     # 从回收站里永久删掉某一个
```

> 这个和桌面共用同一个回收站 `~/.local/share/Trash`

