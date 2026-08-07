---
---

# 使用 wslu 连接器连接 windows

## 我在 wsl 终端中如何用 Windows软件打开图片


在 WSL 终端中，可以直接调用 Windows 可执行文件打开图片。最常用的方法：

```bash
explorer.exe 图片路径
```

例如：
```bash
explorer.exe /mnt/c/Users/你的用户名/Pictures/photo.jpg
```
这会用 Windows 默认图片查看器打开。

其他备选：
- `cmd.exe /c start 图片路径` （效果类似）
- 如果安装了 [wslu](https://github.com/wslutilities/wslu) 工具集，可用 `wslview 图片路径`

路径支持 WSL 格式（如 `/mnt/c/...`），Windows 会自动转换。

## wslview a.png (命令执行报错)
Parameter format not correct - ""


The error "Parameter format not correct - "" " typically occurs when `wslview` passes an empty or malformed path to the Windows shell.  

**Most likely cause:** `a.png` does not exist in the current WSL directory, or the path contains special characters.  

**Try these:**
1. Verify the file exists:  
   `ls -l a.png`
2. Convert the path explicitly:  
   `wslview "$(wslpath -w "$(realpath a.png)")"`  
   (This ensures a proper Windows absolute path.)
3. Alternatively, use `explorer.exe` directly:  
   `explorer.exe "$(wslpath -w a.png)"`

If the file is missing, `wslview` will still try to open it, causing the Windows error.

## link-hint-open-link-at-point 如何调用 windows 里面的浏览器打开链接

方案一：用 wslview（推荐）
``` elisp
(setq browse-url-browser-function 'browse-url-generic
      browse-url-generic-program "/usr/bin/wslview")
```
wslview 是 WSL 官方工具，会自动调用 Windows 默认浏览器，无需写死路径。

方案二：直调 Windows 浏览器 exe
``` elisp
(setq browse-url-browser-function 'browse-url-generic
      browse-url-generic-program "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe")
```

方案三：不改全局，只改 link-hint
如果你只想 link-hint 用 Windows 浏览器，其他保持默认：
``` elisp
(advice-add 'link-hint-open-link-at-point :around
            (lambda (orig-fn &rest args)
              (let ((browse-url-browser-function 'browse-url-generic)
                    (browse-url-generic-program "/usr/bin/wslview"))
                (apply orig-fn args))))
```
加完后重启 Emacs 或 eval-buffer 即可。
