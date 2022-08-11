import uuid
from pydantic import BaseModel, Field


class Permission(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор ограничения')
    title: str = Field(title='Название ограничения')
