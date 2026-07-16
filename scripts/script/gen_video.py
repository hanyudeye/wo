"""将 PPT 转为带 AI 人物口播的短视频"""
import asyncio, json, math, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ─── config ───
OUT = "/home/wuming/me/wo/startup/青野食研所-团餐方案-短视频"
os.makedirs(OUT, exist_ok=True)

# colors
GREEN = (0x7B, 0xA0, 0x5B)
CREAM = (0xF5, 0xF0, 0xE8)
WHITE = (0xFF, 0xFF, 0xFF)
DARK = (0x3D, 0x3D, 0x3D)
LGREEN = (0xE8, 0xF0, 0xE0)
GRAY = (0x88, 0x88, 0x88)
MID_G = (0x9B, 0xBD, 0x7A)
W, H = 1920, 1080

# font
FONT_REG = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 32)
FONT_TITLE = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 64)
FONT_SM = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 26)
FONT_LG = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 48)
FONT_XL = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 80)

def center_x(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return (W - (bbox[2] - bbox[0])) // 2

def rr(draw, xy, r, fill, outline=None):
    """rounded rect"""
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline)

# ─── slide renders ───

def slide_cover():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    # left green block
    draw.rectangle([0, 0, 830, H], fill=GREEN)
    # title
    for txt, y, sz in [("青野食研所", 240, 80), ("QINGYE FOOD LAB", 370, 32),
                         ("企业团餐合作方案", 480, 56)]:
        draw.text((center_x(draw, txt, FONT_XL if sz == 80 else FONT_LG if sz==56 else FONT_TITLE), y),
                  txt, fill=WHITE if "青" in txt or "企业" in txt else (0xCD,0xE0,0xC0),
                  font=FONT_XL if sz==80 else FONT_LG if sz==56 else FONT_TITLE)
    # right side
    draw.text((center_x(draw, "健康 · 新鲜 · 便捷", FONT_LG), 500),
              "健康 · 新鲜 · 便捷", fill=GREEN, font=FONT_LG)
    draw.text((center_x(draw, "为您的团队提供高品质午餐配送服务", FONT_REG), 580),
              "为您的团队提供高品质午餐配送服务", fill=DARK, font=FONT_REG)
    draw.text((center_x(draw, "让每一位员工吃好，工作更好", FONT_REG), 630),
              "让每一位员工吃好，工作更好", fill=DARK, font=FONT_REG)
    return img

def slide_about():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 20, H], fill=GREEN)
    draw.text((60, 40), "关于青野", fill=GREEN, font=FONT_XL)
    draw.text((60, 120), "ABOUT QINGYE", fill=GRAY, font=FONT_SM)
    texts = [
        "青野食研所成立于 2023 年，专注于健康轻食的研发与配送。",
        "核心团队来自餐饮与营养学背景，坚持「食材干净、调味克制、出品稳定」。",
        "",
        "[位置] CBD 核心商圈，覆盖 3 公里半径即时配送",
        "[产能] 日均产能 500+ 份，可承接 50-200 人规模团餐",
        "[口碑] 已服务 30+ 家企业，好评率 98%",
    ]
    y = 180
    for t in texts:
        draw.text((60, y), t, fill=DARK, font=FONT_REG)
        y += 48
    # right card
    rr(draw, (960, 140, 1860, 860), 20, LGREEN)
    draw.text((990, 170), "我们的优势", fill=GREEN, font=FONT_LG)
    items = [
        "新鲜现做  — 每日采购，当天制作",
        "准时送达  — 11:30 前到，不误午休",
        "菜单轮换  — 每周 5 套新菜单",
        "企业专享价 — 比单点低 20-30%",
        "环保包装  — 可降解餐盒 + 保温袋",
    ]
    y = 250
    for it in items:
        draw.text((990, y), it, fill=DARK, font=FONT_REG)
        y += 100
    return img

def slide_plans():
    """套餐对比 - 三栏"""
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 20, H], fill=GREEN)
    draw.text((60, 40), "包月套餐对比", fill=GREEN, font=FONT_XL)
    draw.text((60, 120), "MEAL PLANS", fill=GRAY, font=FONT_SM)
    plans = [
        ("轻享版", "¥28/餐", ["主食（三选一）","饮品 1 份"], False),
        ("标准版 ★", "¥38/餐", ["主食+沙拉（各选一）","饮品 1 份","甜品/水果 1 份"], True),
        ("尊享版", "¥48/餐", ["主食+沙拉+小吃","饮品+甜品+水果","月度健康报告"], False),
    ]
    for i, (name, price, feats, hot) in enumerate(plans):
        x = 120 + i * 600
        rr(draw, (x, 200, x+540, 920), 16, LGREEN)
        draw.rectangle([x, 200, x+540, 340], fill=GREEN)
        draw.text((center_x(draw, name, FONT_LG), 220), name, fill=WHITE, font=FONT_LG)
        draw.text((center_x(draw, price, FONT_XL), 270), price, fill=WHITE, font=FONT_XL)
        y = 380
        for f in feats:
            draw.text((x+30, y), f"✓  {f}", fill=DARK, font=FONT_REG)
            y += 70
        if hot:
            draw.text((center_x(draw, "👍 推荐选择", FONT_REG), 820),
                      "👍 推荐选择", fill=GREEN, font=FONT_LG)
    return img

def slide_menu():
    """本周菜单"""
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 20, H], fill=GREEN)
    draw.text((60, 40), "本周菜单示例", fill=GREEN, font=FONT_XL)
    draw.text((60, 120), "SAMPLE MENU", fill=GRAY, font=FONT_SM)
    days = ["周一","周二","周三","周四","周五"]
    menus = [
        ["烤鸡胸沙拉+南瓜浓汤","金枪鱼波奇饭+抹茶拿铁","凯撒沙拉+柠檬水"],
        ["照烧鸡腿三明治+水果杯","牛油果拌饭+味噌汤","地中海沙拉+气泡水"],
        ["烟熏三文鱼波奇饭","黑椒牛肉卷饼+蔬菜杯","泰式虾仁沙拉+椰子水"],
        ["日式鸡排饭+泡菜","吞拿鱼三明治+酸奶","考伯沙拉+蜂蜜柠檬茶"],
        ["香草鸡胸全麦卷","韩式拌饭+海带汤","鲜虾牛油果沙拉+豆浆"],
    ]
    for i, day in enumerate(days):
        x = 50 + i * 370
        rr(draw, (x, 180, x+350, 920), 12, LGREEN)
        draw.rectangle([x, 180, x+350, 250], fill=GREEN)
        draw.text((center_x(draw, day, FONT_LG), 195), day, fill=WHITE, font=FONT_LG)
        y = 290
        for m in menus[i]:
            draw.text((x+20, y), m, fill=DARK, font=FONT_SM)
            y += 110
    return img

def slide_pricing():
    """价格方案 - 表格"""
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 20, H], fill=GREEN)
    draw.text((60, 40), "价格方案", fill=GREEN, font=FONT_XL)
    draw.text((60, 120), "PRICING", fill=GRAY, font=FONT_SM)
    rows = [
        ("试吃体验", "前 3 天", "免费", "让团队先体验再决定"),
        ("月度合作", "20 工作日", "¥28-48/餐", "月结开票"),
        ("季度合作", "60 工作日", "¥25-43/餐", "享 9 折优惠"),
        ("年度合作", "240 工作日", "¥23-40/餐", "享 85 折+专属定制"),
    ]
    cols_w = [300, 280, 300, 380]
    x0, y0 = 120, 220
    # header
    hdr = ["方案", "周期", "单价", "说明"]
    x = x0
    for j, h in enumerate(hdr):
        draw.rectangle([x, y0, x+cols_w[j], y0+70], fill=GREEN)
        draw.text((center_x(draw, h, FONT_REG) if j==0 else x+15, y0+15),
                  h, fill=WHITE, font=FONT_REG)
        x += cols_w[j]
    for i, row in enumerate(rows):
        y = y0 + 70 + i * 80
        bg = LGREEN if i % 2 == 0 else WHITE
        x = x0
        for j, val in enumerate(row):
            draw.rectangle([x, y, x+cols_w[j], y+80], fill=bg)
            draw.text((x+20, y+20), val, fill=DARK, font=FONT_REG)
            x += cols_w[j]
    draw.text((60, 920), "* 以上不含税，餐费月结，可开增值税普通发票", fill=GRAY, font=FONT_SM)
    return img

def slide_contact():
    """尾页"""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 830, H], fill=GREEN)
    draw.text((center_x(draw, "让每一餐", FONT_XL) + 0 - 415, 300),
              "让每一餐", fill=WHITE, font=FONT_XL)
    draw.text((center_x(draw, "都值得期待", FONT_XL) - 415, 380),
              "都值得期待", fill=WHITE, font=FONT_XL)
    draw.text((center_x(draw, "期待与您的企业合作", FONT_REG) - 415, 480),
              "期待与您的企业合作", fill=(0xCD,0xE0,0xC0), font=FONT_REG)
    # right
    draw.text((center_x(draw, "联系我们", FONT_XL) + 0 + 50, 260),
              "联系我们", fill=GREEN, font=FONT_XL)
    info = ["TEL  138-0000-8888", "MAIL  qingye@foodlab.com",
            "WECHAT  qingye_food", "ADD  北京市朝阳区建国路 88 号"]
    y = 380
    for t in info:
        draw.text((center_x(draw, t, FONT_LG) + 60, y), t, fill=DARK, font=FONT_LG)
        y += 90
    return img

# ─── narration script ───
SCENES = [
    (slide_cover, "青野食研所企业团餐合作方案。健康、新鲜、便捷，为您的团队提供高品质午餐配送服务。"),
    (slide_about, "青野食研所成立于二零二三年，专注健康轻食。日均产能超过五百份，已服务三十多家企业，好评率百分之九十八。"),
    (slide_plans, "我们提供三档包月套餐：轻享版二十八元每餐，标准版三十八元每餐是最受欢迎的选择，尊享版四十八元每餐享受全品类自由搭配。"),
    (slide_menu, "每周菜单五天不重样。从烤鸡胸沙拉到日式鸡排饭，从波奇饭到全麦卷，每餐都有多种选择。"),
    (slide_pricing, "合作方式灵活。支持试吃体验、月度、季度和年度合作，长期合作最高可享八五折优惠。"),
    (slide_contact, "欢迎扫码联系，预约免费试餐。青野食研所，让每一餐都值得期待。"),
]

# ─── render all slides ───
print("Rendering slides...")
for i, (fn, _) in enumerate(SCENES):
    img = fn()
    path = os.path.join(OUT, f"slide_{i:02d}.png")
    img.save(path)
    print(f"  slide {i+1} saved")

# ─── generate TTS audio ───
print("Generating TTS audio...")

async def gen_tts():
    import edge_tts
    for i, (_, text) in enumerate(SCENES):
        out_path = os.path.join(OUT, f"audio_{i:02d}.mp3")
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="+10%")
        await communicate.save(out_path)
        print(f"  audio {i+1} saved")

# check if audio already exists
need_tts = any(not os.path.exists(os.path.join(OUT, f"audio_{i:02d}.mp3")) for i in range(len(SCENES)))
if need_tts:
    asyncio.run(gen_tts())
else:
    print("  all audio already exist, skipping")

# ─── assemble video with ffmpeg ───
print("Assembling video...")
ffmpeg_inputs = []
filter_parts = []
audio_inputs = []
offset = 0.0
total_duration = 0.0
durations = []

# get durations from audio files
for i in range(len(SCENES)):
    audio_path = os.path.join(OUT, f"audio_{i:02d}.mp3")
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", audio_path],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    dur = float(data["format"]["duration"])
    durations.append(dur)
    total_duration += dur

# Build complex filter for slideshow
# Each slide is an image, each with corresponding audio
# We crossfade between slides

# Simple approach: use concat with individual segments
# For each slide: [slide_image][audio] -> segment with fade-in/out

# Write a concat file for ffmpeg
concat_lines = []
temp_files = []

for i in range(len(SCENES)):
    slide_path = os.path.join(OUT, f"slide_{i:02d}.png")
    audio_path = os.path.join(OUT, f"audio_{i:02d}.mp3")
    dur = durations[i]

    # Create a temporary video segment for this slide
    seg_path = os.path.join(OUT, f"seg_{i:02d}.mp4")

    # fade in first 0.3s, fade out last 0.3s
    fade_in = min(0.3, dur / 4)
    fade_out = min(0.3, dur / 4)

    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", slide_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-t", str(dur),
        "-pix_fmt", "yuv420p",
        "-vf", f"fade=t=in:st=0:d={fade_in},fade=t=out:st={dur-fade_out}:d={fade_out}",
        "-af", f"afade=t=in:st=0:d=0.2,afade=t=out:st={dur-0.2}:d=0.2",
        "-r", "24",
        seg_path
    ], capture_output=True)
    temp_files.append(seg_path)
    concat_lines.append(f"file '{seg_path}'")
    print(f"  segment {i+1} done ({dur:.1f}s)")

# Concatenate all segments
concat_path = os.path.join(OUT, "concat.txt")
with open(concat_path, "w") as f:
    f.write("\n".join(concat_lines))

output_path = os.path.join(OUT, "青野食研所_团餐方案_口播视频.mp4")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_path,
    "-c", "copy",
    output_path
], capture_output=True)

print(f"\n✅ Video saved: {output_path}")
print(f"   Duration: {total_duration:.1f}s")

# clean up temp segments
for f in temp_files:
    os.remove(f)

print("Done!")
