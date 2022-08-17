from typing import Any, Optional
from flask_jwt_extended import create_access_token, decode_token

from .base import BaseTokenService


class AccessTokenService(BaseTokenService):

    def create(self, identity: Any, claims: Optional[dict[str, Any]] = None) -> str:
        return create_access_token(identity=identity, additional_claims=claims)

    def add_to_blocklist(self, token: str) -> None:
        jti = decode_token(token).get('jti')
        self.storage_svc.set(key=f'revoked::token::{jti}', data='')
