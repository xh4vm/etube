from uuid import UUID

from pydantic import BaseModel, Field

from .base import Permission
from ...base import AuthorizationHeader


class UpdatePermissionParams(BaseModel):
    """Схема body-параметров обновления ограничения
    ---
    """
    id: UUID = Field(title='Идентификатор ограничения')
    title: str = Field(title='Название ограничения')
    description: str = Field(title='Подробное описание ограничения')
    http_method: str = Field(title='HTTP метод ограничения')
    url: str = Field(title='URL ограничения')


class UpdatePermissionResponse(BaseModel):
    """Схема ответа обновления ограничения
    ---
    """
    __root__: Permission = Field(title='Результат изменения ограничение')


class UpdatePermissionError(BaseModel):
    """Схема ответа обновления ограничения
    ---
    """
    message: Permission = Field(title='Сообщение об ошибке')


class UpdatePermissionHeader(AuthorizationHeader):
    """Схема заголовков обновления ограничения
    ---
    """
    pass
