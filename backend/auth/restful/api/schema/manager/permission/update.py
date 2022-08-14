from typing import Literal
from pydantic import BaseModel, Field

from ...base import AuthorizationHeader
from .base import Permission, PermissionAction


class UpdatePermissionBodyParams(BaseModel):
    """Схема body-параметров обновления ограничения
    ---
    """
    permission_id: int = Field(title='Идентификатор ограничения')
    title: str = Field(title='Название ограничения')
    description: str = Field(title='Подробное описание ограничения')
    http_method: str = Field(title='HTTP метод ограничения')
    url: str = Field(title='URL ограничения')
    action: Literal[PermissionAction.ACCESS, PermissionAction.DENY] = Field(
        title='Action ограничения', 
        example=PermissionAction.ACCESS
    )


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
