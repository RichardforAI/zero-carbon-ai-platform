"""重新生成 static-site 静态页面，将 ECharts canvas 图表转为内嵌图片，解决图表空白问题。"""
from playwright.sync_api import sync_playwright
import time
import os

BASE = "http://localhost:5173"
OUT_DIR = "/Users/qingyangxu./VibeCoding/Trae1/Zero-Carbon project/static-site"

# 将 canvas 替换为 dataURL 图片的 JS
CANVAS_TO_IMG_JS = """
() => {
  const canvases = document.querySelectorAll('canvas');
  canvases.forEach((canvas, i) => {
    try {
      const w = canvas.width, h = canvas.height;
      if (w < 10 || h < 10) return;  // 跳过无效 canvas
      const dataURL = canvas.toDataURL('image/png');
      if (!dataURL || dataURL === 'data:,') return;
      const img = document.createElement('img');
      img.src = dataURL;
      img.style.cssText = canvas.style.cssText;
      img.style.width = canvas.style.width;
      img.style.height = canvas.style.height;
      img.setAttribute('data-chart-image', 'true');
      // 替换 canvas（保留父容器）
      canvas.parentNode.replaceChild(img, canvas);
    } catch (e) {
      // 跨域或空 canvas，跳过
    }
  });
  return document.querySelectorAll('img[data-chart-image]').length;
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
            # 等待数据加载
            time.sleep(3)

            # 白皮书需要先点击生成
            if "whitepaper" in path:
                btn = page.locator("button:has-text('一键生成')")
                if btn.count() > 0:
                    btn.first.click()
                    time.sleep(4)

            # 将 canvas 转为图片
            img_count = page.evaluate(CANVAS_TO_IMG_JS)
            time.sleep(1)

            # 保存完整 HTML
            html = page.content()
            out_path = os.path.join(OUT_DIR, filename)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)

            size = os.path.getsize(out_path) / 1024
            print(f"  ✓ {filename} ({size:.0f}KB, 图表图片{img_count}个)")
        except Exception as e:
            print(f"  ✗ {filename} 失败: {str(e)[:100]}")

    browser.close()

print("\nstatic-site 重新生成完成！")
