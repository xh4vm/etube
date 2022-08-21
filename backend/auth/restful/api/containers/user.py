"""
Контейнер сервиса ролей пользователя.

"""

from dependency_injector import containers, providers

from ..services.roles import RolesService
from ..services.sign_in_history import SignInHistoryService
from ..services.token.access import AccessTokenService
from ..services.user import UserService
from .base import BaseContainer
from .token import TokenFactory


class ServiceContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.manager.user'])

    access_token_service = TokenFactory(AccessTokenService, storage_svc=BaseContainer.storage_svc)
    roles_service = providers.Factory(RolesService, storage_svc=BaseContainer.storage_svc)
    user_service = providers.Factory(UserService, storage_svc=BaseContainer.storage_svc)
    history_service = providers.Factory(SignInHistoryService, storage_svc=BaseContainer.storage_svc)
