// 搬瓦工库存监控 - 前端交互逻辑 (独立脚本，由 index.html 通过 <script src> 引用)
// 运行时数据由 static/js/data.js 注入到全局: window.appConfig / window.appData
// 该文件为可维护的源代码；index.html 由 scripts/build_html.py 自动生成，勿手改 index.html。

let appConfig = window.appConfig || {};
let appData = window.appData || { products: [] };

let currentTag = 'all';
let searchQuery = '';

// 从 localStorage 读取用户偏好（排序与视图模式）
let currentSort = localStorage.getItem('bwh_stock_sort') || 'default';
let currentView = localStorage.getItem('bwh_stock_view') || (window.innerWidth < 1024 ? 'card' : 'table');

// 初始化：加载 config.json（仅一次）+ products.json（定时刷新）
async function init() {
  // 还原排序下拉选框状态
  const sortSelect = document.getElementById('sortSelect');
  if (sortSelect) sortSelect.value = currentSort;

  updateViewToggleButtons();
  renderAll();

  // config.json 几乎不变，仅在页面加载时读取一次
  await loadConfig();
  await loadProducts();
  // 每隔 5 分钟静默拉取最新库存数据（与后端探测频率对齐）
  setInterval(loadProducts, 300000);
}

async function loadConfig() {
  try {
    const timestamp = new Date().getTime();
    const confRes = await fetch(`data/config.json?t=${timestamp}`, { cache: 'no-cache' });
    if (confRes.ok) {
      const loadedConf = await confRes.json();
      appConfig = Object.assign(appConfig, loadedConf);
      applyConfig(appConfig);
    }
  } catch (e) {
    console.warn('使用内置默认 config 配置:', e);
  }
}

let _lastUpdatedAt = '';
async function loadProducts() {
  try {
    const timestamp = new Date().getTime();
    const prodRes = await fetch(`data/products.json?t=${timestamp}`, { cache: 'no-cache' });
    if (!prodRes.ok) throw new Error('网络请求异常');
    const prodData = await prodRes.json();

    // 如果数据未变化（时间戳相同），跳过重渲染
    const newUpdatedAt = prodData.updated_at || '';
    if (newUpdatedAt && newUpdatedAt === _lastUpdatedAt) return;
    _lastUpdatedAt = newUpdatedAt;

    appData.products = prodData.products || prodData || [];

    if (prodData.updated_at) {
      document.getElementById('statUpdatedTime').textContent = prodData.updated_at;
    }

    renderStats();
    renderAll();
  } catch (err) {
    console.error('加载 products.json 失败:', err);
  }
}

// 将 config.json 的设置应用到 DOM
function applyConfig(cfg) {
  if (cfg.site) {
    if (cfg.site.title) document.title = cfg.site.title;
    if (cfg.site.brand_name) document.getElementById('brandName').textContent = cfg.site.brand_name;
    if (cfg.site.subtitle) document.getElementById('brandSubtitle').textContent = cfg.site.subtitle;
  }
  if (cfg.affiliate) {
    if (cfg.affiliate.promo_code) document.getElementById('promoCodeText').textContent = cfg.affiliate.promo_code;
    if (cfg.affiliate.discount_text) document.getElementById('discountTag').textContent = cfg.affiliate.discount_text;
  }
  if (cfg.social && cfg.social.tg_channel) {
    document.getElementById('tgChannelBtn').href = cfg.social.tg_channel;
  }
  if (cfg.footer && cfg.footer.disclaimer) {
    document.getElementById('footerDisclaimer').textContent = cfg.footer.disclaimer;
  }
}

// 统计面板 (类型安全转换)
function renderStats() {
  const total = appData.products.length;
  const inStock = appData.products.filter(p => Number(p.status) === 1).length;
  document.getElementById('statTotal').textContent = total;
  document.getElementById('statInStock').textContent = inStock;
}

// 深度分词多条件搜索引擎
function getFilteredAndSortedProducts() {
  let filtered = appData.products.filter(item => {
    const isItemInStock = Number(item.status) === 1;
    const isItemRecommended = Number(item.recommended) === 1;

    if (currentTag === 'instock' && !isItemInStock) return false;
    if (currentTag === 'recommend' && !isItemRecommended) return false;
    if (currentTag !== 'all' && currentTag !== 'instock' && currentTag !== 'recommend') {
      if (!item.tags || !item.tags.includes(currentTag)) return false;
    }
    return true;
  });

  if (searchQuery.trim()) {
    const terms = searchQuery.trim().toLowerCase().split(/\s+/);

    filtered = filtered.filter(item => {
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
        item.cpu ? `${item.cpu}核 ${item.cpu}core ${item.cpu}c` : '',
        item.memory || '',
        item.ssd || '',
        item.band || '',
        item.bandwidth || '',
        item.price || '',
        `$${item.price}`,
        statusText,
        recommendText,
        aliases
      ].join(' ').toLowerCase();

      return terms.every(term => fullIndex.includes(term));
    });
  }

  if (currentSort === 'price-asc') {
    filtered.sort((a, b) => (parseFloat(a.price) || 0) - (parseFloat(b.price) || 0));
  } else if (currentSort === 'price-desc') {
    filtered.sort((a, b) => (parseFloat(b.price) || 0) - (parseFloat(a.price) || 0));
  } else if (currentSort === 'mem-asc') {
    filtered.sort((a, b) => parseMemoryMB(a.memory) - parseMemoryMB(b.memory));
  } else if (currentSort === 'mem-desc') {
    filtered.sort((a, b) => parseMemoryMB(b.memory) - parseMemoryMB(a.memory));
  }

  return filtered;
}

function parseMemoryMB(memStr) {
  if (!memStr) return 0;
  const str = String(memStr).toUpperCase();
  const val = parseFloat(str) || 0;
  if (str.includes('G')) return val * 1024;
  return val;
}

function renderAll() {
  const filtered = getFilteredAndSortedProducts();
  const matchCountEl = document.getElementById('matchCount');
  if (matchCountEl) matchCountEl.textContent = filtered.length;

  const noResults = document.getElementById('noResults');
  const tableContainer = document.getElementById('tableViewContainer');
  const cardContainer = document.getElementById('cardViewContainer');

  if (filtered.length === 0) {
    tableContainer.classList.add('hidden');
    cardContainer.classList.add('hidden');
    noResults.classList.remove('hidden');
    return;
  }

  noResults.classList.add('hidden');

  if (currentView === 'table') {
    tableContainer.classList.remove('hidden');
    cardContainer.classList.add('hidden');
    renderTable(filtered);
  } else {
    tableContainer.classList.add('hidden');
    cardContainer.classList.remove('hidden');
    renderCards(filtered);
  }
}

function renderTable(products) {
  const tbody = document.getElementById('productTableBody');
  const affId = appConfig.affiliate?.aff_id || '78613';
  const discRate = appConfig.affiliate?.discount_rate || 0.0678;
  const promoCode = appConfig.affiliate?.promo_code || 'BWHCXZAVFBVY';
  const tgChannel = appConfig.social?.tg_channel || 'https://t.me/bwg191';

  const rows = products.map(item => {
    const isInStock = Number(item.status) === 1;
    const buyUrl = `https://bwh81.net/aff.php?aff=${encodeURIComponent(affId)}&pid=${encodeURIComponent(item.pid)}&promocode=${encodeURIComponent(promoCode)}`;
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
            <span class="truncate max-w-[180px] sm:max-w-none">${escapeHtml(item.name)}</span>
            ${recommendBadge}
          </div>
          <div class="text-xs text-slate-500 mt-0.5 whitespace-nowrap">
            <span class="truncate max-w-[200px] text-[11px]">${escapeHtml(item.circuit_type)}</span>
          </div>
        </td>
        <td class="py-3 px-2 sm:px-3 whitespace-nowrap">
          <div class="text-slate-800 font-medium">${escapeHtml(item.cpu)} 核 / ${escapeHtml(item.memory)}</div>
          <div class="text-[11px] text-slate-400 font-mono">${escapeHtml(item.ssd)} SSD</div>
        </td>
        <td class="py-3 px-2 sm:px-3 whitespace-nowrap">
          <div class="text-slate-800 font-medium">${escapeHtml(item.band)}</div>
          <div class="text-[11px] text-slate-400">${escapeHtml(item.bandwidth)}</div>
        </td>
        <td class="py-3 px-2 sm:px-3 max-w-[240px]">
          <div class="text-xs text-slate-600 line-clamp-2 leading-relaxed" title="${escapeHtml(item.datacenter)}">
            ${escapeHtml(item.datacenter || '常规节点')}
          </div>
        </td>
        <td class="py-3 px-2 sm:px-3 text-right whitespace-nowrap font-mono text-slate-400">
          <span class="line-through text-xs">$${escapeHtml(item.price)}</span>
        </td>
        <td class="py-3 px-2 sm:px-3 text-right whitespace-nowrap font-mono">
          <span class="text-base font-bold text-blue-600">$${escapeHtml(discPrice)}</span>
          <span class="text-[10px] text-slate-400 block -mt-1">/${escapeHtml(billingCycle)}</span>
        </td>
        <td class="py-3 px-2 sm:px-3 text-center whitespace-nowrap">
          ${
            isInStock
              ? '<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/80"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-dot mr-1.5"></span>有货</span>'
              : '<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-rose-50 text-rose-600 border border-rose-200/80">缺货</span>'
          }
        </td>
        <td class="py-3 px-3 sm:px-4 text-center whitespace-nowrap">
          ${
            isInStock
              ? `<a href="${buyUrl}" target="_blank" rel="nofollow noopener" onclick="onBuyClick(event)" class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition active:scale-95 space-x-1">
                  <span>立即抢购</span>
                  <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>`
              : `<a href="${escapeHtml(tgChannel)}" target="_blank" rel="nofollow noopener" class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-medium transition space-x-1">
                  <i class="fa-brands fa-telegram text-sky-500"></i>
                  <span>补货通知</span>
                </a>`
          }
        </td>
      </tr>
    `;
  }).join('');
  tbody.innerHTML = rows;
}

function renderCards(products) {
  const container = document.getElementById('cardViewContainer');
  const affId = appConfig.affiliate?.aff_id || '78613';
  const discRate = appConfig.affiliate?.discount_rate || 0.0678;
  const promoCode = appConfig.affiliate?.promo_code || 'BWHCXZAVFBVY';
  const tgChannel = appConfig.social?.tg_channel || 'https://t.me/bwg191';

  const cards = products.map(item => {
    const isInStock = Number(item.status) === 1;
    const buyUrl = `https://bwh81.net/aff.php?aff=${encodeURIComponent(affId)}&pid=${encodeURIComponent(item.pid)}&promocode=${encodeURIComponent(promoCode)}`;
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
                <span class="font-bold text-slate-900 text-sm sm:text-base leading-tight break-words">${escapeHtml(item.name)}</span>
                ${recommendBadge}
              </div>
              <div class="text-xs text-slate-500 font-medium mt-1 break-words leading-tight">
                <span class="text-[12px] text-slate-600">${escapeHtml(item.circuit_type)}</span>
              </div>
            </div>

            <div class="shrink-0">
              ${
                isInStock
                  ? '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-dot mr-1"></span>有货</span>'
                  : '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-rose-50 text-rose-600 border border-rose-200">缺货</span>'
              }
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2 bg-slate-50/80 rounded-xl p-2.5 text-xs">
          <div class="space-y-0.5">
            <span class="text-[10px] text-slate-400 uppercase font-semibold">计算 / 内存</span>
            <p class="font-semibold text-slate-800 break-words">${escapeHtml(item.cpu)} 核 / ${escapeHtml(item.memory)}</p>
          </div>
          <div class="space-y-0.5">
            <span class="text-[10px] text-slate-400 uppercase font-semibold">高速 SSD</span>
            <p class="font-semibold text-slate-800 font-mono break-words">${escapeHtml(item.ssd)}</p>
          </div>
          <div class="space-y-0.5">
            <span class="text-[10px] text-slate-400 uppercase font-semibold">月流量</span>
            <p class="font-semibold text-slate-800 font-mono break-words">${escapeHtml(item.band)}</p>
          </div>
          <div class="space-y-0.5">
            <span class="text-[10px] text-slate-400 uppercase font-semibold">网络带宽</span>
            <p class="font-semibold text-slate-800 font-mono break-words">${escapeHtml(item.bandwidth)}</p>
          </div>
        </div>

        <div class="text-[11px] text-slate-600 leading-relaxed bg-slate-50/70 p-2.5 rounded-xl border border-slate-200/60 break-words">
          <div class="flex items-start space-x-1.5">
            <i class="fa-solid fa-location-dot text-blue-500 mt-0.5 shrink-0 text-[11px]"></i>
            <span class="leading-normal">${escapeHtml(item.datacenter || '常规全球机房')}</span>
          </div>
        </div>

        <div class="pt-2 border-t border-slate-100 flex items-center justify-between gap-2">
          <div class="min-w-0">
            <div class="text-[10px] text-slate-400 line-through font-mono">$${escapeHtml(item.price)}</div>
            <div class="flex items-baseline space-x-0.5">
              <span class="text-xl font-extrabold text-blue-600 font-mono">$${escapeHtml(discPrice)}</span>
              <span class="text-xs text-slate-500 font-medium whitespace-nowrap">/${escapeHtml(billingCycle)}</span>
            </div>
          </div>

          <div class="shrink-0">
            ${
              isInStock
                ? `<a href="${buyUrl}" target="_blank" rel="nofollow noopener" onclick="onBuyClick(event)" class="inline-flex items-center justify-center px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition active:scale-95 space-x-1.5 whitespace-nowrap">
                    <span>立即抢购</span>
                    <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                  </a>`
                : `<a href="${escapeHtml(tgChannel)}" target="_blank" rel="nofollow noopener" class="inline-flex items-center justify-center px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-medium transition space-x-1.5 whitespace-nowrap">
                    <i class="fa-brands fa-telegram text-sky-500"></i>
                    <span>补货通知</span>
                  </a>`
            }
          </div>
        </div>

      </div>
    `;
  }).join('');
  container.innerHTML = cards;
}

function switchView(view) {
  currentView = view;
  localStorage.setItem('bwh_stock_view', view);
  updateViewToggleButtons();
  renderAll();
}

function updateViewToggleButtons() {
  const cardBtn = document.getElementById('viewCardBtn');
  const tableBtn = document.getElementById('viewTableBtn');
  if (currentView === 'card') {
    cardBtn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-white text-blue-600 shadow-xs transition';
    tableBtn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-500 hover:text-slate-900 transition';
  } else {
    tableBtn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-white text-blue-600 shadow-xs transition';
    cardBtn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-500 hover:text-slate-900 transition';
  }
}

function changeSort(sortVal) {
  currentSort = sortVal;
  localStorage.setItem('bwh_stock_sort', sortVal);
  renderAll();
}

document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => {
      b.className = 'tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-slate-600 hover:bg-slate-100 whitespace-nowrap transition';
    });
    btn.className = 'tab-btn px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl bg-blue-600 text-white whitespace-nowrap transition';
    currentTag = btn.getAttribute('data-tag');
    renderAll();
  });
});

// 搜索输入防抖处理 (120ms Debounce)
let searchDebounceTimer = null;
const searchInput = document.getElementById('searchInput');
const clearBtn = document.getElementById('clearSearchBtn');

searchInput.addEventListener('input', (e) => {
  const val = e.target.value;
  if (val.trim()) {
    clearBtn.classList.remove('hidden');
  } else {
    clearBtn.classList.add('hidden');
  }

  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    searchQuery = val;
    renderAll();
  }, 120);
});

function clearSearch() {
  searchInput.value = '';
  searchQuery = '';
  clearBtn.classList.add('hidden');
  renderAll();
  searchInput.focus();
}

function copyPromoCode() {
  const code = appConfig.affiliate?.promo_code || 'BWHCXZAVFBVY';
  navigator.clipboard.writeText(code).then(() => {
    showToast(`优惠码 ${code} 已复制到剪贴板！`);
    const label = document.getElementById('copyBtnLabel');
    if (label) {
      label.textContent = '已复制';
      setTimeout(() => {
        label.textContent = '复制';
      }, 2000);
    }
  }).catch(() => {
    showToast('复制失败，请手动复制');
  });
}

// 用户点击立即抢购时：自动静默将优惠码写入剪贴板并弹出温馨提示
function onBuyClick(event) {
  const code = appConfig.affiliate?.promo_code || 'BWHCXZAVFBVY';
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(code).then(() => {
      showToast(`🎉 优惠码 ${code} 已自动复制！结账时粘贴立省 6.78%`);
    }).catch(() => {});
  }
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  document.getElementById('toastMessage').textContent = msg;
  toast.classList.remove('translate-y-16', 'opacity-0');
  setTimeout(() => {
    toast.classList.add('translate-y-16', 'opacity-0');
  }, 2500);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, m => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[m]);
}

init();
