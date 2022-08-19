import uuid

from pydantic import BaseModel, Field

from ...base import AuthorizationHeader


class RoleRetrievePermissionBodyParams(BaseModel):
    """Схема body-параметров удаления ограничения у роли
    ---
    """
    role_id: uuid.UUID = Field(title='Идентификатор пользователя, которому назначается разрешение')
    permission_id: uuid.UUID = Field(title='Идентификаторы ограничений')


class RoleRetrievePermissionResponse(BaseModel):
    """Схема ответа удаления ограничения у роли
    ---
    """
    message: str = Field(title='Сообщение ответа')


class RoleRetrievePermissionHeader(AuthorizationHeader):
    """Схема заголовков удаления ограничения у роли
    ---
    """
    pass
