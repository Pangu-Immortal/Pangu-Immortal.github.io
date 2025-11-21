#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

DJANGO_PORT=7011
VITE_PORT=7010

function kill_port() {
  local port=$1
  if command -v lsof >/dev/null 2>&1; then
    local pids
    pids=$(lsof -ti :"$port" || true)
    if [[ -n "$pids" ]]; then
      echo "正在停止端口 $port 上的进程..."
      kill -9 $pids || true
      sleep 1
    fi
  fi
}

function start_django() {
  echo "🚀 启动 Django 后端服务 (端口 $DJANGO_PORT)..."
  kill_port "$DJANGO_PORT"
  cd "$ROOT_DIR"
  
  # 检查并激活 conda 环境
  if command -v conda >/dev/null 2>&1; then
    eval "$(conda shell.bash hook)"
    conda activate RunProject 2>/dev/null || echo "⚠️  警告: 无法激活 conda 环境 RunProject，使用当前 Python 环境"
  fi
  
  python3 manage.py migrate --noinput || true
  echo "✅ Django 后端服务已启动: http://127.0.0.1:$DJANGO_PORT"
  echo "📝 管理后台: http://127.0.0.1:$DJANGO_PORT/backend/"
  python3 manage.py runserver 0.0.0.0:"$DJANGO_PORT" > /tmp/django.log 2>&1 &
  echo $! > /tmp/django.pid
}

function start_frontend() {
  echo "🚀 启动 Vue 前端服务 (端口 $VITE_PORT)..."
  kill_port "$VITE_PORT"
  cd "$FRONTEND_DIR"
  export VITE_BACKEND_TARGET="http://127.0.0.1:$DJANGO_PORT"
  
  # 检查 node_modules
  if [[ ! -d "node_modules" ]]; then
    echo "📦 安装前端依赖..."
    npm install
  fi
  
  echo "✅ Vue 前端服务已启动: http://127.0.0.1:$VITE_PORT"
  npm run dev > /tmp/vite.log 2>&1 &
  echo $! > /tmp/vite.pid
}

function stop_all() {
  echo "🛑 停止所有服务..."
  kill_port "$DJANGO_PORT"
  kill_port "$VITE_PORT"
  
  # 清理 PID 文件
  rm -f /tmp/django.pid /tmp/vite.pid
  echo "✅ 所有服务已停止"
}

function restart_all() {
  echo "🔄 重启所有服务..."
  stop_all
  sleep 2
  start_django
  sleep 2
  start_frontend
  echo ""
  echo "✨ 服务重启完成！"
  echo "   - 前端: http://127.0.0.1:$VITE_PORT"
  echo "   - 后端: http://127.0.0.1:$DJANGO_PORT"
  echo "   - 管理后台: http://127.0.0.1:$DJANGO_PORT/backend/"
  echo ""
  echo "查看日志:"
  echo "   - Django: tail -f /tmp/django.log"
  echo "   - Vite: tail -f /tmp/vite.log"
}

function show_status() {
  echo "📊 服务状态:"
  if lsof -ti :"$DJANGO_PORT" >/dev/null 2>&1; then
    echo "   ✅ Django (端口 $DJANGO_PORT): 运行中"
  else
    echo "   ❌ Django (端口 $DJANGO_PORT): 未运行"
  fi
  
  if lsof -ti :"$VITE_PORT" >/dev/null 2>&1; then
    echo "   ✅ Vue (端口 $VITE_PORT): 运行中"
  else
    echo "   ❌ Vue (端口 $VITE_PORT): 未运行"
  fi
}

case "${1:-start}" in
  start)
    start_django
    sleep 2
    start_frontend
    echo ""
    echo "✨ 所有服务已启动！"
    echo "   - 前端: http://127.0.0.1:$VITE_PORT"
    echo "   - 后端: http://127.0.0.1:$DJANGO_PORT"
    echo "   - 管理后台: http://127.0.0.1:$DJANGO_PORT/backend/"
    echo ""
    echo "按 Ctrl+C 停止所有服务"
    wait
    ;;
  stop)
    stop_all
    ;;
  restart)
    restart_all
    wait
    ;;
  status)
    show_status
    ;;
  *)
    echo "用法: $0 [start|stop|restart|status]"
    echo ""
    echo "命令说明:"
    echo "  start   - 启动所有服务（默认）"
    echo "  stop    - 停止所有服务"
    echo "  restart - 重启所有服务"
    echo "  status  - 查看服务状态"
    exit 1
    ;;
esac
