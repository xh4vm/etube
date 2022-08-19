"""
Контейнер сервисов регистрации пользователя.

"""

from typing import Optional, Type

from dependency_injector import containers, providers

from ..services.token.access import AccessTokenService
from ..services.user import UserService

from .token import TokenFactory
from .base import BaseContainer



class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.action'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    user_service = providers.Factory(UserService, storage_svc=BaseContainer.storage_svc)