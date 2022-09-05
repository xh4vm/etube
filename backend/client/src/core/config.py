import logging
from logging import config as logging_config

from pydantic import BaseSettings, Field

from .logger import LOGGING


class Settings(BaseSettings):
    class Config:
        # Для локального запуска
        env_file = '../../../.env'


class AppSettings(Settings):
    host: str = Field('localhost', env='CLIENT_APP_HOST')
    port: int = Field(..., env='CLIENT_APP_PORT')
    project_name: str = Field(..., env='PROJECT_NAME')
    api_path: str = Field(..., env='API_PATH')
    page: int = Field(..., env='PAGE_DEFAULT')
    page_size: int = Field(..., env='PAGE_SIZE_DEFAULT')
    version: str = Field(..., env='API_VERSION')
    swagger_path: str = Field(..., env='SWAGGER_PATH')
    json_swagger_path: str = Field(..., env='JSON_SWAGGER_PATH')


class RedisSettings(Settings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')
    expire: int = Field(..., env='CACHE_EXPIRE')


class ElasticsearchSettings(Settings):
    protocol: str = Field(..., env='ES_PROTOCOL')
    user: str = Field(..., env='ES_USER')
    password: str = Field(..., env='ES_PASSWORD')
    host: str = Field(..., env='ES_HOST')
    port: int = Field(..., env='ES_PORT')


class JaegerAgentSettings(BaseSettings):
    host: str = Field(..., env='JAEGER_AGENT_HOST')
    port: int = Field(..., env='JAEGER_AGENT_PORT')


class JaegerSettings(BaseSettings):
    agent: JaegerAgentSettings = JaegerAgentSettings()


class Config(Settings):
    APP: AppSettings = AppSettings()
    REDIS: RedisSettings = RedisSettings()
    ELASTIC: ElasticsearchSettings = ElasticsearchSettings()
    JAEGER: JaegerSettings = JaegerSettings()


CONFIG = Config()

logging_config.dictConfig(LOGGING)
service_logger = logging.getLogger('SERVICE')
