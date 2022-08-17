from abc import ABC, abstractmethod
from typing import Any
from flask_jwt_extended import verify_jwt_in_request

from ..storage.base import BaseStorage


class BaseTokenService(ABC):

    def __init__(self, storage_svc: BaseStorage):
        self.storage_svc = storage_svc

    @abstractmethod
    def create(self, claims: Any) -> str:
        '''Метод для генерации токена'''
    
    @abstractmethod
    def add_to_blocklist(self, expired_time: int) -> None:
        '''Помечивание токена как протухшего'''

    def is_valid_into_request(self) -> bool:
        try:
            if verify_jwt_in_request() is not None:
                return True
        except Exception:
            pass
        
        return False
