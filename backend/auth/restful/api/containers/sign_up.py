"""
Контейнер сервисов регистрации пользователя.

"""

from dependency_injector import containers, providers

from ..services.token.access import AccessTokenService
from ..services.user import UserService
from .base import BaseContainer
from .token import TokenFactory


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    user_service = providers.Factory(UserService, storage_svc=BaseContainer.storage_svc)
