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
from datetime import datetime, timezone, timedelta

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")
PRODUCTS_PATH = os.path.join(PROJECT_ROOT, "products.json")
INDEX_PATH = os.path.join(PROJECT_ROOT, "index.html")
SITEMAP_PATH = os.path.join(PROJECT_ROOT, "sitemap.xml")

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
            f'<a href="{buy_url}" target="_blank" rel="nofollow noopener" onclick="onBuyClick(event)" class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition active:scale-95 space-x-1">'
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
            f'<a href="{buy_url}" target="_blank" rel="nofollow noopener" onclick="onBuyClick(event)" class="inline-flex items-center justify-center px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition active:scale-95 space-x-1.5 whitespace-nowrap">'
            f'<span>立即抢购</span><i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></a>'
            if is_in_stock else
            f'<a href="{tg_channel}" target="_blank" rel="nofollow noopener" class="inline-flex items-center justify-center px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-medium transition space-x-1.5 whitespace-nowrap">'
            f'<i class="fa-brands fa-telegram text-sky-500"></i><span>补货通知</span></a>'
        )

        card = f"""      <div class="bg-white rounded-2xl border border-slate-200/80 p-4 shadow-xs flex flex-col justify-between hover:shadow-md transition space-y-3.5">
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

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  
  <!-- 基础 SEO 核心元标签 -->
  <title id="pageTitle">{escape(site_title)}</title>
  <meta name="description" content="全网最全搬瓦工(BandwagonHost)库存实时监控系统，覆盖香港CN2 GIA、日本软银/GIA、美国CN2 GIA-E、The Plan限量版等全系套餐，支持多维度详细检索、即时补货提醒与6.78%循环优惠码。">
  <meta name="keywords" content="搬瓦工,搬瓦工库存,搬瓦工优惠码,BandwagonHost,CN2 GIA,The Plan,搬瓦工补货通知,搬瓦工DC6,搬瓦工DC9,香港CN2 GIA,日本软银,VPS库存监控">
  <meta name="author" content="{escape(brand_name)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="google-site-verification" content="Vi8ircfK8SuZNzZBrtU7av_aXeiUKrLDKgef-84unTM">
  <link rel="canonical" href="{escape(site_url)}">
  <meta name="theme-color" content="#2563eb">

  <!-- Open Graph 社交媒体分享协议 (微信/TG/Facebook等) -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(site_title)}">
  <meta property="og:description" content="全网最全搬瓦工(BandwagonHost)库存实时监控系统，实时更新78+款VPS库存状态与最新6.78%循环优惠码。">
  <meta property="og:url" content="{escape(site_url)}">
  <meta property="og:site_name" content="{escape(brand_name)}">
  <meta property="og:image" content="{escape(site_url)}apple-touch-icon.png">
  <meta property="og:locale" content="zh_CN">

  <!-- Twitter Cards 标签 -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(site_title)}">
  <meta name="twitter:description" content="全网最全搬瓦工(BandwagonHost)库存实时监控系统，实时更新78+款VPS库存与最新优惠码。">
  <meta name="twitter:image" content="{escape(site_url)}apple-touch-icon.png">

  <!-- 网站图标 Favicon -->
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">

  <!-- 本地化编译后的独立 Tailwind CSS (消除 CDN 警告，提升秒开速度) -->
  <link rel="stylesheet" href="static/css/tailwind.min.css">
  <!-- 本地化 Font Awesome 6 图标与字体资源 -->
  <link rel="stylesheet" href="static/fontawesome/css/all.min.css">

  <!-- Schema.org 结构化数据 (JSON-LD) - 极大提升 Google 搜索富媒体展示与 AI 抓取解析 -->
  <script type="application/ld+json">
{schema_json_ld}
  </script>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col font-sans selection:bg-blue-500 selection:text-white">

  <!-- 顶部导航栏 (宽屏 1600px 自适应) -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs backdrop-blur-md bg-white/95">
    <div class="max-w-[1600px] mx-auto px-3 sm:px-5 lg:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20 shrink-0">
          <i class="fa-solid fa-server text-lg"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 id="brandName" class="text-base sm:text-lg font-bold text-slate-900 leading-tight">{escape(brand_name)}</h1>
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-dot mr-1"></span>实时
            </span>
          </div>
          <p id="brandSubtitle" class="text-xs text-slate-400 hidden sm:block">{escape(subtitle)}</p>
        </div>
      </div>

      <div class="flex items-center space-x-2 sm:space-x-3">
        <a id="tgChannelBtn" href="{escape(tg_channel)}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-sky-50 text-sky-600 hover:bg-sky-100 text-xs sm:text-sm font-medium transition duration-150 border border-sky-200/60">
          <i class="fa-brands fa-telegram text-sky-500 text-sm"></i>
          <span class="hidden xs:inline sm:inline">TG 频道</span>
        </a>
        <button onclick="copyPromoCode()" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-blue-600 text-white hover:bg-blue-700 text-xs sm:text-sm font-medium shadow-sm transition duration-150 active:scale-95">
          <i class="fa-solid fa-tags"></i>
          <span>优惠码</span>
        </button>
      </div>
    </div>
  </header>

  <!-- 主体内容 (宽屏 1600px) -->
  <main class="max-w-[1600px] mx-auto px-3 sm:px-5 lg:px-6 py-4 sm:py-5 flex-1 w-full space-y-4">

    <!-- 顶部状态与优惠码卡片 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
      
      <!-- 统计卡片 1: 实时库存 -->
      <div class="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200/80 shadow-xs flex items-center justify-between">
        <div class="space-y-0.5 sm:space-y-1">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">实时库存情况</span>
          <div class="flex items-baseline space-x-2">
            <span id="statInStock" class="text-2xl sm:text-3xl font-black text-emerald-600">{in_stock_count}</span>
            <span class="text-xs sm:text-sm text-slate-400 font-medium">/ <span id="statTotal">{total_count}</span> 款有货</span>
          </div>
        </div>
        <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-lg sm:text-xl shrink-0">
          <i class="fa-solid fa-box-open"></i>
        </div>
      </div>

      <!-- 统计卡片 2: 最后更新 -->
      <div class="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200/80 shadow-xs flex items-center justify-between">
        <div class="space-y-0.5 sm:space-y-1">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">最新探测时间 (北京时间)</span>
          <div class="flex items-center space-x-2 text-slate-800 font-medium text-xs sm:text-sm">
            <span class="w-2 h-2 rounded-full bg-emerald-500 pulse-dot inline-block shrink-0"></span>
            <span id="statUpdatedTime" class="font-semibold text-slate-700 truncate">{escape(updated_at)}</span>
          </div>
        </div>
        <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center text-lg sm:text-xl shrink-0">
          <i class="fa-solid fa-clock-rotate-left"></i>
        </div>
      </div>

      <!-- 统计卡片 3: 优惠码一键复制 -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 sm:p-5 rounded-2xl text-white shadow-sm flex items-center justify-between sm:col-span-2 lg:col-span-1">
        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <span class="text-xs font-semibold text-blue-100 uppercase tracking-wider">最新循环优惠码</span>
            <span id="discountTag" class="px-2 py-0.5 rounded-full bg-white/20 text-[11px] font-medium text-white">{escape(disc_text)}</span>
          </div>
          <div class="flex items-center space-x-2 pt-0.5">
            <code id="promoCodeText" class="text-lg sm:text-xl font-mono font-bold tracking-wider text-amber-200">{escape(promo_code)}</code>
            <button onclick="copyPromoCode()" id="copyBtn" class="px-2.5 py-1 rounded-md bg-white text-blue-700 hover:bg-blue-50 text-xs font-semibold transition active:scale-95 flex items-center space-x-1 shadow-xs shrink-0">
              <i class="fa-regular fa-copy"></i>
              <span id="copyBtnLabel">复制</span>
            </button>
          </div>
        </div>
        <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-xl bg-white/15 text-white flex items-center justify-center text-lg sm:text-xl shrink-0">
          <i class="fa-solid fa-ticket"></i>
        </div>
      </div>

    </div>

    <!-- 筛选、搜索与视图切换控制栏 -->
    <div class="bg-white rounded-2xl border border-slate-200/80 p-3.5 sm:p-4 shadow-xs space-y-3">
      
      <!-- 分类 Tab 栏 (移动端支持横向平滑滑动) -->
      <div class="flex items-center space-x-1.5 overflow-x-auto custom-scrollbar pb-1 text-xs sm:text-sm font-medium" id="categoryTabs">
        <button data-tag="all" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl bg-blue-600 text-white whitespace-nowrap transition">全部方案</button>
        <button data-tag="instock" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition flex items-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-500 inline-block shrink-0"></span>
          <span>仅看有货</span>
        </button>
        <button data-tag="recommend" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition">⭐️ 热门推荐</button>
        <button data-tag="limited" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition">⚡️ 限量版</button>
        <button data-tag="hk" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition">🇭🇰 香港</button>
        <button data-tag="japan" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition">🇯🇵 日本</button>
        <button data-tag="cn2gia" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition">🇺🇸 CN2 GIA-E</button>
        <button data-tag="singapore" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition">🇸🇬 新加坡</button>
        <button data-tag="kvm" class="tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition">常规 KVM</button>
      </div>

      <!-- 详细搜索与排序筛选栏 -->
      <div class="pt-2 border-t border-slate-100 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-2.5">
        
        <!-- 超级详细搜索框 (支持多关键词空格分词) -->
        <div class="relative flex-1">
          <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs sm:text-sm"></i>
          <input 
            type="text" 
            id="searchInput" 
            placeholder="搜索支持空格分词: 如 '香港 1T' / 'DC6 2G' / 'PID 44' / '2核 40G' / '有货'..." 
            class="w-full pl-9 pr-8 py-2 text-xs sm:text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
          />
          <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 w-5 h-5 flex items-center justify-center rounded-full text-xs">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>

        <!-- 排序 & 视图切换器 -->
        <div class="flex items-center space-x-2 self-end md:self-auto w-full md:w-auto justify-between md:justify-end">
          
          <!-- 匹配数量统计 -->
          <div class="text-xs text-slate-400 font-medium px-1">
            匹配: <span id="matchCount" class="text-blue-600 font-bold">{total_count}</span> 款
          </div>

          <!-- 排序下拉 -->
          <div class="relative">
            <select id="sortSelect" onchange="changeSort(this.value)" class="appearance-none bg-slate-50 border border-slate-200 text-slate-700 text-xs rounded-xl pl-3 pr-7 py-2 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 cursor-pointer">
              <option value="default">默认排序</option>
              <option value="price-asc">价格：从低到高 ⬆️</option>
              <option value="price-desc">价格：从高到低 ⬇️</option>
              <option value="mem-asc">内存：从小到大</option>
              <option value="mem-desc">内存：从大到小</option>
            </select>
            <i class="fa-solid fa-chevron-down absolute right-2.5 top-1/2 -translate-y-1/2 text-[10px] text-slate-400 pointer-events-none"></i>
          </div>

          <!-- 视图切换 (桌面端/移动端可选卡片或表格) -->
          <div class="bg-slate-100 p-0.5 rounded-xl flex items-center">
            <button id="viewCardBtn" onclick="switchView('card')" title="卡片视图" class="px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:text-slate-900 transition">
              <i class="fa-solid fa-grip"></i>
            </button>
            <button id="viewTableBtn" onclick="switchView('table')" title="表格视图" class="px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:text-slate-900 transition">
              <i class="fa-solid fa-table-list"></i>
            </button>
          </div>

        </div>

      </div>

    </div>

    <!-- ==================== 1. 移动端/平板/宽屏 现代卡片流视图 (静态预渲染，爬虫与AI直读) ==================== -->
    <div id="cardViewContainer" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
{cards_html}
    </div>

    <!-- ==================== 2. PC / 宽屏 经典数据表格视图 (静态预渲染) ==================== -->
    <div id="tableViewContainer" class="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-left text-xs sm:text-sm text-slate-600">
          <thead class="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200/80 text-[11px] sm:text-xs uppercase tracking-wider">
            <tr>
              <th scope="col" class="py-3 px-3 sm:px-4 min-w-[200px]">套餐方案 / 线路</th>
              <th scope="col" class="py-3 px-2 sm:px-3 whitespace-nowrap">CPU / 内存 / SSD</th>
              <th scope="col" class="py-3 px-2 sm:px-3 whitespace-nowrap">流量 / 带宽</th>
              <th scope="col" class="py-3 px-2 sm:px-3">可选机房</th>
              <th scope="col" class="py-3 px-2 sm:px-3 text-right whitespace-nowrap">原价</th>
              <th scope="col" class="py-3 px-2 sm:px-3 text-right whitespace-nowrap">折后价</th>
              <th scope="col" class="py-3 px-2 sm:px-3 text-center whitespace-nowrap">库存状态</th>
              <th scope="col" class="py-3 px-3 sm:px-4 text-center whitespace-nowrap">直达抢购</th>
            </tr>
          </thead>
          <tbody id="productTableBody" class="divide-y divide-slate-100">
{table_rows_html}
          </tbody>
        </table>
      </div>
    </div>

    <!-- 无搜索结果友好提示 -->
    <div id="noResults" class="hidden bg-white rounded-2xl border border-slate-200/80 p-12 text-center">
      <div class="w-16 h-16 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto text-2xl mb-3">
        <i class="fa-solid fa-inbox"></i>
      </div>
      <h3 class="text-base font-semibold text-slate-800">未找到匹配的 VPS 方案</h3>
      <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">请尝试调整搜索关键词（如减少筛选条件、搜索套餐名称或机房别名）</p>
      <button onclick="clearSearch()" class="mt-4 px-4 py-2 bg-blue-50 text-blue-600 hover:bg-blue-100 text-xs font-semibold rounded-xl transition">
        清空搜索条件
      </button>
    </div>

    <!-- ==================== 3. 搬瓦工 VPS 选购指南与机房线路深度解析 (SEO/AI 语义强化) ==================== -->
    <section class="bg-white rounded-2xl border border-slate-200/80 p-5 sm:p-6 shadow-xs space-y-4">
      <div class="flex items-center space-x-2.5 pb-3 border-b border-slate-100">
        <div class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
          <i class="fa-solid fa-compass text-base"></i>
        </div>
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 leading-tight">搬瓦工 (BandwagonHost) 选购指南与核心机房线路解析</h2>
          <p class="text-xs text-slate-400">针对电信 CN2 GIA、联通 9929/软银与移动 CMI 直连线路的详细实测与选购建议</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5 pt-1 text-xs">
        
        <!-- 机房卡片 1 -->
        <div class="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60 space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-sm flex items-center">
              <span class="mr-1.5">🇭🇰</span>香港 CN2 GIA
            </span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-100 text-blue-700">顶级极速</span>
          </div>
          <p class="text-slate-600 leading-relaxed">
            机房代码 <code class="font-mono text-slate-700 bg-white px-1 py-0.5 rounded border border-slate-200">HKHK_8</code>，三网双向直连，国内延迟仅 <strong>10~30ms</strong>，体验媲美境内服务器。适合预算充裕、追求超低延迟的极速建站与外贸业务。
          </p>
        </div>

        <!-- 机房卡片 2 -->
        <div class="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60 space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-sm flex items-center">
              <span class="mr-1.5">🇯🇵</span>日本东京/大阪
            </span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-700">亚太优选</span>
          </div>
          <p class="text-slate-600 leading-relaxed">
            东京 <code class="font-mono text-slate-700 bg-white px-1 py-0.5 rounded border border-slate-200">TYO_8</code> (CN2 GIA) 与大阪 <code class="font-mono text-slate-700 bg-white px-1 py-0.5 rounded border border-slate-200">JPOS_1</code> (软银 Softbank)。亚太超低延迟 <strong>40~60ms</strong>，联通及北方宽带体验极佳。
          </p>
        </div>

        <!-- 机房卡片 3 -->
        <div class="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60 space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-sm flex items-center">
              <span class="mr-1.5">🇺🇸</span>美西 DC6 / DC9
            </span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-100 text-amber-800">性价比王</span>
          </div>
          <p class="text-slate-600 leading-relaxed">
            洛杉矶 <code class="font-mono text-slate-700 bg-white px-1 py-0.5 rounded border border-slate-200">USCA_6</code> (最高 10Gbps CN2 GIA-E 带宽) 与 <code class="font-mono text-slate-700 bg-white px-1 py-0.5 rounded border border-slate-200">USCA_9</code>，晚高峰极度稳定，大流量与全天候主力机首选。
          </p>
        </div>

        <!-- 机房卡片 4 -->
        <div class="p-4 rounded-xl bg-slate-50/80 border border-slate-200/60 space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-sm flex items-center">
              <span class="mr-1.5">⚡️</span>The Plan 传家宝
            </span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-purple-100 text-purple-700">自由切换</span>
          </div>
          <p class="text-slate-600 leading-relaxed">
            搬瓦工爆款限量版神机，支持多达 <strong>17+ 个机房免费自由迁移</strong>（含香港、日本软银、美西双 GIA、荷兰 9929 等），2核/2G/40G/1000G，补货必抢。
          </p>
        </div>

      </div>
    </section>

    <!-- ==================== 4. 搬瓦工常见问题解答 (FAQ) ==================== -->
    <section class="bg-white rounded-2xl border border-slate-200/80 p-5 sm:p-6 shadow-xs space-y-4">
      <div class="flex items-center space-x-2.5 pb-3 border-b border-slate-100">
        <div class="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
          <i class="fa-solid fa-circle-question text-base"></i>
        </div>
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 leading-tight">搬瓦工购买与使用常见问题 (FAQ)</h2>
          <p class="text-xs text-slate-400">整理新手购买搬瓦工 VPS 最常遇到的优惠码、机房更换与售后政策解答</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs leading-relaxed text-slate-600">
        
        <div class="p-4 rounded-xl bg-slate-50/70 border border-slate-100 space-y-1.5">
          <h3 class="font-bold text-slate-800 text-sm flex items-center">
            <i class="fa-solid fa-ticket text-blue-500 mr-2 text-xs"></i>搬瓦工最新可用优惠码是多少？如何使用？
          </h3>
          <p>
            当前全网力度最大的官方循环优惠码为 <code class="font-mono font-bold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200">{escape(promo_code)}</code>。在结算页面的 <span class="font-medium text-slate-700">Promotional Code</span> 处输入并点击 Validate Code，即可立减 <strong>6.78%</strong>（续费循环享受同样折扣）。
          </p>
        </div>

        <div class="p-4 rounded-xl bg-slate-50/70 border border-slate-100 space-y-1.5">
          <h3 class="font-bold text-slate-800 text-sm flex items-center">
            <i class="fa-brands fa-telegram text-sky-500 mr-2 text-xs"></i>心仪的套餐缺货了怎么办？
          </h3>
          <p>
            搬瓦工的热门限量套餐（如 The Plan、CN2 GIA 限量版）不定期补货。你可以加入我们的 Telegram 补货通知频道 <a href="{escape(tg_channel)}" target="_blank" rel="noopener noreferrer" class="text-sky-600 hover:underline font-medium">@bwg191</a>，一旦监测到补货上线将毫秒级自动推送并置顶提醒。
          </p>
        </div>

        <div class="p-4 rounded-xl bg-slate-50/70 border border-slate-100 space-y-1.5">
          <h3 class="font-bold text-slate-800 text-sm flex items-center">
            <i class="fa-solid fa-arrows-rotate text-emerald-500 mr-2 text-xs"></i>购买后可以免费更换机房或更换 IP 吗？
          </h3>
          <p>
            支持。登录搬瓦工 KiwiVM 控制面板，在侧边栏点击 <span class="font-medium text-slate-700">Migrate to another DC</span> 即可一键迁移至套餐支持的其他机房，系统会自动分配新机房的独立 IP，原有数据和配置完全保留且完全免费。
          </p>
        </div>

        <div class="p-4 rounded-xl bg-slate-50/70 border border-slate-100 space-y-1.5">
          <h3 class="font-bold text-slate-800 text-sm flex items-center">
            <i class="fa-solid fa-credit-card text-purple-500 mr-2 text-xs"></i>支持哪些付款方式？有退款保障吗？
          </h3>
          <p>
            搬瓦工官方原生支持 <strong>支付宝 (Alipay)、微信支付、PayPal 及各类国际/银联信用卡</strong>。新用户首次购买 30 天内，在 IP 正常且未违反 TOS 的前提下，可在官网后台直接发起工单申请全额退款。
          </p>
        </div>

      </div>
    </section>

    <!-- NoScript 纯静态降级友好保障 (针对完全关闭 JS 的用户和极简爬虫) -->
    <noscript>
      <div class="bg-amber-50 border border-amber-200 rounded-2xl p-5 text-amber-800 text-xs leading-relaxed space-y-2">
        <p class="font-bold text-sm">💡 温馨提示：检测到您的浏览器未开启 JavaScript</p>
        <p>页面已自动为您展现完整的静态 VPS 套餐与价格列表。当前最新循环优惠码为：<strong>{escape(promo_code)}</strong>（享受 {escape(disc_text)}）。如需使用即时搜索、排序与实时筛选功能，请开启浏览器的 JavaScript 支持。</p>
      </div>
    </noscript>

  </main>

  <!-- 底部 Footer (由 config.json 动态驱动) -->
  <footer class="bg-white border-t border-slate-200 mt-12 py-8 text-center text-xs text-slate-400 space-y-2">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 space-y-1.5">
      <div class="flex items-center justify-center space-x-4 text-slate-500 font-medium pb-1">
        <a href="{escape(site_url)}" class="hover:text-blue-600 transition">监控首页</a>
        <span>•</span>
        <a href="sitemap.xml" target="_blank" class="hover:text-blue-600 transition">站点地图 (Sitemap)</a>
        <span>•</span>
        <a href="llms.txt" target="_blank" class="hover:text-blue-600 transition">AI 规范 (llms.txt)</a>
        <span>•</span>
        <a href="{escape(tg_channel)}" target="_blank" rel="noopener noreferrer" class="hover:text-sky-600 transition">Telegram 补货推送</a>
      </div>
      <p id="footerBrand" class="font-medium text-slate-500">{escape(brand_name)} - BandwagonHost 全方案库存与补货推送系统</p>
      <p id="footerDisclaimer" class="text-slate-400 max-w-2xl mx-auto">{escape(disclaimer)}</p>
    </div>
  </footer>

  <!-- Toast 消息提示 -->
  <div id="toast" class="fixed bottom-6 right-6 bg-slate-900/90 backdrop-blur-md text-white text-xs sm:text-sm px-4 py-2.5 rounded-xl shadow-xl transform translate-y-16 opacity-0 transition-all duration-300 pointer-events-none flex items-center space-x-2 z-50">
    <i class="fa-solid fa-circle-check text-emerald-400"></i>
    <span id="toastMessage">已成功复制</span>
  </div>

  <script>
    let appConfig = {json.dumps(config, ensure_ascii=False, indent=6)};

    let appData = {{
      products: {json.dumps(products, ensure_ascii=False)}
    }};

    let currentTag = 'all';
    let searchQuery = '';
    
    // 从 localStorage 读取用户偏好（排序与视图模式）
    let currentSort = localStorage.getItem('bwh_stock_sort') || 'default';
    let currentView = localStorage.getItem('bwh_stock_view') || (window.innerWidth < 1024 ? 'card' : 'table');

    // 初始化：同时加载 config.json 和 products.json
    async function init() {{
      // 还原排序下拉选框状态
      const sortSelect = document.getElementById('sortSelect');
      if (sortSelect) sortSelect.value = currentSort;

      updateViewToggleButtons();
      renderAll();

      await loadData();
      // 每隔 60 秒在后台静默拉取一次最新数据，无需用户手动刷新
      setInterval(loadData, 60000);
    }}

    async function loadData() {{
      const timestamp = new Date().getTime();
      
      // 1. 加载公共配置文件 config.json (防缓存)
      try {{
        const confRes = await fetch(`config.json?t=${{timestamp}}`, {{ cache: 'no-cache' }});
        if (confRes.ok) {{
          const loadedConf = await confRes.json();
          appConfig = Object.assign(appConfig, loadedConf);
          applyConfig(appConfig);
        }}
      }} catch (e) {{
        console.warn('使用内置默认 config 配置:', e);
      }}

      // 2. 加载最新库存数据 products.json (防缓存)
      try {{
        const prodRes = await fetch(`products.json?t=${{timestamp}}`, {{ cache: 'no-cache' }});
        if (!prodRes.ok) throw new Error('网络请求异常');
        const prodData = await prodRes.json();
        
        appData.products = prodData.products || prodData || [];

        if (prodData.updated_at) {{
          document.getElementById('statUpdatedTime').textContent = prodData.updated_at;
        }}

        renderStats();
        renderAll();
      }} catch (err) {{
        console.error('加载 products.json 失败:', err);
      }}
    }}

    // 将 config.json 的设置应用到 DOM
    function applyConfig(cfg) {{
      if (cfg.site) {{
        if (cfg.site.title) document.title = cfg.site.title;
        if (cfg.site.brand_name) document.getElementById('brandName').textContent = cfg.site.brand_name;
        if (cfg.site.subtitle) document.getElementById('brandSubtitle').textContent = cfg.site.subtitle;
      }}
      if (cfg.affiliate) {{
        if (cfg.affiliate.promo_code) document.getElementById('promoCodeText').textContent = cfg.affiliate.promo_code;
        if (cfg.affiliate.discount_text) document.getElementById('discountTag').textContent = cfg.affiliate.discount_text;
      }}
      if (cfg.social && cfg.social.tg_channel) {{
        document.getElementById('tgChannelBtn').href = cfg.social.tg_channel;
      }}
      if (cfg.footer && cfg.footer.disclaimer) {{
        document.getElementById('footerDisclaimer').textContent = cfg.footer.disclaimer;
      }}
    }}

    // 统计面板 (类型安全转换)
    function renderStats() {{
      const total = appData.products.length;
      const inStock = appData.products.filter(p => Number(p.status) === 1).length;
      document.getElementById('statTotal').textContent = total;
      document.getElementById('statInStock').textContent = inStock;
    }}

    // 深度分词多条件搜索引擎
    function getFilteredAndSortedProducts() {{
      let filtered = appData.products.filter(item => {{
        const isItemInStock = Number(item.status) === 1;
        const isItemRecommended = Number(item.recommended) === 1;

        if (currentTag === 'instock' && !isItemInStock) return false;
        if (currentTag === 'recommend' && !isItemRecommended) return false;
        if (currentTag !== 'all' && currentTag !== 'instock' && currentTag !== 'recommend') {{
          if (!item.tags || !item.tags.includes(currentTag)) return false;
        }}
        return true;
      }});

      if (searchQuery.trim()) {{
        const terms = searchQuery.trim().toLowerCase().split(/\\s+/);
        
        filtered = filtered.filter(item => {{
          const statusText = Number(item.status) === 1 ? "有货 in stock instock 现货 补货" : "缺货 out of stock outofstock 售罄";
          const recommendText = Number(item.recommended) === 1 ? "推荐 热门 hot recommend" : "";
          
          let aliases = "";
          const dc = (item.datacenter || "").toLowerCase();
          const circuit = (item.circuit_type || "").toLowerCase();
          const name = (item.name || "").toLowerCase();

          if (dc.includes("hk") || circuit.includes("hk") || name.includes("hk")) aliases += " 香港 hongkong hk ";
          if (dc.includes("dc6") || dc.includes("dc9") || circuit.includes("gia-e") || circuit.includes("gia")) aliases += " 美西 美国洛杉矶 la us usa cn2gia ";
          if (dc.includes("tokyo") || dc.includes("osaka") || circuit.includes("tokyo") || circuit.includes("osaka") || name.includes("tokyo") || name.includes("osaka")) aliases += " 日本 东京 大阪 japan jp softbank 软银 ";
          if (dc.includes("sg") || circuit.includes("sg") || name.includes("sg")) aliases += " 新加坡 singapore sg ";
          if (dc.includes("dubai") || circuit.includes("dubai")) aliases += " 迪拜 dubai ";
          if (dc.includes("amsterdam") || circuit.includes("amsterdam") || name.includes("amsterdam")) aliases += " 荷兰 阿姆斯特丹 nl ";
          if (name.includes("plan") || circuit.includes("plan") || name.includes("chicken") || name.includes("box")) aliases += " 传家宝 神机 限量版 limited ";

          const fullIndex = [
            item.name || '',
            item.pid || '',
            'pid:' + item.pid,
            item.circuit_type || '',
            item.datacenter || '',
            item.cpu ? `${{item.cpu}}核 ${{item.cpu}}core ${{item.cpu}}c` : '',
            item.memory || '',
            item.ssd || '',
            item.band || '',
            item.bandwidth || '',
            item.price || '',
            `$${{item.price}}`,
            statusText,
            recommendText,
            aliases
          ].join(' ').toLowerCase();

          return terms.every(term => fullIndex.includes(term));
        }});
      }}

      if (currentSort === 'price-asc') {{
        filtered.sort((a, b) => (parseFloat(a.price) || 0) - (parseFloat(b.price) || 0));
      }} else if (currentSort === 'price-desc') {{
        filtered.sort((a, b) => (parseFloat(b.price) || 0) - (parseFloat(a.price) || 0));
      }} else if (currentSort === 'mem-asc') {{
        filtered.sort((a, b) => parseMemoryMB(a.memory) - parseMemoryMB(b.memory));
      }} else if (currentSort === 'mem-desc') {{
        filtered.sort((a, b) => parseMemoryMB(b.memory) - parseMemoryMB(a.memory));
      }}

      return filtered;
    }}

    function parseMemoryMB(memStr) {{
      if (!memStr) return 0;
      const str = String(memStr).toUpperCase();
      const val = parseFloat(str) || 0;
      if (str.includes('G')) return val * 1024;
      return val;
    }}

    function renderAll() {{
      const filtered = getFilteredAndSortedProducts();
      const matchCountEl = document.getElementById('matchCount');
      if (matchCountEl) matchCountEl.textContent = filtered.length;

      const noResults = document.getElementById('noResults');
      const tableContainer = document.getElementById('tableViewContainer');
      const cardContainer = document.getElementById('cardViewContainer');

      if (filtered.length === 0) {{
        tableContainer.classList.add('hidden');
        cardContainer.classList.add('hidden');
        noResults.classList.remove('hidden');
        return;
      }}

      noResults.classList.add('hidden');

      if (currentView === 'table') {{
        tableContainer.classList.remove('hidden');
        cardContainer.classList.add('hidden');
        renderTable(filtered);
      }} else {{
        tableContainer.classList.add('hidden');
        cardContainer.classList.remove('hidden');
        renderCards(filtered);
      }}
    }}

    function renderTable(products) {{
      const tbody = document.getElementById('productTableBody');
      const affId = appConfig.affiliate?.aff_id || '78613';
      const discRate = appConfig.affiliate?.discount_rate || 0.0678;
      const promoCode = appConfig.affiliate?.promo_code || 'BWHCXZAVFBVY';
      const tgChannel = appConfig.social?.tg_channel || 'https://t.me/bwg191';

      const rows = products.map(item => {{
        const isInStock = Number(item.status) === 1;
        const buyUrl = `https://bwh81.net/aff.php?aff=${{encodeURIComponent(affId)}}&pid=${{encodeURIComponent(item.pid)}}&promocode=${{encodeURIComponent(promoCode)}}`;
        const rawPrice = parseFloat(item.price) || 0;
        const discPrice = (rawPrice * (1 - discRate)).toFixed(2);
        const billingCycle = item.billing_cycle || '年付';

        const recommendBadge = Number(item.recommended) === 1 
          ? '<span class="inline-flex items-center shrink-0 whitespace-nowrap px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-50 text-amber-700 border border-amber-200/60 ml-2"><i class="fa-solid fa-fire text-amber-500 mr-1 text-[10px]"></i>热门推荐</span>' 
          : '';

        return `
          <tr class="hover:bg-slate-50/80 transition group">
            <td class="py-3 px-3 sm:px-4">
              <div class="font-semibold text-slate-900 flex items-center whitespace-nowrap">
                <span class="truncate max-w-[180px] sm:max-w-none">${{escapeHtml(item.name)}}</span>
                ${{recommendBadge}}
              </div>
              <div class="text-xs text-slate-500 mt-0.5 whitespace-nowrap">
                <span class="truncate max-w-[200px] text-[11px]">${{escapeHtml(item.circuit_type)}}</span>
              </div>
            </td>
            <td class="py-3 px-2 sm:px-3 whitespace-nowrap">
              <div class="text-slate-800 font-medium">${{escapeHtml(item.cpu)}} 核 / ${{escapeHtml(item.memory)}}</div>
              <div class="text-[11px] text-slate-400 font-mono">${{escapeHtml(item.ssd)}} SSD</div>
            </td>
            <td class="py-3 px-2 sm:px-3 whitespace-nowrap">
              <div class="text-slate-800 font-medium">${{escapeHtml(item.band)}}</div>
              <div class="text-[11px] text-slate-400">${{escapeHtml(item.bandwidth)}}</div>
            </td>
            <td class="py-3 px-2 sm:px-3 max-w-[240px]">
              <div class="text-xs text-slate-600 line-clamp-2 leading-relaxed" title="${{escapeHtml(item.datacenter)}}">
                ${{escapeHtml(item.datacenter || '常规节点')}}
              </div>
            </td>
            <td class="py-3 px-2 sm:px-3 text-right whitespace-nowrap font-mono text-slate-400">
              <span class="line-through text-xs">$${{escapeHtml(item.price)}}</span>
            </td>
            <td class="py-3 px-2 sm:px-3 text-right whitespace-nowrap font-mono">
              <span class="text-base font-bold text-blue-600">$${{escapeHtml(discPrice)}}</span>
              <span class="text-[10px] text-slate-400 block -mt-1">/${{escapeHtml(billingCycle)}}</span>
            </td>
            <td class="py-3 px-2 sm:px-3 text-center whitespace-nowrap">
              ${{
                isInStock 
                  ? '<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/80"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-dot mr-1.5"></span>有货</span>'
                  : '<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-rose-50 text-rose-600 border border-rose-200/80">缺货</span>'
              }}
            </td>
            <td class="py-3 px-3 sm:px-4 text-center whitespace-nowrap">
              ${{
                isInStock
                  ? `<a href="${{buyUrl}}" target="_blank" rel="nofollow noopener" onclick="onBuyClick(event)" class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition active:scale-95 space-x-1">
                      <span>立即抢购</span>
                      <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>`
                  : `<a href="${{escapeHtml(tgChannel)}}" target="_blank" rel="nofollow noopener" class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-medium transition space-x-1">
                      <i class="fa-brands fa-telegram text-sky-500"></i>
                      <span>补货通知</span>
                    </a>`
              }}
            </td>
          </tr>
        `;
      }}).join('');
      tbody.innerHTML = rows;
    }}

    function renderCards(products) {{
      const container = document.getElementById('cardViewContainer');
      const affId = appConfig.affiliate?.aff_id || '78613';
      const discRate = appConfig.affiliate?.discount_rate || 0.0678;
      const promoCode = appConfig.affiliate?.promo_code || 'BWHCXZAVFBVY';
      const tgChannel = appConfig.social?.tg_channel || 'https://t.me/bwg191';

      const cards = products.map(item => {{
        const isInStock = Number(item.status) === 1;
        const buyUrl = `https://bwh81.net/aff.php?aff=${{encodeURIComponent(affId)}}&pid=${{encodeURIComponent(item.pid)}}&promocode=${{encodeURIComponent(promoCode)}}`;
        const rawPrice = parseFloat(item.price) || 0;
        const discPrice = (rawPrice * (1 - discRate)).toFixed(2);
        const billingCycle = item.billing_cycle || '年付';

        const recommendBadge = Number(item.recommended) === 1 
          ? '<span class="inline-flex items-center shrink-0 whitespace-nowrap px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-50 text-amber-700 border border-amber-200/60"><i class="fa-solid fa-fire text-amber-500 mr-1"></i>推荐</span>' 
          : '';

        return `
          <div class="bg-white rounded-2xl border border-slate-200/80 p-4 shadow-xs flex flex-col justify-between hover:shadow-md transition space-y-3.5">
            <div>
              <div class="flex items-start justify-between gap-2">
                <div class="space-y-1 flex-1 min-w-0">
                  <div class="flex items-center space-x-1.5 flex-wrap gap-y-1">
                    <span class="font-bold text-slate-900 text-sm sm:text-base leading-tight break-words">${{escapeHtml(item.name)}}</span>
                    ${{recommendBadge}}
                  </div>
                  <div class="text-xs text-slate-500 font-medium mt-1 break-words leading-tight">
                    <span class="text-[12px] text-slate-600">${{escapeHtml(item.circuit_type)}}</span>
                  </div>
                </div>

                <div class="shrink-0">
                  ${{
                    isInStock
                      ? '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-dot mr-1"></span>有货</span>'
                      : '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-rose-50 text-rose-600 border border-rose-200">缺货</span>'
                  }}
                </div>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2 bg-slate-50/80 rounded-xl p-2.5 text-xs">
              <div class="space-y-0.5">
                <span class="text-[10px] text-slate-400 uppercase font-semibold">计算 / 内存</span>
                <p class="font-semibold text-slate-800 break-words">${{escapeHtml(item.cpu)}} 核 / ${{escapeHtml(item.memory)}}</p>
              </div>
              <div class="space-y-0.5">
                <span class="text-[10px] text-slate-400 uppercase font-semibold">高速 SSD</span>
                <p class="font-semibold text-slate-800 font-mono break-words">${{escapeHtml(item.ssd)}}</p>
              </div>
              <div class="space-y-0.5">
                <span class="text-[10px] text-slate-400 uppercase font-semibold">月流量</span>
                <p class="font-semibold text-slate-800 font-mono break-words">${{escapeHtml(item.band)}}</p>
              </div>
              <div class="space-y-0.5">
                <span class="text-[10px] text-slate-400 uppercase font-semibold">网络带宽</span>
                <p class="font-semibold text-slate-800 font-mono break-words">${{escapeHtml(item.bandwidth)}}</p>
              </div>
            </div>

            <div class="text-[11px] text-slate-600 leading-relaxed bg-slate-50/70 p-2.5 rounded-xl border border-slate-200/60 break-words">
              <div class="flex items-start space-x-1.5">
                <i class="fa-solid fa-location-dot text-blue-500 mt-0.5 shrink-0 text-[11px]"></i>
                <span class="leading-normal">${{escapeHtml(item.datacenter || '常规全球机房')}}</span>
              </div>
            </div>

            <div class="pt-2 border-t border-slate-100 flex items-center justify-between gap-2">
              <div class="min-w-0">
                <div class="text-[10px] text-slate-400 line-through font-mono">$${{escapeHtml(item.price)}}</div>
                <div class="flex items-baseline space-x-0.5">
                  <span class="text-xl font-extrabold text-blue-600 font-mono">$${{escapeHtml(discPrice)}}</span>
                  <span class="text-xs text-slate-500 font-medium whitespace-nowrap">/${{escapeHtml(billingCycle)}}</span>
                </div>
              </div>

              <div class="shrink-0">
                ${{
                  isInStock
                    ? `<a href="${{buyUrl}}" target="_blank" rel="nofollow noopener" onclick="onBuyClick(event)" class="inline-flex items-center justify-center px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition active:scale-95 space-x-1.5 whitespace-nowrap">
                        <span>立即抢购</span>
                        <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                      </a>`
                    : `<a href="${{escapeHtml(tgChannel)}}" target="_blank" rel="nofollow noopener" class="inline-flex items-center justify-center px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-medium transition space-x-1.5 whitespace-nowrap">
                        <i class="fa-brands fa-telegram text-sky-500"></i>
                        <span>补货通知</span>
                      </a>`
                }}
              </div>
            </div>

          </div>
        `;
      }}).join('');
      container.innerHTML = cards;
    }}

    function switchView(view) {{
      currentView = view;
      localStorage.setItem('bwh_stock_view', view);
      updateViewToggleButtons();
      renderAll();
    }}

    function updateViewToggleButtons() {{
      const cardBtn = document.getElementById('viewCardBtn');
      const tableBtn = document.getElementById('viewTableBtn');
      if (currentView === 'card') {{
        cardBtn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-white text-blue-600 shadow-xs transition';
        tableBtn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-500 hover:text-slate-900 transition';
      }} else {{
        tableBtn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-white text-blue-600 shadow-xs transition';
        cardBtn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-500 hover:text-slate-900 transition';
      }}
    }}

    function changeSort(sortVal) {{
      currentSort = sortVal;
      localStorage.setItem('bwh_stock_sort', sortVal);
      renderAll();
    }}

    document.querySelectorAll('.tab-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.tab-btn').forEach(b => {{
          b.className = 'tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition';
        }});
        btn.className = 'tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl bg-blue-600 text-white whitespace-nowrap transition';
        currentTag = btn.getAttribute('data-tag');
        renderAll();
      }});
    }});

    // 搜索输入防抖处理 (120ms Debounce)
    let searchDebounceTimer = null;
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearSearchBtn');

    searchInput.addEventListener('input', (e) => {{
      const val = e.target.value;
      if (val.trim()) {{
        clearBtn.classList.remove('hidden');
      }} else {{
        clearBtn.classList.add('hidden');
      }}

      clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(() => {{
        searchQuery = val;
        renderAll();
      }}, 120);
    }});

    function clearSearch() {{
      searchInput.value = '';
      searchQuery = '';
      clearBtn.classList.add('hidden');
      renderAll();
      searchInput.focus();
    }}

    function copyPromoCode() {{
      const code = appConfig.affiliate?.promo_code || 'BWHCXZAVFBVY';
      navigator.clipboard.writeText(code).then(() => {{
        showToast(`优惠码 ${{code}} 已复制到剪贴板！`);
        const label = document.getElementById('copyBtnLabel');
        if (label) {{
          label.textContent = '已复制';
          setTimeout(() => {{
            label.textContent = '复制';
          }}, 2000);
        }}
      }}).catch(() => {{
        showToast('复制失败，请手动复制');
      }});
    }}

    // 用户点击立即抢购时：自动静默将优惠码写入剪贴板并弹出温馨提示
    function onBuyClick(event) {{
      const code = appConfig.affiliate?.promo_code || 'BWHCXZAVFBVY';
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(code).then(() => {{
          showToast(`🎉 优惠码 ${{code}} 已自动复制！结账时粘贴立省 6.78%`);
        }}).catch(() => {{}});
      }}
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      document.getElementById('toastMessage').textContent = msg;
      toast.classList.remove('translate-y-16', 'opacity-0');
      setTimeout(() => {{
        toast.classList.add('translate-y-16', 'opacity-0');
      }}, 2500);
    }}

    function escapeHtml(str) {{
      if (!str) return '';
      return String(str).replace(/[&<>"']/g, m => ({{
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      }})[m]);
    }}

    init();
  </script>
</body>
</html>
"""

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
