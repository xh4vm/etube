from dependency_injector import containers

from ..services.film import FilmService
from .base import BaseContainer, ServiceFactory


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.films'])

    film_service = ServiceFactory(FilmService, cache_svc=BaseContainer.cache_svc, search_svc=BaseContainer.search_svc)
