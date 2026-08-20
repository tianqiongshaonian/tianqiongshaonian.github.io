#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存检测核心模块 (Stock Checker Core)
支持多线程并发探测、智能容错与多镜像轮询、库存变动比对、自动通知与数据落地
"""

import sys
import os
import json
import time
import random
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# 确保无论在根目录还是 scripts 目录下执行都能正确导入
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.config import Config, JSON_PATH, DOMAINS, USER_AGENTS
from scripts.notifier import TelegramNotifier

class StockChecker:
    """搬瓦工库存探测器"""

    def __init__(self, max_workers=4, timeout=10):
        self.config = Config()
        self.notifier = TelegramNotifier()
        self.max_workers = max_workers
        self.timeout = timeout

    def check_pid(self, pid, retries=3):
        """探测单个 PID 套餐库存状态 (0: 缺货, 1: 有货, None: 探测异常)"""
        # 随机微小延时，防止瞬间高并发触发 Cloudflare / 503 频控
        time.sleep(random.uniform(0.1, 0.35))

        for attempt in range(retries):
            # 轮询官方主域名与镜像域名
            domain = self.config.check_domain if attempt == 0 else DOMAINS[attempt % len(DOMAINS)]
            url = f"{domain}/cart.php?a=add&pid={pid}"
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "Connection": "keep-alive"
            }

            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    content = response.read().decode("utf-8", errors="ignore")

                    # 1. 明确提示 Out of Stock 则为缺货
                    if "Out of Stock" in content or "currently out of stock" in content.lower():
                        return pid, 0

                    # 2. 包含购物车结账或配置项则为有货
                    if "order-web20cart" in content or "cart.php" in response.url or "Configure" in content:
                        return pid, 1

                    return pid, 0
            except Exception as e:
                if attempt == retries - 1:
                    print(f"[-] PID {pid} 检测失败 ({domain}): {e}")
                    return pid, None
                time.sleep(1 + attempt)

        return pid, None

    def run(self):
        """执行完整库存探测与数据更新"""
        if not os.path.exists(JSON_PATH):
            print(f"[-] 找不到数据源文件: {JSON_PATH}")
            return

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        products = data.get("products", data) if isinstance(data, dict) else data
        print(f"[*] 开始并发探测 {len(products)} 款套餐库存 (主探测点: {self.config.check_domain})...")
        start_time = time.time()

        # 多线程并发执行
        results = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_pid = {
                executor.submit(self.check_pid, p["pid"]): p["pid"]
                for p in products
            }
            for future in as_completed(future_to_pid):
                pid, status = future.result()
                if status is not None:
                    results[str(pid)] = status

        # 比对库存状态变化
        restocked_items = []
        in_stock_count = 0

        for p in products:
            pid_str = str(p["pid"])
            if pid_str in results:
                new_status = results[pid_str]
                old_status = p.get("status", 0)

                # 检测到 0 -> 1 补货
                if old_status == 0 and new_status == 1:
                    restocked_items.append(p)
                    print(f"[🔥 发现补货] {p['name']} (PID: {p['pid']}) 重新有货！")

                p["status"] = new_status
                if new_status == 1:
                    in_stock_count += 1
            else:
                if p.get("status", 0) == 1:
                    in_stock_count += 1

        # 更新时间戳（北京时间 UTC+8）
        utc_dt = datetime.now(timezone.utc)
        bj_dt = utc_dt + timedelta(hours=8)

        output_data = {
            "updated_at": bj_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "in_stock_count": in_stock_count,
            "total_count": len(products),
            "products": products
        }

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        elapsed = round(time.time() - start_time, 2)
        print(f"[✓] 检测完毕！耗时: {elapsed}s | 当前有货: {in_stock_count}/{len(products)}")

        # 触发 Telegram 推送与自动置顶
        if restocked_items:
            print(f"[*] 正在为 {len(restocked_items)} 款新补货套餐发送 Telegram 推送...")
            for item in restocked_items:
                self.notifier.send_restock_alert(item)

def main():
    checker = StockChecker()
    checker.run()

if __name__ == "__main__":
    main()
