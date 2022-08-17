"""
Сервис регистрации пользователя.

"""
import uuid
from http import HTTPStatus

from api.errors.action.sign_up import SignUpActionError
from api.model.models import User
from api.schema.base import User as validator
from api.utils.system import json_abort

from .base import BaseSignUpService


class FormSignUpService(BaseSignUpService):

    def registration(self, login: str, email: str, password: str) -> uuid:
        if User.query.filter_by(email=email).first():
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, SignUpActionError.ALREADY_EXISTS)

        id = uuid.uuid4()
        user_data = validator(
                id=id,
                login=login,
                email=email,
                roles=[],
            ).dict()
        user_data['password'] = password
        user_data.pop('roles')

        user = User(**user_data)
        user.insert_and_commit()

        return user.id
