from pydantic import BaseModel, Field
from ..base import AuthorizationHeader, JWT, BaseError


class LogoutBodyParams(BaseModel):
    """Схема body-параметров выхода пользователя
    ---
    """
    access_token: str = Field(title='Кратковременный jwt токен')


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
