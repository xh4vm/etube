import uuid

from api.schema.base import User as UserSchema
from api.model.models import User
from .storage.base import BaseStorage


class UserService:

    def __init__(self, storage_svc: BaseStorage) -> None:
        self.storage_svc = storage_svc

    def get_by_id(self, id: uuid.UUID) -> UserSchema:
        user = self.storage_svc.get(key=f'user::get_by_id::{id}')
        
        if user is None:
            user = User.query.get(id)

            roles_with_permissions = user.roles_with_permissions

            user = UserSchema(
                id=user.id, 
                login=user.login, 
                email=user.email, 
                roles=roles_with_permissions.get('roles'),
                permissions=roles_with_permissions.get('permissions')
            ).dict()
        
        self.storage_svc.set(key=f'user::get_by_id::{id}', data=user)

        return UserSchema(**user)
