---
layout: default
toc: false
title: chrome
date:  2026-05-30T15:49:08+08:00
categories: ['']
draft: true
---

# chrome 浏览器开启 gemini

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

## 安装应用 app（PWA）与专注

用 Chrome 的"安装应用"（PWA，独立窗口）比在标签页浏览更能保持专注：

- 窗口独立：不和其他标签页挤在一起，视觉干扰更少
- 减少切换诱惑：按 Cmd/Ctrl+Tab 或点标签时，不会无意跳进别的网站
- 空间更干净：PWA 窗口通常隐藏地址栏/书签栏，内容更纯粹（Notion、YouTube、Telegram 等）
- 任务感更强：独立窗口更像"一个应用"，心理上更容易进入单一任务状态

不过短期任务（几分钟查资料）没必要，多开窗口也占屏幕。

做法：重点应用（笔记、邮件、IM）用 PWA 常驻，临时浏览用标签页。

