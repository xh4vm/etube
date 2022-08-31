from typing import Optional, Type

from dependency_injector import containers, providers

from api.services.authorization.oauth.base import BaseOAuth
from api.services.authorization.oauth.vk_auth import VKAuth
from api.services.authorization.oauth.yandex_auth import YandexAuth
from ..services.sign_in_history import SignInHistoryService
from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService
from .base import BaseContainer
from .token import TokenFactory


class AuthFactory(providers.Factory):
    provided_type: Optional[Type] = BaseOAuth


class YandexAuthContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    refresh_token_service = TokenFactory(RefreshTokenService, storage_svc=BaseContainer.storage_svc)
    auth_service = AuthFactory(YandexAuth)
    sign_in_history_service = providers.Factory(SignInHistoryService, storage_svc=BaseContainer.storage_svc)


class VKAuthContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    refresh_token_service = TokenFactory(RefreshTokenService, storage_svc=BaseContainer.storage_svc)
    auth_service = AuthFactory(VKAuth)
    sign_in_history_service = providers.Factory(SignInHistoryService, storage_svc=BaseContainer.storage_svc)
