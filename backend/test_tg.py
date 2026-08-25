#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 推送与置顶测试工具 (Test Telegram Alert)
使用方法：
    python3 backend/test_tg.py [BOT_TOKEN] [CHAT_ID]
"""

import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.config import Config
from backend.notifier import TelegramNotifier

def main():
    config = Config()
    
    # 优先使用命令行参数，其次读取环境变量与 config.json
    bot_token = sys.argv[1].strip() if len(sys.argv) > 1 else config.tg_bot_token
    chat_id = sys.argv[2].strip() if len(sys.argv) > 2 else config.tg_chat_id

    if not bot_token:
        print("❌ 错误：未提供 TG_BOT_TOKEN！")
        print("\n使用方法示例：")
        print('  python3 backend/test_tg.py "123456789:ABCdefGhIJKlmNoPQRstuVWxYz"')
        sys.exit(1)

    print(f"[*] 正在向 {chat_id} 发送测试卡片并执行自动置顶...")
    notifier = TelegramNotifier(bot_token=bot_token, chat_id=chat_id)

    mock_product = {
        "pid": "159",
        "name": "The Amsterdam Plan VPS (测试推送)",
        "circuit_type": "荷兰阿姆斯特丹限量版",
        "cpu": "2",
        "memory": "2GB",
        "ssd": "40GB",
        "band": "1000GB",
        "bandwidth": "2.5Gbps",
        "datacenter": "荷兰阿姆斯特丹 EUNL_9 (中国联通 AS9929 优化)",
        "price": "49.99"
    }

    success = notifier.send_restock_alert(mock_product)
    if success:
        print(f"✅ 测试成功！请打开 Telegram 频道 {chat_id} 查看。")
    else:
        print(f"❌ 测试失败，请检查 Bot 是否已添加为频道管理员并开启发消息权限。")

if __name__ == "__main__":
    main()
