"""
Сервис получения списка разрешений пользователя.

"""
from http import HTTPStatus

from api.errors.manager.permissions import PermissionsError
from api.model.models import Permission
from api.schema.base import Permission as PermissionSchema
from api.utils.system import json_abort

from jaeger_telemetry.tracer import tracer

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

        if (perm := self.model.query.filter_by(**kwargs).first()) is None:
            json_abort(HTTPStatus.NOT_FOUND, self.error.NOT_EXISTS)

        perm = self.schema(title=perm.title, description=perm.description, http_method=perm.http_method, url=perm.url,)

        self.storage_svc.set(key=storage_key, data=perm.dict())
        return perm

    @tracer.start_as_current_span('permission::all')
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
