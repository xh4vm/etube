import uuid

from pydantic import BaseModel, Field

from ...base import AuthorizationHeader


class RoleSetPermissionBodyParams(BaseModel):
    """Схема body-параметров назначения ограничения роли
    ---
    """
    role_id: uuid.UUID = Field(title='Идентификатор роли, которой назначается разрешение')
    permission_id: uuid.UUID = Field(title='Идентификатор ограничения')


class RoleSetPermissionResponse(BaseModel):
    """Схема ответа назначения ограничения роли
    ---
    """
    message: str = Field(title='Сообщение ответа')


class RoleSetPermissionHeader(AuthorizationHeader):
    """Схема заголовков назначения ограничения роли
    ---
    """
    pass
