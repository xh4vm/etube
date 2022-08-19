"""
Ошибки CRUD разрешений пользователя.

"""
from ..base import BaseError


class PermissionsError(BaseError):
    ALREADY_EXISTS = 'Разрешение уже существует.'
    NOT_EXISTS = 'Разрешение не существует.'
