from http import HTTPStatus

from api.app import spec
from api.containers.roles import ServiceContainer
from api.errors.manager.permissions import PermissionsError
from api.errors.manager.roles import RolesError
from api.schema.base import RoleMap
from api.schema.manager.role.create import (CreateRoleBodyParams,
                                            CreateRoleHeader,
                                            CreateRoleResponse)
from api.schema.manager.role.delete import (DeleteRoleBodyParams,
                                            DeleteRoleHeader,
                                            DeleteRoleResponse)
from api.schema.manager.role.get import GetRoleHeader, GetRoleResponse
from api.schema.manager.role.retrieve import (RoleRetrievePermissionBodyParams,
                                              RoleRetrievePermissionHeader,
                                              RoleRetrievePermissionResponse)
from api.schema.manager.role.set import (RoleSetPermissionBodyParams,
                                         RoleSetPermissionHeader,
                                         RoleSetPermissionResponse)
from api.schema.manager.role.update import (UpdateRoleBodyParams,
                                            UpdateRoleHeader,
                                            UpdateRoleResponse)
from api.services.permissions import PermissionsService
from api.services.roles import RolesService
from api.utils.decorators import (access_exception_handler, json_response,
                                  token_extractor, unpack_models)
from api.utils.system import json_abort
from auth_client.src.decorators import grpc_access_required
from core.config import CONFIG
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic_spec import Request, Response

bp = Blueprint('role', __name__, url_prefix='/role')
TAG = 'Manager'
URL = f'{CONFIG.APP.APP_HOST}:{CONFIG.APP.APP_PORT}/api/v1/auth/manager/role'


@bp.route('', methods=['GET'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL: 'GET'})
@spec.validate(headers=GetRoleHeader, resp=Response(HTTP_200=GetRoleResponse, HTTP_403=None), tags=[TAG])
@unpack_models
@jwt_required()
@json_response
@inject
def get_roles(
    headers: GetRoleHeader, roles_service: RolesService = Provide[ServiceContainer.roles_service],
):
    """ Получение списка ролей
    ---
        Получаем список ролей
    """

    return GetRoleResponse(roles=roles_service.all())


@bp.route('', methods=['POST'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL: 'POST'})
@spec.validate(
    body=Request(CreateRoleBodyParams),
    headers=CreateRoleHeader,
    resp=Response(HTTP_200=CreateRoleResponse, HTTP_403=None),
    tags=[TAG],
)
@unpack_models
@jwt_required()
@json_response
@inject
def create_role(
    body: CreateRoleBodyParams,
    headers: CreateRoleHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
) -> CreateRoleResponse:
    """ Создание роли
    ---
        Создаем новую роль
    """
    if roles_service.exists(title=body.title):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.ALREADY_EXISTS)

    role: RoleMap = roles_service.create(title=body.title, description=body.description)

    return CreateRoleResponse(id=role.id, message=f'Роль {body.title} создана.')


@bp.route('', methods=['PUT'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL: 'PUT'})
@spec.validate(
    body=Request(UpdateRoleBodyParams),
    headers=UpdateRoleHeader,
    resp=Response(HTTP_200=UpdateRoleResponse, HTTP_403=None),
    tags=[TAG],
)
@unpack_models
@jwt_required()
@json_response
@inject
def update_role(
    body: UpdateRoleBodyParams,
    headers: UpdateRoleHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
) -> UpdateRoleResponse:
    """ Обновление роли
    ---
        Обновляем роль
    """
    if not roles_service.exists(id=body.id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)

    role = roles_service.update(id=body.id, title=body.title, description=body.description)

    return UpdateRoleResponse(__root__=role)


@bp.route('', methods=['DELETE'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL: 'DELETE'})
@spec.validate(
    body=Request(DeleteRoleBodyParams),
    headers=DeleteRoleHeader,
    resp=Response(HTTP_200=DeleteRoleResponse, HTTP_403=None),
    tags=[TAG],
)
@unpack_models
@jwt_required()
@json_response
@inject
def delete_role(
    body: DeleteRoleBodyParams,
    headers: DeleteRoleHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
) -> DeleteRoleResponse:
    """ Удаление роли
    ---
        Удаляем роль
    """

    if not roles_service.exists(id=body.id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)

    roles_service.delete(id=body.id)

    return DeleteRoleResponse(message=f'Роль {body.id} удалена.')


@bp.route('/permission', methods=['POST'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL + '/permission': 'POST'})
@spec.validate(
    body=Request(RoleSetPermissionBodyParams),
    headers=RoleSetPermissionHeader,
    resp=Response(HTTP_200=RoleSetPermissionResponse, HTTP_403=None),
    tags=[TAG],
)
@unpack_models
@jwt_required()
@json_response
@inject
def set_permission(
    body: RoleSetPermissionBodyParams,
    headers: RoleSetPermissionHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
    permissions_service: PermissionsService = Provide[ServiceContainer.permissions_service],
) -> RoleSetPermissionResponse:
    """ Докинуть ограничение в роль
    ---
        Докидываем ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION в роль
    """
    if not roles_service.exists(id=body.role_id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)

    if not permissions_service.exists(id=body.permission_id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, PermissionsError.NOT_EXISTS)

    roles_service.set_permission(role_id=body.role_id, permission_id=body.permission_id)

    return RoleSetPermissionResponse(message=f'Разрешение {body.permission_id} для роли {body.role_id} добавлено.')


@bp.route('/permission', methods=['DELETE'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL + '/permission': 'DELETE'})
@spec.validate(
    body=Request(RoleRetrievePermissionBodyParams),
    headers=RoleRetrievePermissionHeader,
    resp=Response(HTTP_200=RoleRetrievePermissionResponse, HTTP_403=None),
    tags=[TAG],
)
@unpack_models
@jwt_required()
@json_response
@inject
def retrieve_permission(
    body: RoleRetrievePermissionBodyParams,
    headers: RoleRetrievePermissionHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
    permissions_service: PermissionsService = Provide[ServiceContainer.permissions_service],
) -> RoleRetrievePermissionResponse:
    """ Отобрать ограничение из роли
    ---
        Отобрать ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION из роли
    """

    if not roles_service.exists(id=body.role_id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)

    if not permissions_service.exists(id=body.permission_id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, PermissionsError.NOT_EXISTS)

    roles_service.retrieve_permission(role_id=body.role_id, permission_id=body.permission_id)

    return RoleRetrievePermissionResponse(message=f'Разрешение {body.permission_id} для роли {body.role_id} удалено.')
