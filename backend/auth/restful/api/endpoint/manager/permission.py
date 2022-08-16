import uuid
from typing import Union

from flask import Blueprint, abort
from flask_pydantic_spec import Response

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
@json_response
def get_permissions(
        query: GetPermissionParams,
        headers: GetPermissionHeader,
) -> Union[GetPermissionResponse, GetPermissionError]:
    """ Получение списка ограничений конкретной роли.
    """
    user = User.query.get_or_404(query.user_id)
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
    )


@bp.route('', methods=['POST'])
@spec.validate(
    body=CreatePermissionParams,
    headers=CreatePermissionHeader,
    resp=Response(HTTP_200=CreatePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def create_permission(body: CreatePermissionParams, headers: CreatePermissionHeader) -> CreatePermissionResponse:
    """ Создание ограничения.
    """
    id = uuid.uuid4()
    permission = Permission.query.filter_by(title=body.title).first()
    if permission:
        return CreatePermissionResponse(
            id='',
            message=f'Разрешение {body.title} уже существует.',
        )
    permission = Permission(
        **validator(
            id=id,
            title=body.title,
            description=body.description,
            http_method=body.http_method,
            url=body.url,
        ).dict()
    )
    db.session.add(permission)
    db.session.commit()

    return CreatePermissionResponse(
        id=id,
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
@json_response
def update_permission(
        body: UpdatePermissionParams,
        headers: UpdatePermissionHeader,
) -> Union[UpdatePermissionResponse, UpdatePermissionError]:
    """ Обновление ограничения.
    """
    permission = Permission.query.get_or_404(body.id)
    validated_permission = validator(
        id=body.id,
        title=body.title,
        description=body.description,
        http_method=body.http_method,
        url=body.url,
    )

    permission.title = validated_permission.title
    permission.description = validated_permission.description
    permission.http_method = validated_permission.http_method
    permission.url = validated_permission.url

    db.session.commit()

    return UpdatePermissionResponse(__root__=validated_permission)


@bp.route('', methods=['DELETE'])
@spec.validate(
    body=DeletePermissionParams,
    headers=DeletePermissionHeader,
    resp=Response(HTTP_200=DeletePermissionResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def delete_permission(body: DeletePermissionParams, headers: DeletePermissionHeader) -> DeletePermissionResponse:
    """ Удаление ограничения.
    """
    Permission.query.filter_by(id=body.id).delete()
    db.session.commit()

    return DeletePermissionResponse(message=f'Разрешение {body.id} удалено.')
