import uuid
from pydantic import BaseModel, Field
from typing import Literal

from ...base import AuthorizationHeader
from .base import PermissionAction


class CreatePermissionBodyParams(BaseModel):
    """Схема body-параметров создания ограничения
    ---
    """
    title: str = Field(title='Название ограничения')
    description: str = Field(title='Подробное описание ограничения')
    http_method: str = Field(title='HTTP метод ограничения')
    url: str = Field(title='URL ограничения')
    action: Literal[PermissionAction.ACCESS, PermissionAction.DENY] = Field(
        title='Action ограничения', 
        example=PermissionAction.ACCESS
    )

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
