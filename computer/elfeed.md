# elfeed — Emacs 里的 RSS 阅读器

## 思路

- 论坛/社交媒体大多有 RSS/Atom，没有的用 [RSSHub](https://rsshub.app) 兜底
- 一个 elfeed 聚合所有订阅，`M-x elfeed` 一键进入，不用装一堆专用客户端

## 配置模板（use-package）

```elisp
(use-package elfeed
  :ensure t
  :commands elfeed
  :bind (("C-x w" . elfeed)
         :map elfeed-search-mode-map
         ("q" . elfeed-search-quit-window)
         ("g" . elfeed-search-update)
         ("y" . elfeed-search-yank))
  :config
  ;; 订阅源：<url> <标题> <标签>
  (setq elfeed-feeds
        '(("https://rsshub.app/v2ex" v2ex)
          ("https://hnrss.org/frontpage" hacker-news)
          ("https://rsshub.app/bilibili/user/dynamic/xxx" bilibili)
          ("https://www.ruanyifeng.com/blog/atom.xml" 博客)
          ;; 添加你自己的源...
          ))

  ;; 未读条数显示在 mode-line
  (require 'elfeed-org))

;; 快捷键：elfeed-search 视图内
;;   g       刷新
;;   RET     打开条目
;;   b       在浏览器打开（见 emacs.md 的 eww 配置）
;;   r       标为已读
;;   u       标为未读
;;   y       复制链接
;;   s       按标题/内容搜索
;;   + / -   对条目打标签（tag）
;;   #       按标签过滤
;;   S       按日期排序
```

## 过滤标签

```elisp
;; 打开时只显示 v2ex 标签的条目
(elfeed-search-set-filter "@6-months-ago +v2ex")
```

## 常用标签习惯

- 每个源打一个标签：`+v2ex`、`+hn`、`+博客`
- 看完一个源按 `#` 输入标签过滤，全部读完再清空

## 没有 RSS 的网站

- 用 [RSSHub](https://rsshub.app) 官方实例，路由如 `/weibo/user/xxx`、`/twitter/user/xxx`
- 冷门路由可能失效，可自己部署 RSSHub 实例（Docker 一条命令）
- 自建实例：`docker run -p 1200:1200 diygod/rsshub`

## 其他终端/Emacs 方案速查

| 平台        | Emacs            | 终端 CLI            |
|-------------|------------------|---------------------|
| Reddit      | `rnews`          | `tuir`              |
| Hacker News | `hackernews.el`  | `haxor-news`        |
| Mastodon    | `mastodon.el`    | `toot`              |
| IRC         | `erc`（内置）    | `weechat` / `irssi` |
| 通用 RSS    | `elfeed`（推荐） | `newsboat`          |
