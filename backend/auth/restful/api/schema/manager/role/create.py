import uuid

from pydantic import BaseModel, Field

from ...base import AuthorizationHeader


class CreateRoleBodyParams(BaseModel):
    """Схема body-параметров создания роли
    ---
    """
    title: str = Field(title='Название роли')
    description: str = Field(title='Описание роли')


class CreateRoleResponse(BaseModel):
    """Схема ответа создания роли
    ---
    """
    id: uuid.UUID = Field(title='Идентификатор роли')
    message: str = Field(title='Сообщение ответа')


class CreateRoleHeader(AuthorizationHeader):
    """Схема заголовков создания роли
    ---
    """
    pass
