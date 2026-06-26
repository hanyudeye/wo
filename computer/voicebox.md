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
