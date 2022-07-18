from logging import config as logging_config

from pydantic import BaseSettings, Field

from .logger import LOGGING


class Settings(BaseSettings):
    class Config:
        env_file = '../../../.env'


class AppSettings(Settings):
    project_name: str = Field(..., env='PROJECT_NAME')


class RedisSettings(Settings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')


class ElasticsearchSettings(Settings):
    protocol: str = Field(..., env='ES_PROTOCOL')
    user: str = Field(..., env='ES_USER')
    password: str = Field(..., env='ES_PASSWORD')
    host: str = Field(..., env='ES_HOST')
    port: int = Field(..., env='ES_PORT')


REDIS_CONFIG = RedisSettings()
ELASTIC_CONFIG = ElasticsearchSettings()
APP_CONFIG = AppSettings()

logging_config.dictConfig(LOGGING)
