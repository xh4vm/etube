"""
Ошибки CRUD ролей пользователя.

"""
from ..base import BaseError


class RolesError(BaseError):
    ALREADY_EXISTS = 'Роль уже существует.'
    NOT_EXISTS = 'Роль не существует.'
    NOT_BELONG = 'Разрешение не принадлежит роли.'
