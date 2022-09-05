"""
Базовый сервис авторизации через сторонние сервисы.

Переопределяет метод авторизации:
сначала ведется поиск пользователя в таблице сервисов.
Если пользователь не найден, ведется поиск в таблице пользователей.
При необходимости создаются записи в таблице пользователей (с фейковыми логином и паролем)
и в таблице сервисов (со связью с таблицей пользователей).

"""

import uuid
from faker import Faker
from typing import Union

from api.model.models import User, UserSocial
from api.schema.base import User as UserSchema
from api.schema.base import UserSocialMap
from api.services.authorization.base import BaseAuthService

class BaseOAuth(BaseAuthService):

    def __init__(self):
        self.faker = Faker()

    def authorization(self, user_id: str) -> User:
        user = User.query.get(user_id)

        return UserSchema(
            id=user.id,
            login=user.login,
            email=user.email,
            roles=user.roles_with_permissions.get('roles'),
            permissions=user.roles_with_permissions.get('permissions'),
        )
