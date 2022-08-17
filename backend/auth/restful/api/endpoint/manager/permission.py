import uuid
from typing import Union

from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic_spec import Response

from dependency_injector.wiring import inject, Provide

from ...app import spec
from ...schema.manager.permission.get import (GetPermissionParams, GetPermissionHeader,
                                              GetPermissionResponse, GetPermissionError)
from ...schema.manager.permission.create import CreatePermissionParams, CreatePermissionHeader, CreatePermissionResponse
from ...schema.manager.permission.update import (UpdatePermissionParams, UpdatePermissionHeader,
                                                 UpdatePermissionResponse, UpdatePermissionError)
from ...schema.manager.permission.delete import DeletePermissionParams, DeletePermissionHeader, DeletePermissionResponse
from ...schema.base import Permission as validator
from ...utils.decorators import json_response, unpack_models

from ...model.models import User, Permission
from ...model.base import db

from ...services.manager.permissions.base import BasePermissionsService
from ...containers.permissions import ServiceContainer


bp = Blueprint('permission', __name__, url_prefix='/permission')
TAG = 'Manager'

@bp.route('', methods=['GET'])
@spec.validate(
    query=GetPermissionParams,
    headers=GetPermissionHeader,
    resp=Response(HTTP_200=GetPermissionResponse, HTTP_404=GetPermissionError, HTTP_403=None),
    tags=[TAG]
)
@unpack_models
@jwt_required()
@json_response
@inject
def get_permissions(
    query: GetPermissionParams,
    headers: GetPermissionHeader,
    permissions_service: BasePermissionsService = Provide[ServiceContainer.permissions_service],
) -> Union[GetPermissionResponse, GetPermissionError]:
    """ Получение списка ограничений конкретной роли.
    """
    return GetPermissionResponse(
        permissions=permissions_service.permissions_list(query.user_id),
    )


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
    permissions_service: BasePermissionsService = Provide[ServiceContainer.permissions_service],
) -> CreatePermissionResponse:
    """ Создание разрешения.
    """

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
    permissions_service: BasePermissionsService = Provide[ServiceContainer.permissions_service],
) -> Union[UpdatePermissionResponse, UpdatePermissionError]:
    """ Обновление ограничения.
    """

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
    permissions_service: BasePermissionsService = Provide[ServiceContainer.permissions_service],
) -> DeletePermissionResponse:
    """ Удаление ограничения.
    """
    permissions_service.delete(permission_id=body.id)

    return DeletePermissionResponse(message=f'Разрешение {body.id} удалено.')
