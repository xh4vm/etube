from abc import ABCMeta, abstractmethod
from typing import Optional

from elastic_transport import ObjectApiResponse
from pydantic.main import ModelMetaclass

from .cache.base import BaseCache
from .search.base import BaseSearch, SearchParams, SearchResult
from ..models.models import PageModel


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
    def search_fields(self) -> list[str]:
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
            search_fields: Optional[list[str]] = None,
            search_value: Optional[str] = None,
            sort_fields: Optional[str] = None,
            custom_index: Optional[str] = None,
    ) -> PageModel[ModelMetaclass]:
        # Поиск данных с условиями.
        # Если параметры search_field и search_value не заданы,
        # возвращается список документов соответствующего индекса,
        # ограниченный параметром page_size.
        # custom_index - применяется вместо self.index при поиске фильмов,
        # соответствующих ранее выбранному жанру или персоне.

        search_params = SearchParams(
            page=page,
            page_size=page_size,
            search_fields=search_fields or self.search_fields,
            search_value=search_value,
            sort_field=sort_fields.split(',')
        )
        # Если custom_index задан, нужно искать фильмы. В противном случае ищем в self.index.
        active_index = custom_index if custom_index else self.index

        cache_key = f'{self.index}.search({search_params}'

        data = await self.cache_svc.get(key=cache_key)

        if data is None:
            data: SearchResult = await self.search_svc.search(index=active_index, params=search_params)

            if data.total == 0:
                return []

            await self.cache_svc.set(key=cache_key, data=data.dict())
        else:
            data = SearchResult(**data)

        if custom_index:
            return data.items

        return PageModel(
            next_page=search_params.page + 1 if search_params.page * search_params.page_size < data.total else None,
            prev_page=search_params.page - 1 if search_params.page > 1 else None,
            page=search_params.page,
            page_size=search_params.page_size,
            total=data.total,
            items=[self.model(**elem) for elem in data.items]
        )
