from dependency_injector import containers

from ..services.film import FilmService
from ..services.person import PersonService

from .base import ServiceFactory, BaseContainer
from .film import ServiceContainer as FilmServiceContainer
from .cache import CacheResource, RedisCacheResource
from .search import SearchResource, ElasticSearchResource


@containers.copy(FilmServiceContainer)
class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=["..api.v1.persons"])

    person_service = ServiceFactory(
        PersonService,
        cache_svc=BaseContainer.cache_svc,
        search_svc=BaseContainer.search_svc
    )
