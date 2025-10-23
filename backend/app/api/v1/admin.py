"""
管理员API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.user import User
from app.models.setting import SystemSetting

router = APIRouter()


class DifyConfigRequest(BaseModel):
    """Dify配置请求"""
    api_key: str


class DifyConfigResponse(BaseModel):
    """Dify配置响应"""
    is_configured: bool
    api_key_preview: str = ""  # 只显示前后几位


@router.get("/dify/config", response_model=DifyConfigResponse)
async def get_dify_config(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取Dify配置状态"""
    setting = db.query(SystemSetting).filter(
        SystemSetting.key == "dify_api_key"
    ).first()

    if setting and setting.value:
        # 只显示密钥的前4位和后4位
        api_key = setting.value
        preview = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
        return {
            "is_configured": True,
            "api_key_preview": preview
        }

    return {
        "is_configured": False,
        "api_key_preview": ""
    }


@router.post("/dify/config", response_model=DifyConfigResponse)
async def set_dify_config(
    config: DifyConfigRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    设置Dify API密钥

    - **api_key**: Dify API密钥
    """
    # 查找或创建配置
    setting = db.query(SystemSetting).filter(
        SystemSetting.key == "dify_api_key"
    ).first()

    if setting:
        setting.value = config.api_key
        setting.updated_by = current_admin.id
    else:
        setting = SystemSetting(
            key="dify_api_key",
            value=config.api_key,
            description="Dify API密钥",
            updated_by=current_admin.id
        )
        db.add(setting)

    db.commit()
    db.refresh(setting)

    # 返回预览
    api_key = setting.value
    preview = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"

    return {
        "is_configured": True,
        "api_key_preview": preview
    }


@router.delete("/dify/config", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dify_config(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除Dify API密钥"""
    setting = db.query(SystemSetting).filter(
        SystemSetting.key == "dify_api_key"
    ).first()

    if setting:
        db.delete(setting)
        db.commit()

    return None
