import hashlib

import pytest

from ..utils.auth.jwt import create_token
from ..utils.errors.permission_granter import PermissionGranterError

pytestmark = pytest.mark.asyncio


async def test_check_permission_success(make_request, grpc_client):
    url = 'sub.domain.com/manager/user'
    access_token = create_token(
        claims={
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf',
            'permissions': {hashlib.md5(url.encode(), usedforsecurity=False).hexdigest(): ['POST']},
        }
    )

    result = grpc_client.is_accessible(token=access_token, method='POST', url=url)
    assert result.get('is_accessible') is True
    assert result.get('message') == PermissionGranterError.ACCESS_SUCCESS


async def test_check_permission_denied_method(make_request, grpc_client):
    url = 'sub.domain.com/manager/user'
    access_token = create_token(
        claims={
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf',
            'permissions': {hashlib.md5(url.encode(), usedforsecurity=False).hexdigest(): ['GET']},
        }
    )

    result = grpc_client.is_accessible(token=access_token, method='POST', url=url)
    assert result.get('is_accessible') is False
    assert result.get('message') == PermissionGranterError.ACCESS_ERROR


async def test_check_permission_denied_url(make_request, grpc_client):
    url = 'sub.domain.com/manager/user'
    access_token = create_token(
        claims={
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf',
            'permissions': {hashlib.md5(f'{url}_other'.encode(), usedforsecurity=False).hexdigest(): ['POST']},
        }
    )

    result = grpc_client.is_accessible(token=access_token, method='POST', url=url)
    assert result.get('is_accessible') is False
    assert result.get('message') == PermissionGranterError.ACCESS_ERROR
