from typing import Optional, Type
from dependency_injector import containers, providers

from .base import BaseContainer
from .token import TokenFactory

from ..services.action.sign_in.base import BaseSignInService
from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService
from ..services.action.sign_in.login_passowrd import LoginPasswordSignInService
from ..services.sign_in_history import SignInHistoryService


class SignInFactory(providers.Factory):
    provided_type: Optional[Type] = BaseSignInService


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    refresh_token_service = TokenFactory(RefreshTokenService, storage_svc=BaseContainer.storage_svc)
    sign_in_service = SignInFactory(LoginPasswordSignInService)
    sign_in_history_service = providers.Factory(SignInHistoryService)