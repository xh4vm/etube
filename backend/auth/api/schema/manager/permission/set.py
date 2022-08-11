from pydantic import BaseModel, Field
from ...base import AuthorizationHeader, JWT, BaseError


class SetPermissionBodyParams(BaseModel):
    """Схема body-параметров назначения ограничения пользователю
    ---
    """
    user_id: int = Field(title='Идентификатор пользователя, которому назначается разрешение')
    permission_id: int = Field(title='Идентификатор ограничения')


class SetPermissionResponse(BaseModel):
    """Схема ответа назначения ограничения пользователю
    ---
    """
    pass


class SetPermissionHeader(AuthorizationHeader):
    """Схема заголовков назначения ограничения пользователю
    ---
    """
    pass
