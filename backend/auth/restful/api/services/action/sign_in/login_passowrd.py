from http import HTTPStatus

from api.model.base import BaseModel
from api.model.models import User

from api.errors.action.sign_in import SignInActionError
from api.utils.system import json_abort

from .base import BaseSignInService


class LoginPasswordSignInService(BaseSignInService):

    def authorization(self, login: str, password: str) -> BaseModel:
        user = (User
            .query
            .filter_by(login=login)
            .first())
        
        if user is None or \
            not user.check_password(password):
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, SignInActionError.NOT_VALID_AUTH_DATA)
        
        return user
