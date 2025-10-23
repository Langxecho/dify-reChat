"""
对话管理API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationResponse, ConversationUpdate
from app.schemas.message import MessageResponse

router = APIRouter()


@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的对话列表

    - **skip**: 跳过记录数
    - **limit**: 返回记录数（最多50）
    """
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.is_archived == False
    ).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()

    # 添加消息数量
    result = []
    for conv in conversations:
        conv_dict = ConversationResponse.model_validate(conv).model_dump()
        message_count = db.query(func.count(Message.id)).filter(
            Message.conversation_id == conv.id
        ).scalar()
        conv_dict['message_count'] = message_count
        result.append(ConversationResponse(**conv_dict))

    return result


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取单个对话详情"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )

    return conversation


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取对话的消息列表

    - **conversation_id**: 对话ID
    - **skip**: 跳过记录数
    - **limit**: 返回记录数（最多100）
    """
    # 验证对话归属
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )

    # 获取消息
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()

    return messages


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    update_data: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新对话

    - **title**: 对话标题
    - **is_archived**: 是否归档
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )

    # 更新字段
    if update_data.title is not None:
        conversation.title = update_data.title
    if update_data.is_archived is not None:
        conversation.is_archived = update_data.is_archived

    db.commit()
    db.refresh(conversation)

    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除对话"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )

    db.delete(conversation)
    db.commit()

    return None
