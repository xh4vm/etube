from dependency_injector import containers

from ..services.genre import GenreService
from .base import BaseContainer, ServiceFactory
from .film import ServiceContainer as FilmServiceContainer


@containers.copy(FilmServiceContainer)
class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.genres'])

    genre_service = ServiceFactory(
        GenreService, cache_svc=BaseContainer.cache_svc, search_svc=BaseContainer.search_svc
    )
