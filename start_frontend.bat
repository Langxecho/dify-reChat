@echo off
chcp 65001 >nul
echo ========================================
echo  Dify ReChat - 启动前端服务
echo ========================================
echo.

cd frontend

echo [1/2] 检查依赖...
if not exist "node_modules" (
    echo node_modules不存在，正在安装依赖...
    call npm install
    echo ✓ 依赖安装完成
) else (
    echo ✓ 依赖已存在
)
echo.

echo [2/2] 启动前端服务...
echo.
echo ========================================
echo  前端服务启动中...
echo ========================================
echo  访问地址: http://localhost:5173
echo ========================================
echo.
echo 按 Ctrl+C 停止服务
echo.

call npm run dev

pause
