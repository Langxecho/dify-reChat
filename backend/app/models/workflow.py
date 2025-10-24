"""
工作流模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Workflow(Base):
    """工作流配置表"""

    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="工作流ID")
    name = Column(String(100), nullable=False, comment="工作流显示名称")
    description = Column(Text, comment="工作流描述")
    dify_api_url = Column(String(500), nullable=False, comment="Dify API URL")
    dify_api_key = Column(String(500), nullable=False, comment="Dify API密钥")
    icon = Column(String(100), comment="图标名称或路径")
    category = Column(String(50), default="general", comment="分类（如：客服、创作、编程等）")
    is_active = Column(Boolean, default=True, comment="是否启用")
    is_default = Column(Boolean, default=False, comment="是否为默认工作流")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_by = Column(Integer, ForeignKey("users.id"), comment="创建者ID")
    updated_by = Column(Integer, ForeignKey("users.id"), comment="更新者ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )

    # 关系
    creator = relationship("User", foreign_keys=[created_by], backref="created_workflows")
    updater = relationship("User", foreign_keys=[updated_by], backref="updated_workflows")
    conversations = relationship("ConversationWorkflow", back_populates="workflow")


class ConversationWorkflow(Base):
    """对话工作流关联表"""

    __tablename__ = "conversation_workflows"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="关联ID")
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, comment="对话ID")
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, comment="工作流ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    # 关系
    conversation = relationship("Conversation", back_populates="workflow")
    workflow = relationship("Workflow", back_populates="conversations")