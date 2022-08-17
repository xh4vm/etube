from pydantic import BaseModel
from ..base import AuthorizationHeader


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
