# Voicebox 使用教程

**Voicebox** 是一款开源、本地运行的 AI 语音工作室（作者 Jamie Pine，也是 Spacedrive 的作者），可作为 ElevenLabs 的免费替代品。支持声音克隆、文本转语音、听写、多轨故事编辑等功能，所有数据本地处理，隐私安全。

- 官网: <https://voicebox.sh>
- GitHub: <https://github.com/jamiepine/voicebox>
- 文档: <https://docs.voicebox.sh>

## 安装

| 平台 | 下载 |
|------|------|
| macOS (Apple Silicon) | [Download DMG](https://voicebox.sh/download/mac-arm) |
| macOS (Intel) | [Download DMG](https://voicebox.sh/download/mac-intel) |
| Windows | [Download MSI](https://voicebox.sh/download/windows) |
| Linux / Docker | `docker compose up` |

首次启动会自动下载模型（约 3-5GB），耐心等待。

## 克隆声音

### 1. 创建语音档案 (Voice Profile)

1. 点击左侧 **Profiles** 标签
2. 点击 **+ New Profile**
3. 填写名称、选择语言
4. 提供声音样本（二选一）：
   - **上传音频** — 拖入 WAV/MP3/M4A 文件，推荐 10-30 秒清晰语音
   - **录音** — 点击 Record Sample，对着麦克风说 10-30 秒
5. 点击 **Create Profile**

### 2. 选择克隆引擎

Voicebox 内置多个 TTS 引擎，在 Profile 中可切换：

| 引擎 | 语言 | 特点 |
|------|------|------|
| **Qwen3-TTS 1.7B** | 10 种（含中英日韩） | 综合质量最佳，推荐首选 |
| **Qwen3-TTS 0.6B** | 10 种 | 生成更快，质量稍低 |
| **Chatterbox Multilingual** | 23 种 | 语言覆盖最广（阿拉伯语、印地语等） |
| **Chatterbox Turbo** | 仅英语 | 支持 `[laugh]` `[sigh]` 等情感标签 |
| **LuxTTS** | 仅英语 | 轻量，CPU 也能跑，48kHz 输出 |

### 3. 克隆技巧

- 音频样本 10-30 秒最佳，太短效果差
- 安静环境录音，避免背景噪声和回声
- 可添加多个样本（不同风格/情绪）提升质量
- 首次生成较慢（模型初始化），之后会快很多

## TTS 文本转语音

1. 点击左侧 **Generate** 标签
2. 从下拉菜单选择已创建的语音档案
3. 输入文本
4. 点击 **Generate**，等待几秒
5. 预览播放或下载音频文件

### 格式技巧

- 使用正确标点 `"你好！今天怎么样？"` 控制停顿节奏
- 全大写表示强调：`"这太 AMAZING 了！"`
- 长文本自动分段跨淡处理，无长度限制

### 引擎特色

- **Chatterbox Turbo** 支持情感标签：输入 `/` 弹出标签选择器，可插入 `[laugh]`、`[sigh]`、`[gasp]`、`[clear_throat]` 等
- 其他引擎会逐字读出标签文本，所以不要混用

## API 调用

Voicebox 在 `localhost:17493` 提供 REST API，可编程调用：

```bash
curl -X POST http://localhost:17493/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-tts-1.7b",
    "input": "你好，这是一段测试语音",
    "voice": "你的声音档案ID",
    "response_format": "wav"
  }' \
  --output output.wav
```

也支持 MCP Server，可供 Cursor、Claude Code 等 MCP 客户端调用。

## 更多功能

- **听写 (Dictation)** — 全局快捷键，说话自动转文字粘贴到当前应用
- **故事编辑器 (Stories)** — 多轨时间线，创建多人对话、播客
- **音效处理** — 变调、混响、延迟、压缩等后处理
- **预设声音** — 内置 50+ 预设语音，无需录音直接使用
- **远程模式** — 可在远程 GPU 服务器跑推理，本地连接使用

## 注意事项

- 声音克隆应获得被克隆人同意，遵守当地法律
- 所有数据在本地处理，不上传云端
- GPU（NVIDIA CUDA / Apple Metal）可加速 5-10 倍
- 模型默认下载到 `~/.voicebox/models/`

# whisper 安装使用教程

**OpenAI Whisper** 是 OpenAI 开源的通用语音识别模型，支持 100+ 种语言的语音转文字（ASR），也能做翻译成英文。本地运行，保护隐私。

- GitHub: <https://github.com/openai/whisper>
- 论文: <https://arxiv.org/abs/2212.04356>

## 安装

### 前置条件

- Python 3.9-3.12（3.13 暂不支持，PyTorch 兼容问题）
- ffmpeg（处理音频）
- 推荐 GPU：NVIDIA CUDA（Linux 可用 ROCm，macOS 用 Metal）

```bash
# 系统依赖：ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (choco)
choco install ffmpeg
```

### pip 安装

```bash
pip install -U openai-whisper
```

首次使用时自动下载模型。

### 从源码安装

```bash
pip install -U git+https://github.com/openai/whisper.git
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
```

### 使用 uv（更快）

```bash
uv pip install openai-whisper
```

### Docker

```bash
docker run --rm --gpus all \
  -v "$(pwd):/data" \
  whisper:latest \
  whisper /data/audio.mp3 --model medium --language zh
```

## 命令行使用

### 基本用法

```bash
# 转录音频
whisper audio.mp3

# 指定语言（中文），自动检测可能不准
whisper audio.mp3 --language zh

# 指定模型大小
whisper audio.mp3 --model medium

# 输出字幕文件（srt/vtt/tsv/txt/json）
whisper audio.mp3 --output_format srt

# 翻译成英文（translate 任务）
whisper audio.mp3 --task translate
```

### 模型选项

| 模型 | 参数量 | 速度 | 内存 | 推荐场景 |
|------|--------|------|------|----------|
| `tiny` | 39M | ~10x | ~1GB | 实时/低资源设备 |
| `base` | 74M | ~7x | ~1GB | 快速简单任务 |
| `small` | 244M | ~4x | ~2GB | 日常使用 |
| `medium` | 769M | ~2x | ~5GB | 高精度，推荐 |
| `large-v3` | 1550M | 1x | ~10GB | 最佳精度 |
| `large-v3-turbo` | 809M | ~4x | ~6GB | medium 速度 + large 精度 |

`large-v3-turbo` 是目前推荐首选（速度和精度的最佳平衡）。

### 常用参数

```bash
whisper input.mp3 \
  --model large-v3-turbo \
  --language zh \           # 指定语言
  --task transcribe \       # transcribe（转录）或 translate（翻译）
  --output_format srt \     # 输出格式：txt/vtt/srt/tsv/json/all
  --word_timestamps True \  # 输出逐词时间戳
  --condition_on_previous_text False \  # 避免重复/幻觉
  --verbose True \          # 打印详细信息
  --temperature 0.0 \       # 贪心解码，更确定的结果
  --device cuda \           # cuda / cpu / mps
  --compute_type float16    # 半精度加速（需 GPU）
```

### 批量处理

```bash
# 批处理多个音频
for f in *.mp3; do whisper "$f" --model large-v3-turbo --language zh --output_format srt; done
```

## Python API

### 基础转录

```python
import whisper

model = whisper.load_model("large-v3-turbo")  # 首次自动下载

result = model.transcribe("audio.mp3", language="zh")

print(result["text"])  # 完整文本

# 逐段文本和时间戳
for segment in result["segments"]:
    start = segment["start"]
    end = segment["end"]
    text = segment["text"]
    print(f"[{start:.2f}s -> {end:.2f}s] {text}")
```

### 翻译（中文语音 → 英文文字）

```python
result = model.transcribe("chinese_audio.mp3", task="translate")
print(result["text"])  # 英文输出
```

### 逐词时间戳

```python
result = model.transcribe(
    "audio.mp3",
    word_timestamps=True,
    language="zh"
)
for seg in result["segments"]:
    for word in seg["words"]:
        print(f"{word['word']}: {word['start']:.2f} - {word['end']:.2f}")
```

### 保存字幕文件

```python
result = model.transcribe("audio.mp3", language="zh")

# 保存为 SRT
with open("output.srt", "w", encoding="utf-8") as f:
    for i, seg in enumerate(result["segments"], 1):
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        f.write(f"{i}\n{start} --> {end}\n{seg['text']}\n\n")
```

### VAD（语音活动检测）提高准确率

配合 `silero-vad` 切分静音段落再逐段转录，可大幅减少幻觉和重复：

```bash
pip install silero-vad
```

```python
import torch
from silero_vad import load_silero_vad, get_speech_timestamps, read_audio
import whisper

model = whisper.load_model("large-v3-turbo")
vad_model = load_silero_vad()

wav = read_audio("audio.mp3")
speech_ts = get_speech_timestamps(wav, vad_model, return_seconds=True)

full_text = []
for seg in speech_ts:
    audio_chunk = wav[int(seg['start'] * 16000):int(seg['end'] * 16000)]
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        from scipy.io.wavfile import write
        write(f.name, 16000, audio_chunk)
        result = model.transcribe(f.name, language="zh")
        full_text.append(result["text"])

print(" ".join(full_text))
```

## 替代方案

### faster-whisper（推荐）

CTranslate2 重新实现，速度提升 4x，内存减半，精度几乎无损：

```bash
pip install faster-whisper
```

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.mp3", language="zh")

print(f"检测语言: {info.language} (概率 {info.language_probability:.2f})")

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### whisper.cpp

C/C++ 实现，可在 CPU/低配设备流畅运行，支持树莓派：

```bash
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make
# 下载模型
bash models/download-ggml-model.sh large-v3-turbo
./main -f input.mp3 -m models/ggml-large-v3-turbo.bin -l zh
```

### 在线 API（不本地运行）

```bash
# OpenAI API
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 \
  -F model=whisper-1 \
  -F language=zh

# Groq（免费，速度极快）
curl https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file=@audio.mp3 \
  -F model=whisper-large-v3-turbo \
  -F language=zh
```

## 技巧 & 常见问题

### 提高准确率

- **前处理降噪**: `ffmpeg -i input.mp3 -af afftdn=nf=-25 output.wav`
- **重采样 16kHz**: `ffmpeg -i input.mp3 -ar 16000 output.wav`
- **VAD 切分静音**（见上方 Python 示例）
- 长音频用 `--condition_on_previous_text False` 避免重复
- 如果背景有音乐，开启 `--suppress_tokens`（默认已启用）

### 中文特殊处理

- 中文说话速度较快，推荐 `--word_timestamps True` 对齐更准
- `--language zh` 必须指定，不指定可能误判为英语
- 中文数字、专有名词（英文混合）偶尔出错，需人工校对
- 混合中英文时，用 `--language zh` 效果最好

### 常见问题

| 问题 | 解决 |
|------|------|
| `ModuleNotFoundError: No module named 'torch'` | `pip install torch torchvision torchaudio` |
| CUDA 用不了 | 检查 `torch.cuda.is_available()`；重新装对应 CUDA 版的 PyTorch |
| 显存不足（OOM） | 换小模型（`small`/`medium`），或加 `--compute_type int8` |
| 中文输出全是拼音 | 忘了 `--language zh` |
| 重复/幻觉严重 | 加 `--condition_on_previous_text False` 或配合 VAD |
| ffmpeg 报错 | 确认 ffmpeg 已安装且在 PATH 中 |

### 在 WSL 中使用

```bash
# WSL 需要额外配置 CUDA（参考 nvidia 官方 WSL 文档）
# 音频输入：WSL 默认无麦克风直通，需用 Windows 端录音后传文件处理
# 或用 pwsh 调用 Windows 端的 Python
```

