from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from .base import BaseService
from ..core.indices import GENRE_INDEX

from ..db.redis import get_redis
from ..db.elasticsearch import get_elasticsearch

from .cache.base import BaseCache
from .cache.redis import RedisCache

from .search.base import BaseSearch
from .search.elasticsearch import ElasticSearch


class GenreService(BaseService):
    index = GENRE_INDEX.index
    model = GENRE_INDEX.model
    search_fileds = GENRE_INDEX.search_fields


async def get_genre_service(
    redis: Redis = Depends(get_redis),
    elasticsearch: AsyncElasticsearch = Depends(get_elasticsearch)
) -> GenreService:
    cache: BaseCache = RedisCache(redis=redis)
    search: BaseSearch = ElasticSearch(elasticsearch=elasticsearch)
    return GenreService(cache_svc=cache, search_svc=search)
