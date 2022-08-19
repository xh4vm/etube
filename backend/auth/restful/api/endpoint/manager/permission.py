from http import HTTPStatus
from typing import Union

from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic_spec import Response

from dependency_injector.wiring import inject, Provide

from api.app import spec
from api.schema.manager.permission.get import (GetPermissionHeader, GetPermissionResponse, GetPermissionError)
from api.schema.manager.permission.create import CreatePermissionParams, CreatePermissionHeader, CreatePermissionResponse
from api.schema.manager.permission.update import (UpdatePermissionParams, UpdatePermissionHeader, UpdatePermissionResponse, UpdatePermissionError)
from api.schema.manager.permission.delete import DeletePermissionParams, DeletePermissionHeader, DeletePermissionResponse
from api.errors.manager.permissions import PermissionsError
from api.utils.decorators import json_response, unpack_models
from api.utils.system import json_abort

from api.services.manager.permissions import PermissionsService
from api.containers.permissions import ServiceContainer


bp = Blueprint('permission', __name__, url_prefix='/permission')
TAG = 'Manager'

@bp.route('', methods=['GET'])
@spec.validate(
    headers=GetPermissionHeader,
    resp=Response(HTTP_200=GetPermissionResponse, HTTP_404=GetPermissionError, HTTP_403=None),
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def get_permissions(
    headers: GetPermissionHeader,
    permissions_service: PermissionsService = Provide[ServiceContainer.permissions_service],
) -> Union[GetPermissionResponse, GetPermissionError]:
    """ Получение списка ограничений.
    """
    return GetPermissionResponse(permissions=permissions_service.all())


@bp.route('', methods=['POST'])
@spec.validate(
    body=CreatePermissionParams,
    headers=CreatePermissionHeader,
    resp=Response(HTTP_200=CreatePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def create_permission(
    body: CreatePermissionParams,
    headers: CreatePermissionHeader,
    permissions_service: PermissionsService = Provide[ServiceContainer.permissions_service],
) -> CreatePermissionResponse:
    """ Создание разрешения.
    """

    if permissions_service.exists(title=body.title):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, PermissionsError.ALREADY_EXISTS)

    permission = permissions_service.create(
        title=body.title,
        description=body.description,
        http_method=body.http_method,
        url=body.url,
    )

    return CreatePermissionResponse(
        id=permission,
        message=f'Разрешение {body.title} создано.',
    )


@bp.route('', methods=['PUT'])
@spec.validate(
    body=UpdatePermissionParams,
    headers=UpdatePermissionHeader,
    resp=Response(HTTP_200=UpdatePermissionResponse, HTTP_404=UpdatePermissionError, HTTP_403=None),
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def update_permission(
    body: UpdatePermissionParams,
    headers: UpdatePermissionHeader,
    permissions_service: PermissionsService = Provide[ServiceContainer.permissions_service],
) -> Union[UpdatePermissionResponse, UpdatePermissionError]:
    """ Обновление ограничения.
    """

    if not permissions_service.exists(id=body.id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, PermissionsError.NOT_EXISTS)

    permission = permissions_service.update(
        id=body.id,
        title=body.title,
        description=body.description,
        http_method=body.http_method,
        url=body.url,
    )

    return UpdatePermissionResponse(__root__=permission)


@bp.route('', methods=['DELETE'])
@spec.validate(
    body=DeletePermissionParams,
    headers=DeletePermissionHeader,
    resp=Response(HTTP_200=DeletePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def delete_permission(
    body: DeletePermissionParams,
    headers: DeletePermissionHeader,
    permissions_service: PermissionsService = Provide[ServiceContainer.permissions_service],
) -> DeletePermissionResponse:
    """ Удаление ограничения.
    """

    if not permissions_service.exists(id=body.id):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, PermissionsError.NOT_EXISTS)

    permissions_service.delete(id=body.id)

    return DeletePermissionResponse(message=f'Разрешение {body.id} удалено.')
