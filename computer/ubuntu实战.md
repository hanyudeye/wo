# Ubuntu 实战笔记

## 关机时 libvirt-guests.sh 报错

无害但烦人，解决：`sudo systemctl mask libvirt-guests.service`

## 快捷搜索

- **ulauncher** — 类 Listary，支持自定义 web search

## Wayland 按键映射

| 工具 | 特点 |
|------|------|
| Input Remapper | GUI，Wayland 兼容 |
| keyd | 轻量，配置驱动 |
| wtype | 模拟按键，如 `wtype -k up` |

## 鼠标手势

Wayland 下无同类软件。安全设计：每个程序只能看到自己的窗口，鼠标轨迹被视为敏感输入，其他程序无权获取。

## 游戏手柄

| 软件 | 用途 |
|------|------|
| jstest-gtk | 测试手柄识别 |
| sc-controller | Steam手柄映射 |
| antimicroX | 手柄→键鼠映射 |
| steam | 自带Controller Configurator |

推荐：先用 `jstest-gtk` 确认手柄被识别，再用 `sc-controller` 或 `input-remapper`。
