from typing import Any, Optional
import orjson
from flask_redis import FlaskRedis

from core.config import CONFIG
from .base import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, redis: FlaskRedis, expire: int = CONFIG.APP.ACCESS_EXPIRES):
        self.redis = redis
        self.expire = expire

    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        data = self.redis.get(key)

        if data is None:
            return default_value

        return orjson.loads(data)

    def set(self, key: str, data: Any) -> None:
        self.redis.setex(key, self.expire, orjson.dumps(data))
