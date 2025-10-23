"""
Dify API客户端
用于调用Dify工作流API
"""
import httpx
from typing import AsyncGenerator, Optional
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)


class DifyClient:
    """Dify API客户端"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = settings.DIFY_API_URL

    async def stream_chat(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        user: str = "default_user"
    ) -> AsyncGenerator[str, None]:
        """
        流式调用Dify工作流API

        Args:
            query: 用户消息
            conversation_id: 对话ID（可选）
            user: 用户标识

        Yields:
            SSE格式的响应数据
        """
        url = f"{self.base_url}/v1/chat-messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "streaming",
            "user": user
        }

        if conversation_id:
            payload["conversation_id"] = conversation_id

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as response:
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if line.strip():
                            # SSE格式: data: {...}
                            if line.startswith("data: "):
                                yield line + "\n\n"
                            else:
                                yield f"data: {line}\n\n"

        except httpx.HTTPError as e:
            logger.error(f"Dify API error: {e}")
            error_data = {
                "event": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    async def blocking_chat(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        user: str = "default_user"
    ) -> dict:
        """
        阻塞式调用Dify工作流API

        Args:
            query: 用户消息
            conversation_id: 对话ID（可选）
            user: 用户标识

        Returns:
            完整的响应数据
        """
        url = f"{self.base_url}/v1/chat-messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "user": user
        }

        if conversation_id:
            payload["conversation_id"] = conversation_id

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Dify API error: {e}")
            raise
