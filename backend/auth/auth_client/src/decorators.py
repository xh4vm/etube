from functools import wraps
from grpc import aio
import grpc
from typing import Optional
from http import HTTPStatus

import auth_client.src.services.access.grpc as grpc_client_connector

from auth_client.core.config import CONFIG, BACKOFF_CONFIG, auth_logger
from auth_client.src.services.access.local import authorized
from auth_client.src.exceptions.access import AccessException
from auth_client.src.errors.permission import PermissionError


def access_required(permissions: dict[str, str]):
    def decorator(f):
        @wraps(f)
        def decorated_function(token: Optional[str], *args, **kwargs):
            for url, method in permissions.items():
                is_accessible, message = authorized(token=token, method=method, url=url)
            
                if not is_accessible:        
                    raise AccessException(status=HTTPStatus.FORBIDDEN, message=message)
            
            return f(*args, **kwargs)

        return decorated_function
    return decorator


def async_grpc_access_required(permissions: dict[str, str]):
    def decorator(f):
        @wraps(f)
        async def decorated_function(token: Optional[str], *args, **kwargs):
            async with aio.insecure_channel(target=f'{CONFIG.GRPC.HOST}:{CONFIG.GRPC.PORT}') as channel:
                
                client = grpc_client_connector.AsyncAccessService(channel)

                for url, method in permissions.items():    
                    
                    response = await client.is_accessible(token=token, method=method, url=url)

                    if not response.get('is_accessible'):
                        raise AccessException(status=HTTPStatus.FORBIDDEN, message=PermissionError.ACCESS_ERROR)
                        
            return await f(*args, **kwargs)
            
        return decorated_function
    return decorator


def grpc_access_required(permissions: dict[str, str]):
    def decorator(f):
        @wraps(f)
        def decorated_function(token: Optional[str], *args, **kwargs):
            with grpc.insecure_channel(target=f'{CONFIG.GRPC.HOST}:{CONFIG.GRPC.PORT}') as channel:
                
                client = grpc_client_connector.AccessService(channel)

                for url, method in permissions.items():    
                    response = client.is_accessible(token=token, method=method, url=url)

                    if not response.get('is_accessible'):
                        raise AccessException(status=HTTPStatus.FORBIDDEN, message=PermissionError.ACCESS_ERROR)

            return f(*args, **kwargs)
            
        return decorated_function
    return decorator
