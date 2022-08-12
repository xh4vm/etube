from pydantic import BaseModel, Field
from ...base import AuthorizationHeader


class RetriveRoleBodyParams(BaseModel):
    """Схема body-параметров удаления роли у пользователя
    ---
    """
    user_id: int = Field(title='Идентификатор пользователя, которому назначается роль')
    role_id: int = Field(title='Идентификатор роли')


class RetriveRoleResponse(BaseModel):
    """Схема ответа удаления роли у пользователя
    ---
    """
    pass


class RetriveRoleHeader(AuthorizationHeader):
    """Схема заголовков удаления роли у пользователя
    ---
    """
    pass
