from http import HTTPStatus
from flask import Blueprint
from dependency_injector.wiring import Provide, inject
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic_spec import Response, Request

from api.app import spec
from api.errors.manager.roles import RolesError
from api.errors.user import UserError
from api.containers.user import ServiceContainer
from api.services.roles import RolesService
from api.services.user import UserService

from api.schema.manager.user.get import GetUserHeader, GetUserResponse
from api.schema.manager.user.update import UpdateUserBodyParams, UpdateUserHeader, UpdateUserResponse
from api.schema.manager.user.set_role import UserSetRoleBodyParams, UserSetRoleHeader, UserSetRoleResponse
from api.schema.manager.user.retrive_role import UserRetriveRoleBodyParams, UserRetriveRoleHeader, UserRetriveRoleResponse
from api.utils.decorators import json_response, unpack_models
from api.utils.system import json_abort


bp = Blueprint('user', __name__, url_prefix='/user')
TAG = 'Manager'


@bp.route('', methods=['GET'])
@spec.validate(
    headers=GetUserHeader,
    resp=Response(HTTP_200=GetUserResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def get_user(
    headers: GetUserHeader,
    user_service: UserService = Provide[ServiceContainer.user_service],
):
    """ Получение списка пользователей
    ---
        Получаем список пользщователей
    """

    return GetUserResponse(users=user_service.all())


@bp.route('', methods=['PUT'])
@spec.validate(
    body=Request(UpdateUserBodyParams),
    headers=UpdateUserHeader,
    resp=Response(HTTP_200=UpdateUserResponse, HTTP_403=None),
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def update_user(
    body: UpdateUserBodyParams,
    headers: UpdateUserHeader,
    user_service: RolesService = Provide[ServiceContainer.user_service],
) -> UpdateUserResponse:
    """ Обновление роли
    ---
        Обновляем роль
    """
    if not user_service.exists(id=body.id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, UserError.NOT_EXISTS)

    user = user_service.update(id=body.id, login=body.login, email=body.email, password=body.password)

    return UpdateUserResponse(__root__=user)


@bp.route('/role', methods=['POST'])
@spec.validate(
    body=Request(UserSetRoleBodyParams), 
    headers=UserSetRoleHeader, 
    resp=Response(HTTP_200=UserSetRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def set_role(
    body: UserSetRoleBodyParams, 
    headers: UserSetRoleHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
    user_service: UserService = Provide[ServiceContainer.user_service],
) -> UserSetRoleResponse:
    """ Добавление роли пользователю
    ---
        Накидываем роль пользователю
    """
    if not roles_service.exists(id=body.role_id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)

    if not user_service.exists(id=body.user_id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, UserError.NOT_EXISTS)

    user_service.set_role(role_id=body.role_id, user_id=body.user_id)
    
    return UserSetRoleResponse(message=f'Роль {body.role_id} для пользователя {body.user_id} добавлено.')


@bp.route('/role', methods=['DELETE'])
@spec.validate(
    body=Request(UserRetriveRoleBodyParams), 
    headers=UserRetriveRoleHeader, 
    resp=Response(HTTP_200=UserRetriveRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def retrive_role(
    body: UserRetriveRoleBodyParams, 
    headers: UserRetriveRoleHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
    user_service: UserService = Provide[ServiceContainer.user_service],
) -> UserRetriveRoleResponse:
    """Отбираем роль у пользователя
    ---
        Отбираем роль у пользователя
    """
    if not roles_service.exists(id=body.role_id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)

    if not user_service.exists(id=body.user_id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, UserError.NOT_EXISTS)

    user_service.retrieve_role(role_id=body.role_id, user_id=body.user_id)
    
    return UserRetriveRoleResponse(message=f'Роль {body.role_id} для пользователя {body.user_id} удалена.')
