from abc import ABCMeta, abstractmethod
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from src.core.config import APP_CONFIG


SFTYPE = TypeVar('SFTYPE')


class SearchParams(BaseModel, Generic[SFTYPE]):
    page: int = APP_CONFIG.page
    page_size: int = APP_CONFIG.page_size
    search_fields: Optional[list[str]] = None
    search_value: Optional[str] = None
    sort_fields: Optional[list[SFTYPE]] = None

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
