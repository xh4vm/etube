import pytest
from datetime import datetime
from http import HTTPStatus

from functional.settings import CONFIG

from ..utils.auth.jwt import get_jwt_claims, get_jwt_identity, verify_exp_jwt, create_token
from ..utils.errors.action.sign_in import SignInActionError

pytestmark = pytest.mark.asyncio


async def test_logout_success(make_request, generate_users):
    # Попытка выхода.
    access_token = create_token(
        claims={
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 
            'login': 'cheburashka',
        }
    )
    response = await make_request(
        method='delete',
        target=f'auth/action/logout', 
        headers={'X-Authorization-Token': f'Bearer {access_token}'}
    )

    assert response.status == HTTPStatus.OK
