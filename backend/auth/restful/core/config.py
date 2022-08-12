from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    AUTH_APP_PORT: int = Field(..., env='AUTH_APP_PORT')
    API_URL: str = Field(..., env='AUTH_API_URL')
    API_PATH: str = Field(..., env='AUTH_API_PATH')
    API_VERSION: str = Field(..., env='AUTH_API_VERSION')
    SWAGGER_PATH: str = Field(..., env='AUTH_SWAGGER_PATH')
    SECRET_KEY: str = Field(..., env='AUTH_SECRET_KEY')
    JWT_SECRET_KEY: str = Field(..., env='AUTH_JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(..., env='AUTH_JWT_ACCESS_TOKEN_EXPIRES')
    JWT_REFRESH_TOKEN_EXPIRES: int = Field(..., env='AUTH_JWT_REFRESH_TOKEN_EXPIRES')
    JWT_BLACKLIST_ENABLED: bool = Field(..., env='AUTH_JWT_BLACKLIST_ENABLED')
    JWT_BLACKLIST_TOKEN_CHECKS: list[str] = Field(..., env='AUTH_JWT_BLACKLIST_TOKEN_CHECKS')
    JWT_HEADER_NAME: str = Field(..., env='AUTH_JWT_HEADER_NAME')
    ACCESS_EXPIRES: int = Field(..., env='AUTH_ACCESS_EXPIRES')
    DEBUG: bool = Field(..., env='AUTH_DEBUG')


class RedisSettings(BaseSettings):
    HOST: str = Field(..., env='REDIS_HOST')
    PORT: int = Field(..., env='REDIS_PORT')
    EXPIRE: int = Field(..., env='CACHE_EXPIRE')


class Config(BaseSettings):
    APP: AppSettings = AppSettings()
    REDIS: RedisSettings = RedisSettings()


CONFIG = Config()
