import uuid
from pydantic import BaseModel, Field

from ...base import AuthorizationHeader, JWT, BaseError


class CreatePermissionBodyParams(BaseModel):
    """Схема body-параметров создания ограничения
    ---
    """
    title: str = Field(title='Название ограничения')


class CreatePermissionResponse(BaseModel):
    """Схема ответа создания ограничения
    ---
    """
    id: uuid.UUID = Field(title='Идентификатор ограничения')


class CreatePermissionHeader(AuthorizationHeader):
    """Схема заголовков создания ограничения
    ---
    """
    pass
