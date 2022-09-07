import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from jaeger_telemetry.configurations.thrift import configure_tracer
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

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
    middleware = [
        Middleware(
            RawContextMiddleware,
            plugins=(
                plugins.RequestIdPlugin(),
                plugins.CorrelationIdPlugin()
            )
        )
    ]

    app = FastAPI(
        title=CONFIG.APP.project_name,
        docs_url=f'{CONFIG.APP.api_path}{CONFIG.APP.swagger_path}',
        openapi_url=f'{CONFIG.APP.api_path}{CONFIG.APP.json_swagger_path}',
        default_response_class=ORJSONResponse,
        middleware=middleware,
    )

    register_routers(app=app)
    register_di_containers()

    if CONFIG.JAEGER.enabled:
        configure_tracer(service_name='content', host=CONFIG.JAEGER.agent.host, port=CONFIG.JAEGER.agent.port)
        FastAPIInstrumentor.instrument_app(app)

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
