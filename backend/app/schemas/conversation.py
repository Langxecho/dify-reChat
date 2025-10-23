"""
对话相关的Schema
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ConversationBase(BaseModel):
    """对话基础Schema"""
    title: str = Field(default="新对话", max_length=255)


class ConversationCreate(ConversationBase):
    """对话创建Schema"""
    pass


class ConversationUpdate(BaseModel):
    """对话更新Schema"""
    title: Optional[str] = Field(None, max_length=255)
    is_archived: Optional[bool] = None


class ConversationResponse(ConversationBase):
    """对话响应Schema"""
    id: int
    user_id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0

    model_config = {"from_attributes": True}
