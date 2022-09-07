import logging

from pydantic import BaseSettings


class GRPCSettings(BaseSettings):
    GRPC_HOST: str
    GRPC_PORT: int
    JWT_SECRET_KEY: str
    JWT_DECODE_ALGORITHMS: list[str]
    JWT_ALGORITHM: str

    class Config:
        env_prefix = 'AUTH_'


CONFIG = GRPCSettings()

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
)
grpc_logger = logging.getLogger(name='GRPC Server')
