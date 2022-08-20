from uuid import UUID

from pydantic import BaseModel, Field

from ...base import AuthorizationHeader, User


class UpdateUserBodyParams(BaseModel):
    """Схема body-параметров обновления пользователя
    ---
    """
    id: UUID = Field(title='Идентификатор пользователя')
    login: str = Field(title='Название пользователя')
    email: str = Field(title='Email пользователя')
    password: str = Field(title='Пароль пользователя')


class UpdateUserResponse(BaseModel):
    """Схема ответа обновления пользователя
    ---
    """
    __root__: User = Field(title='Результат изменения пользователя')


class UpdateUserHeader(AuthorizationHeader):
    """Схема заголовков обновления пользователя
    ---
    """
    pass
