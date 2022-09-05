from pydantic import BaseModel, Field

from ..base import JWT, UserAgentHeader, IntegrityTokenHeader


class SignInBodyParams(BaseModel):
    """Схема body-параметров авторизации пользователя
    ---
    """

    login: str = Field(title='Логин пользователя')
    password: str = Field(title='Пароль пользователя')


class OAuthSignInBodyParams(BaseModel):
    """Схема body-параметров авторизации пользователя
    ---
    """

    user_service_id: str = Field(title='ID пользователя в стороннем сервисе')
    email: str = Field(title='Почта пользователя в стороннем сервисе')
    service_name: str = Field(title='Наименование сервиса для внешней авторизации')


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


class OAuthSignInHeader(IntegrityTokenHeader):
    """Схема заголовков авторизации пользователя через сторонний сервис
    ---
    """

    pass
