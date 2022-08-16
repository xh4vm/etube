from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseStorage(ABC):
    @abstractmethod
    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        """Получение данных из хранилище"""

    @abstractmethod
    def set(self, key: str, data: Any) -> None:
        """Установка данных в хранилище"""
