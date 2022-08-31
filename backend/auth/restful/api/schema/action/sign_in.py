from pydantic import BaseModel, Field

from ..base import JWT, UserAgentHeader


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


class OAuthSignInHeader(UserAgentHeader):
    """Схема заголовков авторизации пользователя через сторонний сервис
    ---
    """

    user_data_signature: str = Field(title='Подпись данных пользователя', alias='User-Data-Signature')
