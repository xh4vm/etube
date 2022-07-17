from functools import lru_cache

from typing import Optional

from aioredis import Redis
import elasticsearch
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
import pydantic

from db.elastic import get_elastic
from db.redis import get_redis

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5

class Service:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.model = None

    async def get_by_id(self, doc_id: str, index: str) -> Optional[pydantic.main.ModelMetaclass]:
        doc = await self._doc_from_cache(doc_id)
        if not doc:
            doc = await self._get_doc_from_elastic(doc_id, index)
            if not doc:
                return None
            await self._put_doc_to_cache(doc)
        return doc

    async def _get_doc_from_elastic(self, doc_id: str, index: str) -> Optional[pydantic.main.ModelMetaclass]:
        try:
            doc = await self.elastic.get(index=index, id=doc_id)
        except elasticsearch.NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def _doc_from_cache(self, doc_id: str) -> Optional[pydantic.main.ModelMetaclass]:
        data = await self.redis.get(doc_id)
        if not data:
            return None
        doc = self.model.parse_raw(data)
        return doc

    async def _put_doc_to_cache(self, doc: pydantic.main.ModelMetaclass):
        await self.redis.set(doc.id, doc.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> Service:
    return Service(redis, elastic)
