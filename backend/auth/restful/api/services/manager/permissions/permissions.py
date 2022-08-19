"""
Сервис получения списка разрешений пользователя.

"""
import uuid
from http import HTTPStatus
from typing import Union

from api.errors.manager.permissions import PermissionsError
from api.errors.user import UserError
from api.model.base import db
from api.model.models import Permission, User
from api.utils.system import json_abort

from ....schema.base import Permission as validator
from .base import BasePermissionsService


class PermissionsService(BasePermissionsService):

    def permissions_list(self, user_id: str) -> list:
        # Получение списка разрешений пользователя.
        user = User.query.get(user_id)
        if not user:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, UserError.NOT_EXISTS)

        return [
            validator(
                id=p.id,
                title=p.title,
                description=p.description,
                http_method=p.http_method,
                url=p.url,
            )
            for p in user.permissions
        ]

    def create(self, title: str, description: str, http_method: str, url: str) -> uuid:
        # Создание разрешения.
        if Permission.query.filter_by(title=title).first():
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, PermissionsError.ALREADY_EXISTS)
        permission = Permission(
            **validator(
                title=title,
                description=description,
                http_method=http_method,
                url=url,
            ).dict()
        )
        permission.insert_and_commit()

        return permission.id

    def update(self, id: str, title: str, description: str, http_method: str, url: str) -> validator:
        # Обновление разрешения.
        permission = PermissionsService.check_existence(id)
        validated_permission = validator(
            id=id,
            title=title,
            description=description,
            http_method=http_method,
            url=url,
        )
        permission.title = validated_permission.title
        permission.description = validated_permission.description
        permission.http_method = validated_permission.http_method
        permission.url = validated_permission.url

        db.session.commit()

        return validated_permission

    def delete(self, permission_id: str) -> None:
        permission = PermissionsService.check_existence(permission_id)
        db.session.delete(permission)
        db.session.commit()

    @staticmethod
    def check_existence(permission_id: str) -> Union[None, Permission]:
        permission = Permission.query.get(permission_id)
        if not permission:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, PermissionsError.NOT_EXISTS)

        return permission
