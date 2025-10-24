"""
安全相关功能
包括密码加密、JWT token生成和验证
"""
from datetime import datetime, timedelta
from typing import Optional
import hashlib
from jose import JWTError, jwt
from .config import settings

# 使用SHA-256作为密码哈希算法，更稳定且无长度限制
def get_password_hash(password: str) -> str:
    """使用SHA-256生成密码哈希"""
    # 添加盐值来提高安全性
    salt = "dify_rechat_salt_2024"  # 在生产环境中应该使用随机盐值
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    # 在验证时也使用相同的盐值
    salt = "dify_rechat_salt_2024"
    salted_password = plain_password + salt
    return hashlib.sha256(salted_password.encode('utf-8')).hexdigest() == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌

    Args:
        data: 要编码的数据（通常包含用户ID等）
        expires_delta: 过期时间增量

    Returns:
        编码后的JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    验证JWT token

    Args:
        token: JWT token字符串

    Returns:
        解码后的payload，如果无效则返回None
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
