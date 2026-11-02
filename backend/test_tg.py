#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 推送与置顶测试工具 (Test Telegram Alert)
使用方法：
    python3 backend/test_tg.py [BOT_TOKEN] [CHAT_ID] [restock|out_of_stock|all]
示例：
    python3 backend/test_tg.py
    python3 backend/test_tg.py "BOT_TOKEN" "@bwg191" out_of_stock
"""

import sys
import os
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.config import Config
from backend.notifier import TelegramNotifier

def main():
    config = Config()
    
    # 优先使用命令行参数，其次读取环境变量与 config.json
    bot_token = sys.argv[1].strip() if len(sys.argv) > 1 and not sys.argv[1].startswith("--") and sys.argv[1] not in ["restock", "out_of_stock", "all"] else config.tg_bot_token
    chat_id = sys.argv[2].strip() if len(sys.argv) > 2 and sys.argv[2] not in ["restock", "out_of_stock", "all"] else config.tg_chat_id

    # 测试模式 (restock, out_of_stock, all)
    test_mode = "all"
    for arg in sys.argv[1:]:
        if arg in ["restock", "out_of_stock", "all"]:
            test_mode = arg
            break

    if not bot_token:
        print("❌ 错误：未提供 TG_BOT_TOKEN，且环境变量/配置中未找到！")
        print("\n使用方法示例：")
        print('  python3 backend/test_tg.py "123456789:ABCdefGhIJKlmNoPQRstuVWxYz"')
        print('  python3 backend/test_tg.py "123456789:ABCdefGhIJKlmNoPQRstuVWxYz" "@bwg191" out_of_stock')
        sys.exit(1)

    print(f"[*] 目标频道/会话: {chat_id} | 测试模式: {test_mode}")
    notifier = TelegramNotifier(bot_token=bot_token, chat_id=chat_id)

    mock_product = {
        "pid": "159",
        "name": "The Amsterdam Plan VPS (测试方案)",
        "circuit_type": "荷兰阿姆斯特丹限量版",
        "cpu": "2",
        "memory": "2GB",
        "ssd": "40GB",
        "band": "1000GB",
        "bandwidth": "2.5Gbps",
        "datacenter": "荷兰阿姆斯特丹 EUNL_9 (中国联通 AS9929 优化)",
        "price": "49.99"
    }

    if test_mode in ["restock", "all"]:
        print("[*] 正在测试【补货提醒】推送与自动置顶...")
        ok_restock = notifier.send_restock_alert(mock_product)
        if ok_restock:
            print("  ✅ 补货提醒测试成功！")
        else:
            print("  ❌ 补货提醒测试失败，请检查 Bot 权限。")

    if test_mode == "all":
        time.sleep(2)

    if test_mode in ["out_of_stock", "all"]:
        print("[*] 正在测试【断货/售罄下架】推送...")
        ok_oos = notifier.send_out_of_stock_alert(mock_product)
        if ok_oos:
            print("  ✅ 断货/售罄提醒测试成功！")
        else:
            print("  ❌ 断货/售罄提醒测试失败，请检查 Bot 权限。")

if __name__ == "__main__":
    main()
