import uuid
from pydantic import BaseModel, EmailStr, Field

from ..role.base import Role


class User(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор роли')
    login: str = Field(title='Логин пользователя')
    email: EmailStr = Field(title='Email пользователя')
    roles: list[Role] = Field(title='Список ролей')
