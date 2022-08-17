"""
Контейнер сервиса получения списка разрешений пользователя.

"""

from typing import Optional, Type

from dependency_injector import containers, providers

from ..services.manager.permissions.base import BasePermissionsService
from ..services.manager.permissions.permissions import PermissionsService
from .base import BaseContainer


class PermissionFactory(providers.Factory):
    provided_type: Optional[Type] = BasePermissionsService


class ServiceContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=['..endpoint.manager.permission'])
    permissions_service = PermissionFactory(PermissionsService)
