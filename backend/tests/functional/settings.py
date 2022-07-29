from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        # Для локального запуска
        env_file = '../../.env_local'


class ApiSettings(Settings):
    url: str = Field(..., env='API_URL')
    port: str = Field(..., env='CLIENT_APP_PORT')
    api_path: str = Field(..., env='API_PATH')
    api_version: str = Field(..., env='API_VERSION')


class RedisSettings(Settings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')


class ElasticsearchSettings(Settings):
    protocol: str = Field(..., env='ES_PROTOCOL')
    user: str = Field(..., env='ES_USER')
    password: str = Field(..., env='ES_PASSWORD')
    host: str = Field(..., env='ES_HOST')
    port: int = Field(..., env='ES_PORT')


class Config(Settings):
    API: ApiSettings = ApiSettings()
    REDIS: RedisSettings = RedisSettings()
    ELASTIC: ElasticsearchSettings = ElasticsearchSettings()


CONFIG = Config()
