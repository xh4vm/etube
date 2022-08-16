from uuid import UUID

from pydantic import BaseModel, Field
from ...base import AuthorizationHeader, Permission


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


class GetPermissionError(BaseModel):
    """Схема ответа обновления ограничения
    ---
    """
    message: str = Field(title='Сообщение об ошибке')


class GetPermissionHeader(AuthorizationHeader):
    """Схема заголовков получения ограничений
    ---
    """
    pass
