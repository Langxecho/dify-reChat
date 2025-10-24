"""
工作流数据模式
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class WorkflowBase(BaseModel):
    """工作流基础模式"""
    name: str = Field(..., min_length=1, max_length=100, description="工作流显示名称")
    description: Optional[str] = Field(None, description="工作流描述")
    dify_api_url: str = Field(..., min_length=1, max_length=500, description="Dify API URL")
    dify_api_key: str = Field(..., min_length=1, max_length=500, description="Dify API密钥")
    icon: Optional[str] = Field(None, description="图标名称或路径")
    category: str = Field("general", max_length=50, description="分类")
    is_active: bool = Field(True, description="是否启用")
    is_default: bool = Field(False, description="是否为默认工作流")
    sort_order: int = Field(0, description="排序顺序")


class WorkflowCreate(WorkflowBase):
    """创建工作流模式"""
    pass


class WorkflowUpdate(BaseModel):
    """��新工作流模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="工作流显示名称")
    description: Optional[str] = Field(None, description="工作流描述")
    dify_api_url: Optional[str] = Field(None, min_length=1, max_length=500, description="Dify API URL")
    dify_api_key: Optional[str] = Field(None, min_length=1, max_length=500, description="Dify API密钥")
    icon: Optional[str] = Field(None, description="图标名称或路径")
    category: Optional[str] = Field(None, max_length=50, description="分类")
    is_active: Optional[bool] = Field(None, description="是否启用")
    is_default: Optional[bool] = Field(None, description="是否为默认工作流")
    sort_order: Optional[int] = Field(None, description="排序顺序")


class WorkflowResponse(WorkflowBase):
    """工作流响应模式"""
    id: int
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkflowListResponse(BaseModel):
    """工作流列表响应模式"""
    workflows: List[WorkflowResponse]
    total: int
    active_count: int
    category_count: dict


class WorkflowCategory(BaseModel):
    """工作流分类模式"""
    category: str
    name: str
    count: int
    workflows: List[WorkflowResponse]


class WorkflowSelectOption(BaseModel):
    """工作流选择选项模式"""
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    category: str
    is_default: bool


class WorkflowUsageStats(BaseModel):
    """工作流使用统计模式"""
    workflow_id: int
    workflow_name: str
    usage_count: int
    last_used_at: Optional[datetime] = None