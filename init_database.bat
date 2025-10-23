@echo off
chcp 65001 >nul
echo ========================================
echo  Dify ReChat - 数据库初始化
echo ========================================
echo.

echo [1/3] 正在连接MySQL并创建数据库...
echo 请输入MySQL root密码:
echo.

mysql -u root -p < database_init.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  ✓ 数据库初始化成功！
    echo ========================================
    echo.
    echo 数据库名称: dify_rechat
    echo 已创建的表:
    echo   - users (用户表)
    echo   - conversations (对话表)
    echo   - messages (消息表)
    echo   - system_settings (系统配置表)
    echo.
    echo 下一步:
    echo 1. 编辑 backend\.env 文件，修改数据库密码
    echo 2. 运行 start_backend.bat 启动后端
    echo 3. 运行 start_frontend.bat 启动前端
    echo.
) else (
    echo.
    echo ========================================
    echo  ✗ 数据库初始化失败！
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. MySQL服务未启动
    echo 2. root密码错误
    echo 3. database_init.sql文件不存在
    echo.
    echo 请检查后重试。
    echo.
)

pause
