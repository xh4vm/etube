"""
Ошибки пользователя.

"""
from .base import BaseError


class UserSocialError(BaseError):
    NOT_EXISTS = 'Пользователь внешнего сервиса не существует.'
    ALREADY_EXISTS = 'Пользователь внешнего сервиса уже существует.'
