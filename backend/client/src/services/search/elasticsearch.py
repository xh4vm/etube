from typing import Any, Optional
from elasticsearch import AsyncElasticsearch
from .base import BaseSearch, SearchParams, SearchResult


class ElasticSearch(BaseSearch):

    def __init__(self, elasticsearch: AsyncElasticsearch):
        self.elasticsearch = elasticsearch

    async def get_by_id(self, index: str, id: str) -> Optional[dict[str, Any]]:
        pass

    async def search(self, index: str, params: SearchParams) -> SearchResult:
        pass
