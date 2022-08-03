import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = '../../.env'


class ApiSettings(Settings):
    url: str = Field('http://localhost', env='API_URL')
    port: str = Field('8000', env='CLIENT_APP_PORT')
    api_path: str = Field('/api', env='API_PATH')
    api_version: str = Field('v1', env='API_VERSION')


class RedisSettings(Settings):
    host: str = Field('localhost', env='REDIS_HOST')
    port: int = Field('6379', env='REDIS_PORT')


class ElasticsearchSettings(Settings):
    protocol: str = Field('http', env='ES_PROTOCOL')
    user: str = Field('', env='ES_USER')
    password: str = Field('', env='ES_PASSWORD')
    host: str = Field('localhost', env='ES_HOST')
    port: int = Field('9200', env='ES_PORT')


class Config(Settings):
    API: ApiSettings = ApiSettings()
    REDIS: RedisSettings = RedisSettings()
    ELASTIC: ElasticsearchSettings = ElasticsearchSettings()
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


CONFIG = Config()
