from typing import Optional
import uuid
from http import HTTPStatus

from api.utils.decorators import traced

from api.model.base import db
from api.model.models import User, UserRole
from api.schema.base import User as UserSchema, fake
from api.schema.base import UserMap

from ..errors.user import UserError
from ..utils.system import json_abort
from .base import BaseService


class UserService(BaseService):
    error = UserError
    model = User
    schema = UserSchema
    map = UserMap

    def get(self, **kwargs) -> schema:
        keys_values = [f'{key}::{value}' for key, value in kwargs]
        storage_key: str = f'{self.model.__tablename__}::get::{"::".join(keys_values)}'
        user = self.storage_svc.get(key=storage_key)

        if user is not None:
            return self.schema(**user)

        result = None
        if (user := self.model.query.filter_by(**kwargs).first()) is not None:
            roles_with_permissions = user.roles_with_permissions

            user = self.schema(
                id=user.id,
                login=user.login,
                email=user.email,
                roles=roles_with_permissions.get('roles'),
                permissions=roles_with_permissions.get('permissions'),
            )
            result = user.dict()

        self.storage_svc.set(key=storage_key, data=result)
        return user

    @traced('user::all')
    def all(self) -> schema:
        storage_key: str = f'{self.model.__tablename__}::all'
        users = self.storage_svc.get(key=storage_key)

        if users is not None:
            return [self.schema(**user) for user in users]

        users = []
        for user in self.model.query.all():
            roles_with_permissions = user.roles_with_permissions

            users.append(
                self.schema(
                    id=user.id,
                    login=user.login,
                    email=user.email,
                    roles=roles_with_permissions.get('roles'),
                    permissions=roles_with_permissions.get('permissions'),
                )
            )

        self.storage_svc.set(key=storage_key, data=[user.dict() for user in users])
        return users

    @traced('user::update')
    def update(self, id: str, login: str, email: str, password: str) -> UserMap:
        map_data = UserMap(id=id, login=login, email=email, password=User.encrypt_password(password))
        return super().update(**map_data.dict())

    @traced('user::set_role')
    def set_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> None:
        UserRole(id=uuid.uuid4(), user_id=user_id, role_id=role_id).insert_and_commit()

    @traced('user::retrieve_role')
    def retrieve_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> None:
        user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id,).first()

        if not user_role:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, UserError.NOT_BELONG)

        db.session.delete(user_role)
        db.session.commit()
