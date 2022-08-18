from typing import Any, Optional
from flask_jwt_extended import create_refresh_token, decode_token

from .base import BaseTokenService, revoke_key, user_refresh_key


class RefreshTokenService(BaseTokenService):

    def create(self, identity: Any, claims: Optional[dict[str, Any]] = None) -> str:
        token = create_refresh_token(identity=identity, additional_claims=claims)
        jti = decode_token(token).get('jti')
        
        refresh_list: Optional[list[str]] = self.storage_svc.get(user_refresh_key.substitute(user_id=identity)) or []
        refresh_list.append(jti)

        self.storage_svc.set(
            key=user_refresh_key.substitute(user_id=identity), 
            data=refresh_list
        )
        
        return token

    def add_to_blocklist(self, token: str) -> None:
        payload = decode_token(token)
        
        identity = payload.get('sub')
        jti = payload.get('jti')

        refresh_list: Optional[list[str]] = self.storage_svc.get(user_refresh_key.substitute(user_id=identity)) or []

        if jti in refresh_list:
            refresh_list.remove(jti)

        self.storage_svc.set(
            key=user_refresh_key.substitute(user_id=identity), 
            data=refresh_list
        )

        self.storage_svc.set(key=revoke_key.substitute(jti=jti), data='')
