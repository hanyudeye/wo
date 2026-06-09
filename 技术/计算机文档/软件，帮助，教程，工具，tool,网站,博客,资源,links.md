---
title: 软件，帮助，教程，工具，tool,网站,博客,资源
date:  2025-07-03T07:32:41+08:00
categories: ['']
draft: true
---

## 离线翻译

pip install argostranslate argostranslategui
argos-translate-gui

## 鼠标手势

https://github.com/yingDev/WGestures/releases

## 文件校验

### md5/SHA256

```powershell
Get-FileHash WeChatSetup.exe -Algorithm MD5
Get-FileHash WeChatSetup.exe -Algorithm SHA256
```

## 打开系统剪切板

```powershell
Win+v
Get-Clipboard
```

## tmux

命令:

select-layout even-horizontal 左右布局
select-layout even-vertical 上下布局

## 翻译 libretranslate

更新模块
libretranslate --update-models --load-only zh,en --host 0.0.0.0 --port 5005


