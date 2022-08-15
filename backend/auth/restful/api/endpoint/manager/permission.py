import uuid
from flask import Blueprint
from flask_pydantic_spec import Response

from ...app import spec
from ...schema.manager.permission.get import GetPermissionParams, GetPermissionHeader, GetPermissionResponse
from ...schema.manager.permission.create import CreatePermissionParams, CreatePermissionHeader, CreatePermissionResponse
from ...schema.manager.permission.update import UpdatePermissionParams, UpdatePermissionHeader, UpdatePermissionResponse
from ...schema.manager.permission.delete import DeletePermissionParams, DeletePermissionHeader, DeletePermissionResponse
from ...schema.manager.permission.base import Permission as validator
from ...utils.decorators import json_response, unpack_models

from ...model.models import User, Permission
from ...model.base import db


bp = Blueprint('permission', __name__, url_prefix='/permission')
TAG = 'Manager'

@bp.route('', methods=['GET'])
@spec.validate(
    query=GetPermissionParams,
    headers=GetPermissionHeader,
    resp=Response(HTTP_200=GetPermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def get_permissions(query: GetPermissionParams, headers: GetPermissionHeader) -> GetPermissionResponse:
    """ Получение списка ограничений конкретной роли.
    """
    user = User.query.filter_by(id=query.user_id).first()
    if not user:
        return GetPermissionResponse(
            permissions=[],
            message=f'Пользователь {query.user_id} не существует.',
        )

    response = [
        validator(
            id=p.id,
            title=p.title,
            description=p.description,
            http_method=p.http_method,
            url=p.url,
        )
        for p in user.permissions
    ]

    return GetPermissionResponse(
        permissions=response,
        message=f'Разрешения пользователя {query.user_id}.',
    )


@bp.route('', methods=['POST'])
@spec.validate(
    query=CreatePermissionParams,
    headers=CreatePermissionHeader,
    resp=Response(HTTP_200=CreatePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def create_permission(query: CreatePermissionParams, headers: CreatePermissionHeader) -> CreatePermissionResponse:
    """ Создание ограничения.
    """
    id = uuid.uuid4()
    permission = Permission.query.filter_by(title=query.title).first()
    if permission:
        return CreatePermissionResponse(
            id=permission.id,
            message=f'Разрешение {query.title} уже существует.',
        )
    permission = Permission(
        **validator(
            id=id,
            title=query.title,
            description=query.description,
            http_method=query.http_method,
            url=query.url,
        ).dict()
    )
    db.session.add(permission)
    db.session.commit()

    return CreatePermissionResponse(
        id=id,
        message=f'Разрешение {query.title} создано.',
    )


@bp.route('', methods=['PUT'])
@spec.validate(
    query=UpdatePermissionParams,
    headers=UpdatePermissionHeader,
    resp=Response(HTTP_200=UpdatePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def update_permission(query: UpdatePermissionParams, headers: UpdatePermissionHeader) -> UpdatePermissionResponse:
    """ Обновление ограничения.
    """
    permission = Permission.query.filter_by(id=query.permission_id).first()
    if not permission:
        return UpdatePermissionResponse(message=f'Разрешение {query.permission_id} не существует.')

    validated_permission = validator(
        id=query.permission_id,
        title=query.title,
        description=query.description,
        http_method=query.http_method,
        url=query.url,
    )

    permission.title=validated_permission.title
    permission.description=validated_permission.description
    permission.http_method=validated_permission.http_method
    permission.url=validated_permission.url

    db.session.commit()

    return UpdatePermissionResponse(message=f'Разрешение {query.permission_id} обновлено.')


@bp.route('', methods=['DELETE'])
@spec.validate(
    query=DeletePermissionParams,
    headers=DeletePermissionHeader,
    resp=Response(HTTP_200=DeletePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def delete_permission(query: DeletePermissionParams, headers: DeletePermissionHeader) -> DeletePermissionResponse:
    """ Удаление ограничения.
    """
    Permission.query.filter_by(id=query.permission_id).delete()
    db.session.commit()

    return DeletePermissionResponse(message=f'Разрешение {query.permission_id} удалено.')
