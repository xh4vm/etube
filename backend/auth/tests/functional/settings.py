import os

from pydantic import BaseSettings, Field


class ApiSettings(BaseSettings):
    APP_HOST: str = Field('localhost')
    API_URL: str = Field('http://localhost')
    APP_PORT: str = Field('9090')
    API_PATH: str = Field('/api')
    API_VERSION: str = Field('v1')
    JWT_DECODE_ALGORITHMS: list[str] = Field(['HS256'])
    JWT_SECRET_KEY: str = Field('fn_jj!qd2*mcd4kev#s+8o53sfnc!@(jda9&guxual=7#9#n^$')
    JWT_ALGORITHM: str = Field('HS256')
    JWT_HEADER_NAME: str = Field('X-Authorization-Token')
    JWT_TOKEN_LOCATION: str = Field('headers')

    class Config:
        env_prefix = 'AUTH_'


class GRPCSettings(BaseSettings):
    HOST: str = Field('localhost')
    PORT: str = Field('56567')

    class Config:
        env_prefix = 'AUTH_GRPC_'


class RedisSettings(BaseSettings):
    HOST: str = Field('localhost')
    PORT: int = Field(6379)
    CACHE_EXPIRE: int = Field(600)

    class Config:
        env_prefix = 'REDIS_'


class DatabaseSettings(BaseSettings):
    USER: str = Field('auth')
    PASSWORD: str = Field('123qwe')
    HOST: str = Field('localhost')
    PORT: int = Field('5433')
    NAME: str = Field('auth_database')
    SCHEMA_NAME: str = Field('auth_etube')
    SCHEMA_FILE_NAME: str = Field('schema.sql')

    class Config:
        env_prefix = 'AUTH_DB_'

    def dsn(self):
        return {
            'dbname': self.NAME,
            'user': self.USER,
            'password': self.PASSWORD,
            'host': self.HOST,
            'port': self.PORT,
        }


class OAuthConfig(BaseSettings):
    SECRET: str = Field('P2yV0aGyYs6MDEODdbbd6bf17')

    class Config:
        env_prefix = 'OAUTH_'


class Config(BaseSettings):
    API: ApiSettings = ApiSettings()
    GRPC: GRPCSettings = GRPCSettings()
    REDIS: RedisSettings = RedisSettings()
    DB: DatabaseSettings = DatabaseSettings()
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


class CaptchaSettings(BaseSettings):
    SECRET: str = Field('2nc@hyyd4y(m+5c52ahsg_j&aet6_rm=9g1d^h1ge1$uy^@r7a')

    class Config:
        env_prefix = 'CAPTCHA_'


CONFIG = Config()
OAUTH_CONFIG = OAuthConfig()
CAPTCHA_CONFIG = CaptchaSettings()
