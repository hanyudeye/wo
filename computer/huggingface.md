# HuggingFace 网络问题

## 连不上 / 下载模型慢

### 1. 用镜像站（推荐）

```bash
# Linux/macOS
export HF_ENDPOINT=https://hf-mirror.com

# Windows PowerShell
$env:HF_ENDPOINT = "https://hf-mirror.com"

# 或写入 profile 持久生效
echo 'export HF_ENDPOINT=https://hf-mirror.com' >> ~/.zshrc
```

设置后 `huggingface_hub` 库自动走镜像，代码不用改。

### 2. 浏览器下载 + 手动放缓存

浏览器能上的话去 hf-mirror.com 手动下载，放到：

- Linux: `~/.cache/huggingface/hub/`
- Windows: `%USERPROFILE%\.cache\huggingface\hub\`

### 3. 用 ModelScope 替代

国内平台 <https://modelscope.cn>，大部分模型都有，下载速度快。

### 4. 全局代理

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```
