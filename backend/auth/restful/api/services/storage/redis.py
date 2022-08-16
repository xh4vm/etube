from typing import Any, Optional
import orjson
from flask_redis import FlaskRedis

from core.config import CONFIG
from .base import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, redis: FlaskRedis, expire: int = CONFIG.APP.ACCESS_EXPIRES):
        self.redis = redis
        self.expire = expire

    async def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        data = await self.redis.get(key)

        if data is None:
            return default_value

        return orjson.loads(data)

    async def set(self, key: str, data: Any) -> None:
        await self.redis.set(key=key, value=orjson.dumps(data), expire=self.expire)
