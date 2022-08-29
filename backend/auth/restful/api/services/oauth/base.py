"""
Базовый сервис авторизации через сторонние сервисы.

Переопределяет метод авторизации:
сначала ведется поиск пользователя в таблице сервисов.
Если пользователь не найден, ведется поиск в таблице пользователей.
При необходимости создаются записи в таблице пользователей (с фейковыми логином и паролем)
и в таблице сервисов (со связью с таблицей пользователей).

"""
import hashlib
import hmac
import uuid
from typing import Union

from api.model.models import User, UserSocial
from api.schema.base import User as UserSchema
from api.schema.base import UserMap, UserSocialMap
from api.services.authorization.base import BaseAuthService
from core.config import OAUTH_CONFIG

class BaseOAuth(BaseAuthService):

    def get_user_social(self, user_service_id: str, service_name: str) -> Union[UserSocial, None]:
        return UserSocial.query.filter_by(user_service_id=user_service_id, service_name=service_name).first()

    def authorization(self, user_id: str) -> User:
        user = User.query.get(user_id)
        roles_with_permissions = user.roles_with_permissions

        return UserSchema(
            id=user.id,
            login=user.login,
            email=user.email,
            roles=roles_with_permissions.get('roles'),
            permissions=roles_with_permissions.get('permissions'),
        )

    def create_social_user(self, user_id: uuid, user_service_id: str, email: str, service_name: str) -> UserSocial:
        social_map_data = UserSocialMap(
            user_id=user_id,
            user_service_id=user_service_id,
            email=email,
            service_name=service_name,
        )
        user_social = UserSocial(**social_map_data.dict())
        user_social.insert_and_commit()

        return user_social

    def create_hash(self, user_service_id: str, email: str) -> str:
        message = '{}{}'.format(user_service_id, email)
        signature = hmac.new(bytes(OAUTH_CONFIG.SECRET, 'utf-8'), msg=bytes(message, 'utf-8'),
                             digestmod=hashlib.sha256).hexdigest()

        return signature

    def check_hash(self, user_service_id: str, email: str, hash: str) -> bool:
        return hash == self.create_hash(user_service_id, email)
