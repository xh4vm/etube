from flask import Blueprint
from flask_pydantic_spec import Response, Request

from ..app import spec
from ..schema.action.sign_in import SignInBodyParams, SignInHeader, SignInResponse
from ..schema.action.sign_up import SignUpBodyParams, SignUpHeader, SignUpResponse
from ..schema.action.logout import LogoutBodyParams, LogoutHeader, LogoutResponse
from ..utils.decorators import json_response, unpack_models


bp = Blueprint('action', __name__, url_prefix='/action')
TAG = 'Action'


@bp.route('/sign_in', methods=['POST'])
@spec.validate(
    body=Request(SignInBodyParams), 
    headers=SignInHeader, 
    resp=Response(HTTP_200=SignInResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def sign_in(body: SignInBodyParams, headers: SignInHeader) -> SignInResponse:
    """ Авторизация пользователя
    ---
        На вход поступает логин и пароль, если пользователь существует и авторизация успешна, то создается и возвразается пара jwt токенов.
    """
    return SignInResponse(access_token='', refresh_token='')


@bp.route('/sign_up', methods=['POST'])
@spec.validate(
    body=Request(SignUpBodyParams), 
    headers=SignUpHeader, 
    resp=Response(HTTP_200=SignUpResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def sign_up(body: SignUpBodyParams, headers: SignUpHeader) -> SignUpResponse:
    """ Регистрация пользователя
    ---
        На вход поступает логин и пароль, если регистрация успешна то создается и возвразается пара jwt токенов.
    """
    return SignUpResponse(access_token='', refresh_token='')


@bp.route('/logout', methods=['DELETE'])
@spec.validate(
    body=Request(LogoutBodyParams), 
    headers=LogoutHeader, 
    resp=Response(HTTP_200=LogoutResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def logout(body: LogoutBodyParams, **kwargs):
    """ Выход пользователя из текущей сессии
    ---
        Выход пользователя из текущей сессии. Текущая пара (access_token,refresh_token) становится недействительной.
    """
    return LogoutResponse()
