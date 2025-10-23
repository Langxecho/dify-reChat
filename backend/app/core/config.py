"""
应用配置
使用 pydantic-settings 管理环境变量
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json


class Settings(BaseSettings):
    """应用配置类"""

    # 应用信息
    APP_NAME: str = "Dify ReChat"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # 数据库配置
    DATABASE_URL: str

    # JWT配置
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 43200  # 30天

    # Dify API配置
    DIFY_API_URL: str = "https://api.dify.ai"

    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """解析CORS_ORIGINS（支持JSON字符串格式）"""
        if isinstance(self.CORS_ORIGINS, str):
            try:
                return json.loads(self.CORS_ORIGINS)
            except json.JSONDecodeError:
                return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS


# 全局配置实例
settings = Settings()
