from flask import Blueprint
from flask_pydantic_spec import Response, Request

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
def refresh(body: RefreshTokenBodyParams, **kwargs):
    """ Обновление пары токенов
    ---
        Eсли рефреш токен не протух то выписываем новую пару токенов.
    """
    return RefreshTokenResponse(access_token='', refresh_token='')
