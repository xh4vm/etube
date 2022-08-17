from flask import Blueprint
from flask_pydantic_spec import Response, Request
from flask_jwt_extended.view_decorators import jwt_required
from dependency_injector.wiring import inject, Provide

from ..services.token.base import BaseTokenService
from ..services.sign_in_history import SignInHistoryService
from ..services.action.sign_in.base import BaseSignInService
from ..services.action.sign_up.base import BaseSignUpService

from ..containers.sign_in import ServiceContainer as SignInServiceContainer
from ..containers.sign_up import ServiceContainer as SignUpServiceContainer

from ..app import spec
from ..schema.action.sign_in import SignInBodyParams, SignInHeader, SignInResponse
from ..schema.action.sign_up import SignUpBodyParams, SignUpHeader, SignUpResponse
from ..schema.action.logout import LogoutBodyParams, LogoutHeader, LogoutResponse

from ..decorators.action import already_auth
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
@jwt_required(optional=True)
@already_auth
@json_response
@inject
def sign_in(
    body: SignInBodyParams, 
    headers: SignInHeader,
    access_token_service: BaseTokenService = Provide[SignInServiceContainer.access_token_service],
    refresh_token_service: BaseTokenService = Provide[SignInServiceContainer.refresh_token_service],
    sign_in_service: BaseSignInService = Provide[SignInServiceContainer.sign_in_service],
    sign_in_history_service: SignInHistoryService = Provide[SignInServiceContainer.sign_in_history_service]
) -> SignInResponse:
    """ Авторизация пользователя
    ---
        На вход поступает логин и пароль, если пользователь существует и авторизация успешна, то 
        создается и возвразается пара jwt токенов.
    """
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
@inject
def sign_up(
    body: SignUpBodyParams,
    headers: SignUpHeader,
    sign_up_service: BaseSignUpService = Provide[SignUpServiceContainer.sign_up_service],
) -> SignUpResponse:
    """ Регистрация пользователя
    ---
        На вход поступает логин, почта и пароль, если регистрация успешна, то возвращается id нового пользователя.
    """
    user = sign_up_service.registration(login=body.login, email=body.email, password=body.password)
    return SignUpResponse(
        id=user,
        message='Пользователь успешно зарегистрирован.'
    )


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
