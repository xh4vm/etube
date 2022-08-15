import uuid
from pydantic import BaseModel, Field

from ...base import AuthorizationHeader


class CreatePermissionParams(BaseModel):
    """Схема body-параметров создания ограничения
    ---
    """
    title: str = Field(title='Название ограничения')
    description: str = Field(title='Подробное описание ограничения')
    http_method: str = Field(title='HTTP метод ограничения')
    url: str = Field(title='URL ограничения')

class CreatePermissionResponse(BaseModel):
    """Схема ответа создания ограничения
    ---
    """
    id: uuid.UUID = Field(title='Идентификатор ограничения')
    message: str = Field(title='Сообщение ответа')


class CreatePermissionHeader(AuthorizationHeader):
    """Схема заголовков создания ограничения
    ---
    """
    pass
