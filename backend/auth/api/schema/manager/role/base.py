import uuid
from pydantic import BaseModel, Field

from ..permission.base import Permission


class Role(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор роли')
    title: str = Field(title='Название роли')
    permissions: list[Permission] = Field(title='Список ограничений роли')
