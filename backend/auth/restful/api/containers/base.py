from dependency_injector import containers, providers

from ..services.storage.base import BaseStorage


class BaseContainer(containers.DeclarativeContainer):
    storage_svc = providers.Dependency(instance_of=BaseStorage)
