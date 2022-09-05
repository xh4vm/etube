from functools import wraps
from http import HTTPStatus
from typing import Optional

import auth_client.src.services.access.grpc as grpc_client_connector
import backoff
import grpc
from auth_client.core.config import BACKOFF_CONFIG, CONFIG, auth_logger
from auth_client.src.exceptions.access import AccessException
from auth_client.src.services.access.local import AccessService
from grpc import aio


def access_required(permissions: dict[str, str]):
    def decorator(f):
        @wraps(f)
        def decorated_function(token: Optional[str], *args, **kwargs):
            access_service = AccessService()

            for url, method in permissions.items():
                response = access_service.is_accessible(token=token, method=method, url=url)

                if not response.get('is_accessible'):
                    raise AccessException(status=HTTPStatus.FORBIDDEN, message=response.get('message'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def async_grpc_access_required(permissions: dict[str, str]):
    def decorator(f):
        @backoff.on_exception(**BACKOFF_CONFIG, exception=grpc.RpcError, logger=auth_logger)
        @wraps(f)
        async def decorated_function(token: Optional[str], *args, **kwargs):
            async with aio.insecure_channel(target=f'{CONFIG.GRPC.HOST}:{CONFIG.GRPC.PORT}') as channel:

                access_service = grpc_client_connector.AsyncAccessService(channel)

                for url, method in permissions.items():

                    response = await access_service.is_accessible(token=token, method=method, url=url)

                    if not response.get('is_accessible'):
                        raise AccessException(status=HTTPStatus.FORBIDDEN, message=response.get('message'))

            return await f(*args, **kwargs)

        return decorated_function

    return decorator


def grpc_access_required(permissions: dict[str, str]):
    def decorator(f):
        @backoff.on_exception(**BACKOFF_CONFIG, exception=grpc.RpcError, logger=auth_logger)
        @wraps(f)
        def decorated_function(token: Optional[str], *args, **kwargs):
            with grpc.insecure_channel(target=f'{CONFIG.GRPC.HOST}:{CONFIG.GRPC.PORT}') as channel:

                access_service = grpc_client_connector.AccessService(channel)

                for url, method in permissions.items():
                    response = access_service.is_accessible(token=token, method=method, url=url)

                    if not response.get('is_accessible'):
                        raise AccessException(status=HTTPStatus.FORBIDDEN, message=response.get('message'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
