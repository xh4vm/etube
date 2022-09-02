from abc import ABC, abstractmethod
from typing import Any, Optional
from jaeger_telemetry.tracer import tracer
from src.utils.decorators import traced


class BaseCache(ABC):
    @abstractmethod
    @traced('cache::get')
    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        """Получение данных из кеша"""

    @abstractmethod
    @traced('cache::set')
    def set(self, key: str, data: Any) -> None:
        """Установка данных в кеш"""
