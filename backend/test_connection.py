"""
测试数据库连接
运行此脚本检查数据库配置是否正确
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app.core.config import settings
    from app.core.database import engine
    from sqlalchemy import text

    print("=" * 60)
    print("  测试数据库连接")
    print("=" * 60)
    print()

    print(f"📋 配置信息:")
    print(f"   数据库URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    print()

    print("🔌 正在连接数据库...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.fetchone()[0]

        print(f"✅ 连接成功！")
        print(f"   当前数据库: {db_name}")
        print()

        print("📊 检查数据表...")
        result = conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result.fetchall()]

        if tables:
            print(f"✅ 找到 {len(tables)} 个表:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("⚠️  未找到数据表，请运行数据库迁移:")
            print("   alembic revision --autogenerate -m 'Initial'")
            print("   alembic upgrade head")

        print()
        print("=" * 60)
        print("✅ 数据库配置正确！可以启动后端服务。")
        print("=" * 60)

except Exception as e:
    print()
    print("=" * 60)
    print("❌ 数据库连接失败！")
    print("=" * 60)
    print()
    print(f"错误信息: {e}")
    print()
    print("可能的原因:")
    print("1. MySQL服务未启动")
    print("   解决: 启动MySQL服务")
    print()
    print("2. 数据库配置错误")
    print("   解决: 检查 backend/.env 中的 DATABASE_URL")
    print("   格式: mysql+pymysql://用户名:密码@localhost:3306/数据库名")
    print()
    print("3. 数据库未创建")
    print("   解决: 运行 init_database.bat 或手动创建数据库")
    print()
    print("=" * 60)
    sys.exit(1)
