from uuid import UUID

from pydantic import BaseModel, Field

from ...base import AuthorizationHeader, Role


class GetRoleQueryParams(BaseModel):
    """Схема body-параметров получения ролей
    ---
    """
    user_id: UUID = Field(title='Идентификатор пользователя, которому назначается роль')


class GetRoleResponse(BaseModel):
    """Схема ответа получения ролей
    ---
    """
    roles: list[Role] = Field(title='Список ролей')


class GetRoleHeader(AuthorizationHeader):
    """Схема заголовков получения ролей
    ---
    """
    pass
