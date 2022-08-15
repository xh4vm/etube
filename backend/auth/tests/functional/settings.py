import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = '../../.env'


class ApiSettings(Settings):
    URL: str = Field('http://localhost', env='AUTH_API_URL')
    PORT: str = Field('9090', env='AUTH_APP_PORT')
    API_PATH: str = Field('/api', env='AUTH_API_PATH')
    API_VERSION: str = Field('v1', env='AUTH_API_VERSION')
    JWT_DECODE_ALGORITHMS: list[str] = Field(['HS256'], env='AUTH_JWT_DECODE_ALGORITHMS')
    JWT_SECRET_KEY: str = Field('fn_jj!qd2*mcd4kev#s+8o53sfnc!@(jda9&guxual=7#9#n^$', env='AUTH_JWT_SECRET_KEY')
    JWT_ALGORITHM: str = Field('HS256', env='AUTH_JWT_ALGORITHM')
    

class DatabaseSettings(BaseSettings):
    USER: str = Field('auth', env='AUTH_DB_USER')
    PASSWORD: str = Field('123qwe', env='AUTH_DB_PASSWORD')
    HOST: str = Field('localhost', env='AUTH_DB_HOST')
    PORT: int = Field('5432', env='AUTH_DB_PORT')
    NAME: str = Field('auth_database', env='AUTH_DB_NAME')
    SCHEMA_NAME: str = Field('public', env='AUTH_DB_SCHEMA')
    SCHEMA_FILE_NAME: str = Field('schema.sql', env='AUTH_DB_SCHEMA_FILE_PATH')

    def dsn(self):
        return {
            'dbname': self.NAME,
            'user': self.USER,
            'password': self.PASSWORD,
            'host': self.HOST,
            'port': self.PORT,
        }


class Config(Settings):
    API: ApiSettings = ApiSettings()
    DB: DatabaseSettings = DatabaseSettings()
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


CONFIG = Config()
