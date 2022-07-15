import logging

import backoff
from pydantic import BaseSettings, Field

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    class Config:
        env_file = '../../.env'


class PostgreSQLSettings(Settings):
    dbname: str = Field(..., env='DB_NAME')
    user: str = Field(..., env='DB_USER')
    password: str = Field(..., env='DB_PASSWORD')
    host: str = Field(..., env='DB_HOST')
    port: int = Field(..., env='DB_PORT')

class RedisSettings(Settings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')


class ElasticsearchSettings(Settings):
    protocol: str = Field(..., env='ES_PROTOCOL')
    user: str = Field(..., env='ES_USER')
    password: str = Field(..., env='ES_PASSWORD')
    host: str = Field(..., env='ES_HOST')
    port: int = Field(..., env='ES_PORT')


# class ESIndex(Settings):
#     movies: str = Field(..., env='INDEX_MOVIES')


POSTGRES_DSN = PostgreSQLSettings()
REDIS_CONFIG = RedisSettings()
ELASTIC_CONFIG = ElasticsearchSettings()
# ES_INDEX = ESIndex()

BACKOFF_CONFIG = {'wait_gen': backoff.expo, 'exception': Exception, 'max_value': 128}


class CelerySettings(Settings):
    name = 'ETL'
    broker = f'redis://{REDIS_CONFIG.host}:{REDIS_CONFIG.port}/0'
    backend = f'redis://{REDIS_CONFIG.host}:{REDIS_CONFIG.port}/0'


CELERY_CONFIG = CelerySettings()
