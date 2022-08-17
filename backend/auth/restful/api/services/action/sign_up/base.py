"""
Базовый сервис регистрации пользователя.

"""

from abc import ABC, abstractmethod

from api.model.base import BaseModel


class BaseSignUpService(ABC):

    @abstractmethod
    def registration(self, login: str, email: str, password: str) -> BaseModel:
        '''Метод регистрации'''
