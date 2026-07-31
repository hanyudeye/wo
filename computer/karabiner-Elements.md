
## 切换桌面：Ctrl+Cmd+L 代替 Ctrl+右箭头

macOS 原生只能用固定的 `Ctrl + ←/→` 切换左右桌面，无法改成其他组合。想用 `Ctrl + Cmd + L` 切到右边桌面，需要用 Karabiner-Elements 做按键映射。

### 配置

在 `~/.config/karabiner/assets/complex_modifications/` 下创建规则文件，然后在 Karabiner 的 **Complex Modifications → Add rule** 里启用。两条规则放进同一个 json 的 `rules` 数组：

```json
{
  "title": "Ctrl+Cmd+L/H 切换左右桌面",
  "rules": [
    {
      "description": "Ctrl+Cmd+L 切换右边桌面",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "key_code": "l",
            "modifiers": { "mandatory": ["left_control", "left_command"] }
          },
          "to": [
            { "key_code": "right_arrow", "modifiers": ["control"] }
          ]
        }
      ]
    },
    {
      "description": "Ctrl+Cmd+H 切换左边桌面",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "key_code": "h",
            "modifiers": { "mandatory": ["left_control", "left_command"] }
          },
          "to": [
            { "key_code": "left_arrow", "modifiers": ["control"] }
          ]
        }
      ]
    }
  ]
}
```

### 补充

- 如果只想固定跳到第 N 个桌面，无需 Karabiner：**系统设置 → 键盘 → 键盘快捷键 → 调度中心** 里给「切换到桌面 N」设 `Ctrl + Cmd + 数字` 即可
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
