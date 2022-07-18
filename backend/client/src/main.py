import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import APP_CONFIG, ELASTIC_CONFIG, REDIS_CONFIG
from db import elastic, redis

app = FastAPI(
    title=APP_CONFIG.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool((REDIS_CONFIG.host, REDIS_CONFIG.port), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(hosts=[f'{ELASTIC_CONFIG.host}:{ELASTIC_CONFIG.port}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()

from api.v1.films import router as film_router

app.include_router(router=film_router)

from api.v1.genres import router as genre_router

app.include_router(router=genre_router)

from api.v1.persons import router as person_router

app.include_router(router=person_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
