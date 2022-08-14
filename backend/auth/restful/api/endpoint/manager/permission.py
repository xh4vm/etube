import uuid
from flask import Blueprint
from flask_pydantic_spec import Response, Request

from ...app import spec
from ...schema.manager.permission.get import GetPermissionQueryParams, GetPermissionHeader, GetPermissionResponse
from ...schema.manager.permission.create import CreatePermissionBodyParams, CreatePermissionHeader, CreatePermissionResponse
from ...schema.manager.permission.update import UpdatePermissionBodyParams, UpdatePermissionHeader, UpdatePermissionResponse
from ...schema.manager.permission.delete import DeletePermissionBodyParams, DeletePermissionHeader, DeletePermissionResponse
from ...schema.manager.permission.base import Permission
from ...utils.decorators import json_response, unpack_models


bp = Blueprint('permission', __name__, url_prefix='/permission')
TAG = 'Manager'

@bp.route('', methods=['GET'])
@spec.validate(
    query=GetPermissionQueryParams, 
    headers=GetPermissionHeader,
    resp=Response(HTTP_200=GetPermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def get_permissions(query: GetPermissionQueryParams, headers: GetPermissionHeader):
    """ Получение списка ограничений конкретной роли
    ---
        По uuid роли получаем список ограничений
    """
    return GetPermissionResponse(__root__=[])


@bp.route('', methods=['POST'])
@spec.validate(
    body=Request(CreatePermissionBodyParams), 
    headers=CreatePermissionHeader, 
    resp=Response(HTTP_200=CreatePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def create_permission(body: CreatePermissionBodyParams, headers: CreatePermissionHeader) -> CreatePermissionResponse:
    """ Создание ограничения 
    ---
        Создаем новое ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION
    """
    return CreatePermissionResponse(id=uuid.uuid4())


@bp.route('', methods=['PUT'])
@spec.validate(
    body=Request(UpdatePermissionBodyParams), 
    headers=UpdatePermissionHeader, 
    resp=Response(HTTP_200=UpdatePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def update_permission(body: UpdatePermissionBodyParams, headers: UpdatePermissionHeader) -> UpdatePermissionResponse:
    """ Обновление ограничения 
    ---
        Обновляем ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION
    """
    UpdatePermissionResponse(__root__=Permission())


@bp.route('', methods=['DELETE'])
@spec.validate(
    body=Request(DeletePermissionBodyParams), 
    headers=DeletePermissionHeader, 
    resp=Response(HTTP_200=DeletePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def delete_permission(body: DeletePermissionBodyParams, headers: DeletePermissionHeader) -> DeletePermissionResponse:
    """ Удаление ограничения
    ---
        Удаляем ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION
    """
    return DeletePermissionResponse()
