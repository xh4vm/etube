from typing import Any, Optional
import orjson
from aioredis import Redis

from .base import BaseCache
from src.core.config import REDIS_CONFIG


class RedisCache(BaseCache):

    def __init__(self, redis: Redis, expire: int = REDIS_CONFIG.expire):
        self.redis = redis
        self.expire = expire

    async def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        data = await self.redis.get(key)
        
        if data is None:
            return default_value

        return orjson.loads(data)

    async def set(self, key: str, data: Any) -> None:
        await self.redis.set(key=key, value=orjson.dumps(data), expire=self.expire)
