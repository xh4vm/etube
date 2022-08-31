from abc import ABC, abstractmethod
from typing import Any, Optional
from jaeger_telemetry.tracer import tracer


class BaseStorage(ABC):
    @abstractmethod
    @tracer.start_as_current_span('get-from-storage')
    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        """Получение данных из хранилище"""

    @abstractmethod
    @tracer.start_as_current_span('set-to-storage')
    def set(self, key: str, data: Any, expire: int) -> None:
        """Установка данных в хранилище"""

    @abstractmethod
    @tracer.start_as_current_span('delete-from-storage')
    def delete(self, key: str) -> None:
        """Удаление данных из хранилище"""
