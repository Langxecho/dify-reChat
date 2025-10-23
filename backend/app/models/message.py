"""
消息模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class MessageRole(str, enum.Enum):
    """消息角色枚举"""
    USER = "user"
    ASSISTANT = "assistant"


class Message(Base):
    """消息表"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="消息ID")
    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="对话ID"
    )
    role = Column(Enum(MessageRole), nullable=False, comment="角色(user/assistant)")
    content = Column(Text, nullable=False, comment="消息内容")
    meta_data = Column(Text, comment="元数据(JSON字符串)")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    # 关系
    conversation = relationship("Conversation", back_populates="messages")
