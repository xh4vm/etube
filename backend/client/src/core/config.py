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
    host: str
    port: int
    cache_expire: int

    class Config:
        env_prefix = 'REDIS_'


class ElasticsearchSettings(Settings):
    protocol: str
    user: str
    password: str
    host: str
    port: int

    class Config:
        env_prefix = 'ES_'


class JaegerAgentSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = 'JAEGER_AGENT_'


class JaegerSettings(BaseSettings):
    agent: JaegerAgentSettings = JaegerAgentSettings()
    enabled: bool = Field(..., env='ENABLED_TRACER')


class Config(Settings):
    APP: AppSettings = AppSettings()
    REDIS: RedisSettings = RedisSettings()
    ELASTIC: ElasticsearchSettings = ElasticsearchSettings()
    JAEGER: JaegerSettings = JaegerSettings()


CONFIG = Config()

logging_config.dictConfig(LOGGING)
service_logger = logging.getLogger('SERVICE')
