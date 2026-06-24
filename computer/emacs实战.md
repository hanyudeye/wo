# QUESTIONS

## emacs 如何查看光标所在字符的信息

| 需求 | 操作 |
|------|------|
| 快速看编码、行列位置 | `C-x =` |
| 查生僻字/特殊符号完整 Unicode、字节编码 | `C-u C-x =` / `M-x describe-char` |
| Elisp 脚本获取字符编码数值 | `(following-char)` |
| 想自动显示 Unicode 字符名称 | `(setq what-cursor-show-names t)` |

## emacs helm find file 怎么有些文件没有显示，是新创建的，但就是没显示

1. 目录缓存未刷新 — 在 Helm find files 里按 C-c C-u 强制刷新当前目录列表。

或者使用 C-x C-f，应该是缓存更新问题

## markdown 友好显示

markdown-toggle-markup-hiding
markdown-toggle-url-hiding


## 使用 emacs 编辑 web-page textarea

添加包
edit-server


;; (server-start)

(use-package edit-server
  :ensure t
  :commands edit-server-start
  :init (if after-init-time
            (edit-server-start)
          (add-hook 'after-init-hook
                    #'(lambda() (edit-server-start))))
  :config (setq edit-server-new-frame-alist
                '((name . "Edit with Emacs FRAME")
                  (top . 200)
                  (left . 200)
                  (width . 80)
                  (height . 25)
                  (minibuffer . t)
                  (menu-bar-lines . t)
                  (window-system . x))))

(setq edit-server-new-frame-alist `((window-system . nil)))


修正
(use-package edit-server
  :ensure t
  :commands edit-server-start
  :init (if after-init-time
            (edit-server-start)
          (add-hook 'after-init-hook
                    #'(lambda() (edit-server-start))))
  :config (setq edit-server-new-frame-alist
                '((name . "Edit with Emacs FRAME")
                  (top . 200)
                  (left . 200)
                  (width . 80)
                  (height . 25)
                  (minibuffer . t)
                  (menu-bar-lines . t)
                  (window-system . nil))))

