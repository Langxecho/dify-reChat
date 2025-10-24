"""
API v1路由
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .chat import router as chat_router
from .conversations import router as conversations_router
from .admin import router as admin_router
from .workflows import router as workflows_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(chat_router, prefix="/chat", tags=["聊天"])
api_router.include_router(conversations_router, prefix="/conversations", tags=["对话"])
api_router.include_router(admin_router, prefix="/admin", tags=["管理"])
api_router.include_router(workflows_router, prefix="/workflows", tags=["工作流"])
