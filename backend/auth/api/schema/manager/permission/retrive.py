from pydantic import BaseModel, Field
from ...base import AuthorizationHeader, JWT, BaseError


class RetrivePermissionBodyParams(BaseModel):
    """Схема body-параметров удаления ограничения у пользователя
    ---
    """
    user_id: int = Field(title='Идентификатор пользователя, которому назначается разрешение')
    permission_id: int = Field(title='Идентификатор ограничения')


class RetrivePermissionResponse(BaseModel):
    """Схема ответа удаления ограничения у пользователя
    ---
    """
    pass


class RetrivePermissionHeader(AuthorizationHeader):
    """Схема заголовков удаления ограничения у пользователя
    ---
    """
    pass
