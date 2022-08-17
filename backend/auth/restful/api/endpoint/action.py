from flask import Blueprint
from flask_pydantic_spec import Response, Request
from flask_jwt_extended.view_decorators import jwt_required
from dependency_injector.wiring import inject, Provide
from http import HTTPStatus

from ..services.token.base import BaseTokenService
from ..services.sign_in_history import SignInHistoryService
from ..services.action.sign_in.base import BaseSignInService

from ..containers.sign_in import ServiceContainer

from ..app import spec
from ..schema.action.sign_in import SignInBodyParams, SignInHeader, SignInResponse
from ..schema.action.sign_up import SignUpBodyParams, SignUpHeader, SignUpResponse
from ..schema.action.logout import LogoutBodyParams, LogoutHeader, LogoutResponse

from ..errors.action.sign_in import SignInActionError

from ..utils.decorators import json_response, unpack_models
from ..utils.system import json_abort


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
@jwt_required(optional=True)
@json_response
@inject
def sign_in(
    body: SignInBodyParams, 
    headers: SignInHeader,
    access_token_service: BaseTokenService = Provide[ServiceContainer.access_token_service],
    refresh_token_service: BaseTokenService = Provide[ServiceContainer.refresh_token_service],
    sign_in_service: BaseSignInService = Provide[ServiceContainer.sign_in_service],
    sign_in_history_service: SignInHistoryService = Provide[ServiceContainer.sign_in_history_service]
) -> SignInResponse:
    """ Авторизация пользователя
    ---
        На вход поступает логин и пароль, если пользователь существует и авторизация успешна, то 
        создается и возвразается пара jwt токенов.
    """

    if access_token_service.is_valid_into_request():
        json_abort(HTTPStatus.OK, SignInActionError.ALREADY_AUTH)

    user = sign_in_service.authorization(login=body.login, password=body.password)

    access_token = access_token_service.create(claims=user)
    refresh_token = refresh_token_service.create(claims=user)

    sign_in_history_service.create_record(user_id=user.id, user_agent=headers.user_agent)

    return SignInResponse(access_token=access_token, refresh_token=refresh_token)


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
