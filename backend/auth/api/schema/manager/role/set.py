from pydantic import BaseModel, Field
from ...base import AuthorizationHeader


class SetRoleBodyParams(BaseModel):
    """Схема body-параметров назначения ограничения пользователю
    ---
    """
    user_id: int = Field(title='Идентификатор пользователя, которому назначается роль')
    role_id: int = Field(title='Идентификатор роли')


class SetRoleResponse(BaseModel):
    """Схема ответа назначения роли пользователю
    ---
    """
    pass


class SetRoleHeader(AuthorizationHeader):
    """Схема заголовков назначения роли пользователю
    ---
    """
    pass
