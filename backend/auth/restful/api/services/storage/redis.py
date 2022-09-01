from typing import Any, Optional

import orjson
from core.config import CONFIG
from flask_redis import FlaskRedis
from api.utils.decorators import traced

from .base import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, redis: FlaskRedis):
        self.redis = redis

    @traced('redis::get')
    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        data = self.redis.get(key)

        if data is None:
            return default_value

        return orjson.loads(data)

    @traced('redis::set')
    def set(self, key: str, data: Any, expire: int = CONFIG.APP.ACCESS_EXPIRES) -> None:
        self.redis.setex(key, expire, orjson.dumps(data))

    @traced('redis::delete')
    def delete(self, key: str) -> None:
        self.redis.delete(key)
