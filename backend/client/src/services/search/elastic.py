from typing import Any, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError

from .base import BaseSearch, SearchParams, SearchResult


class ElasticSearch(BaseSearch):

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, index: str, id: str) -> Optional[dict[str, Any]]:
        try:
            doc = await self.elastic.get(index=index, id=id)
        except NotFoundError:
            return None
        return doc

    async def search(self, index: str, params: SearchParams) -> SearchResult:
        query = {'query': {'match_all': {}}}
        if params.search_field:
            query = {'query': {'match': {
                params.search_field: params.search_value,
            }}}
        docs = await self.elastic.search(
            index=index,
            body=query,
            size=params.page_size,
        )
        data = SearchResult(
            total=len(docs.get('hits').get('hits')),
            items=[doc['_source'] for doc in docs.get('hits').get('hits')],
        )

        return data
