from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from .base import BaseService
from ..core.indices import PERSON_INDEX

from ..db.redis import get_redis
from ..db.elasticsearch import get_elasticsearch

from .cache.base import BaseCache
from .cache.redis import RedisCache

from .search.base import BaseSearch
from .search.elasticsearch import ElasticSearch


class PersonService(BaseService):
    index = PERSON_INDEX.index
    model = PERSON_INDEX.model
    search_fileds = PERSON_INDEX.search_fields

async def get_person_service(
    redis: Redis = Depends(get_redis),
    elasticsearch: AsyncElasticsearch = Depends(get_elasticsearch)
) -> PersonService:
    cache: BaseCache = RedisCache(redis=redis)
    search: BaseSearch = ElasticSearch(elasticsearch=elasticsearch)
    return PersonService(cache_svc=cache, search_svc=search)
