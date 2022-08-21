from dependency_injector import containers

from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService
from .base import BaseContainer
from .token import TokenFactory


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    refresh_token_service = TokenFactory(RefreshTokenService, storage_svc=BaseContainer.storage_svc)
