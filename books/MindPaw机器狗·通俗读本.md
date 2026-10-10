# MindPaw 机器狗·通俗读本

> 一台约 50 元、能听会走有情绪、还能聊 AI 的桌面四足机器狗
> 改编自开源仓库 `ace-trump-tech/MindPaw`（v2.0），给零基础初学者看

来源仓库：https://github.com/ace-trump-tech/MindPaw
许可证：代码 MIT，硬件/3D 模型 CC BY-NC 4.0，文档 CC BY 4.0

---

## 一句话认识它

- MindPaw 是一只趴在桌面的小狗，用 4 个舵机当腿
- 大脑是一块 ESP8266（ESP12F 模块，约 5 元）
- 眼睛是 OV2640 摄像头，嘴是喇叭，脸是 OLED 小屏幕，耳朵是语音模块 HLK-V20
- 你可以：手机网页遥控它、对它说话、朝它挥手、跟它聊豆包大模型
- 它有情绪：理你多就开心，晾着它就无聊，撞墙会吓一跳
- v2.0 多了一个本事：把摄像头画面发给电脑网关，算出前方有没有障碍，还能在浏览器里看到稀疏点云

初学者记住两条路就行：

- **Demo 路**：复刻一只会动会叫的狗，不用学 Python、Docker
- **研究路**：再玩 `ai-infra` 网关，研究边缘计算、Agent 调度、3D 感知

两条路共用同一套硬件和固件，网关地址留空就是纯 Demo 模式。

---

## 第一章 硬件清单：50 元是怎么凑出来的

### 完整版（约 50 元，带摄像头）

- ESP12F 裸模块：约 5 元。别买 NodeMCU 开发板（约 15 元），贵 3 倍。先用 NodeMCU 验证环境，正式做时换裸模块
- SG90 舵机 x4：约 12 元。拼多多 4 个装最划算
- SSD1306 OLED 128x64 I2C：约 6 元。白色最便宜
- OV2640 摄像头裸板：约 15 元。别买 ArduCAM Mini（约 25 元），不要带 FIFO 的
- HLK-V20 语音模块：约 9 元。搜 SU-03T，是同一个东西，更便宜
- 8Ω 喇叭 + S8050 三极管 + 电阻：约 3 元
- PCB 打样：约 0 元。嘉立创每月有免费券
- 3D 打印：约 0 元。嘉立创新用户有免费券
- USB 供电：约 0 元。手机充电器 + MicroUSB 线

邮费另算约 8 元，一次买齐只付一次。

### 基础版（约 35 元）

- 去掉摄像头，其他全留：语音 + 网页遥控 + AI 对话 + 情绪全有
- 适合先入门再升级

### 软件和账号准备

- VSCode + PlatformIO 扩展：编译烧录用
- Python 3：图片转 OLED 表情用
- 嘉立创 EDA 专业版：看电路图用
- SU-03T 配置工具：给语音模块烧命令用
- 心知天气（可选）：显示天气，免费版每天 1000 次够用
- 火山引擎方舟（可选）：豆包 AI 对话，新用户有免费 Token

---

## 第二章 原理速通：不吓人的那部分

### 狗是怎么走的

- 舵机就是能转到指定角度的小马达，给它 PWM 信号，它就转到 0-180 度的某个位置
- 4 条腿交替摆动，看起来就在走。前进后退左转右转坐下趴下，都是 4 个角度随时间变化的剧本，写在 `motion_emotion.cpp` 里

### 三种线要分清

- I2C：两根线（SDA 数据 + SCL 时钟），OLED 用它。像两个人用两根绳子传纸条，慢但省线
- SPI：四根线（CS/SCK/MOSI/MISO），摄像头用它。快，适合传图片
- UART：两根线（TX 发 + RX 收），语音模块用它。像打电话，一来一回

### ESP8266 引脚为什么这么挤

- ESP8266 能用的脚太少，所以 MindPaw 让舵机和摄像头共用三根线，中间各串一个 1KΩ 电阻防打架
- 两条铁律：
  - GPIO15 必须用 10KΩ 电阻拉到 GND，不然开不了机，这是芯片硬件规定
  - 烧录时 GPIO0 要接地进下载模式，烧完断开再复位

### 完整接线一页纸

- Servo1 信号：GPIO14，Servo2：GPIO16，Servo3：GPIO12，Servo4：GPIO13。红线全接 5V，别接 3.3V
- OLED：GPIO4 当 SDA，GPIO5 当 SCL，各加 4.7KΩ 上拉到 3.3V
- OV2640：CS 接 GPIO15（加 10KΩ 下拉），SCK/MISO/MOSI 分别经 1KΩ 接 GPIO14/12/13
- HLK-V20：TX 接 GPIO0，RX 悬空，VCC 接 3.3V
- 喇叭：GPIO16 经 1KΩ 接 NPN 三极管基极，喇叭一头接 5V，一头接三极管 C 极，E 极接地
- GPIO16 只能二选一：要么接 Servo2，要么接喇叭。都想要就加一块 PCA9685（约 5 元），走 I2C 扩出 16 路 PWM，或者直接换 ESP32
- 按键：GPIO2 接按键到 GND。电池检测：分压后进 A0。串口 TX/RX 留给 USB-TTL 调试

---

## 第三章 复刻五步走

### 第一步：先让代码跑起来

1. 安装 VSCode，再在扩展商店装 PlatformIO
2. `git clone https://github.com/ace-trump-tech/MindPaw.git`，用 VSCode 打开 `MindPaw_main` 文件夹
3. `pio run` 编译，第一次要下载库，等 1-3 分钟看到 SUCCESS
4. `pio run -t uploadfs` 上传网页（11 个 HTML），首次必须做
5. GPIO0 接 GND 再上电进下载模式，`pio run -t upload` 烧固件，烧完断开 GPIO0，按 RST
6. 串口 115200 看到 `热点已启动` 就是成了

烧录报错对照：

- `Failed to connect`：没进下载模式，查 GPIO0 是否接地后重新上电
- `chip doesn't exist`：TX/RX 接反或没供 3.3V
- `Timed out`：降速，在 platformio.ini 加 `upload_speed = 115200`

### 第二步：PCB 和外壳

- 用嘉立创 EDA 专业版打开 `SCH&PCB/MindPaw_SCH&PCB.epro2`，导出 Gerber 下单，用免费券
- 把 `3Dmodel/body.stl bottom.stl foot.stl` 上传打样，选 PLA
- 不想打样也行：洞洞板手焊 + 纸板身体，照样跑

### 第三步：焊接组装

- 顺序：先焊电源测 3.3V/5V，再焊 ESP12F 烧固件验证，再逐个加 OLED、舵机、语音、摄像头、喇叭
- 底盘装 4 个舵机，身体合上，走线走空腔，脚装到舵机摇臂上调到 90 度
- 先 USB 供电调试，5V/2A 以上充电器最稳。4 个 SG90 全动峰值约 2.8A，普通走路约 500mA

### 第四步：配 API（可选）

- 天气：心知官网注册免费版，复制 Key，在 `http://192.168.4.1` 设置页填 Key + 城市拼音
- AI：火山方舟建推理接入点（推荐 Doubao-pro-32k 或 lite），复制 Endpoint ID + API Key，在 `http://192.168.4.1/aiconfig.html` 保存，再去 `aichat.html` 聊天

### 第五步：配语音模块

- USB-TTL 交叉连 HLK-V20（TX-RX，RX-TX），3.3V 供电
- 上位机波特率 9600，唤醒词如小狗小狗，加 22 条命令，输出设为 CMD1-CMD22 后烧录
- 插回狗身上，上电即用。距离 0.5-1 米最好

22 条命令速查：前进 CMD1，后退 CMD2，左转 CMD3，右转 CMD4，停下 CMD5，坐下 CMD6，趴下 CMD7，开心 CMD8，生气 CMD9，难受 CMD10，好奇 CMD11，喜欢 CMD12，睡觉 CMD13，自由 CMD14，抬左手 CMD15，抬右手 CMD16，时间 CMD17，天气 CMD18，标志 CMD19，你好 CMD20，再见 CMD21，CMD22 保留。

---

## 第四章 玩起来：5 分钟体验

1. 插 USB，OLED 亮 Logo，舵机回中，响开机音
2. 手机连 WiFi `MindPaw`，密码 `mindpaw1234`
3. 浏览器开 `http://192.168.4.1`，点前进看走路，点开心看表情，点坐下看姿态
4. 说你好前进开心试语音
5. 配好 Key 后去 aichat 聊天，狗会用动作 + 表情 + 旋律回你

网页有 11 个页面：首页 home，遥控 control，动作 motion，表情 expression，聊天 aichat，配置 aiconfig，网络 network，设置 setting，彩蛋 egg，点云 recon_view，入口 index。记住 control、aichat、aiconfig 三个就够。

串口也能玩：`front back left right sitdown lie dosleep kaixin shengqi nanshou haoqi xihuan shijian tianqi`，`ask 你好` 问 AI，`emotion` 看情绪，`gesture` 测一次手势。

---

## 第五章 它为什么有情绪

- 用的是 PAD 模型：P 开心不开心，A 兴奋平静，D 强势顺从，三个数定位心情
- 理你多 P 上升，晾着它 P 下降，撞墙 A  spike 进惊讶警觉
- `emotion_engine` 管心情，`motion_emotion` 管把心情翻译成动作表情声音，`multimodal_fusion` 管把语音手势网页 AI 融合成一件事
- OLED 有 7 种表情 + 天气 + 时间，喇叭有开机确认情绪共 10 种旋律

---

## 第六章 手势是怎么认出来的

- 摄像头抓一帧缩成 40x30 灰度图（1200 个数），喂给一个很小的 MLP 神经网络 `gesture_nn`
- 挥手握拳指点各对应一个动作，`tools/distill_gesture.py` 是训练脚本
- 光线暗就认不准，这是正常的，先保证脸亮

---

## 第七章 v2.0 感知层：让狗看见前方

### 为什么要加

- 1.0 的摄像头只认手势，不知道前面是墙还是空，不知道自己在哪
- 2.0 把图片推给 Edge 网关算深度和障碍，再传回一个 hazard 结果，思想参考 ABot-Recon 的 12 帧滑动 KV 缓存

### 链路长什么样

- OV2640 出 160x120 JPEG，每帧 POST 到网关 `ai-infra/recon`
- 网关跑 student 模型（没有权重就用 mock 先调通链路），维护 12 帧上下文，输出深度均值、最近距离、漂移
- 狗轮询 `/recon/hazard`，浏览器用 WebSocket 看点云

### 延迟多少

- 采集约 50ms + WiFi 30-80ms + 推理 mock 约 20ms / CPU 约 80-120ms + 回传 20-50ms
- mock/CPU/GPU 三档分别约 150ms、250ms、150ms，每秒约 4-7 帧。比传统 SLAM 秒级快很多，但别指望它像激光雷达

### 三档危险度

- 0 SAFE：正常走
- 1 CAUTION：警觉，优先稳住
- 2 STOP：小于约 18cm 直接停，表情切惊讶

### 开箱三步

1. `cd ai-infra && pip install -r requirements.txt && uvicorn recon.service:app --host 0.0.0.0 --port 8001`，或 `docker compose up -d` 同时起 8000 网关 + 8001 感知
2. 连狗热点，在 aiconfig.html 填 Recon 地址 `http://网关IP:8001`，帧率先设 5，3-8 之间调
3. 推狗向墙试 STOP，电脑开 `http://网关IP:8001/recon_view.html` 看点云

### 安全话必须说

- 没有超声波和 ToF，这是软避障，楼梯边千万别用
- 网关 1.5 秒没帧、网关挂了，狗不会自动停，必须人接管，1.0 功能不受影响
- mock 只能验证链路，不能真避障。真用要放 `weights/student.onnx`，`.env` 写 `RECON_WEIGHTS` 绝对路径，`curl /healthz` 看到 `using_mock:false` 才算成

### API 一览

- `GET /healthz` 看活着没，`POST /recon/frame` 传 JPEG（≤20KB），`GET /recon/hazard` 拿最新危险，`GET /recon/trajectory` 拿轨迹，`POST /recon/reset` 清缓存，`POST /recon/start|stop` 标记起止，`WS /recon/stream` 看直播
- hazard 长这样：`frame_id ts_ms nearest_m hazard pose_drift_cm depth_mean_m`

排障速查：一直 mock 查权重路径，查看器连不上查网关和 Token，慢降到 3FPS，全蓝 SAFE 是还在 mock，415 是没传 JPEG。

---

## 第八章 ai-infra 网关：可选，别有压力

- 初学者跳过完全不影响玩狗
- 它是个 OpenAI 兼容入口 `POST /v1/chat/completions`，管鉴权、超时、动作表情旋律 JSON 校验，支持豆包方舟、OpenAI 兼容、本地 Ollama、mock
- 三层思想：设备管急活（停走语音），网关管稳活（会话路由缓存），云管难活（闲聊共情）
- 启动：复制 `.env.example` 为 `.env`，填 `GATEWAY_TOKEN AI_PROVIDER` 和 Key，`pip install -r requirements.txt && uvicorn gateway.app:app --host 0.0.0.0 --port 8000`，或 `docker compose up --build -d`
- 没 Key 就把 `AI_PROVIDER=mock` 先调链路，再在 aiconfig.html 填 API Key 为 Token、Endpoint 为 mindpaw、网关地址为 `http://网关IP:8000/v1/chat/completions`

---

## 第九章 故障排查一页纸

- 不开机：查 3.3V/5V，查 GPIO15 下拉，查 GPIO0 是否还接地没松开
- 搜不到 MindPaw：ESP 没启动，看串口
- 打不开 192.168.4.1：确认连的是狗热点不是家里 WiFi
- 舵机不动：红线是否 5V 直供，充电器是否 2A 以上，信号线是否对
- OLED 不亮：I2C 上拉 4.7KΩ，地址 0x3C，接线 SDA/SCL 别反
- 语音没反应：单测模块串口有没有 CMD 输出，波特率 9600，距离近点
- AI 说未配置：Key 和 Endpoint 有空格没，实名了没，网关通不通
- 天气 Need NET：狗还没连外网，先在设置页配家里 WiFi
- 摄像头不行：GPIO15 下拉 + 共享线 1KΩ，光照够不够

---

## 第十章 进阶路线

- 腿不够稳：加 PCA9685，走 I2C，舵机全独立，控制更稳
- 脚不够多：换 ESP32，引脚多、内存大、有蓝牙，改 board 为 nodemcu-32s 再重排脚
- 想出门：加 2S 锂电 + A0 分压测电量，先 USB 调通再加电池
- 想改脸：看 `Docs/03_Image_Conversion.md`，BMP 转数组写进 `image.cpp`
- 想提 PR：先看 CONTRIBUTING，要能复现的日志和测量，AI 只能辅助不能代替硬件安全审查，改舵机供电引脚动作必须写断电措施和兼容说明

---

## 附录：文件去哪找

- 接线：`MindPaw_main/PIN_WIRING.md`
- 烧录：`Docs/04_Firmware_Flashing.md`
- 组装：`Docs/05_Assembly_Guide.md`
- 上手：`Docs/06_Quick_Start.md`
- API：`Docs/07_API_Guide.md`
- 给不懂技术的人：`Docs/08_Product_Manual.md`
- 感知：`Docs/09_Streaming_Recon.md` + `ai-infra/recon/README.md`
- 网关：`ai-infra/README.md` + `ai-infra/gateway/app.py`
- 硬件：`SCH&PCB/README.md` + `hardware-manifest.json`
- 固件入口：`MindPaw_main/src/main.cpp`，情绪：`emotion_engine.*`，动作：`motion_emotion.*`，语音：`hlkv20.*`，摄像头：`ov2640.*`，喇叭：`speaker.*`，手势：`gesture_nn.*`，融合：`multimodal_fusion.*`，AI：`doubao_agent.* doubao_config.h`，感知客户端：`streaming_recon.*`
