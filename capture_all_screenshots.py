"""Capture screenshots of all platform pages using Playwright."""
from playwright.sync_api import sync_playwright
import time

BASE = "http://localhost:5173"
OUT = "/Users/qingyangxu./VibeCoding/Trae1/Zero-Carbon project"

pages = [
    ("screenshot-01-dashboard.png", "/dashboard", "Dashboard总览"),
    ("screenshot-02-tool-list.png", "/tools", "工具箱浏览"),
    ("screenshot-03-tool-detail.png", "/tools/7", "工具详情"),
    ("screenshot-04-park-match-ai.png", "/match", "园区匹配"),
    ("screenshot-05-report.png", "/report", "AI报告生成"),
    ("screenshot-06-policies.png", "/policies", "政策法规"),
    ("screenshot-07-news.png", "/news", "新闻资讯"),
    ("screenshot-08-tool-edit.png", "/tools/new", "工具编辑"),
    ("screenshot-09-whitepaper.png", "/whitepaper", "零碳白皮书"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    page = context.new_page()

    for filename, path, label in pages:
        try:
            print(f"截取 {label} ({path})...")
            page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=20000)
            time.sleep(2)  # wait for data load
            page.screenshot(path=f"{OUT}/{filename}", full_page=False)
            print(f"  ✓ {filename}")
        except Exception as e:
            print(f"  ✗ {label} 失败: {str(e)[:80]}")

    # 单独处理：白皮书需要先点击生成按钮
    try:
        print("截取 零碳白皮书（生成后）...")
        page.goto(f"{BASE}/whitepaper", wait_until="networkidle", timeout=20000)
        time.sleep(1)
        # 点击"一键生成白皮书"按钮
        gen_btn = page.locator("button:has-text('一键生成')")
        if gen_btn.count() > 0:
            gen_btn.first.click()
            time.sleep(4)
            page.screenshot(path=f"{OUT}/screenshot-09-whitepaper.png", full_page=False)
            print("  ✓ screenshot-09-whitepaper.png (生成后)")
    except Exception as e:
        print(f"  ✗ 白皮书生成失败: {str(e)[:80]}")

    browser.close()

print("\n截图完成！")
