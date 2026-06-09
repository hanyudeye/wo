---
layout: default
toc: false
title: chrome
date:  2026-05-30T15:49:08+08:00
categories: ['']
draft: true
---

# chrome 浏览器开启 genimi

1. 找到这个文件：

C:\Users\你的用户名\AppData\Local\Google\Chrome\User Data\Local State

2. 备份

3. 找到这三个字段并修改：

"is_glic_eligible": true
"variations_country": "us"

// 注意这一项不是把值完全改成us，是把国家简称改成us
"variations_permanent_consistency_country": "us"
如果找不到就手动加进去，注意JSON格式别写错。

保存，关闭。

第五步：重启Chrome

重新打开浏览器，右上角应该就能看到Gemini图标了。

