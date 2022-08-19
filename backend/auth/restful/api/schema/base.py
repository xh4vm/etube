from typing import Any
import uuid
from pydantic import BaseModel, EmailStr, Field, validator
from user_agents import parse


def get_new_id() -> str:
    return str(uuid.uuid4())


class AuthorizationHeader(BaseModel):
    """Схема заголовков JWT авторизации 
    ---
    """

    token: str = Field(
        title='Authorization JWT токен', 
        alias='X-Authorization-Token',
    )

    @validator('token')
    def load_user_agent(cls, token: str):
        if not token.startswith('Bearer '):
            raise ValueError('Bearer authorization токен не найден')
        return token

    def get_token(self) -> str:
        return self.token.split()[1]


class UserAgentHeader(BaseModel):
    """Схема заголовков получения / обработки юзерагента пользователя  
    ---
    """

    user_agent: str = Field(
        title='Заголовок User-Agent', 
        alias='User-Agent', 
        example='Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
    )

    @validator('user_agent')
    def load_user_agent(cls, user_agent: str):
        return parse(user_agent)


class JWT(BaseModel):
    """Схема JWT токенаов  
    ---
    """
    
    access: str = Field(title='Кратковременный JWT токен', alias='access_token')
    refresh: str = Field(title='Долговременный JWT токен', alias='refresh_token')


class BaseError(BaseModel):
    """Базования схема ошибки  
    ---
    """
    
    message: str = Field(title='Сообщение об ошибке', default='Error')


class Permission(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор ограничения', default_factory=get_new_id)
    title: str = Field(title='Название ограничения')
    description: str = Field(title='Подробное описание ограничения')
    http_method: str = Field(title='HTTP метод ограничения')
    url: str = Field(title='URL ограничения')


class Role(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор роли', default_factory=get_new_id)
    title: str = Field(title='Название роли')
    description: str = Field(title='Описание роли')
    permissions: list[str] = Field(title='Список ограничений роли')


class User(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор роли', default_factory=get_new_id)
    login: str = Field(title='Логин пользователя')
    email: EmailStr = Field(title='Email пользователя')
    roles: list[str] = Field(title='Список ролей', default=[])
    permissions: dict[str, list[str]] = Field(title='Список permissions: md5_hashed_url: list(http_methods)', default={})

    def get_claims(self) -> dict[str, Any]:
        return {
            'login': self.login,
            'email': self.email,
            'roles': self.roles,
            'permissions': self.permissions,
        }


class UserMap(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор роли', default_factory=get_new_id)
    login: str = Field(title='Логин пользователя')
    password: str = Field(title='Пароль пользователя')
    email: EmailStr = Field(title='Email пользователя')


class SignInRecord(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор записи', default_factory=get_new_id)
    user_id: uuid.UUID = Field(title='Идентификатор пользователя')
    os: str = Field(title='Операционная система пользователя')
    device: str = Field(title='Устройство пользователя')
    browser: str = Field(title='Браузер пользователя')
