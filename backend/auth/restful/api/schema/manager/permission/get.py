from pydantic import BaseModel, Field
from ...base import AuthorizationHeader
from .base import Permission


class GetPermissionQueryParams(BaseModel):
    """Схема body-параметров получения ограничений
    ---
    """
    user_id: int = Field(title='Идентификатор пользователя, которому назначается разрешение')


class GetPermissionResponse(BaseModel):
    """Схема ответа получения ограничений
    ---
    """
    __root__: list[Permission] = Field(title='Список ограничений')


class GetPermissionHeader(AuthorizationHeader):
    """Схема заголовков получения ограничений
    ---
    """
    pass
