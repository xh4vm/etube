"""
Контейнер сервиса получения списка разрешений пользователя.

"""

from dependency_injector import containers, providers

from ..services.permissions import PermissionsService
from .base import BaseContainer


class ServiceContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=['..endpoint.v1.manager.permission'])
    permissions_service = providers.Factory(PermissionsService, storage_svc=BaseContainer.storage_svc)
