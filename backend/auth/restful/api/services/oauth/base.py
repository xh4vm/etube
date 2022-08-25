"""
Базовый сервис авторизации через сторонние сервисы.

Переопределяет метод авторизации:
сначала ведется поиск пользователя в таблице сервисов.
Если пользователь не найден, ведется поиск в таблице пользователей
При необходимости создаются записи в таблице пользователей (с фейковыми логином и паролем)
и в таблице сервисов (со связью с таблицей пользователей).

"""
import uuid

from faker import Faker

from api.model.models import User, UserSocial
from api.schema.base import User as UserSchema
from api.schema.base import UserMap, UserSocialMap
from api.services.authorization.base import BaseAuthService
from api.services.user import UserService


class BaseOAuthAuthorization(BaseAuthService):

    def authorization(self, user_service_id: str, email: str, service_name: str, user_service: UserService) -> User:
        user_social = UserSocial.query.filter_by(user_service_id=user_service_id, service_name=service_name).first()

        if user_social is None:
            user = User.query.filter_by(email=email).first()
            if user is None:
                user_id = user_service.create(
                    login=Faker().user_name(),
                    email=email,
                    password=Faker().password(length=12),
                )
            else:
                user_id = user.id

            user_social = self.create_social_user(
                user_id=user_id,
                user_service_id=user_service_id,
                email=email,
                service_name=service_name,
            )

        user = User.query.get(user_social.user_id)
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
