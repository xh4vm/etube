from grpc import aio
from messages.permission_pb2 import AccessibleRequest, AccessibleResponse
from messages.permission_pb2_grpc import PermissionStub


class PermissionClient:
    def __init__(self, channel: aio.Channel) -> None:
        self.client = PermissionStub(channel)

    async def is_accessible(self, token: str, method: str, url: str) -> AccessibleResponse:
        request = AccessibleRequest(token=token, method=method, url=url)
        response = await self.client.is_accessible(request)

        return {'is_accessible': response.is_accessible, 'message': response.message}
