"""
Генерации фейковых данных, которые используются для тестов.

"""

from abc import ABC, abstractmethod

from pydantic.main import ModelMetaclass


class BaseDataGenerator(ABC):
    @property
    @abstractmethod
    def fake_model(self) -> ModelMetaclass:
        """Fake model"""

    @property
    @abstractmethod
    def conn(self):
        """Datastore connector"""

    @property
    def data(self) -> list[ModelMetaclass]:
        """Сгенерированные фейковые данные"""

    @property
    def response_data(self) -> list[ModelMetaclass]:
        """Данные ответа"""

    @abstractmethod
    async def load(self) -> list[ModelMetaclass]:
        """Метод загрузки тестовых данных в хранилище"""

    @abstractmethod
    async def clean(self) -> None:
        """Метод удаления тестовых данных из хранилища"""

    def __init__(self, conn) -> None:
        self.conn = conn
