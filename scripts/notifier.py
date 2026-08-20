#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知推送模块 (Notification Service)
负责消息模板渲染、Telegram 机器人消息发送与自动置顶
"""

import json
import urllib.request
import urllib.parse
from scripts.config import Config

class TelegramNotifier:
    """Telegram 推送服务类"""

    def __init__(self, bot_token=None, chat_id=None):
        self.config = Config()
        self.bot_token = bot_token or self.config.tg_bot_token
        self.chat_id = chat_id or self.config.tg_chat_id

    def is_configured(self):
        """检查是否已配置 BotToken 和 ChatID"""
        return bool(self.bot_token and self.chat_id)

    def render_message(self, product):
        """根据配置模板渲染补货通知文本"""
        buy_url = f"https://bwh81.net/aff.php?aff={self.config.aff_id}&pid={product.get('pid', '')}"
        try:
            return self.config.tg_template.format(
                name=product.get("name", ""),
                circuit_type=product.get("circuit_type", ""),
                cpu=product.get("cpu", ""),
                memory=product.get("memory", ""),
                ssd=product.get("ssd", ""),
                band=product.get("band", ""),
                bandwidth=product.get("bandwidth", ""),
                datacenter=product.get("datacenter", ""),
                price=product.get("price", ""),
                pid=product.get("pid", ""),
                promo_code=self.config.promo_code,
                discount_text=self.config.discount_text,
                buy_url=buy_url,
                site_url=self.config.site_url
            )
        except Exception as e:
            print(f"[-] 模板自定义渲染失败，降级为默认模板: {e}")
            return self.config.DEFAULT_TEMPLATE.format(
                name=product.get("name", ""),
                circuit_type=product.get("circuit_type", ""),
                cpu=product.get("cpu", ""),
                memory=product.get("memory", ""),
                ssd=product.get("ssd", ""),
                band=product.get("band", ""),
                bandwidth=product.get("bandwidth", ""),
                datacenter=product.get("datacenter", ""),
                price=product.get("price", ""),
                pid=product.get("pid", ""),
                promo_code=self.config.promo_code,
                discount_text=self.config.discount_text,
                buy_url=buy_url,
                site_url=self.config.site_url
            )

    def send_message(self, text, auto_pin=None):
        """发送单条消息并可选自动置顶"""
        if not self.is_configured():
            print("[*] Telegram 未配置 TG_BOT_TOKEN 或 TG_CHAT_ID，跳过推送")
            return False, None

        send_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                send_url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    resp_json = json.loads(resp.read().decode("utf-8"))
                    msg_id = resp_json.get("result", {}).get("message_id")
                    
                    # 是否开启自动置顶
                    should_pin = self.config.tg_auto_pin if auto_pin is None else auto_pin
                    if should_pin and msg_id:
                        self.pin_message(msg_id)
                        
                    return True, msg_id
        except Exception as e:
            print(f"[-] Telegram 消息发送失败: {e}")
            return False, str(e)

    def pin_message(self, message_id):
        """置顶指定消息"""
        pin_url = f"https://api.telegram.org/bot{self.bot_token}/pinChatMessage"
        payload = {
            "chat_id": self.chat_id,
            "message_id": message_id,
            "disable_notification": False
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                pin_url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    print(f"[+] 消息 (ID: {message_id}) 已成功置顶到频道顶部")
                    return True
        except Exception as e:
            print(f"[-] 自动置顶失败: {e}")
            return False

    def send_restock_alert(self, product):
        """发送补货提醒"""
        text = self.render_message(product)
        success, msg_id = self.send_message(text)
        if success:
            print(f"[+] 补货通知已推送: {product.get('name')} (Message ID: {msg_id})")
        return success
