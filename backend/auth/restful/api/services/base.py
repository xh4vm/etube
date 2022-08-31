import uuid
from abc import ABC, abstractmethod, abstractproperty
from http import HTTPStatus

from pydantic.main import ModelMetaclass

from jaeger_telemetry.tracer import tracer

from ..errors.base import BaseError
from ..model.base import BaseModel, db
from ..utils.system import json_abort
from .storage.base import BaseStorage


class BaseService(ABC):
    @abstractproperty
    def schema(self) -> ModelMetaclass:
        """Схема данных"""

    @abstractproperty
    def map(self) -> ModelMetaclass:
        """Схема данных в бд"""

    @abstractproperty
    def model(self) -> BaseModel:
        """Схема данных в бд"""

    @abstractproperty
    def error(self) -> BaseError:
        """Класс ошибок"""

    def __init__(self, storage_svc: BaseStorage) -> None:
        self.storage_svc = storage_svc

    @abstractmethod
    @tracer.start_as_current_span('service-getter')
    def get(self, **kwargs) -> ModelMetaclass:
        """Получение экземпляра"""

    @tracer.start_as_current_span('service-exist-checker')
    def exists(self, **kwargs) -> bool:
        storage_key = f'{self.model.__tablename__}::exists::{"::".join(kwargs.keys())}'
        is_exists = self.storage_svc.get(key=storage_key)

        if is_exists is not None:
            return is_exists

        if set(kwargs.values()) == {None}:
            return False

        query = self.model.query

        query = query.filter_by(**kwargs)

        result = query.first() is not None
        self.storage_svc.set(key=storage_key, data=result)
        return result

    @tracer.start_as_current_span('service-creator')
    def create(self, **kwargs) -> str:
        map_data = self.map(**kwargs)

        elem = self.model(**map_data.dict())
        elem.insert_and_commit()

        return elem.id

    @tracer.start_as_current_span('service-updater')
    def update(self, id: str, **kwargs) -> ModelMetaclass:
        map_data = self.map(id=id, **kwargs)
        self.model.query.filter_by(id=id).update(map_data.dict())
        db.session.commit()

        return map_data

    @tracer.start_as_current_span('service-deleter')
    def delete(self, id: uuid) -> None:
        elem = self.model.query.get(id)
        if not elem:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)

        db.session.delete(elem)
        db.session.commit()
