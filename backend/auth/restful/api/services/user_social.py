from http import HTTPStatus
from api.model.models import UserSocial
from api.schema.base import UserSocial as UserSocialSchema, UserSocialMap

from ..errors.user_social import UserSocialError
from ..utils.system import json_abort
from .base import BaseService


class UserSocialService(BaseService):
    error = UserSocialError
    model = UserSocial
    schema = UserSocialSchema
    map = UserSocialMap

    def get(self, **kwargs) -> schema:
        keys_values = [f'{key}::{value}' for key, value in kwargs.items()]
        storage_key: str = f'{self.model.__tablename__}::get::{"::".join(keys_values)}'
        user_social = self.storage_svc.get(key=storage_key)

        if user_social is not None:
            return self.schema(**user_social)

        result = None
        if (user_social := self.model.query.filter_by(**kwargs).first()) is not None:
            user_social = self.schema(
                id=user_social.id,
                user_id=user_social.user_id,
                user_service_id=user_social.user_service_id,
                email=user_social.email,
                service_name=user_social.service_name,
            )
            result = user_social.dict()

        self.storage_svc.set(key=storage_key, data=result)
        return user_social
