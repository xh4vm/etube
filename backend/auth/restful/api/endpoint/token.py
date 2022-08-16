from flask import Blueprint
from flask_pydantic_spec import Response, Request
from dependency_injector.wiring import inject, Provide

from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService

from ..containers.token import ServiceContainer

from ..app import spec
from ..schema.token.refresh import RefreshTokenBodyParams, RefreshTokenHeader, RefreshTokenResponse
from ..utils.decorators import json_response, unpack_models


bp = Blueprint('token', __name__, url_prefix='/token')
TAG = 'Token'


@bp.route('/refresh', methods=['POST'])
@spec.validate(
    body=Request(RefreshTokenBodyParams), 
    headers=RefreshTokenHeader, 
    resp=Response(HTTP_200=RefreshTokenResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
@inject
def refresh(
    body: RefreshTokenBodyParams, 
    access_token_service: AccessTokenService = Provide[ServiceContainer.access_token_service],
    refresh_token_service: RefreshTokenService = Provide[ServiceContainer.refresh_token_service],
    **kwargs
):
    """ Обновление пары токенов
    ---
        Eсли рефреш токен не протух то выписываем новую пару токенов.
    """

    # access_token = access_token_service.create(claims=user)
    # refresh_token = refresh_token_service.create(claims=user)

    return RefreshTokenResponse(access_token=access_token, refresh_token=refresh_token)
