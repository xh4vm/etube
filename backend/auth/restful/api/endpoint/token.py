import uuid
from flask import Blueprint
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_pydantic_spec import Response, Request
from dependency_injector.wiring import inject, Provide

from ..services.token.access import AccessTokenService
from ..services.token.refresh import RefreshTokenService
from ..services.user import UserService

from ..containers.token import ServiceContainer

from ..app import spec
from ..schema.base import User
from ..schema.token.refresh import RefreshTokenHeader, RefreshTokenResponse
from ..utils.decorators import json_response, unpack_models


bp = Blueprint('token', __name__, url_prefix='/token')
TAG = 'Token'


@bp.route('/refresh', methods=['POST'])
@spec.validate(
    headers=RefreshTokenHeader, 
    resp=Response(HTTP_200=RefreshTokenResponse, HTTP_422=None), 
    tags=[TAG]
)
@unpack_models
@jwt_required(refresh=True)
@json_response
@inject
def refresh(
    access_token_service: AccessTokenService = Provide[ServiceContainer.access_token_service],
    refresh_token_service: RefreshTokenService = Provide[ServiceContainer.refresh_token_service],
    user_service: UserService = Provide[ServiceContainer.user_service],
    **kwargs
):
    """ Обновление пары токенов
    ---
        Eсли рефреш токен не протух то выписываем новую пару токенов.
    """

    user_id: uuid.UUID = refresh_token_service.get_identity()
    
    user: User = user_service.get_by_id(user_id)

    access_token: str = access_token_service.create(identity=user.id, claims=user.get_claims())
    refresh_token: str = refresh_token_service.create(identity=user.id)

    return RefreshTokenResponse(access_token=access_token, refresh_token=refresh_token)
