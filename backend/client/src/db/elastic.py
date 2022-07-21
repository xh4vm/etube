from typing import Optional

from elasticsearch import AsyncElasticsearch

es: Optional[AsyncElasticsearch] = None


async def get_elasticsearch() -> AsyncElasticsearch:
    return es
