from pydantic import BaseModel, EmailStr, Field
from ..base import UserAgentHeader, JWT


class SignUpBodyParams(BaseModel):
    """Схема body-параметров регистрации пользователя
    ---
    """
    login: str = Field(title='Логин пользователя')
    email: EmailStr = Field(title='Почта пользователя')
    password: str = Field(title='Пароль пользователя')


class SignUpResponse(JWT):
    """Схема ответа регистрации пользователя
    ---
    """
    pass


class SignUpHeader(UserAgentHeader):
    """Схема заголовков регистрации пользователя
    ---
    """
    pass
