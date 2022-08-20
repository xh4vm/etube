from pydantic import BaseModel, Field

from ..base import JWT, UserAgentHeader


class SignInBodyParams(BaseModel):
    """Схема body-параметров авторизации пользователя
    ---
    """

    login: str = Field(title='Логин пользователя')
    password: str = Field(title='Пароль пользователя')


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
