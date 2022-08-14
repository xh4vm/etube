import logging
import grpc
from concurrent import futures
 
from services.permission import PermissionServer
from messages.permission_pb2_grpc import add_PermissionServicer_to_server
from core.config import CONFIG, grpc_logger

 
def serve(logger: logging.Logger):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=(
            ('grpc.keepalive_time_ms', 10000),
            ('grpc.keepalive_timeout_ms', 5000),
            ('grpc.keepalive_permit_without_calls', True),
            ('grpc.http2.max_pings_without_data', 0),
            ('grpc.http2.min_time_between_pings_ms', 10000),
            ('grpc.http2.min_ping_interval_without_data_ms',  5000),
        )
    )
    add_PermissionServicer_to_server(PermissionServer(), server)

    server.add_insecure_port(f'[::]:{CONFIG.AUTH_GRPC_PORT}')

    logger.info(f'GRPC running on {CONFIG.AUTH_GRPC_PORT} port.')

    server.start()
    server.wait_for_termination()

 
if __name__ == '__main__':
    serve(logger=grpc_logger)
