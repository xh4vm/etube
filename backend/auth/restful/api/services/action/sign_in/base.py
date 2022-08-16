from abc import ABC, abstractmethod

from api.model.base import BaseModel


class BaseSignInService(ABC):

    @abstractmethod
    def authorization(self, login: str, password: str) -> BaseModel:
        '''Метод авторизации'''