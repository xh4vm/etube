import uuid
from flask import Blueprint
from flask_pydantic_spec import Response, Request

from ...app import spec
from ...schema.manager.permission.get import GetPermissionBodyParams, GetPermissionHeader, GetPermissionResponse
from ...schema.manager.permission.create import CreatePermissionBodyParams, CreatePermissionHeader, CreatePermissionResponse
from ...schema.manager.permission.update import UpdatePermissionBodyParams, UpdatePermissionHeader, UpdatePermissionResponse
from ...schema.manager.permission.delete import DeletePermissionBodyParams, DeletePermissionHeader, DeletePermissionResponse
from ...schema.manager.permission.set import SetPermissionBodyParams, SetPermissionHeader, SetPermissionResponse
from ...schema.manager.permission.retrive import RetrivePermissionBodyParams, RetrivePermissionHeader, RetrivePermissionResponse
from ...utils.decorators import json_response, unpack_models


bp = Blueprint('permission', __name__, url_prefix='/permission')
TAG = 'Manager'

@bp.route('', methods=['GET'])
@spec.validate(
    body=Request(GetPermissionBodyParams), 
    headers=GetPermissionHeader,
    resp=Response(HTTP_200=GetPermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def get_permissions():
    """ Получение списка ограничений конкретной роли
    ---
        По uuid роли получаем список ограничений
    """
    return GetPermissionResponse(permissions=[])


@bp.route('', methods=['POST'])
@spec.validate(
    body=Request(CreatePermissionBodyParams), 
    headers=CreatePermissionHeader, 
    resp=Response(HTTP_200=CreatePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def create_permission() -> CreatePermissionResponse:
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
def update_permission() -> UpdatePermissionResponse:
    """ Обновление ограничения 
    ---
        Обновляем ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION
    """
    UpdatePermissionResponse(id=uuid.uuid4(), title='')


@bp.route('', methods=['DELETE'])
@spec.validate(
    body=Request(DeletePermissionBodyParams), 
    headers=DeletePermissionHeader, 
    resp=Response(HTTP_200=DeletePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def delete_permission() -> DeletePermissionResponse:
    """ Удаление ограничения
    ---
        Удаляем ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION
    """
    return DeletePermissionResponse()


@bp.route('/role', methods=['POST'])
@spec.validate(
    body=Request(SetPermissionBodyParams), 
    headers=SetPermissionHeader, 
    resp=Response(HTTP_200=SetPermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def set_permission() -> SetPermissionResponse:
    """ Докинуть ограничение в роль
    ---
        Докидываем ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION в роль
    """
    return SetPermissionResponse()


@bp.route('/role', methods=['DELETE'])
@spec.validate(
    body=Request(RetrivePermissionBodyParams), 
    headers=RetrivePermissionHeader, 
    resp=Response(HTTP_200=RetrivePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def retrive_permission() -> RetrivePermissionResponse:
    """ Отобрать ограничение из роли
    ---
        Отобрать ограничение ID::HTTP_METHOD::URL::<ACCESS or DENY>::TITLE::DESCRIPTION из роли
    """
    return RetrivePermissionResponse()