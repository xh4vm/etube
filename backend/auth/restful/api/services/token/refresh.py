from typing import Any
from flask_jwt_extended import create_refresh_token

from core.config import CONFIG
from .base import BaseTokenService


class RefreshTokenService(BaseTokenService):

    def create(self, claims: Any) -> str:
        return create_refresh_token(identity=claims)

    def add_to_blocklist(self, token: str, expire: int = CONFIG.APP.ACCESS_EXPIRES) -> None:
        self.storage_svc.set(token, expire)
