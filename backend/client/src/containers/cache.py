from typing import Optional, Type

from dependency_injector import providers, resources

from ..db.redis import get_redis
from ..services.cache.base import BaseCache
from ..services.cache.redis import RedisCache


class CacheResource(providers.Resource):
    provided_type: Optional[Type] = BaseCache


class RedisCacheResource(resources.AsyncResource):
    async def init(self, *args, **kwargs) -> BaseCache:
        redis = await get_redis()
        return RedisCache(redis=redis)
