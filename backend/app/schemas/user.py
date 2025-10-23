"""
用户相关的Schema
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """用户基础Schema"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """用户创建Schema"""
    password: str = Field(..., min_length=6, description="密码,至少6位")


class UserLogin(BaseModel):
    """用户登录Schema"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """用户更新Schema"""
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserBase):
    """用户响应Schema"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Token响应Schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token数据Schema"""
    user_id: Optional[int] = None
