import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .core.config import APP_CONFIG, ELASTIC_CONFIG, REDIS_CONFIG
from .db import elastic, redis

API_PATH = f'{APP_CONFIG.api_path}/{APP_CONFIG.version}'
app = FastAPI(
    title=APP_CONFIG.project_name,
    docs_url=f'{APP_CONFIG.api_path}{APP_CONFIG.swagger_path}',
    openapi_url=f'{APP_CONFIG.api_path}{APP_CONFIG.json_swagger_path}',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool((REDIS_CONFIG.host, REDIS_CONFIG.port), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(hosts=[f'{ELASTIC_CONFIG.protocol}://{ELASTIC_CONFIG.host}:{ELASTIC_CONFIG.port}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


from .api.v1.films import router as film_router  # noqa E402

app.include_router(router=film_router, prefix=API_PATH)

from .api.v1.genres import router as genre_router  # noqa E402

app.include_router(router=genre_router, prefix=API_PATH)

from .api.v1.persons import router as person_router  # noqa E402

app.include_router(router=person_router, prefix=API_PATH)
