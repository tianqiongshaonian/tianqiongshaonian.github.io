#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搬瓦工产品数据全自动同步与新方案发现工具 (BandwagonHost Product Auto-Sync & Discovery)

功能特性：
1. 自动抓取官方公开产品列表 (cart.php) 并智能解析硬件规格、价格与周期
2. 支持 PID 增量盲扫探测 (Discovery)，自动发现官方新上架的隐藏/限量版套餐
3. 非破坏性智能合并：保留用户自定义的中文机房别名、推荐标记与自定义分类
4. 自动为新发现的套餐分配分类标签与线路说明

使用方法：
    python3 scripts/sync_products.py                  # 全量同步公开产品数据
    python3 scripts/sync_products.py --scan-new 20    # 同步并扫描探测最新 20 个新 PID
    python3 scripts/sync_products.py --scan-range 1 200 # 深度全量扫描指定 PID 范围
    python3 scripts/sync_products.py --dry-run        # 仅试运行，不修改 products.json
"""

import sys
import os
import re
import json
import time
import random
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 确保在任何目录下执行都能正确导入
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.config import Config, JSON_PATH, DOMAINS, USER_AGENTS

CYCLE_MAP = {
    "annually": "年付",
    "semi-annually": "半年付",
    "quarterly": "季付",
    "monthly": "月付",
    "biennially": "两年付",
    "triennially": "三年付"
}

class ProductSyncManager:
    """产品同步与新套餐发现管理器"""

    def __init__(self, timeout=12, max_workers=6):
        self.config = Config()
        self.timeout = timeout
        self.max_workers = max_workers

    def _get_headers(self):
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Connection": "keep-alive"
        }

    # ==================== 1. 公开产品列表抓取 ====================

    def fetch_public_products(self):
        """抓取搬瓦工官方公开产品列表 (cart.php)"""
        print("[*] 正在从搬瓦工官方抓取公开在售产品列表 (cart.php)...")
        content = None

        for domain in [self.config.check_domain] + DOMAINS:
            url = f"{domain}/cart.php"
            try:
                req = urllib.request.Request(url, headers=self._get_headers())
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    raw_html = resp.read().decode("utf-8", errors="ignore")
                    if "cartbox" in raw_html:
                        content = raw_html
                        print(f"[+] 成功连接至 {domain} 并获取页面数据")
                        break
            except Exception as e:
                print(f"[-] 连接 {domain} 异常: {e}，尝试切换备用镜像...")

        if not content:
            print("❌ 获取 cart.php 失败，请检查网络连接")
            return []

        boxes = content.split('<div class="cartbox">')
        parsed_products = []

        for b in boxes[1:]:
            item = self._parse_cartbox(b)
            if item:
                parsed_products.append(item)

        print(f"[✓] 成功解析出 {len(parsed_products)} 款公开套餐！")
        return parsed_products

    def _parse_cartbox(self, box_html):
        """解析单条 cartbox HTML"""
        pid_match = re.search(r'cart\.php\?a=add&pid=(\d+)', box_html)
        name_match = re.search(r'<nobr>(.*?)</nobr>', box_html, re.IGNORECASE)
        price_match = re.search(r'\$([0-9\.]+)\s*USD\s*([A-Za-z\-]+)?', box_html, re.IGNORECASE)
        ssd_match = re.search(r'SSD:\s*([^<\n]+)', box_html, re.IGNORECASE)
        ram_match = re.search(r'RAM:\s*([^<\n]+)', box_html, re.IGNORECASE)
        cpu_match = re.search(r'CPU:\s*([^<\n]+)', box_html, re.IGNORECASE)
        transfer_match = re.search(r'Transfer:\s*([^<\n]+)', box_html, re.IGNORECASE)
        link_match = re.search(r'Link speed:\s*([^<\n]+)', box_html, re.IGNORECASE)

        if not (pid_match and name_match):
            return None

        pid = str(pid_match.group(1))
        name = name_match.group(1).strip()
        price = price_match.group(1) if price_match else "0.00"
        cycle_raw = (price_match.group(2) if price_match and price_match.group(2) else "annually").lower()
        billing_cycle = CYCLE_MAP.get(cycle_raw, "年付")

        cpu = self._clean_cpu(cpu_match.group(1)) if cpu_match else "1"
        memory = self._clean_memory(ram_match.group(1)) if ram_match else "1GB"
        ssd = self._clean_ssd(ssd_match.group(1)) if ssd_match else "20GB"
        band = self._clean_band(transfer_match.group(1)) if transfer_match else "1TB"
        bandwidth = self._clean_bandwidth(link_match.group(1)) if link_match else "1Gbps"
        status = 1 if "order now" in box_html.lower() else 0

        return {
            "pid": pid,
            "name": name,
            "cpu": cpu,
            "memory": memory,
            "ssd": ssd,
            "band": band,
            "bandwidth": bandwidth,
            "price": price,
            "billing_cycle": billing_cycle,
            "status": status
        }

    # ==================== 2. 隐藏 / 指定 PID 单体探测 ====================

    def probe_pid(self, pid):
        """探测指定单个 PID，若存在有效套餐则解析返回"""
        time.sleep(random.uniform(0.1, 0.25))
        for domain in [self.config.check_domain] + DOMAINS:
            url = f"{domain}/cart.php?a=add&pid={pid}"
            try:
                req = urllib.request.Request(url, headers=self._get_headers())
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    content = resp.read().decode("utf-8", errors="ignore")
                    content_lower = content.lower()

                    # 拦截页
                    if any(sig in content_lower for sig in ["cf-chl", "challenge-platform", "just a moment", "attention required"]):
                        continue

                    # 无效 PID (重定向或无相关内容)
                    if "the product you selected could not be found" in content_lower:
                        return None

                    # 尝试从页面中提取产品名称
                    title_match = re.search(r'<h3>(.*?)</h3>', content, re.IGNORECASE)
                    if not title_match:
                        title_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE)
                    
                    if title_match:
                        name = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                        if "shopping cart" not in name.lower() and "error" not in name.lower() and name:
                            status = 0 if "out of stock" in content_lower else 1
                            return {
                                "pid": str(pid),
                                "name": name,
                                "status": status,
                                "cpu": "1",
                                "memory": "1GB",
                                "ssd": "20GB",
                                "band": "1TB",
                                "bandwidth": "1Gbps",
                                "price": "49.99",
                                "billing_cycle": "年付"
                            }
                    return None
            except Exception:
                continue
        return None

    def scan_pids(self, start_pid, end_pid):
        """并发扫描指定 PID 范围内的有效套餐"""
        print(f"[*] 正在并发探测 PID {start_pid} ~ {end_pid} 是否有新套餐...")
        found_products = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_pid = {
                executor.submit(self.probe_pid, pid): pid
                for pid in range(start_pid, end_pid + 1)
            }
            for future in as_completed(future_to_pid):
                item = future.result()
                if item:
                    print(f"[🔥 探测到有效套餐] PID {item['pid']}: {item['name']}")
                    found_products.append(item)

        print(f"[✓] 范围扫描完成，发现 {len(found_products)} 款有效套餐！")
        return found_products

    # ==================== 3. 智能非破坏性数据合并 ====================

    def smart_merge(self, existing_products, crawled_products):
        """将抓取到的数据与现有数据智能合并，保留人工定制的机房别名、分类标签和推荐标记"""
        existing_map = {str(p["pid"]): p for p in existing_products}
        updated_count = 0
        added_count = 0

        for new_p in crawled_products:
            pid = str(new_p["pid"])
            if pid in existing_map:
                # 已存在的产品：更新官方硬件参数与价格，保留人工设置的机房/推荐/分类
                target = existing_map[pid]
                target["name"] = new_p.get("name", target.get("name"))
                target["price"] = new_p.get("price", target.get("price"))
                target["billing_cycle"] = new_p.get("billing_cycle", target.get("billing_cycle", "年付"))
                target["cpu"] = new_p.get("cpu", target.get("cpu"))
                target["memory"] = new_p.get("memory", target.get("memory"))
                target["ssd"] = new_p.get("ssd", target.get("ssd"))
                target["band"] = new_p.get("band", target.get("band"))
                target["bandwidth"] = new_p.get("bandwidth", target.get("bandwidth"))
                updated_count += 1
            else:
                # 新发现的产品：智能推导分类标签与线路
                inferred_tags, circuit_type, datacenter = self._infer_metadata(new_p["name"])
                new_p["circuit_type"] = circuit_type
                new_p["datacenter"] = datacenter
                new_p["tags"] = inferred_tags
                new_p["recommended"] = 0
                existing_products.append(new_p)
                existing_map[pid] = new_p
                added_count += 1
                print(f"[+] 自动入库新套餐: PID {pid} - {new_p['name']} (标签: {inferred_tags})")

        # 按 PID 数字大小升序排序
        existing_products.sort(key=lambda x: int(x.get("pid", 0)))
        return existing_products, updated_count, added_count

    # ==================== 4. 辅助清洗与智能标签推导 ====================

    @staticmethod
    def _clean_cpu(s):
        m = re.search(r'(\d+)', s)
        return m.group(1) if m else "1"

    @staticmethod
    def _clean_memory(s):
        s = s.strip()
        m_mb = re.search(r'(\d+)\s*MB', s, re.I)
        if m_mb:
            mb = int(m_mb.group(1))
            if mb >= 1024 and mb % 1024 == 0:
                return f"{mb // 1024}GB"
            return f"{mb}MB"
        m_gb = re.search(r'(\d+)\s*GB', s, re.I)
        if m_gb:
            return f"{m_gb.group(1)}GB"
        return s

    @staticmethod
    def _clean_ssd(s):
        m = re.search(r'(\d+)\s*GB', s, re.I)
        if m:
            return f"{m.group(1)}GB"
        return s.replace("RAID-10", "").strip()

    @staticmethod
    def _clean_band(s):
        s = s.replace("/mo", "").strip()
        m = re.search(r'(\d+)\s*(TB|GB)', s, re.I)
        if m:
            return f"{m.group(1)}{m.group(2).upper()}"
        return s

    @staticmethod
    def _clean_bandwidth(s):
        s = s.strip()
        if "1 Gigabit" in s:
            return "1Gbps"
        if "2.5 Gigabit" in s:
            return "2.5Gbps"
        if "10 Gigabit" in s:
            return "10Gbps"
        m = re.search(r'([\d\.]+)\s*(Gigabit|Gbps)', s, re.I)
        if m:
            return f"{m.group(1)}Gbps"
        return s

    @staticmethod
    def _infer_metadata(name):
        """根据套餐名称智能推导分类标签、线路类型与默认机房"""
        name_lower = name.lower()
        tags = []
        circuit_type = "常规 KVM"
        datacenter = "常规全球机房 (支持切换机房)"

        if "hong kong" in name_lower or "hk" in name_lower:
            tags.append("hk")
            circuit_type = "香港 CN2 GIA / CMI"
            datacenter = "中国香港 HKHK_8 机房"
        elif "tokyo" in name_lower or "osaka" in name_lower or "japan" in name_lower:
            tags.append("japan")
            circuit_type = "日本软银 / CN2 GIA"
            datacenter = "日本东京 / 大阪机房"
        elif "singapore" in name_lower or "sg" in name_lower:
            tags.append("singapore")
            circuit_type = "新加坡 CN2 GIA"
            datacenter = "新加坡 SGSG_1 机房"
        elif "cn2 gia" in name_lower or "gia-e" in name_lower or "dc6" in name_lower or "dc9" in name_lower:
            tags.append("cn2gia")
            circuit_type = "美西 CN2 GIA-E 优化线路"
            datacenter = "洛杉矶 DC6 CN2 GIA-E / DC9 / 软银 / 欧洲多机房"
        elif "kvm" in name_lower:
            tags.append("kvm")
            circuit_type = "KVM 常规系列"
            datacenter = "DC3 CN2/DC2 AO/DC8 ZNET/弗里蒙特/新泽西/荷兰等"

        if "plan" in name_lower or "limited" in name_lower or "special" in name_lower or "chicken" in name_lower or "box" in name_lower:
            tags.append("limited")

        if not tags:
            tags.append("kvm")

        return list(set(tags)), circuit_type, datacenter

    # ==================== 5. 执行同步主流程 ====================

    def run(self, scan_new_count=0, scan_range=None, dry_run=False):
        """执行完整产品抓取、探测与同步"""
        if not os.path.exists(JSON_PATH):
            print(f"❌ 找不到数据文件: {JSON_PATH}")
            return

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        existing_products = data.get("products", data) if isinstance(data, dict) else data
        print(f"[*] 当前本地库中已有产品: {len(existing_products)} 款")

        # 1. 抓取公开产品列表
        crawled = self.fetch_public_products()

        # 2. 如果开启了 PID 范围探测
        if scan_range:
            start_p, end_p = scan_range
            scanned = self.scan_pids(start_p, end_p)
            crawled.extend(scanned)
        elif scan_new_count > 0:
            max_pid = max([int(p.get("pid", 0)) for p in existing_products] or [0])
            print(f"[*] 库中最大 PID 为 {max_pid}，将向后扫描 {scan_new_count} 个新 PID ({max_pid+1} ~ {max_pid+scan_new_count})...")
            scanned = self.scan_pids(max_pid + 1, max_pid + scan_new_count)
            crawled.extend(scanned)

        # 3. 智能合并
        merged_products, updated_count, added_count = self.smart_merge(existing_products, crawled)

        print(f"\n==================== 同步结果统计 ====================")
        print(f"  • 更新已有套餐参数: {updated_count} 款")
        print(f"  • 新增入库套餐: {added_count} 款")
        print(f"  • 合并后总套餐数: {len(merged_products)} 款")
        print(f"=======================================================")

        if dry_run:
            print("[*] 当前为 Dry-Run 模式，不写入文件。")
            return

        # 4. 落盘保存
        output_data = {
            "updated_at": data.get("updated_at", time.strftime("%Y-%m-%d %H:%M:%S")),
            "in_stock_count": sum(1 for p in merged_products if NumberSafe(p.get("status")) == 1),
            "total_count": len(merged_products),
            "products": merged_products
        }

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"[✓] 成功更新并保存至 {JSON_PATH}！")

def NumberSafe(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

def main():
    import argparse
    parser = argparse.ArgumentParser(description="搬瓦工产品自动同步与探测工具")
    parser.add_argument("--scan-new", type=int, default=0, help="从当前最大 PID 往后扫描的新 PID 数量 (如 --scan-new 20)")
    parser.add_argument("--scan-range", nargs=2, type=int, metavar=('START', 'END'), help="指定扫描 PID 起止区间 (如 --scan-range 1 200)")
    parser.add_argument("--dry-run", action="store_true", help="仅预览抓取与合并结果，不写入 products.json")
    args = parser.parse_args()

    manager = ProductSyncManager()
    manager.run(scan_new_count=args.scan_new, scan_range=args.scan_range, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
