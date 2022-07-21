from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from ..db.elastic import get_elasticsearch
from ..db.redis import get_redis
from .base import BaseService
from .cache.redis import RedisCache
from .film import FilmService
from .genre import GenreService
from .person import PersonService
from .search.elastic import ElasticSearch


class RedisElasticServiceGiver:
    """Реализация параметризованной зависимости, для получения сервисов."""

    def __init__(self, name: BaseService):
        self.service = name

    @lru_cache
    def __call__(
        self, redis: Redis = Depends(get_redis), elasticsearch: AsyncElasticsearch = Depends(get_elasticsearch)
    ):
        cache_svc = RedisCache(redis=redis)
        search_svc = ElasticSearch(elastic=elasticsearch)
        return self.service(cache_svc=cache_svc, search_svc=search_svc)


film_service = RedisElasticServiceGiver(name=FilmService)
genre_service = RedisElasticServiceGiver(name=GenreService)
person_service = RedisElasticServiceGiver(name=PersonService)
