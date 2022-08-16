from pydantic import BaseModel, Field

from ...base import AuthorizationHeader, Role


class UpdateRoleBodyParams(BaseModel):
    """Схема body-параметров обновления ограничения
    ---
    """
    role_id: int = Field(title='Идентификатор ограничения')
    title: str = Field(title='Название ограничения')


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
