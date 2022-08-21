"""
Контейнер сервиса ролей пользователя.

"""

from dependency_injector import containers, providers

from ..services.permissions import PermissionsService
from ..services.roles import RolesService
from .base import BaseContainer


class ServiceContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.manager.role'])

    roles_service = providers.Factory(RolesService, storage_svc=BaseContainer.storage_svc)
    permissions_service = providers.Factory(PermissionsService, storage_svc=BaseContainer.storage_svc)
