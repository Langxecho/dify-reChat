"""
工作流管理API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.workflow import Workflow, ConversationWorkflow
from app.schemas.workflow import (
    WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowListResponse,
    WorkflowCategory, WorkflowSelectOption, WorkflowUsageStats
)
from app.api.deps import get_current_admin

router = APIRouter()


@router.get("/", response_model=WorkflowListResponse)
async def get_workflows(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    active_only: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    获取工作流列表
    """
    query = db.query(Workflow)

    if active_only:
        query = query.filter(Workflow.is_active == True)

    if category:
        query = query.filter(Workflow.category == category)

    # 按排序顺序和创建时间排序
    query = query.order_by(Workflow.sort_order, Workflow.created_at.desc())

    # 获取总数
    total = query.count()

    # 分页
    workflows = query.offset(skip).limit(limit).all()

    # 计算活跃数量
    active_count = db.query(Workflow).filter(Workflow.is_active == True).count()

    # 计算分类数量
    category_count = {}
    if active_only:
        category_results = db.query(
            Workflow.category,
            func.count(Workflow.id)
        ).filter(
            Workflow.is_active == True
        ).group_by(Workflow.category).all()

        for cat, count in category_results:
            category_count[cat] = count

    return WorkflowListResponse(
        workflows=workflows,
        total=total,
        active_count=active_count,
        category_count=category_count
    )


@router.get("/categories", response_model=List[WorkflowCategory])
async def get_workflow_categories(current_user: User = Depends(get_current_user)):
    """
    获取工作流分类
    """
    categories = db.query(
        Workflow.category,
        func.count(Workflow.id).label('count')
    ).filter(
        Workflow.is_active == True
    ).group_by(Workflow.category).order_by(
        Workflow.category
    ).all()

    result = []
    for cat, count in categories:
        workflows = db.query(Workflow).filter(
            Workflow.category == cat,
            Workflow.is_active == True
        ).order_by(Workflow.sort_order, Workflow.created_at.desc()).all()

        result.append(WorkflowCategory(
            category=cat,
            name=cat.title(),
            count=count,
            workflows=workflows
        ))

    return result


@router.get("/select-options", response_model=List[WorkflowSelectOption])
async def get_workflow_select_options(current_user: User = Depends(get_current_user)):
    """
    获取工作流选择选项（用于下拉选择）
    """
    workflows = db.query(Workflow).filter(
        Workflow.is_active == True
    ).order_by(
        Workflow.is_default.desc(),
        Workflow.sort_order,
        Workflow.name
    ).all()

    return [
        WorkflowSelectOption(
            id=w.id,
            name=w.name,
            description=w.description,
            icon=w.icon,
            category=w.category,
            is_default=w.is_default
        )
        for w in workflows
    ]


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    获取单个工作流详情
    """
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工作流不存在"
        )

    return workflow


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    创建工作流（仅管理员）
    """
    # 检查名称是否重复
    existing = db.query(Workflow).filter(
        Workflow.name == workflow_data.name,
        Workflow.is_active == True
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="工作流名称已存在"
        )

    # 如果设置为默认，先取消其他默认工作流
    if workflow_data.is_default:
        db.query(Workflow).filter(
            Workflow.is_default == True
        ).update({"is_default": False})

    workflow = Workflow(
        **workflow_data.dict(),
        created_by=current_user.id,
        updated_by=current_user.id
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return workflow


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    workflow_data: WorkflowUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    更新工作流（仅管理员）
    """
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工作流不存在"
        )

    # 检查名称是否重复
    if workflow_data.name and workflow_data.name != workflow.name:
        existing = db.query(Workflow).filter(
            Workflow.name == workflow_data.name,
            Workflow.is_active == True,
            Workflow.id != workflow_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="工作流名称已存在"
            )

    # 如果设置为默认，先取消其他默认工作流
    if workflow_data.is_default and not workflow.is_default:
        db.query(Workflow).filter(
            Workflow.is_default == True
        ).update({"is_default": False})

    # 更新字段
    update_data = workflow_data.dict(exclude_unset=True)
    update_data["updated_by"] = current_user.id

    for field, value in update_data.items():
        setattr(workflow, field, value)

    db.commit()
    db.refresh(workflow)

    return workflow


@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    删除工作流（仅管理员）
    """
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工作流不存在"
        )

    # 检查是否有对话在使用此工作流
    conversation_count = db.query(ConversationWorkflow).filter(
        ConversationWorkflow.workflow_id == workflow_id
    ).count()

    if conversation_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该工作流正被 {conversation_count} 个对话使用，无法删除"
        )

    # 软删除：标记为不活跃
    workflow.is_active = False
    workflow.updated_by = current_user.id
    db.commit()

    return {"message": "工作流已删除"}


@router.post("/{workflow_id}/set-default")
async def set_default_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    设置默认工作流（仅管理员）
    """
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工作流不存在"
        )

    if not workflow.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能设置活跃的工作流为默认"
        )

    # 取消其他默认工作流
    db.query(Workflow).filter(
        Workflow.is_default == True
    ).update({"is_default": False})

    # 设置当前为默认
    workflow.is_default = True
    workflow.updated_by = current_user.id
    db.commit()

    return {"message": "已设置为默认工作流"}


@router.get("/stats/usage", response_model=List[WorkflowUsageStats])
async def get_workflow_usage_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取工作流使用统计（仅管理员）
    """
    stats = db.query(
        Workflow.id,
        Workflow.name,
        func.count(ConversationWorkflow.id).label('usage_count'),
        func.max(ConversationWorkflow.created_at).label('last_used_at')
    ).outerjoin(
        ConversationWorkflow,
        Workflow.id == ConversationWorkflow.workflow_id
    ).group_by(
        Workflow.id,
        Workflow.name
    ).order_by(
        func.count(ConversationWorkflow.id).desc()
    ).all()

    return [
        WorkflowUsageStats(
            workflow_id=s.id,
            workflow_name=s.name,
            usage_count=s.usage_count or 0,
            last_used_at=s.last_used_at
        )
        for s in stats
    ]