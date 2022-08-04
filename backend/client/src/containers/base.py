from typing import Optional, Type

from dependency_injector import containers, providers

from ..services.base import BaseService
from ..services.cache.base import BaseCache
from ..services.search.base import BaseSearch


class ServiceFactory(providers.Factory):
    provided_type: Optional[Type] = BaseService


class BaseContainer(containers.DeclarativeContainer):
    cache_svc = providers.Dependency(instance_of=BaseCache)
    search_svc = providers.Dependency(instance_of=BaseSearch)
