from abc import ABCMeta, abstractmethod
from typing import Optional

from elastic_transport import ObjectApiResponse
from pydantic.main import ModelMetaclass
from src.core.config import APP_CONFIG, service_logger

from ..models.base import PageModel
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
        """Название индекса для поиска"""

    @property
    @abstractmethod
    def search_fields(self) -> list[str]:
        """Поля по которым будет производиться поиск"""

    @property
    @abstractmethod
    def brief_model(self) -> ModelMetaclass:
        """Название pydantic модели для получения усеченного результата"""

    @property
    @abstractmethod
    def full_model(self) -> ModelMetaclass:
        """Название pydantic модели для получения полного результата"""

    @property
    @abstractmethod
    def model_sort(self) -> ModelMetaclass:
        """Название pydantic модели для вариантов сортировки"""

    @property
    @abstractmethod
    def model_filter(self) -> ModelMetaclass:
        """Название pydantic модели для вариантов фильтрации"""

    async def get_by_id(self, id: str) -> Optional[ModelMetaclass]:
        cache_key = f'{self.index}.get_by_id(id={id})'
        data = await self.cache_svc.get(cache_key)

        if data is None:
            service_logger.info(f'Кеш в методе "get_by_id" пo ключу {cache_key} не найден.')
            data: ObjectApiResponse = await self.search_svc.get_by_id(index=self.index, id=id)

            if data is None:
                service_logger.info('Данные не найдены.')
                return None

            await self.cache_svc.set(key=cache_key, data=data.body)

        return self.full_model.parse_obj(data['_source'])

    async def search(
        self,
        page: int = APP_CONFIG.page,
        page_size: int = APP_CONFIG.page_size,
        search_fields: Optional[list[str]] = None,
        search_value: Optional[str] = None,
        sort_fields: Optional[str] = None,
        filters: Optional[str] = None,
        model_mapping: Optional[ModelMetaclass] = None,
    ) -> PageModel[ModelMetaclass]:

        # Фильтрую параметры фильтрации. В поиск идут только валидные
        filters = (
            [
                tuple(filter_tuple)
                for filter_ in filters.split(',')
                if self.model_filter.find_elem((filter_tuple := filter_.split(':'))[0]) is not None
            ]
            if filters is not None
            else None
        )

        service_logger.info(f'Фильтpы, прошедшие валидацию: {filters}')

        # Фильтрую параметры сортировки. В поиск идут только валидные
        sort_fields = (
            list(filter(lambda x: self.model_sort.find_elem(x) is not None, sort_fields.split(',')))
            if sort_fields is not None
            else None
        )

        service_logger.info(f'Параметры сортировки, прошедшие валидацию: {sort_fields}')

        search_params: SearchParams[self.model_sort] = SearchParams(
            page=page,
            page_size=page_size,
            search_fields=search_fields or self.search_fields,
            search_value=search_value,
            sort_fields=sort_fields,
            filters=filters,
        )

        cache_key = f'{self.index}.search({search_params}'

        data = await self.cache_svc.get(key=cache_key)

        if data is None:
            service_logger.info(f'Кеш в методе "search" пo ключу {cache_key} не найден.')
            data: SearchResult = await self.search_svc.search(index=self.index, params=search_params)
            await self.cache_svc.set(key=cache_key, data=data.dict())
        else:
            service_logger.info(f'Кеш в методе "search" пo ключу {cache_key} найден.')
            data = SearchResult(**data)

        model_mapping = model_mapping or self.brief_model

        return PageModel(
            next_page=search_params.page + 1 if search_params.page * search_params.page_size < data.total else None,
            prev_page=search_params.page - 1 if search_params.page > 1 else None,
            page=search_params.page,
            page_size=search_params.page_size,
            total=data.total,
            items=[model_mapping(**elem) for elem in data.items],
        )
