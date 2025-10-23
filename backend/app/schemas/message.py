"""
消息相关的Schema
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.message import MessageRole


class MessageBase(BaseModel):
    """消息基础Schema"""
    content: str = Field(..., min_length=1, description="消息内容")


class MessageCreate(MessageBase):
    """消息创建Schema"""
    conversation_id: int
    role: MessageRole


class MessageResponse(MessageBase):
    """消息响应Schema"""
    id: int
    conversation_id: int
    role: MessageRole
    meta_data: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    """聊天请求Schema"""
    message: str = Field(..., min_length=1, description="用户消息")
    conversation_id: Optional[int] = Field(None, description="对话ID,不传则创建新对话")


class ChatResponse(BaseModel):
    """聊天响应Schema"""
    conversation_id: int
    user_message: MessageResponse
    assistant_message: MessageResponse
