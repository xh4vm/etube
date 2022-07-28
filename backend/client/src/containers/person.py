from dependency_injector import containers

from ..services.film import FilmService
from ..services.person import PersonService

from .base import ServiceFactory
from .cache import CacheResource, RedisCacheResource
from .search import SearchResource, ElasticSearchResource


class ServiceRedisElasticContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["..api.v1.persons"])
    
    cache_svc = CacheResource(RedisCacheResource)
    search_svc = SearchResource(ElasticSearchResource)

    film_service = ServiceFactory(
        FilmService,
        cache_svc=cache_svc,
        search_svc=search_svc
    )

    person_service = ServiceFactory(
        PersonService,
        cache_svc=cache_svc,
        search_svc=search_svc
    )
