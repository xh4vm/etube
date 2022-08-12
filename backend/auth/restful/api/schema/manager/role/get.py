from pydantic import BaseModel, Field
from ...base import AuthorizationHeader
from .base import Role


class GetRoleQueryParams(BaseModel):
    """Схема body-параметров получения ролей
    ---
    """
    user_id: int = Field(title='Идентификатор пользователя, которому назначается роль')


class GetRoleResponse(BaseModel):
    """Схема ответа получения ролей
    ---
    """
    __root___: list[Role] = Field(title='Список ролей')


class GetRoleHeader(AuthorizationHeader):
    """Схема заголовков получения ролей
    ---
    """
    pass