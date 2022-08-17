from abc import ABC, abstractmethod
from typing import Any, Optional
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from http import HTTPStatus

from ..storage.base import BaseStorage
from api.errors.token import TokenError
from api.schema.base import BaseError


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

    @classmethod
    def expired_token_callback(cls, header, payload):
        return BaseError(message=TokenError.EXPIRED).dict(), HTTPStatus.UNAUTHORIZED

    @classmethod
    def token_in_blocklist_callback(cls, header, payload) -> bool:
        jti = payload.get("jti")

        if jti is None:
            return False

        token_in_redis = cls.storage_svc.get(jti)
        return token_in_redis is not None

    @classmethod
    def invalid_token_callback(cls, reason: str):
        return BaseError(message=TokenError.INVALID).dict(), HTTPStatus.UNPROCESSABLE_ENTITY

    @classmethod
    def revoked_token_callback(cls, header, payload):
        return BaseError(message=TokenError.REVOKED).dict(), HTTPStatus.UNPROCESSABLE_ENTITY

    @classmethod
    def unauthorized_callback(reason: str):
        return BaseError(message=TokenError.UNAUTORIZED).dict(), HTTPStatus.UNAUTHORIZED

    @classmethod
    def token_verification_failed_callback(cls, header, payload):
        return BaseError(message=TokenError.VERIFY).dict(), HTTPStatus.UNPROCESSABLE_ENTITY
