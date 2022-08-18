from abc import ABC, abstractmethod
from typing import Any, Optional
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from http import HTTPStatus
from string import Template


from ..storage.base import BaseStorage
from api.errors.token import TokenError
from api.schema.base import BaseError


revoke_key = Template('revoked::token::$jti')
user_refresh_key = Template('refresh_token::$user_id')

class BaseTokenService(ABC):

    def __init__(self, storage_svc: BaseStorage):
        self.storage_svc = storage_svc

    @abstractmethod
    def create(self, identity: Any, claims: Optional[dict[str, Any]] = None) -> str:
        '''Метод для генерации токена'''
    
    @abstractmethod
    def add_to_blocklist(self, token: str) -> None:
        '''Помечивание токена как протухшего'''

    def get_identity(self) -> Any:
        return get_jwt_identity()

    def get_claims(self) -> dict[str, Any]:
        return get_jwt()

    def is_valid_into_request(self) -> bool:
        try:
            if verify_jwt_in_request() is not None:
                return True
        except Exception:
            pass
        
        return False
