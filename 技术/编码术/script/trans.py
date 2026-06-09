import requests
import json

# ===================== WSL 修复版配置 =====================
# API_URL = "http://host.docker.internal:5000/translate"  # WSL 专用
API_URL = "http://127.0.0.1:5000/translate"  # WSL 专用
SOURCE_LANG = "auto"
TARGET_LANG = "zh"
# ==========================================================

def translate(text):
    try:
        data = {
            "q": text,
            "source": SOURCE_LANG,
            "target": TARGET_LANG,
            "format": "text"
        }
        res = requests.post(API_URL, json=data, timeout=8)
        res.raise_for_status()
        return res.json()["translatedText"]
    except Exception as e:
        return f"翻译失败：{str(e)}"

def main():
    print("=" * 50)
    print(" LibreTranslate 终端翻译工具（循环输入版）")
    print(" 输入文字 → 回车翻译 | 输入 quit 退出")
    print("=" * 50)

    while True:
        # 接收输入（自动等待你打字）
        try:
            # user_input = input("\n请输入要翻译的内容：").strip()
            user_input = input("\n").strip()
        except KeyboardInterrupt:
            print("\n退出程序")
            break

        # 退出条件
        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit", "q", "退出"]:
            print("再见！")
            break

        # 翻译并输出
        result = translate(user_input)
        # print(f"→ 翻译结果：{result}")
        print(f"{result}")

if __name__ == "__main__":
    main()