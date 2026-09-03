#!/bin/bash
# ============================================================
# 一键同步静态展示站点（static-site/）与项目最新数据
# 用法：bash sync_static_site.sh
# 说明：cron 定时任务环境 PATH 有限，这里显式补齐关键命令路径
# ============================================================
set -e

# cron 环境下 PATH 精简，手动补齐 python3/npm/curl 等命令路径
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.14/bin:$PATH"

CURL="/usr/bin/curl"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
NPM="/usr/local/bin/npm"

cd "$(dirname "$0")"

echo "=============================================="
echo "  同步静态展示站点 static-site/"
echo "=============================================="

# 1. 检查后端服务
if ! "$CURL" -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/health 2>/dev/null | grep -q "200"; then
  echo "⚠️  后端未运行，正在启动..."
  cd backend
  nohup "$PYTHON" -m uvicorn app.main:app --host 0.0.0.0 --port 8080 > /tmp/backend.log 2>&1 &
  cd ..
  sleep 3
  echo "✓ 后端已启动 (http://localhost:8080)"
else
  echo "✓ 后端运行中 (http://localhost:8080)"
fi

# 2. 检查前端服务
if ! "$CURL" -s -o /dev/null -w "%{http_code}" http://localhost:5173/ 2>/dev/null | grep -q "200"; then
  echo "⚠️  前端未运行，正在启动..."
  cd frontend
  nohup "$NPM" run dev -- --host 0.0.0.0 > /tmp/frontend.log 2>&1 &
  cd ..
  sleep 6
  echo "✓ 前端已启动 (http://localhost:5173)"
else
  echo "✓ 前端运行中 (http://localhost:5173)"
fi

# 3. 重新生成静态站点
echo ""
echo "🔄 正在生成最新静态快照..."
"$PYTHON" regenerate_static_site.py

echo ""
echo "=============================================="
echo "  ✅ 同步完成！静态站点已更新到最新数据"
echo "  打开 static-site/index.html 查看"
echo "=============================================="
