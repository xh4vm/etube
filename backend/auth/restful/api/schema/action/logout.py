from pydantic import BaseModel, Field

from ..base import AuthorizationHeader


class LogoutBodyRequest(BaseModel):
    """Схема запроса выхода пользователя
    ---
    """

    refresh_token: str = Field(title='Рефреш токен пользователя')


class LogoutResponse(BaseModel):
    """Схема ответа выхода пользователя
    ---
    """

    pass


class LogoutHeader(AuthorizationHeader):
    """Схема заголовков выхода пользователя
    ---
    """

    pass
