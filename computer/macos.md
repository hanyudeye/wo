# macOS

## iTerm2 弹出终端（Hotkey Window）

iTerm2 内置 Hotkey Window 功能，一键弹出/收起终端。

### 推荐快捷键

- `Option + Space`（Quake 风格，最常用）
- `Option + ` `` ``
- `Ctrl + ` `` ``
- `Cmd + ` `` ``

> `Option + Space` 最直观，注意不要和 Spotlight（`Cmd + Space`）冲突。

### 设置步骤

1. iTerm2 → Settings（`Cmd + ,`）
2. **Keys** → **Hotkey**
3. 勾选 **"Show/hide all windows with a system-wide hotkey"**
4. 点击 **"Create a Dedicated Hotkey Window"**，按你想设的快捷键
5. **Profiles** → **Window** 中可调：
   - **Style**: `Full Width`（占满屏幕宽度）
   - **Screen**: `Primary Screen`
   - **Transparency**: 透明度

### 建议

- **Window** 设置中勾选 **"Floating window"** 让热键窗口始终在最上面
- **Profiles** → **Window** → **Space** 选 **"All Spaces"**，所有桌面都能呼出
- 注意和 Raycast/Alfred 的快捷键不要冲突

## Karabiner-Elements — CapsLock 映射 Ctrl + 切换输入法

macOS 自带的 CapsLock → Ctrl 映射和输入法切换会冲突：按 Ctrl 组合键（如 `Ctrl+C`）时，macOS 先识别到 Ctrl 单按，触发输入法切换。

Karabiner-Elements 可以区分「轻按」和「长按」，解决这个冲突。

### 安装

```bash
brew install --cask karabiner-elements
```

或者去 https://karabiner-elements.pqrs.org/ 下载 `.dmg` 手动安装。

### 规则配置

在 `~/.config/karabiner/assets/complex_modifications/` 下创建规则文件：

```json
{
    "title": "CapsLock: 长按=Ctrl, 轻按=切换输入法",
    "rules": [
        {
            "description": "CapsLock held → left_control, CapsLock tapped → Ctrl+Space (切换输入源)",
            "manipulators": [
                {
                    "type": "basic",
                    "from": {
                        "key_code": "caps_lock",
                        "modifiers": { "optional": ["any"] }
                    },
                    "to": [
                        { "key_code": "left_control", "lazy": true }
                    ],
                    "to_if_alone": [
                        { "key_code": "spacebar", "modifiers": ["left_control"] }
                    ]
                }
            ]
        }
    ]
}
```

### 启用步骤

1. 打开 Karabiner-Elements → **Complex Modifications** → **Add rule** → 启用该规则
2. **系统设置 → 键盘 → 修饰键** → CapsLock 设为「无操作」（让 Karabiner 接管）
3. **系统设置 → 键盘 → 输入法** → 取消「使用 CapsLock 键切换中英文」

### 效果

- **轻按 CapsLock** → 切换输入法（发送 Ctrl+Space）
- **按住 CapsLock + 其他键** → 作为 Ctrl 修饰键（`Ctrl+C`、`Ctrl+A` 等正常工作）

> `to_if_alone` 中空格键的 key_code 是 `spacebar`（不是 `space`）。

## Karabiner-Elements — option+space 映射为 f1

### 规则配置

在 `~/.config/karabiner/assets/complex_modifications/` 下创建规则文件：

```json
{
    "title": "option+space → f1",
    "rules": [
        {
            "description": "option+space sends f1",
            "manipulators": [
                {
                    "type": "basic",
                    "from": {
                        "key_code": "spacebar",
                        "modifiers": {
                            "mandatory": ["option"]
                        }
                    },
                    "to": [
                        { "key_code": "f1" }
                    ]
                }
            ]
        }
    ]
}
```

### 启用步骤

1. 打开 Karabiner-Elements → **Complex Modifications** → **Add rule** → 启用该规则

> 如果想同时保留 option+space 的原功能，可以加 `to_if_alone` 发送 `spacebar`。
> 注意不要和 iTerm2 的 Hotkey Window（推荐也是 option+space）冲突。
