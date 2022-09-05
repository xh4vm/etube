from abc import ABC, abstractmethod
from typing import Any, Optional

from api.utils.decorators import traced


class BaseStorage(ABC):
    @abstractmethod
    @traced('storage::get')
    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        """Получение данных из хранилище"""

    @abstractmethod
    @traced('storage::set')
    def set(self, key: str, data: Any, expire: int) -> None:
        """Установка данных в хранилище"""

    @abstractmethod
    @traced('storage::delete')
    def delete(self, key: str) -> None:
        """Удаление данных из хранилище"""
