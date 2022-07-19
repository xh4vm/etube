from abc import ABCMeta, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel
from pydantic.main import ModelMetaclass


class SearchParams(BaseModel):
    page: int = 1
    page_size: int = 50
    search_fields: Optional[list[str]] = None
    search_value: Optional[str] = None
    sort_fields: Optional[list[str]] = None

    def __str__(self) -> str:
        return (f'page={self.page},page_size={self.page_size}search_fields={self.search_fields},'
            f'search_value={self.search_value},sort_field={self.sort_fields}')


class SearchResult(BaseModel):
    items: list[dict[str, Any]]
    total: int = 0


class BaseSearch:
    metaclass = ABCMeta

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[ModelMetaclass]:
        '''Получить результат по ид'''

    @abstractmethod
    def search(self, index: str, params: SearchParams) -> SearchResult:
        '''Поиск по search_filds внутри индекса'''
