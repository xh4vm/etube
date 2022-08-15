from uuid import UUID

from pydantic import BaseModel, Field
from ...base import AuthorizationHeader
from .base import Permission


class GetPermissionParams(BaseModel):
    """Схема body-параметров получения ограничений
    ---
    """
    user_id: UUID = Field(title='Идентификатор пользователя, которому назначается разрешение')


class GetPermissionResponse(BaseModel):
    """Схема ответа получения ограничений
    ---
    """
    permissions: list[Permission] = Field(title='Список ограничений')
    message: str = Field(title='Сообщение ответа')


class GetPermissionHeader(AuthorizationHeader):
    """Схема заголовков получения ограничений
    ---
    """
    pass
