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
    JWT_ALGORITHM: str = Field(..., env='AUTH_JWT_ALGORITHM')
    ACCESS_EXPIRES: int = Field(..., env='AUTH_ACCESS_EXPIRES')
    JWT_DECODE_ALGORITHMS: list[str] = Field(..., env='AUTH_JWT_DECODE_ALGORITHMS')
    JWT_TOKEN_LOCATION: str = Field('headers', env='AUTH_JWT_TOKEN_LOCATION')
    DEBUG: bool = Field(..., env='AUTH_DEBUG')


class RedisSettings(BaseSettings):
    HOST: str = Field(..., env='REDIS_HOST')
    PORT: int = Field(..., env='REDIS_PORT')
    EXPIRE: int = Field(..., env='CACHE_EXPIRE')


class DatabaseSettings(BaseSettings):
    SCHEMA_NAME: str = Field('auth_etube', env='AUTH_DB_SCHEMA')
    DRIVER: str = Field(..., env='AUTH_DB_DRIVER')
    USER: str = Field(..., env='AUTH_DB_USER')
    PASSWORD: str = Field(..., env='AUTH_DB_PASSWORD')
    HOST: str = Field(..., env='AUTH_DB_HOST')
    PORT: int = Field(..., env='AUTH_DB_PORT')
    NAME: str = Field(..., env='AUTH_DB_NAME')


class Config(BaseSettings):
    APP: AppSettings = AppSettings()
    REDIS: RedisSettings = RedisSettings()
    DB: DatabaseSettings = DatabaseSettings()


CONFIG = Config()


class InteractionConfig:
    SQLALCHEMY_DATABASE_URI = (
        f'{CONFIG.DB.DRIVER}://{CONFIG.DB.USER}:{CONFIG.DB.PASSWORD}'
        f'@{CONFIG.DB.HOST}:{CONFIG.DB.PORT}/{CONFIG.DB.NAME}'
    )
    REDIS_URL = f'redis://{CONFIG.REDIS.HOST}:{CONFIG.REDIS.PORT}/0'


INTERACTION_CONFIG = InteractionConfig()
