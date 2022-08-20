import uuid

from pydantic import BaseModel, EmailStr, Field

from ..base import UserAgentHeader


class SignUpBodyParams(BaseModel):
    """Схема body-параметров регистрации пользователя
    ---
    """

    login: str = Field(title='Логин пользователя')
    email: EmailStr = Field(title='Почта пользователя')
    password: str = Field(title='Пароль пользователя')


class SignUpResponse(BaseModel):
    """Схема ответа регистрации пользователя
    ---
    """

    id: uuid.UUID = Field(title='Идентификатор пользователя')
    message: str = Field(title='Сообщение ответа')


class SignUpHeader(UserAgentHeader):
    """Схема заголовков регистрации пользователя
    ---
    """

    pass
