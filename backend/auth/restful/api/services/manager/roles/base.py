"""
Базовый сервис ролей пользователя.

"""

from abc import ABC, abstractmethod

from api.model.base import BaseModel


class BaseRolesService(ABC):

    @abstractmethod
    def roles_list(self, user_id) -> BaseModel:
        '''Метод получения списка ролей'''

    @abstractmethod
    def create(self, **kwargs) -> BaseModel:
        '''Метод создания роли'''

    @abstractmethod
    def update(self, **kwargs) -> BaseModel:
        '''Метод обновления роли'''

    @abstractmethod
    def delete(self, role_id) -> BaseModel:
        '''Метод удаления роли'''

    @abstractmethod
    def set_permission(self, role_id, permissions) -> BaseModel:
        '''Метод добавления разрешения роли'''

    @abstractmethod
    def retrieve_permission(self, role_id, permissions) -> BaseModel:
        '''Метод удаления разрешения роли'''
