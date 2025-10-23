"""
API依赖项
包括身份验证、数据库会话等
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.models.setting import SystemSetting
from typing import Optional

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户

    Args:
        credentials: HTTP Bearer Token
        db: 数据库会话

    Returns:
        当前用户对象

    Raises:
        HTTPException: 401 未授权
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前管理员用户

    Args:
        current_user: 当前用户

    Returns:
        管理员用户对象

    Raises:
        HTTPException: 403 无权限
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user


def get_dify_api_key(db: Session = Depends(get_db)) -> Optional[str]:
    """
    获取Dify API密钥

    Args:
        db: 数据库会话

    Returns:
        API密钥，如果未配置则返回None
    """
    setting = db.query(SystemSetting).filter(
        SystemSetting.key == "dify_api_key"
    ).first()

    if setting:
        return setting.value
    return None
