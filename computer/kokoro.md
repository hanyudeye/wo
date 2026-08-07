---
---
# Kokoro TTS 中文语音合成

比Piper更自然的中文语音合成引擎。

## 安装依赖

```bash
pip install --user --break-system-packages kokoro-onnx soundfile "misaki[zh]"
```

## 模型文件

位置：`~/soft/kokoro-models/`

- `kokoro-v1.1-zh.onnx` (328MB) - 主模型
- `voices-v1.1-zh.bin` (52MB) - 语音数据

## 使用方法

### 基本用法
```bash
~/soft/kokoro-say.sh "要朗读的文字" output.wav
aplay output.wav
```

### 指定语音
```bash
# 女声（默认）
~/soft/kokoro-say.sh "你好世界" output.wav zf_001

# 男声
~/soft/kokoro-say.sh "你好世界" output.wav zm_001
```

### Python直接调用
```python
import soundfile as sf
from kokoro_onnx import Kokoro
from misaki import zh

g2p = zh.ZHG2P()
kokoro = Kokoro("kokoro-v1.1-zh.onnx", "voices-v1.1-zh.bin")

text = "你好世界"
phonemes, _ = g2p(text)
samples, sample_rate = kokoro.create(phonemes, voice="zf_001", speed=1.0, is_phonemes=True)
sf.write("output.wav", samples, sample_rate)
```

## 添加快捷命令

在 `~/.zshrc` 中添加：
```bash
alias kokoro-say='~/soft/kokoro-say.sh'
```

然后：
```bash
source ~/.zshrc
kokoro-say "你好世界" output.wav
```

## 可用语音

| 语音ID | 性别 | 说明 |
|--------|------|------|
| zf_001 | 女声 | 默认，清晰自然 |
| zm_001 | 男声 | 低沉稳重 |

## 文件位置

- 便捷脚本: `~/soft/kokoro-say.sh`
- Python脚本: `~/soft/kokoro-models/kokoro-say.py`
- 模型目录: `~/soft/kokoro-models/`

## 故障排除

1. **缺少espeak-ng**:
   ```bash
   sudo apt install espeak-ng
   ```

2. **模型下载慢**: 
   模型文件从GitHub下载，首次使用需下载380MB

3. **音素转换错误**:
   确保安装了 `misaki[zh]`：`pip install --user --break-system-packages "misaki[zh]"`

## 对比 Piper

| 特性 | Piper | Kokoro |
|------|-------|--------|
| 模型大小 | 61MB | 380MB |
| 音质 | 好 | 更自然 |
| 速度 | 快 | 稍慢 |
| 中文支持 | 基础 | 更好 |