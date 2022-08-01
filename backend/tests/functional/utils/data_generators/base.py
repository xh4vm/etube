"""
Генерации фейковых данных, которые используются для тестов.

"""

from abc import ABC, abstractmethod
from pydantic.main import ModelMetaclass


class BaseDataGenerator(ABC):

    @property
    @abstractmethod
    def conn(self):
        '''Datastore connector'''

    @property
    @abstractmethod
    def fake_model(self) -> ModelMetaclass:
        '''Fake model'''

    @property
    @abstractmethod
    def data(self) -> list[ModelMetaclass]:
        '''Сгенерированные фейковые данные'''

    @abstractmethod
    async def load(self):
        '''Метод загрузки тестовых данных в хранилище'''

    @abstractmethod
    async def clean(self):
        '''Метод удаления тестовых данных из хранилища'''
