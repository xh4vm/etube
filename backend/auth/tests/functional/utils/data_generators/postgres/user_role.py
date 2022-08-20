from ...fake_models.user_role import FakeUserRole
from .base import BasePostgresDataGenerator


class UserRoleDataGenerator(BasePostgresDataGenerator):
    table = 'user_roles'
    fake_model = FakeUserRole
