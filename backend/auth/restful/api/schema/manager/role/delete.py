from uuid import UUID

from pydantic import BaseModel, Field

from ...base import AuthorizationHeader


class DeleteRoleBodyParams(BaseModel):
    """Схема body-параметров удаления роли
    ---
    """

    id: UUID = Field(title='Идентификатор роли')


class DeleteRoleResponse(BaseModel):
    """Схема ответа удаления роли
    ---
    """

    message: str = Field(title='Сообщение ответа')


class DeleteRoleHeader(AuthorizationHeader):
    """Схема заголовков удаления роли
    ---
    """

    pass
