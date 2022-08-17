"""
Базовый сервис получения списка разрешений пользователя.

"""

from abc import ABC, abstractmethod

from api.model.base import BaseModel


class BasePermissionsService(ABC):

    @abstractmethod
    def permissions_list(self, user_id) -> BaseModel:
        '''Метод получения списка разрешений'''

    @abstractmethod
    def create(self, **kwargs) -> BaseModel:
        '''Метод создания разрешения'''

    @abstractmethod
    def update(self, **kwargs) -> BaseModel:
        '''Метод обновления разрешения'''

    @abstractmethod
    def delete(self, permission_id) -> BaseModel:
        '''Метод удаления разрешения'''
