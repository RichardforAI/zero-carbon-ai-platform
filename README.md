# AI赋能零碳园区策略平台

> Zero-Carbon Industrial Park AI Strategy Platform

面向零碳园区建设的 AI 知识平台，集 AI 工具知识库、园区智能匹配、政策法规检索、零碳白皮书生成和全球新闻资讯于一体的可生长型 AI 知识平台。

清华大学人工智能应用实践课程项目 · 柯谨（建筑学院）· 徐青杨（化工学院）· 指导教师：宋伟泽助理教授

---

## 🎯 项目简介

针对零碳园区建设中 **AI 工具信息分散**、**政策法规庞杂**、**技术落地路径不清晰** 三大痛点，本平台构建了从"用什么 AI 工具"到"找谁来做"到"行业最新动态"的全链路服务：

- 🔮 **AI 工具知识库**：20 个 AI 工具，9 大技术分类，10+ 维度元数据
- 🤖 **LLM 智能匹配**：基于 DeepSeek 大模型的园区-工具五维度语义匹配
- 📋 **政策法规库**：24 条双碳政策，4 层级 6 主题，全文官方链接
- 📖 **零碳白皮书**：一键生成六章约 2 万字白皮书，支持 PDF 导出
- 📰 **新闻资讯**：20 条全球 AI+双碳动态，5 分类 5 主题
- 🔄 **一键更新**：AI 驱动的数据动态生长，平台持续进化

## 📊 核心数据

| 数据类型 | 数量 | 覆盖 |
|---------|:---:|------|
| AI 工具 | 20 个 | 9 大分类 × 6 运营环节 |
| 零碳园区 | 21 个 | 4 大类 × 9 小类全覆盖 |
| 双碳政策 | 24 条 | 国际/国家/地方/行业标准 |
| 供应商/专家 | 42 家 | 20/20 工具 100% 覆盖 |
| 商业案例 | 15 个 | 覆盖 12 个工具 |
| 新闻资讯 | 20 条 | 5 分类 × 5 主题 |

## 🛠️ 技术栈

- **后端**：Python FastAPI + SQLAlchemy + SQLite
- **前端**：React 18 + TypeScript + Ant Design 5 + ECharts
- **AI**：OpenAI 兼容 SDK（DeepSeek），LLM Agent 智能匹配 + 报告生成
- **构建**：Vite

## 🚀 快速开始

```bash
# 1. 启动后端（端口 8080）
cd backend
pip install -r requirements.txt
cp .env.example .env  # 填入真实 DeepSeek API Key
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080

# 2. 启动前端（端口 5173）
cd frontend
npm install
npm run dev -- --host 0.0.0.0

# 3. 访问
open http://localhost:5173
```

> 未配置 API Key 时，平台自动运行在 Demo 模式（规则匹配 + 预置数据），功能完整可演示。

## 📁 成果展示

- **`platform-demo.html`** — 单文件自包含成果展示（含 9 页截图，双击即开）
- **`static-site/`** — 完整静态站点快照（多页面，可用 GitHub Pages 托管）
- **`screenshot-*.png`** — 各页面截图

## 📂 项目结构

```
Zero-Carbon project/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── main.py          # 入口
│   │   ├── models.py        # ORM 模型（8张表）
│   │   ├── schemas.py       # Pydantic Schema
│   │   ├── seed_data.py     # 种子数据
│   │   ├── services/        # LLM 服务封装
│   │   └── routers/         # 14+ API 端点
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # React 前端
│   ├── src/
│   │   ├── pages/           # 9 个页面
│   │   ├── components/      # 布局组件
│   │   └── api/             # API 客户端
│   └── package.json
├── static-site/             # 静态站点快照
├── platform-demo.html       # 单文件成果展示
└── 文档/                    # 周报、结题报告、中期检查表
```

## 📄 文档

- 开题报告、中期检查表、结题实践报告
- 第 2~6 周进展周报（Markdown + Word + PDF）
- 结题实践报告含完整的技术方案、数据分析、创新点和白皮书全文

## ⚠️ 注意事项

- `backend/.env` 已被 `.gitignore` 排除（保护 API Key），请使用 `.env.example` 创建本地配置
- SQLite 数据库 `zero_carbon.db` 会在每次后端启动时自动重建
- `frontend/node_modules` 需通过 `npm install` 安装

---

*本项目为清华大学人工智能应用实践课程成果，2026 年 8 月*
