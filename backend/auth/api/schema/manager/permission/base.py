import uuid
import enum
from typing import Literal
from pydantic import BaseModel, Field


class PermissionAction(str, enum.Enum):
    ACCESS = 'ACCESS'
    DENY = 'DENY'

class Permission(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор ограничения')
    title: str = Field(title='Название ограничения')
    description: str = Field(title='Подробное описание ограничения')
    http_method: str = Field(title='HTTP метод ограничения')
    url: str = Field(title='URL ограничения')
    action: Literal[PermissionAction.ACCESS, PermissionAction.DENY] = Field(
        title='Action ограничения', 
        example=PermissionAction.ACCESS
    )
