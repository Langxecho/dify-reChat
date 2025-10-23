"""
FastAPI主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="Dify工作流API封装的AI对话平台",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # 允许的源
    allow_credentials=True,                     # 允许携带cookie
    allow_methods=["*"],                        # 允许所有HTTP方法
    allow_headers=["*"],                        # 允许所有HTTP头
)

# 注册API路由
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
