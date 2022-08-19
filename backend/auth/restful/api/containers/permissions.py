"""
Контейнер сервиса получения списка разрешений пользователя.

"""

from dependency_injector import containers, providers

from ..services.manager.permissions import PermissionsService
from .base import BaseContainer


class ServiceContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=['..endpoint.manager.permission'])
    permissions_service = providers.Factory(PermissionsService, storage_svc=BaseContainer.storage_svc)
