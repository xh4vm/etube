import backoff
from pydantic import BaseSettings, Field
from typing import Any
import logging


class AppSettings(BaseSettings):
    AUTH_APP_HOST: str = Field('localhost', env='AUTH_APP_HOST')
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
    RATELIMIT_STRATEGY: str = Field('fixed-window', env='AUTH_RATELIMIT_STRATEGY')
    DEBUG: bool = Field(..., env='AUTH_DEBUG')


class RedisSettings(BaseSettings):
    HOST: str = Field(..., env='REDIS_HOST')
    PORT: int = Field(..., env='REDIS_PORT')
    EXPIRE: int = Field(..., env='CACHE_EXPIRE')


class JaegerAgentSettings(BaseSettings):
    HOST: str = Field(..., env='JAEGER_AGENT_HOST')
    PORT: int = Field(..., env='JAEGER_AGENT_PORT')


class JaegerSettings(BaseSettings):
    AGENT: JaegerAgentSettings = JaegerAgentSettings()


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
    CLIENT_ID: str = Field(..., env='YANDEX_CLIENT_ID')
    CLIENT_SECRET: str = Field(..., env='YANDEX_CLIENT_SECRET')
    BASEURL: str = Field(..., env='YANDEX_BASEURL')


class VKAppConfig(BaseSettings):
    CLIENT_ID: str = Field(..., env='VK_CLIENT_ID')
    CLIENT_SECRET: str = Field(..., env='VK_CLIENT_SECRET')
    BASEURL: str = Field(..., env='VK_BASEURL')
    REDIRECT: str = Field(..., env='VK_REDIRECT')
    DISPLAY: str = Field(..., env='VK_DISPLAY')
    SCOPE: str = Field(..., env='VK_SCOPE')
    RESPONSE: str = Field(..., env='VK_RESPONSE')


class OAuthConfig(BaseSettings):
    YANDEX: YandexAppConfig = YandexAppConfig()
    VK: VKAppConfig = VKAppConfig()
    SECRET: str = Field(..., env='OAUTH_SECRET')


OAUTH_CONFIG = OAuthConfig()


class CaptchaSettings(BaseSettings):
    SECRET: str = Field(..., env='CAPTCHA_SECRET')


CAPTCHA_CONFIG = CaptchaSettings()
