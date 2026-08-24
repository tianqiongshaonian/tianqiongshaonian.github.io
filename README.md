# 🚀 BandwagonHost (搬瓦工) VPS 全方案库存监控与 Telegram 补货推送系统

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-success.svg)](https://tianqiongshaonian.github.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![No-Server](https://img.shields.io/badge/Server-100%25%20Free%20Serverless-orange.svg)](#)

基于 **GitHub Pages**（前端展示）+ **GitHub Actions**（云端自动化 Python 探测）构建的 **100% 纯免费、零服务器、零维护** 的搬瓦工全方案库存实时监控与即时推送系统。

---

## ✨ 核心特性

- ⚡️ **零成本云端自动化**：由 GitHub Actions 每 10 分钟在云端自动运行 Python 探测，无需自备 VPS 服务器。
- 📱 **全设备自适应布局**：
  - **PC / 宽屏**：1600px 黄金视野，清晰表格展示，彻底消除横向滚动条。
  - **手机 / 平板**：自动切换为原生 App 级卡片流，2x2 核心参数网格，单手操作丝滑。
- 🔍 **超级详细智能搜索**：
  - 支持**空格分词多条件组合搜索**（如 `香港 1T`、`DC6 2G 有货`、`2核 40G`、`PID 44`）。
  - 支持智能地域与别名映射（`HK`、`日本`、`软银`、`美西`、`新加坡`、`The Plan`、`传家宝` 等）。
- 🔔 **Telegram 秒级补货推送 & 自动置顶**：
  - 探测到从“缺货”变为“有货”时，机器人自动向指定频道/群组推送精美卡片，并**自动置顶最新补货消息**。
- 🎨 **100% 纯本地化静态资源**：
  - 独立编译精简版 Tailwind CSS 与本地 Font Awesome 图标字体，**零外部 CDN 依赖**，控制台 0 警告，首屏极速秒开。
- 🚀 **极致 SEO 与 AI 抓取优化 (GEO / AI SEO Ready)**：
  - **双模渲染**：集成静态预渲染（Static Pre-rendering）+ 动态水合，爬虫与 AI（SearchGPT、Claude、Perplexity 等）无需执行 JS 即可秒抓全站 78+ 款方案、配置、实时库存与价格。
  - **结构化数据**：内嵌完整的 Schema.org (`WebSite`, `Product`, `ItemList`, `FAQPage`) JSON-LD，尊享 Google 富媒体搜索摘要与 AI 权威引用。
  - **全套搜索引擎与 AI 规范**：开箱即用 `robots.txt`、`sitemap.xml`、`llms.txt` 与 `llms-full.txt`，全面拥抱 AI 搜索时代。
- 🛡️ **智能提交流水线与 14 天长效心跳保活**：
  - **零垃圾提交**：无变动时仅构建并发布最新页面到 Pages，仅在真实发生补货/售罄变动时才触发 Git Commit。
  - **突破 60 天休眠限制**：内置双模提交，每 14 天自动由 PAT 签发一次心跳活跃记录，定时任务永久全自动运行。
- ⚙️ **极简配置架构**：
  - 所有的返利 ID、优惠码、Telegram 频道、消息模板均统一由 [`config.json`](config.json) 控制，改一处全站同步！

---

## 📁 项目目录结构

```text
├── config.json                 # ⭐️ 全局唯一配置文件（返利ID、优惠码、TG推送模板等）
├── index.html                  # 现代化响应式前端网页（静态预渲染 + PC表格/移动卡片）
├── products.json               # 核心数据源（78+ 款搬瓦工套餐配置与实时库存）
├── robots.txt                  # 搜索引擎与 AI 爬虫抓取协议规范
├── sitemap.xml                 # XML 站点地图（自动更新时间戳）
├── llms.txt                    # 🤖 面向大模型与 AI Agent 的精炼摘要规范
├── llms-full.txt               # 📚 面向大模型的搬瓦工完整知识库文档
├── static/                     # 🎨 100% 本地化静态样式与字体库
│   ├── css/
│   │   └── tailwind.min.css    # 本地编译的高性能独立 Tailwind CSS
│   └── fontawesome/            # 本地 Font Awesome 6 图标与 WebFonts
├── scripts/                    # 🐍 模块化 Python 后端探测与推送系统
│   ├── __init__.py             # Python 包初始化文件
│   ├── config.py               # 配置中心：统一解析 config.json 与环境变量
│   ├── build_html.py           # 静态预渲染与 SEO/Sitemap 构建器
│   ├── notifier.py             # 通知模块：负责 TG 模板渲染、消息发送与自动置顶
│   ├── checker.py              # 探测核心：多线程高并发库存探测与数据落地
│   └── test_tg.py              # 调试工具：命令行一键测试 Telegram 推送与置顶
├── .github/
│   └── workflows/
│       └── monitor.yml         # GitHub Actions 自动化定时工作流
└── README.md                   # 项目使用与部署说明文档
```

---

## 🛠️ 新手 3 分钟一键部署教程

> 无论你是小白还是开发者，只需按照以下 3 步即可拥有专属的库存监控网站与 Telegram 推送机器人！

### 第一步：Fork 或新建 GitHub 仓库

1. 点击本仓库右上角的 **Fork** 按钮，将项目复制到你自己的 GitHub 账号下。
2. （或者）在 GitHub 新建一个仓库（如命名为 `你的用户名.github.io`），将本项目代码上传推送上去。

---

### 第二步：开启 GitHub Pages 网站服务

1. 进入你 Fork 后的 GitHub 仓库，点击顶部菜单的 **Settings（设置）**。
2. 在左侧侧边栏点击 **Pages**。
3. 在 **Build and deployment** 下方的 **Source** 下拉菜单中，选择 **`GitHub Actions`**。

> 💡 开启后，GitHub 将自动运行流水线，你的监控网站地址为：  
> **`https://<你的GitHub用户名>.github.io/<仓库名>/`**（若仓库名为 `<用户名>.github.io` 则为根域名直达）。

---

### 第三步：自定义配置与开启 Telegram 补货提醒

#### 1. 修改你的专属返利 ID 与优惠码
直接在 GitHub 网页上编辑本仓库的 [`config.json`](config.json) 文件：

```json
{
  "site": {
    "title": "搬瓦工库存监控 - BandwagonHost VPS 实时库存与全网补货通知",
    "brand_name": "搬瓦工库存监控",
    "subtitle": "BandwagonHost Real-time Stock & Restock Monitor"
  },
  "affiliate": {
    "aff_id": "你的搬瓦工AFF返利ID",
    "promo_code": "BWHCXZAVFBVY",
    "discount_text": "6.78% 循环优惠",
    "discount_rate": 0.0678
  },
  "social": {
    "tg_channel": "https://t.me/你的频道用户名",
    "tg_group": "https://t.me/你的交流群用户名"
  },
  "telegram": {
    "auto_pin": true,
    "template": "🎉 <b>搬瓦工补货提醒 (Restock Alert)</b>\n\n📦 <b>方案名称</b>：{name}\n⚡️ <b>线路类型</b>：{circuit_type}\n💻 <b>配置规格</b>：{cpu}核 CPU / {memory} 内存 / {ssd} SSD\n🌐 <b>流量带宽</b>：{band} / {bandwidth}\n🏢 <b>机房节点</b>：{datacenter}\n💵 <b>官方原价</b>：<b>${price}</b>\n🎟 <b>优惠码</b>：<code>{promo_code}</code> ({discount_text})\n\n👉 <a href=\"{buy_url}\"><b>【点击立即直达抢购】</b></a>\n🌐 <a href=\"{site_url}\"><b>【查看更多方案库存监控】</b></a>"
  }
}
```

#### 2. 配置 Telegram 推送与永久保活密钥（强烈推荐）

为实现 **补货即时通知** 以及 **突破 GitHub 60 天休眠限制**，请在 GitHub 仓库中配置以下 Secrets：

1. 打开 GitHub 仓库页面 $\rightarrow$ **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions**。
2. 点击 **New repository secret**，添加以下三个密钥：

| 密钥名称 (Secret Name) | 是否必填 | 作用与获取方式 |
| :--- | :--- | :--- |
| `MY_PAT` | **强烈推荐** | **突破 60 天休眠**：在 GitHub [Tokens Settings](https://github.com/settings/tokens/new) 生成一个勾选 `repo` 与 `workflow` 权限的个人访问令牌（PAT），使定时任务永久保持真人活跃，免除休眠。 |
| `TG_BOT_TOKEN` | 可选 | **TG 补货推送**：Telegram 搜索 [@BotFather](https://t.me/BotFather) 发送 `/newbot` 获取的机器人口令。 |
| `TG_CHAT_ID` | 可选 | **接收推送频道**：将机器人拉入频道设为管理员后，填入你的频道或群组用户名（如 `@bwg191`）。 |

---

## 🧪 本地调试与手动运行

项目完全基于 Python 原生标准库，**无需 `pip install` 任何第三方依赖**，克隆即跑！

### 1. 本地运行库存探测
```bash
python3 scripts/checker.py
```

### 2. 测试 Telegram 推送与自动置顶
```bash
python3 scripts/test_tg.py "你的_TG_BOT_TOKEN" "@你的频道用户名"
```

### 3. 在 GitHub 网页上手动触发一次云端运行
1. 打开 GitHub 仓库的 **Actions** 标签页。
2. 在左侧列表点击 **“搬瓦工库存监控与自动部署”**。
3. 点击右侧 **Run workflow** 按钮即可手动立即执行一次探测、更新与部署。

---

## 🌐 绑定独立自定义域名（可选）

如果你拥有自己的域名（例如 `stock.mydomain.com`）：
1. 在仓库的 **Settings** $\rightarrow$ **Pages** $\rightarrow$ **Custom domain** 中填入你的自定义域名并保存。
2. 在你的 DNS 解析服务商（如 Cloudflare / 腾讯云 / 阿里云）添加一条 `CNAME` 解析记录：
   - 主机记录：`stock`
   - 记录类型：`CNAME`
   - 记录值：`<你的GitHub用户名>.github.io`
3. 在 GitHub Pages 设置中勾选 **Enforce HTTPS**，免费开启 SSL 安全访问。

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 开源，欢迎 Fork、Star 和二次开发！
