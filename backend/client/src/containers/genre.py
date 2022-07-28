from dependency_injector import containers

from ..services.film import FilmService
from ..services.genre import GenreService

from .base import ServiceFactory
from .cache import CacheResource, RedisCacheResource
from .search import SearchResource, ElasticSearchResource


class ServiceRedisElasticContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["..api.v1.genres"])
    
    cache_svc = CacheResource(RedisCacheResource)
    search_svc = SearchResource(ElasticSearchResource)

    film_service = ServiceFactory(
        FilmService,
        cache_svc=cache_svc,
        search_svc=search_svc
    )

    genre_service = ServiceFactory(
        GenreService,
        cache_svc=cache_svc,
        search_svc=search_svc
    )
