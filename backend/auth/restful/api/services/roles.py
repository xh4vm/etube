"""
Сервис ролей пользователя.

"""
import uuid
from http import HTTPStatus

from api.errors.manager.roles import RolesError
from api.model.base import db
from api.model.models import Role, RolePermission
from api.schema.base import Role as RoleSchema
from api.schema.base import RoleMap
from api.utils.system import json_abort

from .base import BaseService


class RolesService(BaseService):
    error = RolesError
    model = Role
    schema = RoleSchema
    map = RoleMap

    def get(self, **kwargs) -> schema:
        keys_values = [f'{key}::{value}' for key, value in kwargs]
        storage_key: str = f'{self.model.__tablename__}::get::{"::".join(keys_values)}'
        role = self.storage_svc.get(key=storage_key)

        if role is not None:
            return self.schema(**role)

        if (role := self.model.query.filter_by(**kwargs).first()) is None:
            json_abort(HTTPStatus.NOT_FOUND, RolesError.NOT_EXISTS)

        role = self.schema(title=role.title, description=role.description,)

        self.storage_svc.set(key=storage_key, data=role.dict())
        return role

    def all(self) -> schema:
        storage_key: str = f'{self.model.__tablename__}::all'
        roles = self.storage_svc.get(key=storage_key)

        if roles is not None:
            return [self.schema(**role) for role in roles]

        roles = [self.schema(title=role.title, description=role.description,) for role in self.model.query.all()]

        self.storage_svc.set(key=storage_key, data=[role.dict() for role in roles])
        return roles

    def set_permission(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> None:
        # Добавление разрешения роли.
        RolePermission(id=uuid.uuid4(), role_id=role_id, permission_id=permission_id).insert_and_commit()

    def retrieve_permission(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> None:
        # Удаление разрешения роли.
        role_permission = RolePermission.query.filter_by(role_id=role_id, permission_id=permission_id,).first()

        if not role_permission:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, RolesError.NOT_BELONG)

        db.session.delete(role_permission)
        db.session.commit()
