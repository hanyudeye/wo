# QUESTIONS

## emacs 如何查看光标所在字符的信息

| 需求 | 操作 |
|------|------|
| 快速看编码、行列位置 | `C-x =` |
| 查生僻字/特殊符号完整 Unicode、字节编码 | `C-u C-x =` / `M-x describe-char` |
| Elisp 脚本获取字符编码数值 | `(following-char)` |
| 想自动显示 Unicode 字符名称 | `(setq what-cursor-show-names t)` |
