"""
聊天相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.models.workflow import Workflow, ConversationWorkflow
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
    - **workflow_id**: 工作流ID（可选，不传则使用默认工作流）
    """
    # 获取工作流配置
    workflow = None
    if request.workflow_id:
        # 使用指定工作流
        workflow = db.query(Workflow).filter(
            Workflow.id == request.workflow_id,
            Workflow.is_active == True
        ).first()
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="工作流不存在或已禁用"
            )
    else:
        # 使用默认工作流
        workflow = db.query(Workflow).filter(
            Workflow.is_default == True,
            Workflow.is_active == True
        ).first()

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="未找到可用的Dify工作流，请联系管理员配置"
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

        # 关联工作流
        conversation_workflow = ConversationWorkflow(
            conversation_id=conversation.id,
            workflow_id=workflow.id
        )
        db.add(conversation_workflow)
        db.commit()

    # 保存用户消息
    user_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=request.message,
        meta_data=json.dumps({"workflow_id": workflow.id, "workflow_name": workflow.name})
    )
    db.add(user_message)
    db.commit()

    # 调用Dify API
    dify_client = DifyClient(workflow.dify_api_key)

    async def event_generator():
        """SSE事件生成器"""
        # 先发送对话ID和工作流信息
        yield f"data: {json.dumps({'conversation_id': conversation.id, 'workflow_id': workflow.id, 'workflow_name': workflow.name, 'event': 'conversation_info'})}\n\n"

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
                content=assistant_content,
                meta_data=json.dumps({"workflow_id": workflow.id, "workflow_name": workflow.name})
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
