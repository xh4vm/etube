from pydantic import BaseModel, Field
from ..base import AuthorizationHeader, JWT


class RefreshTokenBodyParams(BaseModel):
    """Схема body-параметров обновления токена
    ---
    """
    access_token: str = Field(title='Кратковременный jwt токен')


class RefreshTokenResponse(JWT):
    """Схема ответа обновления токена
    ---
    """
    pass


class RefreshTokenHeader(AuthorizationHeader):
    """Схема заголовков обновления токена
    ---
    """
    pass
