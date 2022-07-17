from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from .base import BaseService
from ..core.indices import FILM_INDEX

from .cache.base import BaseCache
from .cache.redis import RedisCache

from .search.base import BaseSearch
from .search.elasticsearch import ElasticSearch

from ..db.redis import get_redis
from ..db.elasticsearch import get_elasticsearch


class FilmService(BaseService):
    index = FILM_INDEX.index
    model = FILM_INDEX.model
    search_fileds = FILM_INDEX.search_fields


async def get_film_service(
    redis: Redis = Depends(get_redis), 
    elasticsearch: AsyncElasticsearch = Depends(get_elasticsearch)
) -> FilmService:

    cache: BaseCache = RedisCache(redis=redis)
    search: BaseSearch = ElasticSearch(elasticsearch==elasticsearch)
    return FilmService(cache_svc=cache, search_svc=search)
