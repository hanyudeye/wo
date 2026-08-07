---
---
# Piper 剪贴板朗读器

监听系统剪贴板变化，自动朗读新复制的文本。

## 安装依赖

```bash
sudo apt install xsel alsa-utils
```

## 使用方法

### 基本用法
```bash
./piper-clipboard-monitor.sh
```

### 常用选项
```bash
# 设置检查间隔（默认1秒）
./piper-clipboard-monitor.sh -i 2

# 静默模式（不显示状态信息）
./piper-clipboard-monitor.sh -q

# 后台运行
./piper-clipboard-monitor.sh &

# 组合使用
./piper-clipboard-monitor.sh -i 0.5 -q &
```

### 停止监听
按 `Ctrl+C` 或查找进程并杀死：
```bash
pkill -f piper-clipboard-monitor
```

## 添加快捷命令

在 `~/.zshrc` 或 `~/.bashrc` 中添加：
```bash
alias piper-listen='~/soft/piper-clipboard-monitor.sh'
alias piper-stop='pkill -f piper-clipboard-monitor'
```

然后重新加载：
```bash
source ~/.zshrc
```

现在可以使用：
```bash
piper-listen      # 启动监听
piper-stop        # 停止监听
```

## 配置说明

- **模型路径**: `~/soft/piper-models/zh_CN-huayan-medium.onnx`
- **检查间隔**: 默认1秒，可通过 `-i` 参数调整
- **音频文件**: 临时文件自动清理

## 故障排除

1. **没有声音**:
   - 检查音量设置
   - 运行 `aplay ~/soft/test.wav` 测试音频

2. **剪贴板不工作**:
   - 确保安装了xsel: `sudo apt install xsel`
   - 测试: `echo "test" | xsel --clipboard && xsel --clipboard --output`

3. **Piper错误**:
   - 检查模型文件是否存在
   - 手动测试: `echo "测试" | piper --model ~/soft/piper-models/zh_CN-huayan-medium.onnx --output_file test.wav`

## 文件位置

- 主脚本: `~/soft/piper-clipboard-monitor.sh`
- 语音模型: `~/soft/piper-models/zh_CN-huayan-medium.onnx`
- Piper可执行文件: `~/.local/bin/piper`