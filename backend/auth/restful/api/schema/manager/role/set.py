import uuid
from pydantic import BaseModel, Field
from ...base import AuthorizationHeader


class RoleSetPermissionBodyParams(BaseModel):
    """Схема body-параметров назначения ограничения роли
    ---
    """
    role_id: uuid.UUID = Field(title='Идентификатор роли, которой назначается разрешение')
    permission_ids: list[uuid.UUID] = Field(title='Идентификаторы ограничений')


class RoleSetPermissionResponse(BaseModel):
    """Схема ответа назначения ограничения роли
    ---
    """
    pass


class RoleSetPermissionHeader(AuthorizationHeader):
    """Схема заголовков назначения ограничения роли
    ---
    """
    pass
