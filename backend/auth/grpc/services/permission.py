 
from messages.permission_pb2 import AccessibleResponse
from messages.permission_pb2_grpc import PermissionServicer
from core.config import grpc_logger
 
 
class PermissionServer(PermissionServicer):
    def is_accessible(self, request, context):
        grpc_logger.info(request.token)
        grpc_logger.info(request.method)
        grpc_logger.info(request.url)

        return AccessibleResponse(is_accessible=True, message="ASDASD")
 