from pydantic import BaseModel, Field
from ..base import UserAgentHeader, JWT, BaseError


class SignInBodyParams(BaseModel):
    """Схема body-параметров авторизации пользователя
    ---
    """
    login: str = Field(title='Login')
    password: str = Field(title='Password')


class SignInResponse(JWT):
    """Схема ответа авторизации пользователя
    ---
    """
    pass


class SignInHeader(UserAgentHeader):
    """Схема заголовков авторизации пользователя
    ---
    """
    pass
