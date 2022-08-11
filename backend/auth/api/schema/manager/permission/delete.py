from pydantic import BaseModel, Field
from ...base import AuthorizationHeader, JWT, BaseError


class DeletePermissionBodyParams(BaseModel):
    """Схема body-параметров удаления ограничения
    ---
    """
    permission_id: int = Field(title='Идентификатор ограничения')


class DeletePermissionResponse(BaseModel):
    """Схема ответа удаления ограничения
    ---
    """
    pass


class DeletePermissionHeader(AuthorizationHeader):
    """Схема заголовков удаления ограничения
    ---
    """
    pass
