"""
Сервис получения списка разрешений пользователя.

"""
from api.errors.manager.permissions import PermissionsError
from api.model.models import Permission
from api.schema.base import Permission as PermissionSchema
from api.utils.decorators import traced

from .base import BaseService


class PermissionsService(BaseService):
    error = PermissionsError
    model = Permission
    schema = PermissionSchema
    map = PermissionSchema

    def get(self, **kwargs) -> schema:
        keys_values = [f'{key}::{value}' for key, value in kwargs]
        storage_key: str = f'{self.model.__tablename__}::get::{"::".join(keys_values)}'
        perm = self.storage_svc.get(key=storage_key)

        if perm is not None:
            return self.schema(**perm)

        result = None
        if (perm := self.model.query.filter_by(**kwargs).first()) is not None:
            perm = self.schema(
                title=perm.title, description=perm.description, http_method=perm.http_method, url=perm.url,
            )
            result = perm.dict()

        self.storage_svc.set(key=storage_key, data=result)
        return perm

    @traced('permission::all')
    def all(self) -> schema:
        storage_key: str = f'{self.model.__tablename__}::all'
        perms = self.storage_svc.get(key=storage_key)

        if perms is not None:
            return [self.schema(**perm) for perm in perms]

        perms = [
            self.schema(title=perm.title, description=perm.description, http_method=perm.http_method, url=perm.url)
            for perm in self.model.query.all()
        ]

        self.storage_svc.set(key=storage_key, data=[perm.dict() for perm in perms])
        return perms
