import logging
from typing import Any

import backoff
from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    APP_HOST: str = Field('localhost')
    APP_PORT: int
    API_URL: str
    API_PATH: str
    API_VERSION: str
    SWAGGER_PATH: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int
    JWT_REFRESH_TOKEN_EXPIRES: int
    JWT_BLACKLIST_ENABLED: bool
    JWT_BLACKLIST_TOKEN_CHECKS: list[str]
    JWT_HEADER_NAME: str
    JWT_ALGORITHM: str
    ACCESS_EXPIRES: int
    JWT_DECODE_ALGORITHMS: list[str]
    JWT_TOKEN_LOCATION: str = Field('headers')
    RATELIMIT_STRATEGY: str = Field('fixed-window')
    DEBUG: bool

    class Config:
        env_prefix = 'AUTH_'


class RedisSettings(BaseSettings):
    HOST: str
    PORT: int
    CACHE_EXPIRE: int

    class Config:
        env_prefix = 'REDIS_'


class JaegerAgentSettings(BaseSettings):
    HOST: str
    PORT: int

    class Config:
        env_prefix = 'JAEGER_AGENT_'


class JaegerSettings(BaseSettings):
    AGENT: JaegerAgentSettings = JaegerAgentSettings()
    ENABLED: bool = Field(..., env='ENABLED_TRACER')


class DatabaseSettings(BaseSettings):
    SCHEMA_NAME: str = Field('auth_etube')
    DRIVER: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    class Config:
        env_prefix = 'AUTH_DB_'


class Config(BaseSettings):
    APP: AppSettings = AppSettings()
    REDIS: RedisSettings = RedisSettings()
    DB: DatabaseSettings = DatabaseSettings()
    JAEGER: JaegerSettings = JaegerSettings()


CONFIG = Config()
BACKOFF_CONFIG: dict[str, Any] = {'wait_gen': backoff.expo, 'exception': Exception, 'max_value': 128}

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
)
auth_logger = logging.getLogger(name='Auth Restful API')


class InteractionConfig:
    SQLALCHEMY_DATABASE_URI = (
        f'{CONFIG.DB.DRIVER}://{CONFIG.DB.USER}:{CONFIG.DB.PASSWORD}'
        f'@{CONFIG.DB.HOST}:{CONFIG.DB.PORT}/{CONFIG.DB.NAME}'
    )
    REDIS_URL = f'redis://{CONFIG.REDIS.HOST}:{CONFIG.REDIS.PORT}/0'
    RATELIMIT_STORAGE_URI = f'redis://{CONFIG.REDIS.HOST}:{CONFIG.REDIS.PORT}/0'


INTERACTION_CONFIG = InteractionConfig()


class YandexAppConfig(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    BASEURL: str
    LOGINURL: str

    class Config:
        env_prefix = 'YANDEX_'


class VKAppConfig(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    BASEURL: str
    REDIRECT: str
    DISPLAY: str
    SCOPE: str
    RESPONSE: str

    class Config:
        env_prefix = 'VK_'


class OAuthConfig(BaseSettings):
    YANDEX: YandexAppConfig = YandexAppConfig()
    VK: VKAppConfig = VKAppConfig()
    SECRET: str

    class Config:
        env_prefix = 'OAUTH_'


OAUTH_CONFIG = OAuthConfig()


class CaptchaSettings(BaseSettings):
    SECRET: str

    class Config:
        env_prefix = 'CAPTCHA_'


CAPTCHA_CONFIG = CaptchaSettings()
