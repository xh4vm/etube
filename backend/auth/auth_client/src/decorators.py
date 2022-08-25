from flask import request
from functools import wraps
from grpc import aio
from typing import Optional
from http import HTTPStatus

from auth_client.core.config import CONFIG
from auth_client.src.local.access import authorized
from auth_client.src.utils import json_abort, get_token_from_headers
from auth_client.errors.permission import PermissionError


def access_required(permissions: dict[str, str]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_headers(CONFIG.APP.JWT_HEADER_NAME)

            for url, method in permissions.items():
                is_accessible, message = authorized(token=token, method=method, url=url)
            
                if not is_accessible:        
                    json_abort(status=HTTPStatus.FORBIDDEN, message=message)
            
            return f(*args, **kwargs)

        return decorated_function
    return decorator


def grpc_access_required(permissions: dict[str, str]):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            token = get_token_from_headers(CONFIG.APP.JWT_HEADER_NAME)

            async with aio.insecure_channel(target=f'{CONFIG.GRPC.HOST}:{CONFIG.GRPC.PORT}') as channel:
                client = grpc_client_connector.PermissionClient(channel)

                for url, method in permissions.items():    
                    print('AAAAA', url, method)
                    
                    response = await client.is_accessible(token=token, method=method, url=url)
                    print('BBBBB', response)

                    if not response.get('is_accessible'):
                        json_abort(status=HTTPStatus.FORBIDDEN, message=PermissionError.ACCESS_ERROR)
                
            return await f(*args, **kwargs)
            
        return decorated_function
    return decorator
