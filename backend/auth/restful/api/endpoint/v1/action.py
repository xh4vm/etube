import asyncio

from faker import Faker
from http import HTTPStatus

from api.app import spec
from api.containers.logout import ServiceContainer as LogoutServiceContainer
from api.containers.oauth import VKAuthContainer, YandexAuthContainer
from api.containers.sign_in import ServiceContainer as SignInServiceContainer
from api.containers.sign_up import ServiceContainer as SignUpServiceContainer
from api.errors.action.sign_in import SignInActionError
from api.errors.action.sign_up import SignUpActionError
from api.schema.action.logout import (LogoutBodyRequest, LogoutHeader,
                                      LogoutResponse)
from api.schema.action.sign_in import (SignInBodyParams, OAuthSignInBodyParams, SignInHeader,
                                       OAuthSignInHeader, SignInResponse)
from api.schema.action.sign_up import (SignUpBodyParams, SignUpHeader,
                                       SignUpResponse)
from api.schema.base import User as UserSchema
from api.services.authorization.base import BaseAuthService
from api.services.sign_in_history import SignInHistoryService
from api.services.token.base import BaseTokenService
from api.services.user import UserService
from api.utils.decorators import json_response, unpack_models
from api.utils.signature import check_signature
from api.utils.system import json_abort
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, make_response
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic_spec import Request, Response


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


@bp.route('/sign_in/yandex_permission', methods=['GET'])
@spec.validate(
    tags=[TAG],
)
@inject
def yandex_permission(
    auth_service: BaseAuthService = Provide[YandexAuthContainer.auth_service],
):
    """ Редирект на страницу Яндекса.
        ---
        При первом заходе пользователь должен разрешить доступ к его данным в Яндексе.
        При последующих заходах действий от пользователя не требуется.
    """
    return auth_service.get_permission_code()


@bp.route('/sign_in/yandex_user_data', methods=['GET'])
@spec.validate(
    tags=[TAG],
)
@inject
def yandex_user_data(
    auth_service: BaseAuthService = Provide[YandexAuthContainer.auth_service],
) -> Response:
    """ Получение данных от Яндекса.
        ---
        Запрос на получение токенов, которые используются
        для получения данных пользователя в стороннем сервисе.
    """
    api_access_token = auth_service.get_api_tokens(request)
    user_data, signature = asyncio.run(auth_service.get_api_data(api_access_token))

    return make_response(
        {
            'user_service_id': user_data.get('user_service_id'),
            'email': user_data.get('email'),
        },
        200,
        {'user_data_signature': signature}
    )


@bp.route('/sign_in/yandex', methods=['POST'])
@spec.validate(
    body=Request(OAuthSignInBodyParams),
    headers=OAuthSignInHeader,
    resp=Response(HTTP_200=SignInResponse, HTTP_403=None, HTTP_400=None, HTTP_422=None),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def sign_in_yandex(
    body: OAuthSignInBodyParams,
    headers: OAuthSignInHeader,
    access_token_service: BaseTokenService = Provide[SignInServiceContainer.access_token_service],
    refresh_token_service: BaseTokenService = Provide[SignInServiceContainer.refresh_token_service],
    auth_service: BaseAuthService = Provide[YandexAuthContainer.auth_service],
    user_service: UserService = Provide[SignUpServiceContainer.user_service],
    sign_in_history_service: SignInHistoryService = Provide[SignInServiceContainer.sign_in_history_service],
) -> SignInResponse:
    """ Авторизация пользователя через Яндекс.
        ---
    """
    service_name = 'yandex'

    signature = headers.user_data_signature
    if signature is None:
        json_abort(HTTPStatus.BAD_REQUEST, SignInActionError.SIGNATURE_DOES_NOT_EXIST)

    if not check_signature(body, signature):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, SignInActionError.NOT_VALID_SIGNATURE)

    user_service_id = body.user_service_id
    user_email = body.email

    user_social = auth_service.get_user_social(
        user_service_id=user_service_id,
        service_name=service_name,
    )
    if user_social is None:
        if user_service.exists(email=user_email):
            user = user_service.get(email=user_email)
            user_id = user.id
        else:
            user_id = user_service.create(
                login=Faker().user_name(),
                email=user_email,
                password=Faker().password(length=12),
            )
        user_social = auth_service.create_social_user(
                user_id=user_id,
                user_service_id=user_service_id,
                email=user_email,
                service_name=service_name,
        )

    user: UserSchema = auth_service.authorization(user_id=user_social.user_id)

    access_token: str = access_token_service.create(identity=user.id, claims=user.get_claims())
    refresh_token: str = refresh_token_service.create(identity=user.id)

    sign_in_history_service.create_record(user_id=user.id, user_agent=headers.user_agent)

    return SignInResponse(access_token=access_token, refresh_token=refresh_token)


@bp.route('/sign_in/vk_permission', methods=['GET'])
@spec.validate(
    tags=[TAG],
)
@inject
def sign_in_vk_permission(
    auth_service: BaseAuthService = Provide[VKAuthContainer.auth_service],
):
    """ Редирект на страницу VK.
        ---
        При первом заходе пользователь должен разрешить доступ к его данным в VK.
        При последующих заходах действий от пользователя не требуется.
    """
    return auth_service.get_permission_code()


@bp.route('/sign_in/vk_user_data', methods=['GET'])
@spec.validate(
    tags=[TAG],
)
@inject
def vk_user_data(
    auth_service: BaseAuthService = Provide[VKAuthContainer.auth_service],
) -> Response:
    """ Получение данных от VK.
        ---
        Запрос на получение токенов, которые используются
        для получения данных пользователя в стороннем сервисе.
    """
    user_data, signature = asyncio.run(auth_service.get_api_data(request))

    return make_response(
        {
            'user_service_id': user_data.get('user_service_id'),
            'email': user_data.get('email'),
        },
        200,
        {'user_data_signature': signature}
    )


@bp.route('/sign_in/vk', methods=['POST'])
@spec.validate(
    body=Request(OAuthSignInBodyParams),
    headers=OAuthSignInHeader,
    resp=Response(HTTP_200=SignInResponse, HTTP_403=None, HTTP_400=None, HTTP_422=None),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def sign_in_vk(
    body: OAuthSignInBodyParams,
    headers: OAuthSignInHeader,
    access_token_service: BaseTokenService = Provide[SignInServiceContainer.access_token_service],
    refresh_token_service: BaseTokenService = Provide[SignInServiceContainer.refresh_token_service],
    auth_service: BaseAuthService = Provide[VKAuthContainer.auth_service],
    user_service: UserService = Provide[SignUpServiceContainer.user_service],
    sign_in_history_service: SignInHistoryService = Provide[SignInServiceContainer.sign_in_history_service],
) -> SignInResponse:
    """ Авторизация пользователя через VK.
        ---
    """
    service_name = 'vk'

    signature = headers.user_data_signature
    if signature is None:
        json_abort(HTTPStatus.BAD_REQUEST, SignInActionError.SIGNATURE_DOES_NOT_EXIST)

    if not check_signature(body, signature):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, SignInActionError.NOT_VALID_SIGNATURE)

    user_service_id = body.user_service_id
    user_email = body.email

    if user_service_id == 'None':
        json_abort(HTTPStatus.OK, SignInActionError.ALREADY_AUTH)

    user_social = auth_service.get_user_social(
        user_service_id=user_service_id,
        service_name=service_name,
    )
    if user_social is None:
        if user_service.exists(email=user_email):
            user = user_service.get(email=user_email)
            user_id = user.id
        else:
            user_id = user_service.create(
                login=Faker().user_name(),
                email=user_email,
                password=Faker().password(length=12),
            )
        user_social = auth_service.create_social_user(
                user_id=user_id,
                user_service_id=user_service_id,
                email=user_email,
                service_name=service_name,
        )

    user: UserSchema = auth_service.authorization(user_id=user_social.user_id)

    access_token: str = access_token_service.create(identity=user.id, claims=user.get_claims())
    refresh_token: str = refresh_token_service.create(identity=user.id)

    sign_in_history_service.create_record(user_id=user.id, user_agent=headers.user_agent)

    return SignInResponse(access_token=access_token, refresh_token=refresh_token)
