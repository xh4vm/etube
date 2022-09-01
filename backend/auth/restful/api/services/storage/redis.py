from typing import Any, Optional
from jaeger_telemetry.tracer import tracer

import orjson
from core.config import CONFIG
from flask_redis import FlaskRedis

from .base import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, redis: FlaskRedis):
        self.redis = redis

    @tracer.start_as_current_span('redis::get')
    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        data = self.redis.get(key)

        if data is None:
            return default_value

        return orjson.loads(data)

    @tracer.start_as_current_span('redis::set')
    def set(self, key: str, data: Any, expire: int = CONFIG.APP.ACCESS_EXPIRES) -> None:
        self.redis.setex(key, expire, orjson.dumps(data))

    @tracer.start_as_current_span('redis::delete')
    def delete(self, key: str) -> None:
        self.redis.delete(key)
