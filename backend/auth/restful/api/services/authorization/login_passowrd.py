from http import HTTPStatus

from api.errors.action.sign_in import SignInActionError
from api.model.models import User
from api.schema.base import User as UserSchema
from api.utils.system import json_abort

from .base import BaseAuthService


class LoginPasswordAuthService(BaseAuthService):
    def authorization(self, login: str, password: str) -> User:
        user = User.query.filter_by(login=login).first()

        if user is None or not user.check_password(password):
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, SignInActionError.NOT_VALID_AUTH_DATA)

        roles_with_permissions = user.roles_with_permissions

        return UserSchema(
            id=user.id,
            login=user.login,
            email=user.email,
            roles=roles_with_permissions.get('roles'),
            permissions=roles_with_permissions.get('permissions'),
        )
