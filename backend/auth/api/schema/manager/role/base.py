import uuid
from pydantic import BaseModel, Field


class Role(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор роли')
    title: str = Field(title='Название роли')
