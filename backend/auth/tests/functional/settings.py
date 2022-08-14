import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = '../../.env'


class ApiSettings(Settings):
    url: str = Field('http://localhost', env='AUTH_API_URL')
    port: str = Field('9090', env='AUTH_APP_PORT')
    api_path: str = Field('/api', env='AUTH_API_PATH')
    api_version: str = Field('v1', env='AUTH_API_VERSION')


class Config(Settings):
    API: ApiSettings = ApiSettings()
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


CONFIG = Config()
