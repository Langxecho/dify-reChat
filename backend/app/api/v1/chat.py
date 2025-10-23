"""
聊天相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user, get_dify_api_key
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.schemas.message import ChatRequest
from app.services.dify_client import DifyClient
import json

router = APIRouter()


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    流式聊天接口（SSE）

    - **message**: 用户消息
    - **conversation_id**: 对话ID（可选，不传则创建新对话）
    """
    # 获取Dify API密钥
    api_key = get_dify_api_key(db)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Dify API未配置，请联系管理员"
        )

    # 获取或创建对话
    conversation = None
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="对话不存在"
            )
    else:
        # 创建新对话
        conversation = Conversation(
            user_id=current_user.id,
            title=request.message[:50] if len(request.message) > 50 else request.message
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # 保存用户消息
    user_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=request.message
    )
    db.add(user_message)
    db.commit()

    # 调用Dify API
    dify_client = DifyClient(api_key)

    async def event_generator():
        """SSE事件生成器"""
        # 先发送对话ID
        yield f"data: {json.dumps({'conversation_id': conversation.id, 'event': 'conversation_id'})}\n\n"

        assistant_content = ""

        async for chunk in dify_client.stream_chat(
            query=request.message,
            conversation_id=str(conversation.id),
            user=str(current_user.id)
        ):
            # 转发Dify的SSE响应
            yield chunk

            # 尝试解析响应以收集完整内容
            try:
                if chunk.startswith("data: "):
                    data = json.loads(chunk[6:])
                    if data.get("event") == "agent_message" or data.get("event") == "message":
                        assistant_content += data.get("answer", "")
            except:
                pass

        # 流结束后保存助手消息
        if assistant_content:
            assistant_message = Message(
                conversation_id=conversation.id,
                role=MessageRole.ASSISTANT,
                content=assistant_content
            )
            db.add(assistant_message)
            db.commit()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
