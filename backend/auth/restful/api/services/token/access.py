from typing import Any, Optional
from jaeger_telemetry.tracer import tracer
from flask_jwt_extended import create_access_token, decode_token

from .base import BaseTokenService, revoke_key


class AccessTokenService(BaseTokenService):
    @tracer.start_as_current_span('create-access-token')
    def create(self, identity: Any, claims: Optional[dict[str, Any]] = None) -> str:
        return create_access_token(identity=identity, additional_claims=claims)

    @tracer.start_as_current_span('add-access-token-to-blocklost')
    def add_to_blocklist(self, token: str) -> None:
        payload = decode_token(token)
        jti = payload.get('jti')
        self.storage_svc.set(key=revoke_key.substitute(jti=jti), data='')
