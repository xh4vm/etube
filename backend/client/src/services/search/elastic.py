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

        if params.search_value and params.search_fields and len(params.search_value):
            query = {
                'query': {
                    'multi_match': {
                        'query': params.search_value,
                        'fields': params.search_fields,
                        'fuzziness': 'auto',
                        'operator': 'and'
                    }
                }
            }

        docs = await self.elastic.search(
            index=index,
            body=query,
            size=params.page_size,
            sort=params.sort_fields,
            from_=(params.page - 1) * params.page_size
        )

        return SearchResult(
            total=docs.get('hits').get('total').get('value'),
            items=[doc['_source'] for doc in docs.get('hits').get('hits')],
        )
