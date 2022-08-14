import uuid
from pydantic import BaseModel, Field
from ...base import AuthorizationHeader


class UserSetRoleBodyParams(BaseModel):
    """Схема body-параметров назначения ограничения пользователю
    ---
    """
    user_id: uuid.UUID = Field(title='Идентификатор пользователя, которому назначается роль')
    role_ids: list[uuid.UUID] = Field(title='Идентификаторы ролей')


class UserSetRoleResponse(BaseModel):
    """Схема ответа назначения роли пользователю
    ---
    """
    pass


class UserSetRoleHeader(AuthorizationHeader):
    """Схема заголовков назначения роли пользователю
    ---
    """
    pass
