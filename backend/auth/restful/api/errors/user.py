"""
Ошибки пользователя.

"""
from .base import BaseError

class UserError(BaseError):
    NOT_EXISTS = 'Пользователь не существует.'
    ALREADY_EXISTS = 'Пользователь уже существует.'
