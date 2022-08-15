from ...fake_models.user import FakeUser
from .base import BasePostgresDataGenerator


class UserDataGenerator(BasePostgresDataGenerator):
    table = 'users'
    fake_model = FakeUser
