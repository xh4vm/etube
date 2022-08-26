import logging

from pydantic import BaseSettings, Field


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str = Field(..., env='AUTH_JWT_SECRET_KEY')
    JWT_DECODE_ALGORITHMS: list[str] = Field(..., env='AUTH_JWT_DECODE_ALGORITHMS')
    JWT_ALGORITHM: str = Field(..., env='AUTH_JWT_ALGORITHM')
    JWT_HEADER_NAME: str = Field(..., env='AUTH_JWT_HEADER_NAME')
    JWT_TOKEN_LOCATION: str = Field('headers', env='AUTH_JWT_TOKEN_LOCATION')


class GRPCSettings(BaseSettings):
    HOST: str = Field(..., env='AUTH_GRPC_HOST')
    PORT: int = Field(..., env='AUTH_GRPC_PORT') 


class Config(BaseSettings):
    APP: AuthSettings = AuthSettings()
    GRPC: GRPCSettings = GRPCSettings()

CONFIG = Config()

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
)
auth_logger = logging.getLogger(name='Auth Client')
