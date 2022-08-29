import backoff
from grpc import aio
from auth_client.src.messages.permission_pb2 import AccessibleRequest, AccessibleResponse
from auth_client.src.messages.permission_pb2_grpc import PermissionStub
from auth_client.core.config import CONFIG, BACKOFF_CONFIG, auth_logger


class AccessService:
    def __init__(self, channel: aio.Channel) -> None:
        self.client = PermissionStub(channel)

    @backoff.on_exception(**BACKOFF_CONFIG, logger=auth_logger)
    def is_accessible(self, token: str, method: str, url: str) -> AccessibleResponse:
        request = AccessibleRequest(token=token, method=method, url=url)
        response = self.client.is_accessible(request)

        return {'is_accessible': response.is_accessible, 'message': response.message}


class AsyncAccessService:
    def __init__(self, channel: aio.Channel) -> None:
        self.client = PermissionStub(channel)

    @backoff.on_exception(**BACKOFF_CONFIG, logger=auth_logger)
    async def is_accessible(self, token: str, method: str, url: str) -> AccessibleResponse:
        request = AccessibleRequest(token=token, method=method, url=url)
        response = await self.client.is_accessible(request)

        return {'is_accessible': response.is_accessible, 'message': response.message}
