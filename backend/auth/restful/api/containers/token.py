from typing import Optional, Type
from dependency_injector import containers, providers

from .base import BaseContainer

from ..services.token.base import BaseTokenService
from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService


class TokenFactory(providers.Factory):
    provided_type: Optional[Type] = BaseTokenService


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.token'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    refresh_token_service = TokenFactory(RefreshTokenService, storage_svc=BaseContainer.storage_svc)
