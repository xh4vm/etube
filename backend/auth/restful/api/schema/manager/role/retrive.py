import uuid
from pydantic import BaseModel, Field
from ...base import AuthorizationHeader


class RoleRetrivePermissionBodyParams(BaseModel):
    """Схема body-параметров удаления ограничения у роли
    ---
    """
    role_id: uuid.UUID = Field(title='Идентификатор пользователя, которому назначается разрешение')
    permission_ids: list[uuid.UUID] = Field(title='Идентификаторы ограничений')


class RoleRetrivePermissionResponse(BaseModel):
    """Схема ответа удаления ограничения у роли
    ---
    """
    pass


class RoleRetrivePermissionHeader(AuthorizationHeader):
    """Схема заголовков удаления ограничения у роли
    ---
    """
    pass
