from pydantic import BaseModel, Field
from ..base import UserAgentHeader, JWT, BaseError


class SignUpBodyParams(BaseModel):
    """Схема body-параметров регистрации пользователя
    ---
    """
    login: str = Field(title='Login')
    password: str = Field(title='Password')


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
