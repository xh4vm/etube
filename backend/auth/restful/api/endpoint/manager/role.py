import uuid
from flask import Blueprint
from flask_pydantic_spec import Response, Request

from ...app import spec
from ...schema.manager.role.get import GetRoleQueryParams, GetRoleHeader, GetRoleResponse
from ...schema.manager.role.create import CreateRoleBodyParams, CreateRoleHeader, CreateRoleResponse
from ...schema.manager.role.update import UpdateRoleBodyParams, UpdateRoleHeader, UpdateRoleResponse
from ...schema.manager.role.delete import DeleteRoleBodyParams, DeleteRoleHeader, DeleteRoleResponse
from ...schema.manager.role.set import RoleSetPermissionBodyParams, RoleSetPermissionHeader, RoleSetPermissionResponse
from ...schema.manager.role.retrive import RoleRetrivePermissionBodyParams, RoleRetrivePermissionHeader, RoleRetrivePermissionResponse
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
@json_response
def get_roles(query: GetRoleQueryParams, headers: GetRoleHeader):
    """ Получение списка ролей пользователя
    ---
        По uuid пользователя получаем список ролей
    """
    return GetRoleResponse(__root__=[])


@bp.route('', methods=['POST'])
@spec.validate(
    body=Request(CreateRoleBodyParams), 
    headers=CreateRoleHeader, 
    resp=Response(HTTP_200=CreateRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def create_role(body: CreateRoleBodyParams, headers: CreateRoleHeader) -> CreateRoleResponse:
    """ Создание роли 
    ---
        Создаем новую роль
    """
    return CreateRoleResponse(id=uuid.uuid4())


@bp.route('', methods=['PUT'])
@spec.validate(
    body=Request(UpdateRoleBodyParams), 
    headers=UpdateRoleHeader, 
    resp=Response(HTTP_200=UpdateRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def update_role(body: UpdateRoleBodyParams, headers: UpdateRoleHeader) -> UpdateRoleResponse:
    """ Обновление роли
    ---
        Обновляем роль
    """
    UpdateRoleResponse(id=uuid.uuid4(), title='')


@bp.route('', methods=['DELETE'])
@spec.validate(
    body=Request(DeleteRoleBodyParams), 
    headers=DeleteRoleHeader, 
    resp=Response(HTTP_200=DeleteRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def delete_role(body: DeleteRoleBodyParams, headers: DeleteRoleHeader) -> DeleteRoleResponse:
    """ Удаление роли
    ---
        Удаляем роль
    """
    return DeleteRoleResponse()


@bp.route('/permission', methods=['POST'])
@spec.validate(
    body=Request(RoleSetPermissionBodyParams), 
    headers=RoleSetPermissionHeader, 
    resp=Response(HTTP_200=RoleSetPermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def set_permission(body: RoleSetPermissionBodyParams, headers: RoleSetPermissionHeader) -> RoleSetPermissionResponse:
    """ Докинуть ограничение в роль
    ---
        Докидываем ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION в роль
    """
    return RoleSetPermissionResponse()


@bp.route('/permission', methods=['DELETE'])
@spec.validate(
    body=Request(RoleRetrivePermissionBodyParams), 
    headers=RoleRetrivePermissionHeader, 
    resp=Response(HTTP_200=RoleRetrivePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def retrive_permission(body: RoleRetrivePermissionBodyParams, headers: RoleRetrivePermissionHeader) -> RoleRetrivePermissionResponse:
    """ Отобрать ограничение из роли
    ---
        Отобрать ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION из роли
    """
    return RoleRetrivePermissionResponse()