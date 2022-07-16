import backoff
from pydantic import BaseSettings, Field

from models.models import Film, Genre, Person


class Settings(BaseSettings):
    class Config:
        env_file = '../../../.env'


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


POSTGRES_DSN = PostgreSQLSettings()
REDIS_CONFIG = RedisSettings()
ELASTIC_CONFIG = ElasticsearchSettings()


BACKOFF_CONFIG = {'wait_gen': backoff.expo, 'exception': Exception, 'max_value': 128}


class CelerySettings(Settings):
    name = 'ETL'
    broker = f'redis://{REDIS_CONFIG.host}:{REDIS_CONFIG.port}/0'
    backend = f'redis://{REDIS_CONFIG.host}:{REDIS_CONFIG.port}/0'


CELERY_CONFIG = CelerySettings()


# Классы, определяющие параметры переноса данных
# из Postgres в ES, включая названия индексов.
from etl.extractor import (FilmsPostgresExtractor, GenresPostgresExtracor,
                           PersonsPostgresExtractor)

class FilmIndex:
    extractor = FilmsPostgresExtractor
    model = Film
    index = 'movies'

class GenreIndex:
    extractor = GenresPostgresExtracor
    model = Genre
    index = 'genres'

class PersonIndex:
    extractor = PersonsPostgresExtractor
    model = Person
    index = 'persons'
