from datetime import datetime, timezone
from typing import Any, Optional

from flask_jwt_extended import create_refresh_token, decode_token

from .base import BaseTokenService, revoke_key, user_refresh_key


class RefreshTokenService(BaseTokenService):
    def create(self, identity: Any, claims: Optional[dict[str, Any]] = None) -> str:
        token = create_refresh_token(identity=identity, additional_claims=claims)

        payload = decode_token(token)

        jti = payload.get('jti')
        exp = payload.get('exp')

        key = user_refresh_key.substitute(jti=jti)

        ttl = exp - int(datetime.now(timezone.utc).timestamp())
        self.storage_svc.set(key=key, data='', expire=ttl)

        return token

    def add_to_blocklist(self, token: str) -> None:
        payload = decode_token(token)

        jti = payload.get('jti')
        exp = payload.get('exp')

        key = user_refresh_key.substitute(jti=jti)

        if self.storage_svc.get(key):
            self.storage_svc.delete(key)

        ttl = exp - int(datetime.now(timezone.utc).timestamp())
        self.storage_svc.set(key=revoke_key.substitute(jti=jti), data='', expire=ttl)
