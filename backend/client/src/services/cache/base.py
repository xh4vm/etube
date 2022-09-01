from abc import ABC, abstractmethod
from typing import Any, Optional
from jaeger_telemetry.tracer import tracer


class BaseCache(ABC):
    @abstractmethod
    @tracer.start_as_current_span('cache::get')
    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        """Получение данных из кеша"""

    @abstractmethod
    @tracer.start_as_current_span('cache::set')
    def set(self, key: str, data: Any) -> None:
        """Установка данных в кеш"""
