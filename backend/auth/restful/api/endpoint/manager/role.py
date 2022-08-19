from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic_spec import Request, Response

from ...app import spec
from ...containers.roles import ServiceContainer
from ...schema.manager.role.create import (CreateRoleBodyParams,
                                           CreateRoleHeader,
                                           CreateRoleResponse)
from ...schema.manager.role.delete import (DeleteRoleBodyParams,
                                           DeleteRoleHeader,
                                           DeleteRoleResponse)
from ...schema.manager.role.get import (GetRoleHeader, GetRoleQueryParams,
                                        GetRoleResponse)
from ...schema.manager.role.retrieve import (RoleRetrievePermissionBodyParams,
                                             RoleRetrievePermissionHeader,
                                             RoleRetrievePermissionResponse)
from ...schema.manager.role.set import (RoleSetPermissionBodyParams,
                                        RoleSetPermissionHeader,
                                        RoleSetPermissionResponse)
from ...schema.manager.role.update import (UpdateRoleBodyParams,
                                           UpdateRoleHeader,
                                           UpdateRoleResponse)
from ...services.manager.roles.roles import RolesService
from ...utils.decorators import json_response, unpack_models

bp = Blueprint('role', __name__, url_prefix='/role')
TAG = 'Manager'

@bp.route('', methods=['GET'])
@spec.validate(
    query=GetRoleQueryParams, 
    headers=GetRoleHeader,
    resp=Response(HTTP_200=GetRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def get_roles(
    query: GetRoleQueryParams,
    headers: GetRoleHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
):
    """ Получение списка ролей пользователя
    ---
        По uuid пользователя получаем список ролей
    """
    return GetRoleResponse(
        roles=roles_service.roles_list(query.user_id),
    )


@bp.route('', methods=['POST'])
@spec.validate(
    body=Request(CreateRoleBodyParams), 
    headers=CreateRoleHeader, 
    resp=Response(HTTP_200=CreateRoleResponse, HTTP_403=None), 
    tags=[TAG]
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
    role = roles_service.create(
        title=body.title,
        description=body.description,
    )

    return CreateRoleResponse(
        id=role,
        message=f'Роль {body.title} создана.',
    )


@bp.route('', methods=['PUT'])
@spec.validate(
    body=Request(UpdateRoleBodyParams),
    headers=UpdateRoleHeader,
    resp=Response(HTTP_200=UpdateRoleResponse, HTTP_403=None),
    tags=[TAG]
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
    role = roles_service.update(
        id=body.id,
        title=body.title,
        description=body.description,
    )

    return UpdateRoleResponse(__root__=role)


@bp.route('', methods=['DELETE'])
@spec.validate(
    body=Request(DeleteRoleBodyParams),
    headers=DeleteRoleHeader,
    resp=Response(HTTP_200=DeleteRoleResponse, HTTP_403=None),
    tags=[TAG]
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
    roles_service.delete(role_id=body.id)

    return DeleteRoleResponse(message=f'Роль {body.id} удалена.')


@bp.route('/permission', methods=['POST'])
@spec.validate(
    body=Request(RoleSetPermissionBodyParams),
    headers=RoleSetPermissionHeader,
    resp=Response(HTTP_200=RoleSetPermissionResponse, HTTP_403=None),
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def set_permission(
    body: RoleSetPermissionBodyParams,
    headers: RoleSetPermissionHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
) -> RoleSetPermissionResponse:
    """ Докинуть ограничение в роль
    ---
        Докидываем ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION в роль
    """
    permissions = roles_service.set_permission(role_id=body.role_id, permissions=body.permission_ids)
    return RoleSetPermissionResponse(
        permissions=permissions,
        message=f'Разрешения {body.permission_ids} для роли {body.role_id} добавлены.',
    )


@bp.route('/permission', methods=['DELETE'])
@spec.validate(
    body=Request(RoleRetrievePermissionBodyParams),
    headers=RoleRetrievePermissionHeader,
    resp=Response(HTTP_200=RoleRetrievePermissionResponse, HTTP_403=None),
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def retrieve_permission(
    body: RoleRetrievePermissionBodyParams,
    headers: RoleRetrievePermissionHeader,
    roles_service: RolesService = Provide[ServiceContainer.roles_service],
) -> RoleRetrievePermissionResponse:
    """ Отобрать ограничение из роли
    ---
        Отобрать ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION из роли
    """
    permissions = roles_service.retrieve_permission(role_id=body.role_id, permissions=body.permission_ids)
    return RoleRetrievePermissionResponse(
        permissions=permissions,
        message=f'Разрешения {body.permission_ids} для роли {body.role_id} удалены.',
    )
