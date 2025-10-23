"""
系统配置模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class SystemSetting(Base):
    """系统配置表"""

    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="配置ID")
    key = Column(String(100), unique=True, nullable=False, index=True, comment="配置键")
    value = Column(Text, comment="配置值(加密存储敏感信息)")
    description = Column(String(255), comment="配置描述")
    updated_by = Column(Integer, ForeignKey("users.id"), comment="更新者ID")
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )
