from typing import Any, Optional
from jaeger_telemetry.tracer import tracer

import orjson
from aioredis import Redis
from src.core.config import CONFIG

from .base import BaseCache


class RedisCache(BaseCache):
    def __init__(self, redis: Redis, expire: int = CONFIG.REDIS.expire):
        self.redis = redis
        self.expire = expire

    @tracer.start_as_current_span('redis::get')
    async def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        data = await self.redis.get(key)

        if data is None:
            return default_value

        return orjson.loads(data)

    @tracer.start_as_current_span('redis::set')
    async def set(self, key: str, data: Any) -> None:
        await self.redis.set(key=key, value=orjson.dumps(data), expire=self.expire)
