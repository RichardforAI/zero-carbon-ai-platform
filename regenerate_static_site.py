"""重新生成 static-site 静态站点：
1. 将 ECharts canvas 图表转为内嵌图片（解决图表空白）
2. 移除 Vite 开发服务器引用（避免部署后 404）
3. 侧边栏 Menu 导航转为真实 <a> 链接（页面间跳转）
4. tools.html 工具卡片转为详情页链接（tools-{id}.html）
5. 新闻卡片转为原文外链
"""
from playwright.sync_api import sync_playwright
import time
import os
import json
import urllib.request

BASE = "http://localhost:5173"
OUT_DIR = "/Users/qingyangxu./VibeCoding/Trae1/Zero-Carbon project/static-site"


def get_tool_map():
    """从后端 API 获取 工具名 -> id 映射。"""
    try:
        with urllib.request.urlopen("http://localhost:8080/api/tools?page_size=50", timeout=10) as r:
            data = json.loads(r.read())
            return {t['name']: t['id'] for t in data['items']}
    except Exception:
        return {}


TOOL_MAP = get_tool_map()
print(f"已获取工具映射：{len(TOOL_MAP)} 个工具")

# 页面修复 JS：canvas转图 + 移除Vite引用 + Menu转链接 + 工具卡片转链接
FIX_JS = """
(args) => {
  let result = { charts: 0, navLinks: 0, scriptsRemoved: 0, toolLinks: 0 };
  const toolMap = args.toolMap;

  // 1. 移除 Vite 开发服务器脚本引用（部署后会 404）
  document.querySelectorAll('script[src]').forEach(s => {
    if (s.src.includes('vite') || s.src.includes('main.tsx') || s.src.includes('@react-refresh')) {
      s.remove();
      result.scriptsRemoved++;
    }
  });
  document.querySelectorAll('script').forEach(s => {
    if (s.textContent.includes('@react-refresh') || s.textContent.includes('injectIntoGlobalHook')) {
      s.remove();
    }
  });

  // 2. 将 ECharts canvas 替换为图片
  document.querySelectorAll('canvas').forEach((canvas) => {
    try {
      const w = canvas.width, h = canvas.height;
      if (w < 10 || h < 10) return;
      const dataURL = canvas.toDataURL('image/png');
      if (!dataURL || dataURL === 'data:,') return;
      const img = document.createElement('img');
      img.src = dataURL;
      img.style.cssText = canvas.style.cssText;
      img.style.width = canvas.style.width;
      img.style.height = canvas.style.height;
      img.setAttribute('data-chart-image', 'true');
      canvas.parentNode.replaceChild(img, canvas);
      result.charts++;
    } catch (e) {}
  });

  // 3. 主导航 Menu → 真实链接
  const menuMap = {
    '总览仪表盘': 'index.html',
    '工具箱浏览': 'tools.html',
    '园区匹配': 'match.html',
    'AI报告生成': 'report.html',
    '政策法规': 'policies.html',
    '新闻资讯': 'news.html',
    '零碳白皮书': 'whitepaper.html',
  };
  document.querySelectorAll('.ant-menu-item').forEach(item => {
    const text = item.textContent || '';
    for (const [key, href] of Object.entries(menuMap)) {
      if (text.includes(key)) {
        const a = document.createElement('a');
        a.href = href;
        a.style.cssText = 'color:inherit;text-decoration:none;display:block;width:100%;height:100%;position:relative;z-index:2;cursor:pointer;';
        a.innerHTML = item.innerHTML;
        item.innerHTML = '';
        item.appendChild(a);
        item.setAttribute('data-nav-link', href);
        result.navLinks++;
        break;
      }
    }
  });

  // 4. tools 页：工具卡片 → 详情页链接
  document.querySelectorAll('.ant-card').forEach(card => {
    if (card.querySelector('a[href]')) return;
    const text = card.textContent || '';
    for (const [name, id] of Object.entries(toolMap)) {
      if (text.includes(name)) {
        const a = document.createElement('a');
        a.href = `tools-${id}.html`;
        a.style.cssText = 'color:inherit;text-decoration:none;display:block;height:100%;';
        a.innerHTML = card.innerHTML;
        card.innerHTML = '';
        card.appendChild(a);
        card.setAttribute('data-tool-link', id);
        result.toolLinks++;
        break;
      }
    }
  });

  // 4b. news 页：新闻标题 → 原文外链（点击标题跳转原文）
  document.querySelectorAll('.ant-card').forEach(card => {
    if (card.getAttribute('data-tool-link')) return;
    const existing = card.querySelector('a[href^="http"]');
    const title = card.querySelector('strong');
    if (existing && title && !title.querySelector('a')) {
      const url = existing.getAttribute('href');
      const a = document.createElement('a');
      a.href = url;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.style.cssText = 'color:#e0e6ed;text-decoration:none;';
      title.parentNode.replaceChild(a, title);
      a.appendChild(title);
      card.setAttribute('data-news-link', 'true');
    }
  });

  // 5. 注入防御性 CSS
  const style = document.createElement('style');
  style.textContent = `
    .ant-menu-item a::before { pointer-events: none !important; }
    .ant-menu-item a { position: relative !important; z-index: 2 !important; }
    .ant-menu-item { cursor: pointer !important; }
    a[data-nav-link], a[data-tool-link], a[href$=".html"] { pointer-events: auto !important; }
    .ant-card a { color: inherit; }
  `;
  document.head.appendChild(style);

  return result;
}
"""

pages = [
    ("index.html", "/dashboard"),
    ("tools.html", "/tools"),
    ("match.html", "/match"),
    ("report.html", "/report"),
    ("policies.html", "/policies"),
    ("news.html", "/news"),
    ("whitepaper.html", "/whitepaper"),
]

os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    for filename, path in pages:
        try:
            print(f"生成 {filename} ({path})...")
            page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=25000)
            time.sleep(3)

            # 白皮书需要先点击生成
            if "whitepaper" in path:
                btn = page.locator("button:has-text('一键生成')")
                if btn.count() > 0:
                    btn.first.click()
                    time.sleep(4)

            # 执行修复
            result = page.evaluate(FIX_JS, {"toolMap": TOOL_MAP})
            time.sleep(1)

            # 保存完整 HTML
            html = page.content()
            out_path = os.path.join(OUT_DIR, filename)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)

            size = os.path.getsize(out_path) / 1024
            print(f"  ✓ {filename} ({size:.0f}KB, 图表{result['charts']}, 导航{result['navLinks']}, 工具链接{result['toolLinks']}, 移除脚本{result['scriptsRemoved']})")
        except Exception as e:
            print(f"  ✗ {filename} 失败: {str(e)[:100]}")

    browser.close()

print("\nstatic-site 重新生成完成！")
