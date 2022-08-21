"""
Контейнер сервиса ролей пользователя.

"""

from dependency_injector import containers, providers

from ..services.roles import RolesService
from ..services.user import UserService
from .base import BaseContainer


class ServiceContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.manager.user'])

    roles_service = providers.Factory(RolesService, storage_svc=BaseContainer.storage_svc)
    user_service = providers.Factory(UserService, storage_svc=BaseContainer.storage_svc)
