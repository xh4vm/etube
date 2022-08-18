"""
Контейнер сервиса ролей пользователя.

"""

from typing import Optional, Type

from dependency_injector import containers, providers

from ..services.manager.roles.base import BaseRolesService
from ..services.manager.roles.roles import RolesService
from .base import BaseContainer


class RoleFactory(providers.Factory):
    provided_type: Optional[Type] = BaseRolesService


class ServiceContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=['..endpoint.manager.role'])
    roles_service = RoleFactory(RolesService)
