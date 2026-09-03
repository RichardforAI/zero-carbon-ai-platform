"""Generate complete platform demo HTML with all latest screenshots embedded as base64."""
import base64
import os
import json
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))

def img_to_base64(path):
    full = os.path.join(BASE, path)
    if os.path.exists(full):
        with open(full, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read().decode())
    except:
        return None

# Fetch real data
dashboard = fetch("http://localhost:8080/api/dashboard")
parks = fetch("http://localhost:8080/api/parks") or []
tools = fetch("http://localhost:8080/api/tools?page_size=50") or {}
policies = fetch("http://localhost:8080/api/policies?page_size=50") or {}
news = fetch("http://localhost:8080/api/news?page_size=50") or {}

kpi = dashboard.get('kpi', {}) if dashboard else {}
tool_count = kpi.get('total_tools', tools.get('total', 20))
case_count = kpi.get('total_cases', 15)
park_count = len(parks) if isinstance(parks, list) else 21
policy_count = policies.get('total', 24)
news_count = news.get('total', 20)
supplier_count = 42

# Load screenshots
screenshots = [
    ("01", "dashboard", "总览仪表盘", "平台KPI全景、数据可视化、一键更新入口", img_to_base64("screenshot-01-dashboard.png")),
    ("02", "tools", "工具箱浏览", "20个AI工具，9大分类，多维度筛选搜索", img_to_base64("screenshot-02-tool-list.png")),
    ("03", "tool-detail", "工具详情", "技术参数、成熟度评分、案例、供应商资源", img_to_base64("screenshot-03-tool-detail.png")),
    ("04", "match", "园区智能匹配", "AI语义匹配、置信度评分、优先级标注", img_to_base64("screenshot-04-park-match-ai.png")),
    ("05", "report", "AI报告生成", "LLM自动生成五章节园区策略报告", img_to_base64("screenshot-05-report.png")),
    ("06", "policies", "政策法规", "24条双碳政策，4层级6主题，全文链接", img_to_base64("screenshot-06-policies.png")),
    ("07", "news", "新闻资讯", "20条AI+双碳全球动态，5分类5主题", img_to_base64("screenshot-07-news.png")),
    ("08", "tool-edit", "工具编辑", "工具增删改查、AI辅助创建", img_to_base64("screenshot-08-tool-edit.png")),
    ("09", "whitepaper", "零碳白皮书", "一键生成六章白皮书、PDF导出", img_to_base64("screenshot-09-whitepaper.png")),
]

# Build screenshot cards HTML
cards_html = ""
for num, key, title, desc, b64 in screenshots:
    if b64:
        cards_html += f"""
        <div class="screenshot-card">
            <img src="data:image/png;base64,{b64}" alt="{title}" onclick="openModal(this.src)">
            <div class="screenshot-info">
                <span class="screenshot-num">{num}</span>
                <div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
            </div>
        </div>"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI赋能零碳园区策略平台 · 项目成果展示</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #0f1923; color: #e0e6ed; line-height:1.7;
}}
.hero {{
    background: linear-gradient(135deg, #0f1923 0%, #151f2b 50%, #1a2b1f 100%);
    padding: 60px 40px; text-align:center; border-bottom: 1px solid #1e2d3d;
}}
.hero h1 {{
    font-size: 40px; color: #40e495; margin-bottom: 12px; letter-spacing: 2px;
}}
.hero .subtitle {{
    font-size: 18px; color: #b0bec5; margin-bottom: 8px;
}}
.hero .meta {{
    font-size: 14px; color: #6b7d8e; margin-bottom: 24px;
}}
.hero .tags {{
    display:flex; justify-content:center; gap:12px; flex-wrap:wrap;
}}
.hero .tag {{
    background: #1e2d3d; color:#5b9cf5; padding:6px 16px; border-radius:20px;
    font-size:13px; border:1px solid #2a3d4d;
}}
.kpi-section {{
    display:grid; grid-template-columns: repeat(auto-fit, minmax(160px,1fr));
    gap:16px; padding: 40px; max-width:1200px; margin:0 auto;
}}
.kpi-card {{
    background:#151f2b; border:1px solid #1e2d3d; border-radius:12px;
    padding:24px; text-align:center; transition: transform .2s;
}}
.kpi-card:hover {{ transform: translateY(-4px); border-color:#40e495; }}
.kpi-card .number {{
    font-size: 36px; font-weight:bold; color:#40e495; margin-bottom:4px;
}}
.kpi-card .label {{ font-size:13px; color:#6b7d8e; }}
.section-title {{
    text-align:center; font-size:28px; color:#e0e6ed; margin:40px 0 24px;
    position:relative;
}}
.section-title::after {{
    content:''; display:block; width:60px; height:3px; background:#40e495;
    margin:12px auto 0; border-radius:2px;
}}
.screenshots {{
    max-width:1200px; margin:0 auto; padding: 0 40px;
    display:grid; grid-template-columns: repeat(auto-fit, minmax(360px,1fr));
    gap:24px;
}}
.screenshot-card {{
    background:#151f2b; border:1px solid #1e2d3d; border-radius:12px;
    overflow:hidden; transition: transform .2s, border-color .2s;
}}
.screenshot-card:hover {{ transform: translateY(-4px); border-color:#5b9cf5; }}
.screenshot-card img {{
    width:100%; height:auto; display:block; cursor:zoom-in; border-bottom:1px solid #1e2d3d;
}}
.screenshot-info {{
    padding:16px; display:flex; gap:12px; align-items:flex-start;
}}
.screenshot-num {{
    background:#40e495; color:#0f1923; font-weight:bold; width:32px; height:32px;
    border-radius:8px; display:flex; align-items:center; justify-content:center;
    font-size:16px; flex-shrink:0;
}}
.screenshot-info h3 {{ font-size:16px; color:#e0e6ed; margin-bottom:4px; }}
.screenshot-info p {{ font-size:12px; color:#6b7d8e; }}
.highlights {{
    max-width:1200px; margin:0 auto; padding: 0 40px 40px;
    display:grid; grid-template-columns: repeat(auto-fit, minmax(280px,1fr)); gap:20px;
}}
.highlight-card {{
    background:#151f2b; border:1px solid #1e2d3d; border-radius:12px; padding:24px;
}}
.highlight-card .icon {{ font-size:32px; margin-bottom:12px; }}
.highlight-card h3 {{ color:#40e495; font-size:17px; margin-bottom:8px; }}
.highlight-card p {{ color:#b0bec5; font-size:13px; }}
.footer {{
    text-align:center; padding:40px; color:#4a5c6e; font-size:12px;
    border-top:1px solid #1e2d3d;
}}
.modal {{
    display:none; position:fixed; z-index:999; left:0; top:0; width:100%; height:100%;
    background:rgba(0,0,0,.9); align-items:center; justify-content:center; cursor:zoom-out;
}}
.modal img {{ max-width:95%; max-height:95%; border-radius:8px; }}
.modal.show {{ display:flex; }}
</style>
</head>
<body>

<div class="hero">
    <h1>AI赋能零碳园区策略平台</h1>
    <div class="subtitle">Zero-Carbon Industrial Park AI Strategy Platform</div>
    <div class="meta">清华大学人工智能应用实践课程 · 柯谨 徐青杨 · 2026年8月</div>
    <div class="tags">
        <span class="tag">🔮 AI工具知识库</span>
        <span class="tag">🤖 LLM智能匹配</span>
        <span class="tag">📋 政策法规库</span>
        <span class="tag">📖 零碳白皮书</span>
        <span class="tag">📰 新闻资讯</span>
        <span class="tag">🔄 一键更新</span>
    </div>
</div>

<div class="kpi-section">
    <div class="kpi-card"><div class="number">{tool_count}</div><div class="label">AI工具（9大分类）</div></div>
    <div class="kpi-card"><div class="number">{park_count}</div><div class="label">零碳园区（4类9型）</div></div>
    <div class="kpi-card"><div class="number">{policy_count}</div><div class="label">双碳政策（4层级）</div></div>
    <div class="kpi-card"><div class="number">{supplier_count}</div><div class="label">供应商/专家（100%覆盖）</div></div>
    <div class="kpi-card"><div class="number">{case_count}</div><div class="label">商业案例</div></div>
    <div class="kpi-card"><div class="number">{news_count}</div><div class="label">新闻资讯（5分类）</div></div>
</div>

<div class="section-title">平台核心页面</div>
<div class="screenshots">
{cards_html}
</div>

<div class="section-title">平台核心亮点</div>
<div class="highlights">
    <div class="highlight-card">
        <div class="icon">🤖</div>
        <h3>LLM智能匹配引擎</h3>
        <p>集成DeepSeek大语言模型，对21个园区与20个AI工具进行五维度（产业/能耗/碳排/挑战/类型）语义匹配，输出带置信度评分和部署优先级的个性化推荐。</p>
    </div>
    <div class="highlight-card">
        <div class="icon">🔄</div>
        <h3>一键AI动态更新</h3>
        <p>点击按钮即由AI实时生成最新政策、工具、案例和新闻并自动入库，平台从静态知识库升级为可生长的AI原生平台。</p>
    </div>
    <div class="highlight-card">
        <div class="icon">📖</div>
        <h3>零碳白皮书生成</h3>
        <p>基于平台实时数据聚合六章约2万字白皮书，支持一键导出A4标准PDF，可作为园区项目申报和商业计划书参考附件。</p>
    </div>
    <div class="highlight-card">
        <div class="icon">🔗</div>
        <h3>供应商资源全覆盖</h3>
        <p>42家供应商/专家资源100%覆盖全部20个AI工具，从"用什么工具"到"找谁来做"再到"看实际案例"的全链路服务。</p>
    </div>
    <div class="highlight-card">
        <div class="icon">📋</div>
        <h3>四层级政策知识库</h3>
        <p>覆盖国际/国家/地方/行业标准四层级的24条双碳政策，全部含官方来源超链接，支持多维度筛选和全文检索。</p>
    </div>
    <div class="highlight-card">
        <div class="icon">📊</div>
        <h3>数据可视化Dashboard</h3>
        <p>ECharts驱动的KPI卡片、分类饼图、园区覆盖柱状图和成熟度雷达图，一站式掌握平台数据全景。</p>
    </div>
</div>

<div class="footer">
    <p>AI赋能零碳园区策略平台 · 清华大学人工智能应用实践课程项目成果</p>
    <p>柯谨（建筑学院）· 徐青杨（化工学院）· 指导教师：宋伟泽助理教授</p>
    <p style="margin-top:8px">数据更新于 2026年8月 · 平台基于 FastAPI + React + DeepSeek LLM 构建</p>
</div>

<div class="modal" id="modal" onclick="closeModal()">
    <img id="modal-img" src="">
</div>

<script>
function openModal(src) {{
    document.getElementById('modal-img').src = src;
    document.getElementById('modal').classList.add('show');
}}
function closeModal() {{
    document.getElementById('modal').classList.remove('show');
}}
document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') closeModal();
}});
</script>
</body>
</html>"""

out = os.path.join(BASE, "platform-demo.html")
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

size_mb = os.path.getsize(out) / 1024 / 1024
print(f"Demo HTML 已生成: {out}")
print(f"文件大小: {size_mb:.1f}MB")
print(f"嵌入截图: {sum(1 for s in screenshots if s[4])}/9 张")
print(f"数据统计: {tool_count}工具 {park_count}园区 {policy_count}政策 {supplier_count}供应商 {case_count}案例 {news_count}新闻")
