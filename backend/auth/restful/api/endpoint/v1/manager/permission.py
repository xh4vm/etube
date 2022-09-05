from http import HTTPStatus
from typing import Union

from api.app import spec
from api.containers.permissions import ServiceContainer
from api.errors.manager.permissions import PermissionsError
from api.schema.base import Permission as PermissionSchema
from api.schema.manager.permission.create import (CreatePermissionHeader,
                                                  CreatePermissionParams,
                                                  CreatePermissionResponse)
from api.schema.manager.permission.delete import (DeletePermissionHeader,
                                                  DeletePermissionParams,
                                                  DeletePermissionResponse)
from api.schema.manager.permission.get import (GetPermissionError,
                                               GetPermissionHeader,
                                               GetPermissionResponse)
from api.schema.manager.permission.update import (UpdatePermissionError,
                                                  UpdatePermissionHeader,
                                                  UpdatePermissionParams,
                                                  UpdatePermissionResponse)
from api.services.permissions import PermissionsService
from api.utils.decorators import (access_exception_handler, json_response,
                                  token_extractor, unpack_models)
from api.utils.system import json_abort
from auth_client.src.decorators import grpc_access_required
from core.config import CONFIG
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic_spec import Response

bp = Blueprint('permission', __name__, url_prefix='/permission')
TAG = 'Manager'
URL = f'{CONFIG.APP.AUTH_APP_HOST}:{CONFIG.APP.AUTH_APP_PORT}/api/v1/auth/manager/permission'


@bp.route('', methods=['GET'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL: 'GET'})
@spec.validate(
    headers=GetPermissionHeader,
    resp=Response(HTTP_200=GetPermissionResponse, HTTP_404=GetPermissionError, HTTP_403=None),
    tags=[TAG],
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
@token_extractor
@access_exception_handler
@grpc_access_required({URL: 'POST'})
@spec.validate(
    body=CreatePermissionParams,
    headers=CreatePermissionHeader,
    resp=Response(HTTP_200=CreatePermissionResponse, HTTP_403=None),
    tags=[TAG],
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

    permission: PermissionSchema = permissions_service.create(
        title=body.title, description=body.description, http_method=body.http_method, url=body.url,
    )

    return CreatePermissionResponse(id=permission.id, message=f'Разрешение {body.title} создано.',)


@bp.route('', methods=['PUT'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL: 'PUT'})
@spec.validate(
    body=UpdatePermissionParams,
    headers=UpdatePermissionHeader,
    resp=Response(HTTP_200=UpdatePermissionResponse, HTTP_404=UpdatePermissionError, HTTP_403=None),
    tags=[TAG],
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
        id=body.id, title=body.title, description=body.description, http_method=body.http_method, url=body.url,
    )

    return UpdatePermissionResponse(__root__=permission)


@bp.route('', methods=['DELETE'])
@token_extractor
@access_exception_handler
@grpc_access_required({URL: 'DELETE'})
@spec.validate(
    body=DeletePermissionParams,
    headers=DeletePermissionHeader,
    resp=Response(HTTP_200=DeletePermissionResponse, HTTP_403=None),
    tags=[TAG],
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
