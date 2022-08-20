from uuid import UUID

from pydantic import BaseModel, Field

from ...base import AuthorizationHeader, Role


class UpdateRoleBodyParams(BaseModel):
    """Схема body-параметров обновления ограничения
    ---
    """

    id: UUID = Field(title='Идентификатор роли')
    title: str = Field(title='Название роли')
    description: str = Field(title='Описание роли')


class UpdateRoleResponse(BaseModel):
    """Схема ответа обновления ограничения
    ---
    """

    __root__: Role = Field(title='Результат изменения роли')


class UpdateRoleHeader(AuthorizationHeader):
    """Схема заголовков обновления ограничения
    ---
    """

    pass
