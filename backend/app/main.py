"""FastAPI main application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import select, func
import os

from .database import init_db, SessionLocal
from .models import Category, Tool, Park, Case, UpdateLog, Policy, Supplier, News
from .seed_data import CATEGORIES, TOOLS, PARKS, CASES, UPDATE_LOGS, POLICIES, SUPPLIERS, NEWS
from .routers import tools, parks, match, dashboard, agent, policies, whitepaper, news, update

# Remove old DB to force fresh seed
db_path = os.path.join(os.path.dirname(__file__), "..", "zero_carbon.db")
if os.path.exists(db_path):
    os.remove(db_path)

init_db()

# Seed data
db = SessionLocal()
try:
    count = db.query(func.count(Tool.id)).scalar()
    if count == 0:
        for c in CATEGORIES:
            db.add(Category(**c))
        for t in TOOLS:
            db.add(Tool(**t))
        for p in PARKS:
            db.add(Park(**p))
        for cs in CASES:
            db.add(Case(**cs))
        for ul in UPDATE_LOGS:
            db.add(UpdateLog(**ul))
        for pol in POLICIES:
            db.add(Policy(**pol))
        for sup in SUPPLIERS:
            db.add(Supplier(**sup))
        for n in NEWS:
            db.add(News(**n))
        db.commit()
        print(f"Seed data loaded: {len(TOOLS)} tools, {len(PARKS)} parks, {len(CASES)} cases, {len(POLICIES)} policies, {len(SUPPLIERS)} suppliers, {len(NEWS)} news")
finally:
    db.close()

app = FastAPI(
    title="AI赋能零碳园区策略平台",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tools.router)
app.include_router(parks.router)
app.include_router(match.router)
app.include_router(dashboard.router)
app.include_router(agent.router)
app.include_router(policies.router)
app.include_router(whitepaper.router)
app.include_router(news.router)
app.include_router(update.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


# ---- Serve the built frontend (static files + SPA fallback) ----
# 注意：此段必须放在所有 API 路由之后，避免 /api/* 被回退路由拦截。
DIST_DIR = os.path.join(os.path.dirname(__file__), "..", "dist")

if os.path.isdir(DIST_DIR):
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        # 未定义的 /api/* 路径返回 404，而不是回退到首页
        if full_path.startswith("api/"):
            return JSONResponse({"detail": "Not Found"}, status_code=404)
        # 真实存在的文件（如 favicon、robots.txt）直接返回
        candidate = os.path.join(DIST_DIR, full_path)
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        # 其余路径（SPA 路由如 /dashboard、/tools）回退到 index.html
        return FileResponse(os.path.join(DIST_DIR, "index.html"))
