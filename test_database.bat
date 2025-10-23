@echo off
chcp 65001 >nul
echo ========================================
echo  测试数据库连接
echo ========================================
echo.

cd backend

if not exist "venv" (
    echo 虚拟环境不存在，正在创建...
    python -m venv venv
)

call venv\Scripts\activate
pip install -q sqlalchemy pymysql python-dotenv pydantic-settings 2>nul

python test_connection.py

echo.
pause
