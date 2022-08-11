import uuid
from pydantic import BaseModel, Field

from ...base import AuthorizationHeader, JWT, BaseError
from .base import Permission


class UpdatePermissionBodyParams(BaseModel):
    """Схема body-параметров обновления ограничения
    ---
    """
    permission_id: int = Field(title='Идентификатор ограничения')
    title: str = Field(title='Название ограничения')


class UpdatePermissionResponse(BaseModel):
    """Схема ответа обновления ограничения
    ---
    """
    __root__: Permission = Field(title='Результат изменения ограничение')


class UpdatePermissionHeader(AuthorizationHeader):
    """Схема заголовков обновления ограничения
    ---
    """
    pass
