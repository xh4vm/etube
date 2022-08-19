from http import HTTPStatus

from api.schema.base import User as UserSchema, UserMap
from api.model.models import User

from .base import BaseService
from ..errors.user import UserError

from ..utils.system import json_abort


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
        
        if (user := self.model.query.filter_by(**kwargs).first()) is None:
            json_abort(HTTPStatus.NOT_FOUND, self.error.NOT_EXISTS)

        roles_with_permissions = user.roles_with_permissions

        user = self.schema(
            id=user.id, 
            login=user.login, 
            email=user.email, 
            roles=roles_with_permissions.get('roles'),
            permissions=roles_with_permissions.get('permissions')
        )
    
        self.storage_svc.set(key=storage_key, data=user.dict())
        return user
