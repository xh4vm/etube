from api.schema.base import AuthorizationHeader, User
from pydantic import BaseModel, Field


class GetUserResponse(BaseModel):
    """Схема ответа получения ролей
    ---
    """

    users: list[User] = Field(title='Список пользователй')


class GetUserHeader(AuthorizationHeader):
    """Схема заголовков получения ролей
    ---
    """

    pass
