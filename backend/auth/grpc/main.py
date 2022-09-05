import asyncio
import logging

from core.config import CONFIG, grpc_logger
from grpc import aio
from grpc._compression import Gzip
from messages.permission_pb2_grpc import add_PermissionServicer_to_server
from services.permission import PermissionServer


async def serve(logger: logging.Logger):
    server = aio.server(
        options=(
            ('grpc.keepalive_time_ms', 10000),
            ('grpc.keepalive_timeout_ms', 5000),
            ('grpc.keepalive_permit_without_calls', True),
            ('grpc.http2.max_pings_without_data', 0),
            ('grpc.http2.min_time_between_pings_ms', 10000),
        ),
        compression=Gzip,
    )
    add_PermissionServicer_to_server(PermissionServer(), server)

    server.add_insecure_port(f'{CONFIG.AUTH_GRPC_HOST}:{CONFIG.AUTH_GRPC_PORT}')

    logger.info(f'GRPC server running on {CONFIG.AUTH_GRPC_HOST}:{CONFIG.AUTH_GRPC_PORT}.')

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve(logger=grpc_logger))
