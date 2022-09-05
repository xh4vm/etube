import hashlib
import hmac
import uuid
from http import HTTPStatus
from math import tan
from typing import Any, Generic, Optional, TypeVar

import orjson
from api.utils.system import json_abort
from faker import Faker
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.generics import GenericModel
from user_agents import parse

fake = Faker()


def get_new_id() -> str:
    return str(uuid.uuid4())


class AuthorizationHeader(BaseModel):
    """Схема заголовков JWT авторизации
    ---
    """

    token: str = Field(
        title='Authorization JWT токен', alias='X-Authorization-Token',
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
        example=(
            'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 '
            '(KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
        ),
    )

    @validator('user_agent')
    def load_user_agent(cls, user_agent: str):
        return parse(user_agent)


class IntegrityTokenHeader(UserAgentHeader):
    """Схема заголовков с подписью данных
    ---
    """

    integrety_token: str = Field(
        title='Заголовок токена целостности',
        alias='X-Integrity-Token',
        example='adcb671e8e24572464c31e8f9ffc5f638ab302a0b673f72554d3cff96a692740',
    )

    # TODO: plz smarter checker
    @validator('integrety_token')
    def load_integrety_token(cls, integrety_token: str):
        if len(integrety_token) == 64:
            return integrety_token

        json_abort(HTTPStatus.BAD_REQUEST, 'Сигнатура не найдена')


class JWT(BaseModel):
    """Схема JWT токенаов
    ---
    """

    access: str = Field(title='Кратковременный JWT токен', alias='access_token')
    refresh: str = Field(title='Долговременный JWT токен', alias='refresh_token')


class Paginator(BaseModel):

    page: int = Field(default=1, title='Номер текущей страницы')
    page_size: int = Field(default=50, title='Мощность выборки')


PTYPE = TypeVar('PTYPE', bound=BaseModel)


class Page(GenericModel, Generic[PTYPE]):
    """Схема пагинации
    ---
    """

    page: int = Field(default=1, title='Номер текущей страницы')
    page_size: int = Field(default=50, title='Мощность выборки')
    page_prev: Optional[int] = Field(default=None, title='Предыдущая страница')
    page_next: Optional[int] = Field(default=None, title='Следующая страница')
    total: int = Field(default=0, title='Всего записей')
    items: list[PTYPE] = Field(default=[], title='Список объектов')


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
    permissions: list[str] = Field(title='Список ограничений роли', default=[])


class RoleMap(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор роли', default_factory=get_new_id)
    title: str = Field(title='Название роли')
    description: str = Field(title='Описание роли')


class User(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор пользователя', default_factory=get_new_id)
    login: str = Field(title='Логин пользователя')
    email: EmailStr = Field(title='Email пользователя')
    roles: list[str] = Field(title='Список ролей', default=[])
    permissions: dict[str, list[str]] = Field(
        title='Список permissions: md5_hashed_url: list(http_methods)', default={}
    )

    def get_claims(self) -> dict[str, Any]:
        return {
            'login': self.login,
            'email': self.email,
            'roles': self.roles,
            'permissions': self.permissions,
        }


class UserMap(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор пользователя', default_factory=get_new_id)
    login: str = Field(title='Логин пользователя', default_factory=fake.user_name)
    password: str = Field(title='Пароль пользователя', default_factory=fake.password)
    email: EmailStr = Field(title='Email пользователя', default_factory=fake.email)


class UserSocial(BaseModel):
    user_service_id: str = Field(title='Идентификатор пользователя в соц сервисе')
    email: EmailStr = Field(title='Email пользователя')
    service_name: str = Field(title='Название сервиса')

    def sig(self, secret: str) -> str:
        packed_data = str(orjson.dumps(self.dict()))
        return hmac.new(bytes(secret, 'utf-8'), msg=bytes(packed_data, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

    def sig_check(self, secret: str, signature: str) -> bool:
        return signature == self.sig(secret)


class UserSocialMap(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор пользователя в таблице', default_factory=get_new_id)
    user_id: uuid.UUID = Field(title='Идентификатор пользователя приложения')
    user_service_id: str = Field(title='Идентификатор пользователя в стороннем сервисе')
    email: EmailStr = Field(title='Email пользователя')
    service_name: str = Field(title='Название сервиса')


class SignInRecordMap(BaseModel):
    id: uuid.UUID = Field(title='Идентификатор записи', default_factory=get_new_id)
    user_id: uuid.UUID = Field(title='Идентификатор пользователя')
    os: str = Field(title='Операционная система пользователя')
    device: str = Field(title='Устройство пользователя')
    browser: str = Field(title='Браузер пользователя')


class SignInRecord(BaseModel):
    os: str = Field(title='Операционная система пользователя')
    device: str = Field(title='Устройство пользователя')
    browser: str = Field(title='Браузер пользователя')
    created_at: str = Field(title='Дата успешной авторизации')


class CaptchaTask(BaseModel):
    message: str = Field(title='Текст задания', default='Вычислите тангенс угла')
    parameter: int = Field(title='Параметр задачи', default_factory=fake.random_int)
    answer: float = Field(title='Ответ задачи')

    def __init__(self, *args, **kwargs) -> None:
        kwargs['answer'] = kwargs.get('answer') or round(tan(int(kwargs['parameter']) + 1), 3)
        super().__init__(*args, **kwargs)

    def sig(self, secret: str) -> str:
        packed_data = str(orjson.dumps(self.dict()))
        return hmac.new(bytes(secret, 'utf-8'), msg=bytes(packed_data, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

    def sig_check(self, secret: str, signature: str) -> bool:
        return signature == self.sig(secret)
