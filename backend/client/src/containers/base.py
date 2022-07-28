from typing import Optional, Type
from dependency_injector import providers

from ..services.base import BaseService


class ServiceFactory(providers.Factory):
    provided_type: Optional[Type] = BaseService
