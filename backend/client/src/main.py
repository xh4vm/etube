import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .api.v1.films import router as film_router
from .api.v1.genres import router as genre_router
from .api.v1.persons import router as person_router
from .containers.cache import CacheResource, RedisCacheResource
from .containers.film import ServiceContainer as FilmServiceContainer
from .containers.genre import ServiceContainer as GenreServiceContainer
from .containers.person import ServiceContainer as PersonServiceContainer
from .containers.search import ElasticSearchResource, SearchResource
from .core.config import CONFIG
from .db import elastic, redis


def register_di_containers():
    redis_resource = CacheResource(RedisCacheResource)
    elasticsearch_resource = SearchResource(ElasticSearchResource)

    FilmServiceContainer(cache_svc=redis_resource, search_svc=elasticsearch_resource)
    GenreServiceContainer(cache_svc=redis_resource, search_svc=elasticsearch_resource)
    PersonServiceContainer(cache_svc=redis_resource, search_svc=elasticsearch_resource)


def register_routers(app: FastAPI):
    API_PATH = f'{CONFIG.APP.api_path}/{CONFIG.APP.version}'

    app.include_router(router=film_router, prefix=API_PATH)
    app.include_router(router=genre_router, prefix=API_PATH)
    app.include_router(router=person_router, prefix=API_PATH)


def create_app():
    app = FastAPI(
        title=CONFIG.APP.project_name,
        docs_url=f'{CONFIG.APP.api_path}{CONFIG.APP.swagger_path}',
        openapi_url=f'{CONFIG.APP.api_path}{CONFIG.APP.json_swagger_path}',
        default_response_class=ORJSONResponse,
    )

    register_routers(app=app)
    register_di_containers()

    return app


app = create_app()


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool((CONFIG.REDIS.host, CONFIG.REDIS.port), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(hosts=[f'{CONFIG.ELASTIC.protocol}://{CONFIG.ELASTIC.host}:{CONFIG.ELASTIC.port}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()
