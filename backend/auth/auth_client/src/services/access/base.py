from abc import ABC, abstractmethod
from typing import Literal, Union


class BaseAccessService(ABC):
    @abstractmethod
    def is_accessible(
        self, token: str, method: str, url: str
    ) -> dict[Literal['is_accessible', 'message'], Union[bool, str]]:
        """Метод проверки доступа"""
