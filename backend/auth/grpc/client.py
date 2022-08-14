import grpc 

from messages.permission_pb2 import AccessibleRequest, AccessibleResponse
from messages.permission_pb2_grpc import PermissionStub


class PermissionClient:
    def __init__(self, target):
        channel = grpc.insecure_channel(target)
        self.client = PermissionStub(channel)
 
    def is_accessible(self, token: str, method: str, url: str) -> AccessibleResponse:
        request = AccessibleRequest(token=token, method=method, url=url)
        response = self.client.is_accessible(request)

        return {'is_accessible': response.is_accessible, 'message': response.message}
