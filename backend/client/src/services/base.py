from abc import ABCMeta, abstractmethod

from typing import Optional

from pydantic.main import ModelMetaclass

from .cache.base import BaseCache
from .search.base import BaseSearch, SearchParams, SearchResult


class BaseService:
    __metaclass__ = ABCMeta

    def __init__(self, cache_svc: BaseCache, search_svc: BaseSearch):
        self.cache_svc = cache_svc
        self.search_svc = search_svc

    @property
    @abstractmethod
    def index(self):
        '''Название индекса для поиска'''

    @property
    @abstractmethod
    def fields(self):
        '''Поля по которым будет производиться поиск'''

    @property
    @abstractmethod
    def model(self):
        '''Название pydantic модели для получения результата'''

    async def get_by_id(self, id: str) -> Optional[ModelMetaclass]:
        cache_key = f'{self.index}.get_by_id({id})'
        data = await self.cache_svc.get(cache_key)

        if not data:
            data = await self.search_svc.get_by_id(id=id, index=self.index)
            if not data:
                return None
            await self.cache_svc.set(key=cache_key)
        return data

    async def search(self, page: int, page_size: int, value: str) -> list[ModelMetaclass]:
        search_params = SearchParams(page=page, page_size=page_size, search_value=value)
        cache_key = f'{self.index}.search({search_params}'

        data = self.cache_svc.get(key=cache_key)
        
        if data is None:
            data : SearchResult = self.search_svc.search(index=self.index, params=search_params)
        
            if data.total == 0:
                return []

            await self.cache_svc.set(key=cache_key, value=data)        

        return (self.model(**elem) for elem in data.items)
