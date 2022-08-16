from dependency_injector import containers, providers

from .base import BaseContainer
from .token import TokenFactory

from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService
from ..services.sign_in_history import SignInHistoryService


class SignInServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    refresh_token_service = TokenFactory(RefreshTokenService, storage_svc=BaseContainer.storage_svc)
    sign_in_history_service = providers.Factory(SignInHistoryService)
