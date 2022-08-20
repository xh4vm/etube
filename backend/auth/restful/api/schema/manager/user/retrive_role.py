import uuid
from pydantic import BaseModel, Field
from ...base import AuthorizationHeader


class UserRetriveRoleBodyParams(BaseModel):
    """Схема body-параметров удаления роли у пользователя
    ---
    """
    user_id: uuid.UUID = Field(title='Идентификатор пользователя, которому назначается роль')
    role_id: uuid.UUID = Field(title='Идентификатор роли')


class UserRetriveRoleResponse(BaseModel):
    """Схема ответа удаления роли у пользователя
    ---
    """
    pass


class UserRetriveRoleHeader(AuthorizationHeader):
    """Схема заголовков удаления роли у пользователя
    ---
    """
    pass
