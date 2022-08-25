from typing import Optional, Type

from dependency_injector import containers, providers

from ..services.oauth.base import BaseOAuthAuthorization
from ..services.oauth.oauth_authorization import YandexAuth
from ..services.sign_in_history import SignInHistoryService
from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService
from .base import BaseContainer
from .token import TokenFactory


class AuthFactory(providers.Factory):
    provided_type: Optional[Type] = BaseOAuthAuthorization


class YandexAuthContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    refresh_token_service = TokenFactory(RefreshTokenService, storage_svc=BaseContainer.storage_svc)
    auth_service = AuthFactory(YandexAuth)
    sign_in_history_service = providers.Factory(SignInHistoryService, storage_svc=BaseContainer.storage_svc)
