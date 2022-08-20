from http import HTTPStatus

from .base import revoke_key
from ..storage.base import BaseStorage
from api.errors.token import TokenError
from api.schema.base import BaseError


class TokenHandlerService:

    def __init__(self, storage_svc: BaseStorage):
        self.storage_svc = storage_svc

    def expired_token_callback(self, header, payload):
        return BaseError(message=TokenError.EXPIRED).dict(), HTTPStatus.UNAUTHORIZED

    def token_in_blocklist_callback(self, header, payload) -> bool:
        jti = payload.get("jti")

        if jti is None:
            return False

        token_in_redis = self.storage_svc.get(revoke_key.substitute(jti=jti))
        return token_in_redis is not None

    def invalid_token_callback(self, reason: str):
        return BaseError(message=TokenError.INVALID).dict(), HTTPStatus.UNPROCESSABLE_ENTITY

    def revoked_token_callback(self, header, payload):
        return BaseError(message=TokenError.REVOKED).dict(), HTTPStatus.UNPROCESSABLE_ENTITY

    def unauthorized_callback(reason: str):
        return BaseError(message=TokenError.UNAUTORIZED).dict(), HTTPStatus.UNAUTHORIZED

    def token_verification_failed_callback(self, header, payload):
        return BaseError(message=TokenError.VERIFY).dict(), HTTPStatus.UNPROCESSABLE_ENTITY
