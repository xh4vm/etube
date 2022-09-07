from typing import Any, Optional

import orjson
from aioredis import Redis
from src.core.config import CONFIG
from src.utils.decorators import traced

from .base import BaseCache


class RedisCache(BaseCache):
    def __init__(self, redis: Redis, expire: int = CONFIG.REDIS.cache_expire):
        self.redis = redis
        self.expire = expire

    @traced('redis::get')
    async def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        data = await self.redis.get(key)

        if data is None:
            return default_value

        return orjson.loads(data)

    @traced('redis::set')
    async def set(self, key: str, data: Any) -> None:
        await self.redis.set(key=key, value=orjson.dumps(data), expire=self.expire)
