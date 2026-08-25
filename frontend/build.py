#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 静态预渲染与 SEO 强化构建脚本 (Static Pre-renderer & SEO Builder)
将 products.json 中的最新套餐数据预先渲染进 index.html 中，
使各大搜索引擎爬虫与 AI 智能体在无需运行 JS 的情况下即可抓取完整的 VPS 方案、价格、库存和 FAQ 数据。
"""

import os
import json
import html
import shutil
import sys
from datetime import datetime, timezone, timedelta

# 兼容 Windows 控制台默认 GBK 编码：避免打印 ✓/中文 时报 UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

CONFIG_PATH = os.path.join(PROJECT_ROOT, "data", "config.json")
PRODUCTS_PATH = os.path.join(PROJECT_ROOT, "data", "products.json")
INDEX_PATH = os.path.join(PROJECT_ROOT, "index.html")
SITEMAP_PATH = os.path.join(PROJECT_ROOT, "sitemap.xml")
DATA_JS_PATH = os.path.join(PROJECT_ROOT, "static", "js", "data.js")
PARTIALS_DIR = os.path.join(PROJECT_ROOT, "frontend", "templates")
APP_JS_SRC = os.path.join(PROJECT_ROOT, "frontend", "js", "app.js")
APP_JS_DEST = os.path.join(PROJECT_ROOT, "static", "js", "app.js")

def escape(val):
    return html.escape(str(val) if val is not None else "")

def render_table_rows(products, aff_id, promo_code, disc_rate, tg_channel):
    rows = []
    for item in products:
        is_in_stock = int(item.get("status", 0)) == 1
        is_rec = int(item.get("recommended", 0)) == 1
        pid = escape(item.get("pid", ""))
        name = escape(item.get("name", ""))
        circuit_type = escape(item.get("circuit_type", ""))
        cpu = escape(item.get("cpu", ""))
        memory = escape(item.get("memory", ""))
        ssd = escape(item.get("ssd", ""))
        band = escape(item.get("band", ""))
        bandwidth = escape(item.get("bandwidth", ""))
        datacenter = escape(item.get("datacenter", "常规节点"))
        raw_price = float(item.get("price", 0)) if item.get("price") else 0.0
        disc_price = f"{(raw_price * (1 - disc_rate)):.2f}"
        billing_cycle = escape(item.get("billing_cycle", "年付"))
        buy_url = f"https://bwh81.net/aff.php?aff={aff_id}&amp;pid={pid}&amp;promocode={promo_code}"

        rec_badge = (
            '<span class="inline-flex items-center shrink-0 whitespace-nowrap px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-50 text-amber-700 border border-amber-200/60 ml-2">'
            '<i class="fa-solid fa-fire text-amber-500 mr-1 text-[10px]"></i>热门推荐</span>'
            if is_rec else ""
        )

        stock_badge = (
            '<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/80">'
            '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-dot mr-1.5"></span>有货</span>'
            if is_in_stock else
            '<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-rose-50 text-rose-600 border border-rose-200/80">缺货</span>'
        )

        btn = (
            f'<a href="{buy_url}" target="_blank" rel="nofollow noopener" onclick="onBuyClick(event)" class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-sm transition active:scale-95 space-x-1">'
            f'<span>立即抢购</span><i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></a>'
            if is_in_stock else
            f'<a href="{tg_channel}" target="_blank" rel="nofollow noopener" class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-medium transition space-x-1">'
            f'<i class="fa-brands fa-telegram text-sky-500"></i><span>补货通知</span></a>'
        )

        row = f"""            <tr class="hover:bg-slate-50/80 transition group">
              <td class="py-3 px-3 sm:px-4">
                <div class="font-semibold text-slate-900 flex items-center whitespace-nowrap">
                  <span class="truncate max-w-[180px] sm:max-w-none">{name}</span>
                  {rec_badge}
                </div>
                <div class="text-xs text-slate-500 mt-0.5 whitespace-nowrap">
                  <span class="truncate max-w-[200px] text-[11px]">{circuit_type}</span>
                </div>
              </td>
              <td class="py-3 px-2 sm:px-3 whitespace-nowrap">
                <div class="text-slate-800 font-medium">{cpu} 核 / {memory}</div>
                <div class="text-[11px] text-slate-400 font-mono">{ssd} SSD</div>
              </td>
              <td class="py-3 px-2 sm:px-3 whitespace-nowrap">
                <div class="text-slate-800 font-medium">{band}</div>
                <div class="text-[11px] text-slate-400">{bandwidth}</div>
              </td>
              <td class="py-3 px-2 sm:px-3 max-w-[240px]">
                <div class="text-xs text-slate-600 line-clamp-2 leading-relaxed" title="{datacenter}">
                  {datacenter}
                </div>
              </td>
              <td class="py-3 px-2 sm:px-3 text-right whitespace-nowrap font-mono text-slate-400">
                <span class="line-through text-xs">${raw_price:.2f}</span>
              </td>
              <td class="py-3 px-2 sm:px-3 text-right whitespace-nowrap font-mono">
                <span class="text-base font-bold text-blue-600">${disc_price}</span>
                <span class="text-[10px] text-slate-400 block -mt-1">/{billing_cycle}</span>
              </td>
              <td class="py-3 px-2 sm:px-3 text-center whitespace-nowrap">
                {stock_badge}
              </td>
              <td class="py-3 px-3 sm:px-4 text-center whitespace-nowrap">
                {btn}
              </td>
            </tr>"""
        rows.append(row)
    return "\n".join(rows)

def render_cards(products, aff_id, promo_code, disc_rate, tg_channel):
    cards = []
    for item in products:
        is_in_stock = int(item.get("status", 0)) == 1
        is_rec = int(item.get("recommended", 0)) == 1
        pid = escape(item.get("pid", ""))
        name = escape(item.get("name", ""))
        circuit_type = escape(item.get("circuit_type", ""))
        cpu = escape(item.get("cpu", ""))
        memory = escape(item.get("memory", ""))
        ssd = escape(item.get("ssd", ""))
        band = escape(item.get("band", ""))
        bandwidth = escape(item.get("bandwidth", ""))
        datacenter = escape(item.get("datacenter", "常规全球机房"))
        raw_price = float(item.get("price", 0)) if item.get("price") else 0.0
        disc_price = f"{(raw_price * (1 - disc_rate)):.2f}"
        billing_cycle = escape(item.get("billing_cycle", "年付"))
        buy_url = f"https://bwh81.net/aff.php?aff={aff_id}&amp;pid={pid}&amp;promocode={promo_code}"

        rec_badge = (
            '<span class="inline-flex items-center shrink-0 whitespace-nowrap px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-50 text-amber-700 border border-amber-200/60"><i class="fa-solid fa-fire text-amber-500 mr-1"></i>推荐</span>'
            if is_rec else ""
        )

        stock_badge = (
            '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-dot mr-1"></span>有货</span>'
            if is_in_stock else
            '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-rose-50 text-rose-600 border border-rose-200">缺货</span>'
        )

        btn = (
            f'<a href="{buy_url}" target="_blank" rel="nofollow noopener" onclick="onBuyClick(event)" class="inline-flex items-center justify-center px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-sm transition active:scale-95 space-x-1.5 whitespace-nowrap">'
            f'<span>立即抢购</span><i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></a>'
            if is_in_stock else
            f'<a href="{tg_channel}" target="_blank" rel="nofollow noopener" class="inline-flex items-center justify-center px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-medium transition space-x-1.5 whitespace-nowrap">'
            f'<i class="fa-brands fa-telegram text-sky-500"></i><span>补货通知</span></a>'
        )

        card = f"""      <div class="bg-white rounded-2xl border border-slate-200/80 p-4 shadow-sm flex flex-col justify-between hover:shadow-md transition space-y-3.5">
        <div>
          <div class="flex items-start justify-between gap-2">
            <div class="space-y-1 flex-1 min-w-0">
              <div class="flex items-center space-x-1.5 flex-wrap gap-y-1">
                <span class="font-bold text-slate-900 text-sm sm:text-base leading-tight break-words">{name}</span>
                {rec_badge}
              </div>
              <div class="text-xs text-slate-500 font-medium mt-1 break-words leading-tight">
                <span class="text-[12px] text-slate-600">{circuit_type}</span>
              </div>
            </div>
            <div class="shrink-0">
              {stock_badge}
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2 bg-slate-50/80 rounded-xl p-2.5 text-xs">
          <div class="space-y-0.5">
            <span class="text-[10px] text-slate-400 uppercase font-semibold">计算 / 内存</span>
            <p class="font-semibold text-slate-800 break-words">{cpu} 核 / {memory}</p>
          </div>
          <div class="space-y-0.5">
            <span class="text-[10px] text-slate-400 uppercase font-semibold">高速 SSD</span>
            <p class="font-semibold text-slate-800 font-mono break-words">{ssd}</p>
          </div>
          <div class="space-y-0.5">
            <span class="text-[10px] text-slate-400 uppercase font-semibold">月流量</span>
            <p class="font-semibold text-slate-800 font-mono break-words">{band}</p>
          </div>
          <div class="space-y-0.5">
            <span class="text-[10px] text-slate-400 uppercase font-semibold">网络带宽</span>
            <p class="font-semibold text-slate-800 font-mono break-words">{bandwidth}</p>
          </div>
        </div>

        <div class="text-[11px] text-slate-600 leading-relaxed bg-slate-50/70 p-2.5 rounded-xl border border-slate-200/60 break-words">
          <div class="flex items-start space-x-1.5">
            <i class="fa-solid fa-location-dot text-blue-500 mt-0.5 shrink-0 text-[11px]"></i>
            <span class="leading-normal">{datacenter}</span>
          </div>
        </div>

        <div class="pt-2 border-t border-slate-100 flex items-center justify-between gap-2">
          <div class="min-w-0">
            <div class="text-[10px] text-slate-400 line-through font-mono">${raw_price:.2f}</div>
            <div class="flex items-baseline space-x-0.5">
              <span class="text-xl font-extrabold text-blue-600 font-mono">${disc_price}</span>
              <span class="text-xs text-slate-500 font-medium whitespace-nowrap">/{billing_cycle}</span>
            </div>
          </div>
          <div class="shrink-0">
            {btn}
          </div>
        </div>
      </div>"""
        cards.append(card)
    return "\n".join(cards)

def build_schema_json(products, config, in_stock_count, total_count):
    site_url = config.get("site", {}).get("url", "https://tianqiongshaonian.github.io/")
    brand_name = config.get("site", {}).get("brand_name", "搬瓦工库存监控")
    promo_code = config.get("affiliate", {}).get("promo_code", "BWHCXZAVFBVY")
    
    # 挑选推荐和热门产品构建 ItemList
    item_elements = []
    top_items = [p for p in products if p.get("recommended") == 1 or p.get("status") == 1][:12]
    for idx, item in enumerate(top_items, 1):
        price = item.get("price", "0")
        item_elements.append({
            "@type": "ListItem",
            "position": idx,
            "item": {
                "@type": "Product",
                "name": f"搬瓦工 BandwagonHost - {item.get('name', '')} ({item.get('circuit_type', '')})",
                "description": f"配置：{item.get('cpu', '')}核CPU / {item.get('memory', '')}内存 / {item.get('ssd', '')}SSD / {item.get('band', '')}月流量 / {item.get('bandwidth', '')}带宽。机房：{item.get('datacenter', '')}。使用优惠码 {promo_code} 立享 6.78% 折扣。",
                "offers": {
                    "@type": "Offer",
                    "price": str(price),
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock" if int(item.get("status", 0)) == 1 else "https://schema.org/OutOfStock",
                    "url": f"https://bwh81.net/aff.php?aff={config.get('affiliate',{}).get('aff_id','78613')}&pid={item.get('pid','')}&promocode={promo_code}"
                }
            }
        })

    schema_website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": brand_name,
        "url": site_url,
        "description": "全网最全搬瓦工(BandwagonHost)库存实时监控系统，覆盖香港CN2 GIA、日本软银/GIA、美西CN2 GIA-E、The Plan限量版等全系套餐，支持即时补货提醒与6.78%循环优惠码。",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{site_url}?q={{search_term_string}}"
            },
            "query-input": "required name=search_term_string"
        }
    }

    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "搬瓦工最新可用优惠码是多少？如何使用？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"当前搬瓦工全网最新且折扣力度最大的官方循环优惠码为 {promo_code}，结账时在购物车 Promotional Code 输入框粘贴并点击 Validate Code，即可立享 6.78% 循环折扣（续费同样享受折后价）。"
                }
            },
            {
                "@type": "Question",
                "name": "搬瓦工缺货了怎么办？如何第一时间接收补货通知？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"搬瓦工热门传家宝（如 The Plan、香港 CN2 GIA、美西限量版）补货频率不定期。本站每 10 分钟在云端自动探测库存，一旦发现有货将第一时间向 Telegram 补货频道 ({config.get('social',{}).get('tg_channel','https://t.me/bwg191')}) 自动推送提醒并置顶消息。"
                }
            },
            {
                "@type": "Question",
                "name": "搬瓦工支持免费更换机房和 IP 吗？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "支持。绝大多数 CN2 GIA-E 与 The Plan 套餐支持在 KiwiVM 控制面板点击 'Migrate to another DC' 一键免费迁移至其他机房（如在 DC6、DC9、日本软银、荷兰 9929 之间自由切换），系统会自动分配新机房 IP，数据完整保留且完全免费。"
                }
            },
            {
                "@type": "Question",
                "name": "电信、联通、移动网络分别推荐选择搬瓦工哪个机房？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "1. 电信用户：首选香港 CN2 GIA、日本东京 CN2 GIA 或美西洛杉矶 DC6/DC9 CN2 GIA-E；2. 联通用户：首选日本大阪软银 (Softbank)、荷兰 AS9929、美西 DC6 CN2 GIA-E；3. 移动用户：首选香港 CN2 GIA、美西 DC6 CN2 GIA-E。"
                }
            },
            {
                "@type": "Question",
                "name": "搬瓦工支持哪些支付方式？是否支持退款？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "搬瓦工官方全面支持支付宝 (Alipay)、微信支付、PayPal 以及各类银联/国际信用卡。新注册用户在购买首台 VPS 的 30 天内，只要未违反服务条款且 IP 正常，可在官网提交工单申请全额退款。"
                }
            }
        ]
    }

    schema_itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "搬瓦工热门高性价比 VPS 方案列表",
        "description": "精选搬瓦工最受欢迎的 CN2 GIA、日本软银及 The Plan 限量版套餐配置与实时库存",
        "numberOfItems": len(item_elements),
        "itemListElement": item_elements
    }

    return json.dumps([schema_website, schema_faq, schema_itemlist], ensure_ascii=False, indent=2)

def write_data_js(config, products):
    """生成前端运行时数据脚本 static/js/data.js。

    将最新配置与套餐数据注入全局变量 window.appConfig / window.appData，
    供静态页面引用的外部脚本 static/js/app.js 读取并水合交互界面。
    数据与逻辑彻底分离，index.html 不再内联任何脚本。
    """
    os.makedirs(os.path.dirname(DATA_JS_PATH), exist_ok=True)
    content = (
        "// 由 build.py 自动生成的运行时数据 (每次构建自动刷新，请勿手改)\n"
        "window.appConfig = " + json.dumps(config, ensure_ascii=False, indent=2) + ";\n"
        "window.appData = {\n  products: " + json.dumps(products, ensure_ascii=False, indent=2) + "\n};\n"
    )
    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] 成功生成 data.js (包含全局配置与 {len(products)} 款套餐数据)")

def generate_index_html():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
        prod_data = json.load(f)

    products = prod_data.get("products", prod_data) if isinstance(prod_data, dict) else prod_data
    updated_at = prod_data.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    in_stock_count = sum(1 for p in products if int(p.get("status", 0)) == 1)
    total_count = len(products)

    aff_id = str(config.get("affiliate", {}).get("aff_id", "78613"))
    promo_code = config.get("affiliate", {}).get("promo_code", "BWHCXZAVFBVY")
    disc_text = config.get("affiliate", {}).get("discount_text", "6.78% 循环优惠")
    disc_rate = float(config.get("affiliate", {}).get("discount_rate", 0.0678))
    tg_channel = config.get("social", {}).get("tg_channel", "https://t.me/bwg191")
    brand_name = config.get("site", {}).get("brand_name", "搬瓦工库存监控")
    site_title = config.get("site", {}).get("title", "搬瓦工库存监控 - BandwagonHost VPS 实时库存与全网补货通知")
    subtitle = config.get("site", {}).get("subtitle", "BandwagonHost Real-time Stock & Restock Monitor")
    site_url = config.get("site", {}).get("url", "https://tianqiongshaonian.github.io/")
    disclaimer = config.get("footer", {}).get("disclaimer", "免责声明：本站为第三方搬瓦工(BandwagonHost)库存监控工具，非官网运营。实际价格与配置请以结账页面为准。")

    table_rows_html = render_table_rows(products, aff_id, promo_code, disc_rate, tg_channel)
    cards_html = render_cards(products, aff_id, promo_code, disc_rate, tg_channel)
    schema_json_ld = build_schema_json(products, config, in_stock_count, total_count)

    # 将运行时数据(配置 + 套餐)独立打包到 static/js/data.js，HTML 只保留引用
    write_data_js(config, products)

    # 复制前端主脚本 frontend/js/app.js 到 static/js/app.js
    if os.path.exists(APP_JS_SRC):
        os.makedirs(os.path.dirname(APP_JS_DEST), exist_ok=True)
        shutil.copy2(APP_JS_SRC, APP_JS_DEST)
        print(f"[✓] 成功复制 app.js -> {APP_JS_DEST}")

    # ---- 由 frontend/templates/ 分区模板组装静态页面（静态模板与构建逻辑分离，产物仍为内联 SEO 完整页）----
    subs = {
        "{escape(site_title)}": escape(site_title),
        "{escape(site_url)}": escape(site_url),
        "{escape(brand_name)}": escape(brand_name),
        "{escape(subtitle)}": escape(subtitle),
        "{escape(tg_channel)}": escape(tg_channel),
        "{escape(updated_at)}": escape(updated_at),
        "{escape(disc_text)}": escape(disc_text),
        "{escape(promo_code)}": escape(promo_code),
        "{escape(disclaimer)}": escape(disclaimer),
        "{in_stock_count}": str(in_stock_count),
        "{total_count}": str(total_count),
        "{schema_json_ld}": schema_json_ld,
        "{cards_html}": cards_html,
        "{table_rows_html}": table_rows_html,
    }

    def render_partial(relpath):
        with open(os.path.join(PARTIALS_DIR, relpath), encoding="utf-8") as f:
            content = f.read().rstrip("\n")
        for token, value in subs.items():
            content = content.replace(token, value)
        return content

    html_content = "\n\n".join([
        render_partial("head.html"),
        render_partial("header.html"),
        render_partial("stat-cards.html"),
        render_partial("filter-bar.html"),
        render_partial("products.html"),
        render_partial("no-results.html"),
        render_partial("guide.html"),
        render_partial("faq.html"),
        render_partial("noscript.html"),
        render_partial("footer.html"),
        render_partial("toast.html"),
    ])

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[✓] 成功生成预渲染 index.html (包含 {len(products)} 款套餐及 Schema.org 结构化数据)")

def update_sitemap():
    utc_dt = datetime.now(timezone.utc)
    bj_dt = utc_dt + timedelta(hours=8)
    iso_time = bj_dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  <url>
    <loc>https://tianqiongshaonian.github.io/</loc>
    <lastmod>{iso_time}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"[✓] 成功更新 sitemap.xml (lastmod: {iso_time})")

if __name__ == "__main__":
    generate_index_html()
    update_sitemap()
