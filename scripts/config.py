#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局配置管理模块 (Configuration Manager)
统一负责读取 config.json、环境变量与项目绝对路径
"""

import os
import json

# 项目根目录与路径常量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
JSON_PATH = os.path.join(BASE_DIR, "products.json")

# 官方镜像列表（用于主域名频控时自动容错切换）
DOMAINS = [
    "https://bwh81.net",
    "https://bwh88.net",
    "https://bandwagonhost.com"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

class Config:
    """配置类，提供全局统一的配置读取与默认值回退"""

    DEFAULT_TEMPLATE = (
        "🎉 <b>搬瓦工补货提醒 (Restock Alert)</b>\n\n"
        "📦 <b>方案名称</b>：{name}\n"
        "⚡️ <b>线路类型</b>：{circuit_type}\n"
        "💻 <b>配置规格</b>：{cpu}核 CPU / {memory} 内存 / {ssd} SSD\n"
        "🌐 <b>流量带宽</b>：{band} / {bandwidth}\n"
        "🏢 <b>机房节点</b>：{datacenter}\n"
        "💵 <b>官方原价</b>：<b>${price}</b>\n"
        "🎟 <b>优惠码</b>：<code>{promo_code}</code> ({discount_text})\n\n"
        "👉 <a href=\"{buy_url}\"><b>【点击立即直达抢购】</b></a>\n"
        "🌐 <a href=\"{site_url}\"><b>【查看更多方案库存监控】</b></a>"
    )

    def __init__(self):
        self.raw_data = self._load_json()

        # 网站信息
        site = self.raw_data.get("site", {})
        self.site_title = site.get("title", "搬瓦工库存监控")
        self.site_url = site.get("url", "https://tianqiongshaonian.github.io/")

        # 返利推广与优惠码
        aff = self.raw_data.get("affiliate", {})
        self.aff_id = str(aff.get("aff_id", "68648"))
        self.promo_code = aff.get("promo_code", "BWHCXZAVFBVY")
        self.discount_text = aff.get("discount_text", "6.78% 循环优惠")
        self.discount_rate = float(aff.get("discount_rate", 0.0678))

        # 社交媒体与推送渠道
        social = self.raw_data.get("social", {})
        self.tg_channel = social.get("tg_channel", "https://t.me/bwg191")

        # Telegram 推送参数
        tg = self.raw_data.get("telegram", {})
        self.tg_template = tg.get("template", self.DEFAULT_TEMPLATE)
        self.tg_auto_pin = tg.get("auto_pin", True)

        # 环境变量中的敏感密钥
        self.tg_bot_token = os.environ.get("TG_BOT_TOKEN", "").strip()
        self.tg_chat_id = os.environ.get("TG_CHAT_ID", "").strip() or self._extract_chat_id(self.tg_channel)

        # 监控配置
        monitor = self.raw_data.get("monitor", {})
        self.check_domain = monitor.get("check_domain", "https://bwh81.net")

    def _load_json(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[-] 读取 {CONFIG_PATH} 异常: {e}")
        return {}

    @staticmethod
    def _extract_chat_id(channel_url):
        if not channel_url:
            return "@bwg191"
        if "t.me/" in channel_url:
            return "@" + channel_url.split("t.me/")[-1].strip("/")
        return channel_url

# 单例配置实例
get_config = Config
