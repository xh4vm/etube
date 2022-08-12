import logging
from pydantic import BaseSettings, Field


class GRPCSettings(BaseSettings):
    AUTH_GRPC_PORT: int = Field(..., env='AUTH_GRPC_PORT')


CONFIG = GRPCSettings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
grpc_logger = logging.getLogger(name='GRPC Server')