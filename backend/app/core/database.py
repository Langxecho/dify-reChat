"""
数据库配置
SQLAlchemy + MySQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,         # 连接前测试连接是否有效
    pool_recycle=3600,           # 1小时回收连接（MySQL默认8小时超时）
    pool_size=10,                # 连接池大小
    max_overflow=20,             # 最大溢出连接数
    echo=settings.DEBUG,         # 开发模式下打印SQL
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


def get_db():
    """
    依赖注入：获取数据库会话
    在FastAPI路由中使用 Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
