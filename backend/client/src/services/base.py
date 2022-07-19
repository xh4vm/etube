from abc import ABCMeta, abstractmethod
from typing import Optional

from elastic_transport import ObjectApiResponse
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
    def index(self) -> str:
        '''Название индекса для поиска'''

    @property
    @abstractmethod
    def fields(self) -> list[str]:
        '''Поля по которым будет производиться поиск'''

    @property
    @abstractmethod
    def model(self) -> ModelMetaclass:
        '''Название pydantic модели для получения результата'''

    async def get_by_id(self, id: str) -> Optional[ModelMetaclass]:
        cache_key = f'{self.index}.get_by_id(id={id})'
        data = await self.cache_svc.get(cache_key)

        if data is None:
            data: ObjectApiResponse = await self.search_svc.get_by_id(id=id, index=self.index)

            if data is None:
                return None

            await self.cache_svc.set(key=cache_key, data=data.body)

        return self.model.parse_obj(data['_source'])

    async def search(
            self,
            page: int = 1,
            page_size: int = 10,
            search_fields: list = None,
            search_value: str = None,
            custom_index: str = None,
    ) -> list[ModelMetaclass]:
        # Поиск данных с условиями.
        # Если параметры search_field и search_value не заданы,
        # возвращается список документов соответствующего индекса,
        # ограниченный параметром page_size.
        # custom_index - применяется вместо self.index при поиске фильмов,
        # соответствующих ранее выбранному жанру или персоне.
        search_params = SearchParams(
            page=page,
            page_size=page_size,
            search_fields=search_fields,
            search_value=search_value,
        )
        # Если custom_index задан, нужно искать фильмы. В противном случае ищем в self.index.
        active_index = custom_index if custom_index else self.index

        cache_key = f'{self.index}.search({search_params}'

        # AttributeError: 'coroutine' object has no attribute 'items':
        # data = self.cache_svc.get(key=cache_key)
        data = None

        if data is None:
            data: SearchResult = await self.search_svc.search(index=active_index, params=search_params)

            if data.total == 0:
                return []

            # TypeError: RedisCache.set() got an unexpected keyword argument 'value':
            # await self.cache_svc.set(key=cache_key, value=data)

        if custom_index:
            return data.items

        return (self.model(**elem) for elem in data.items)
