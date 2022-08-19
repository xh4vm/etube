import uuid

from typing import Optional

from api.schema.base import User as UserSchema, UserMap
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

    def exists(self, login: Optional[str] = None, email: Optional[str] = None) -> bool:
        is_exists = self.storage_svc.get(key=f'user::exists::{login}::{email}')
                
        if is_exists is not None:
            return is_exists

        if login is None and email is None:
            return False

        query = User.query

        if login is not None:
            query = query.filter_by(login=login)

        if email is not None:
            query = query.filter_by(email=email)

        result = query.first() is not None
        self.storage_svc.set(key=f'user::exists::{login}::{email}', data=result)
        return result

    def create(self, login: str, email: str, password: str) -> str:
        user_data = UserMap(login=login, email=email, password=password)

        user = User(id=user_data.id, login=user_data.login, password=user_data.password, email=user_data.email)
        user.insert_and_commit()

        return user.id
