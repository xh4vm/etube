from pydantic import BaseModel, Field
from ...base import AuthorizationHeader


class DeleteRoleBodyParams(BaseModel):
    """Схема body-параметров удаления роли
    ---
    """
    role_id: int = Field(title='Идентификатор роли')


class DeleteRoleResponse(BaseModel):
    """Схема ответа удаления роли
    ---
    """
    pass


class DeleteRoleHeader(AuthorizationHeader):
    """Схема заголовков удаления роли
    ---
    """
    pass
