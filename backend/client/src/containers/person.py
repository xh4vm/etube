from dependency_injector import containers

from ..services.person import PersonService
from .base import BaseContainer, ServiceFactory
from .film import ServiceContainer as FilmServiceContainer


@containers.copy(FilmServiceContainer)
class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.persons'])

    person_service = ServiceFactory(
        PersonService, cache_svc=BaseContainer.cache_svc, search_svc=BaseContainer.search_svc
    )
