@echo off
chcp 65001 >nul
echo ========================================
echo  Dify ReChat - 启动后端服务
echo ========================================
echo.

cd backend

echo [1/4] 检查虚拟环境...
if not exist "venv" (
    echo 虚拟环境不存在，正在创建...
    python -m venv venv
    echo ✓ 虚拟环境创建成功
) else (
    echo ✓ 虚拟环境已存在
)
echo.

echo [2/4] 激活虚拟环境...
call venv\Scripts\activate
echo ✓ 虚拟环境已激活
echo.

echo [3/4] 安装/更新依赖...
pip install -r requirements.txt -q
echo ✓ 依赖安装完成
echo.

echo [4/4] 启动后端服务...
echo.
echo ========================================
echo  后端服务启动中...
echo ========================================
echo  API文档: http://localhost:8000/api/docs
echo  健康检查: http://localhost:8000/health
echo ========================================
echo.
echo 按 Ctrl+C 停止服务
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
