from http import HTTPStatus

from api.errors.action.sign_up import SignUpActionError
from api.schema.base import User as UserSchema
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic_spec import Request, Response

from ..app import spec
from ..containers.logout import ServiceContainer as LogoutServiceContainer
from ..containers.sign_in import ServiceContainer as SignInServiceContainer
from ..containers.sign_up import ServiceContainer as SignUpServiceContainer
from ..errors.action.sign_in import SignInActionError
from ..schema.action.logout import (LogoutBodyRequest, LogoutHeader,
                                    LogoutResponse)
from ..schema.action.sign_in import (SignInBodyParams, SignInHeader,
                                     SignInResponse)
from ..schema.action.sign_up import (SignUpBodyParams, SignUpHeader,
                                     SignUpResponse)
from ..services.authorization.base import BaseAuthService
from ..services.sign_in_history import SignInHistoryService
from ..services.token.base import BaseTokenService
from ..services.user import UserService
from ..utils.decorators import json_response, unpack_models
from ..utils.system import json_abort

bp = Blueprint('action', __name__, url_prefix='/action')
TAG = 'Action'


@bp.route('/sign_in', methods=['POST'])
@spec.validate(
    body=Request(SignInBodyParams),
    headers=SignInHeader,
    resp=Response(HTTP_200=SignInResponse, HTTP_403=None),
    tags=[TAG],
)
@unpack_models
@jwt_required(optional=True)
@json_response
@inject
def sign_in(
    body: SignInBodyParams,
    headers: SignInHeader,
    access_token_service: BaseTokenService = Provide[SignInServiceContainer.access_token_service],
    refresh_token_service: BaseTokenService = Provide[SignInServiceContainer.refresh_token_service],
    auth_service: BaseAuthService = Provide[SignInServiceContainer.auth_service],
    sign_in_history_service: SignInHistoryService = Provide[SignInServiceContainer.sign_in_history_service],
) -> SignInResponse:
    """ Авторизация пользователя
    ---
        На вход поступает логин и пароль, если пользователь существует и авторизация успешна, то
        создается и возвразается пара jwt токенов.
    """

    if access_token_service.is_valid_into_request():
        json_abort(HTTPStatus.OK, SignInActionError.ALREADY_AUTH)

    user: UserSchema = auth_service.authorization(login=body.login, password=body.password)

    access_token: str = access_token_service.create(identity=user.id, claims=user.get_claims())
    refresh_token: str = refresh_token_service.create(identity=user.id)

    sign_in_history_service.create_record(user_id=user.id, user_agent=headers.user_agent)

    return SignInResponse(access_token=access_token, refresh_token=refresh_token)


@bp.route('/sign_up', methods=['POST'])
@spec.validate(
    body=Request(SignUpBodyParams),
    headers=SignUpHeader,
    resp=Response(HTTP_200=SignUpResponse, HTTP_403=None),
    tags=[TAG],
)
@unpack_models
@jwt_required(optional=True)
@json_response
@inject
def sign_up(
    body: SignUpBodyParams,
    headers: SignUpHeader,
    access_token_service: BaseTokenService = Provide[SignUpServiceContainer.access_token_service],
    user_service: UserService = Provide[SignUpServiceContainer.user_service],
) -> SignUpResponse:
    """ Регистрация пользователя
    ---
        На вход поступает логин, почта и пароль, если регистрация успешна, то возвращается id нового пользователя.
    """
    if access_token_service.is_valid_into_request():
        json_abort(HTTPStatus.OK, SignInActionError.ALREADY_AUTH)

    if user_service.exists(login=body.login, email=body.email):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, SignUpActionError.ALREADY_EXISTS)

    user_id = user_service.create(login=body.login, email=body.email, password=body.password)

    return SignUpResponse(id=user_id, message='Пользователь успешно зарегистрирован.')


@bp.route('/logout', methods=['DELETE'])
@spec.validate(
    body=Request(LogoutBodyRequest),
    headers=LogoutHeader,
    resp=Response(HTTP_200=LogoutResponse, HTTP_403=None),
    tags=[TAG],
)
@unpack_models
@jwt_required()
@json_response
@inject
def logout(
    body: LogoutBodyRequest,
    headers: LogoutHeader,
    access_token_service: BaseTokenService = Provide[LogoutServiceContainer.access_token_service],
    refresh_token_service: BaseTokenService = Provide[LogoutServiceContainer.refresh_token_service],
):
    """ Выход пользователя из текущей сессии
    ---
        Выход пользователя из текущей сессии. Текущая пара (access_token,refresh_token) становится недействительной.
    """
    access_token = headers.get_token()
    access_token_service.add_to_blocklist(access_token)

    refresh_token_service.add_to_blocklist(body.refresh_token)

    return LogoutResponse()
