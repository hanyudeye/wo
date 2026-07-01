# Ubuntu 实战笔记

## 关机时显示 "libvirt-guests.sh can't connect to default, skipping"

关机时 `libvirtd` 已先于脚本被停止，导致连接失败。无害但烦人。

**解决办法：**

| 方案 | 命令 | 说明 |
|------|------|------|
| 直接屏蔽 | `sudo systemctl mask libvirt-guests.service` | 彻底禁用该脚本，重启生效 |
| 重启 libvirtd | `sudo systemctl restart libvirtd` | 偶尔触发的话先试试这个 |
| 查日志 | `journalctl -b -r \| grep libvirt-guests` | 定位具体原因 |

## 类 Listary 快捷搜索软件

- **ulauncher** — 支持自定义 web search 快捷键

## Wayland 下快捷键映射工具

- **Input Remapper** (`input-remapper-gtk`) — 有 GUI，Wayland 兼容
- **keyd** — 轻量配置驱动，无依赖
- **wtype** — 在自带的"自定义快捷键"里模拟按键，例：`wtype -k up`

## Input Remapper 有鼠标手势功能吗，我想让他像 wgestures 一样，可以设置 鼠标右键向上划可以作为复制功能，更好的使用鼠标的特性

没有同类软件，因为Wayland 协议限制获取鼠标轨迹


## Wayland 为什么限制鼠标手势

这是 Wayland 的**安全设计取舍**。

**X11 下：** 任何程序都可以读取全局鼠标位置和轨迹、监听所有窗口的输入事件、甚至向其他窗口发送输入。这带来了键盘记录器、鼠标记录器等安全问题——你输密码时，后台任何一个程序理论上都能读到。

**Wayland 的核心原则：** 每个程序只能看到自己的那扇窗户。鼠标事件被视作敏感输入，只发给当前焦点窗口，其他程序（包括手势工具）无权获取全局鼠标轨迹。

所以 Wayland 下做手势工具，要么靠桌面环境自己提供 API（如 KDE InputActions），要么通过 libei 协议获取权限（正在推进，还未广泛落地）。这是**隐私 vs 功能**的经典取舍，Wayland 选了前者。

## ubuntu 下游戏手柄映射管理软件

| 软件 | 说明 |
|------|------|
| **sc-controller** | Steam Controller 及其他手柄的键鼠映射，GUI 图形化，功能最强 |
| **jstest-gtk** | 测试手柄按键、校准轴 |
| **evdev-joystick** | 用于校准手柄（jscal） |
| **antimicroX** | 手柄按键 → 键盘/鼠标映射，适合无原生手柄支持的游戏 |
| **steam** | 自带 Controller Configurator，支持 Xbox/PS/NS 手柄全面映射 |
| **input-remapper** | 现代映射工具，GUI 直观，支持按键组合、鼠标模拟 |

**推荐：** 先用 `jstest-gtk` 确认手柄被识别，然后 `sc-controller`（Steam 系）或 `input-remapper`（通用映射）按需使用。
