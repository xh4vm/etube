from dependency_injector import containers

from ..services.film import FilmService
from ..services.genre import GenreService

from .base import ServiceFactory, BaseContainer
from .film import ServiceContainer as FilmServiceContainer
from .cache import CacheResource, RedisCacheResource
from .search import SearchResource, ElasticSearchResource


@containers.copy(FilmServiceContainer)
class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=["..api.v1.genres"])
    
    genre_service = ServiceFactory(
        GenreService,
        cache_svc=BaseContainer.cache_svc,
        search_svc=BaseContainer.search_svc
    )
