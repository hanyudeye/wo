# 做个 定时提醒 & 番茄钟, 命令行小脚本，每隔 N 分钟弹出系统通知，提醒喝水、休息或切换任务。

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定时提醒 / 番茄钟：每隔 N 分钟发送系统通知。"""
import argparse
import json
import subprocess
import sys
import time

def notify(title, text):
    """发送系统通知（Linux / macOS / Windows 终端回退）"""
    if sys.platform.startswith('linux'):
        subprocess.run(['notify-send', title, text])
    elif sys.platform == 'darwin':
        cmd = 'display notification {} with title {}'.format(json.dumps(text), json.dumps(title))
        subprocess.run(['osascript', '-e', cmd])
    else:
        print(f"[{title}] {text}")

def wait_seconds(seconds):
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        print("\n已退出")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='定时提醒 & 番茄钟')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--interval', type=int, metavar='MINUTES',
                      help='每隔 MINUTES 分钟提醒一次')
    mode.add_argument('--pomodoro', type=int, nargs=2, metavar=('WORK', 'BREAK'),
                      help='番茄钟：工作 WORK 分钟，休息 BREAK 分钟')
    parser.add_argument('--message', default='休息一下，喝口水！',
                        help='提醒内容（仅 interval 模式使用）')
    args = parser.parse_args()

    if args.interval is not None:
        while True:
            notify('定时提醒', args.message)
            wait_seconds(args.interval * 60)
    else:
        work, rest = args.pomodoro
        round_no = 0
        while True:
            round_no += 1
            notify(f'番茄钟 第{round_no}轮', f'开始工作 {work} 分钟，专注！')
            wait_seconds(work * 60)
            notify(f'番茄钟 第{round_no}轮', f'休息 {rest} 分钟，放松一下！')
            wait_seconds(rest * 60)

if __name__ == '__main__':
    main()

# **用法示例：**

# ```bash
# # 每 30 分钟提醒喝水
# python3 timer.py --interval 30 --message "该喝水了，起来走走！"

# # 每 45 分钟提醒切换任务
# python3 timer.py --interval 45 --message "切换一下任务，保持高效"

# # 番茄钟：工作 25 分钟，休息 5 分钟
# python3 timer.py --pomodoro 25 5
# ```

# 按 `Ctrl+C` 退出。Linux 需安装 `notify-send`（通常自带）；macOS 直接可用；Windows 会打印提示，可自行替换 `notify` 函数。

