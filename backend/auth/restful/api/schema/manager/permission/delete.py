from uuid import UUID

from pydantic import BaseModel, Field

from ...base import AuthorizationHeader


class DeletePermissionParams(BaseModel):
    """Схема body-параметров удаления ограничения
    ---
    """

    id: UUID = Field(title='Идентификатор ограничения')


class DeletePermissionResponse(BaseModel):
    """Схема ответа удаления ограничения
    ---
    """

    message: str = Field(title='Сообщение ответа')


class DeletePermissionHeader(AuthorizationHeader):
    """Схема заголовков удаления ограничения
    ---
    """

    pass
