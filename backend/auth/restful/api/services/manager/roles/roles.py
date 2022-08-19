"""
Сервис ролей пользователя.

"""
import uuid
from http import HTTPStatus

from api.errors.manager.roles import RolesError
from api.errors.user import UserError
from api.model.base import db
from api.model.models import Permission, Role, RolePermission, User
from api.utils.system import json_abort

from ....schema.base import Role as validator
from ..permissions.permissions import PermissionsService


class RolesService:

    def roles_list(self, user_id: uuid) -> list:
        # Получение списка ролей пользователя.
        user = User.query.get(user_id)
        if not user:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, UserError.NOT_EXISTS)

        return [
            validator(
                id=role.id,
                title=role.title,
                description=role.description,
                permissions=[p.title for p in role.permissions],
            )
            for role in user.roles
        ]

    def create(self, title: str, description: str) -> uuid:
        # Создание роли.
        if Role.query.filter_by(title=title).first():
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.ALREADY_EXISTS)
        role = Role(
            **validator(
                title=title,
                description=description,
                permissions=[],
            ).dict()
        )
        role.insert_and_commit()

        return role.id

    def update(self, id: str, title: str, description: str) -> validator:
        # Обновление роли.
        role = Role.query.get(id)
        if not role:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)

        validated_role = validator(
            id=id,
            title=title,
            description=description,
            permissions=[p.title for p in role.permissions],
        )

        role.title = validated_role.title
        role.description = validated_role.description

        db.session.commit()

        return validated_role

    def delete(self, role_id: uuid) -> None:
        # Удаление роли.
        role = Role.query.get(role_id)
        if not role:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)

        db.session.delete(role)
        db.session.commit()

    def set_permission(self, role_id: uuid, permissions: list) -> list:
        # Добавление разрешения роли.
        role = Role.query.get(role_id)
        if not role:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)
        for permission_id in permissions:
            PermissionsService.check_existence(permission_id)
            role_permission = RolePermission(
                role_id=role_id,
                permission_id=permission_id,
            )
            role_permission.insert_and_commit()

        return [p.title for p in role.permissions]

    def retrieve_permission(self, role_id: uuid, permissions: list) -> list:
        # Удаление разрешения роли.
        role = Role.query.get(role_id)
        if not role:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_EXISTS)
        for permission_id in permissions:
            PermissionsService.check_existence(permission_id)
            role_permission = RolePermission.query.filter_by(
                role_id=role_id,
                permission_id=permission_id,
            ).first()
            if not role_permission:
                json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_BELONG)
            db.session.delete(role_permission)
            db.session.commit()

        return [p.title for p in role.permissions]
