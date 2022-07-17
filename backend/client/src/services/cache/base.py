from abc import ABCMeta, abstractmethod

from typing import Any, Optional


class BaseCache:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, key: str, default_value: Optional[str] = None) -> str:
        '''Получение данных из кеша'''

    @abstractmethod
    def set(self, key: str, data: Any) -> None:
        '''Установка данных в кеш'''
