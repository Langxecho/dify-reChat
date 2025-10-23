@echo off
chcp 65001 >nul
echo ========================================
echo  Dify ReChat - 远程数据库初始化
echo ========================================
echo.
echo 数据库信息:
echo   主机: 43.143.8.251
echo   端口: 3306
echo   用户: shy
echo   数据库: dify_rechat
echo.
echo ========================================
echo.

echo [1/2] 正在连接远程MySQL服务器...
echo.

mysql -h 43.143.8.251 -P 3306 -u shy -p < database_init_remote.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  ✓ 远程数据库初始化成功！
    echo ========================================
    echo.
    echo 数据库: dify_rechat @ 43.143.8.251
    echo 已创建的表:
    echo   - users (用户表)
    echo   - conversations (对话表)
    echo   - messages (消息表)
    echo   - system_settings (系统配置表)
    echo   - alembic_version (迁移版本表)
    echo.
    echo 配置文件已更新: backend\.env
    echo.
    echo 下一步:
    echo 1. 运行 test_database.bat 测试连接
    echo 2. 运行 start_backend.bat 启动后端
    echo 3. 运行 start_frontend.bat 启动前端
    echo.
) else (
    echo.
    echo ========================================
    echo  ✗ 远程数据库初始化失败！
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. 网络无法连接到远程服务器
    echo 2. 密码错误
    echo 3. 用户 shy 没有创建数据库的权限
    echo 4. 防火墙阻止了3306端口
    echo.
    echo 请检查:
    echo 1. 网络连接是否正常
    echo 2. 服务器防火墙是否开放3306端口
    echo 3. MySQL用户权限是否足够
    echo.
    echo 测试连接命令:
    echo mysql -h 43.143.8.251 -P 3306 -u shy -p
    echo.
)

pause
