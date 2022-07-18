from datetime import timedelta
from typing import Any, Optional

import orjson
from aioredis import Redis

from .base import BaseCache


class RedisCache(BaseCache):

    def __init__(self, redis: Redis, expire: timedelta = timedelta(minutes=5)):
        self.redis = redis
        self.expire = int(expire.total_seconds())

    async def get(self, key: str, default_value: Optional[str] = None) -> str:
        data = await self.redis.get(key)
        
        if data is None:
            return str(default_value)

        return orjson.loads(data)

    async def set(self, key: str, data: Any) -> None:
        await self.redis.set(key=key, value=orjson.dumps(data), expire=self.expire)
