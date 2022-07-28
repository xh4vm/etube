import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .api.v1.films import router as film_router
from .api.v1.genres import router as genre_router
from .api.v1.persons import router as person_router
from .core.config import CONFIG
from .db import elastic, redis

from .containers.film import ServiceRedisElasticContainer as FilmServiceContainer
from .containers.genre import ServiceRedisElasticContainer as GenreServiceContainer
from .containers.person import ServiceRedisElasticContainer as PersonServiceContainer


API_PATH = f'{CONFIG.APP.api_path}/{CONFIG.APP.version}'
app = FastAPI(
    title=CONFIG.APP.project_name,
    docs_url=f'{CONFIG.APP.api_path}{CONFIG.APP.swagger_path}',
    openapi_url=f'{CONFIG.APP.api_path}{CONFIG.APP.json_swagger_path}',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool((CONFIG.REDIS.host, CONFIG.REDIS.port), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(hosts=[f'{CONFIG.ELASTIC.protocol}://{CONFIG.ELASTIC.host}:{CONFIG.ELASTIC.port}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


film_service_container = FilmServiceContainer()
genre_service_container = GenreServiceContainer()
person_service_container = PersonServiceContainer()

app.include_router(router=film_router, prefix=API_PATH)
app.include_router(router=genre_router, prefix=API_PATH)
app.include_router(router=person_router, prefix=API_PATH)
