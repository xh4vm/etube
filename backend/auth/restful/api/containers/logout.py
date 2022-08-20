from dependency_injector import containers

from .base import BaseContainer
from .token import TokenFactory

from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    refresh_token_service = TokenFactory(RefreshTokenService, storage_svc=BaseContainer.storage_svc)
