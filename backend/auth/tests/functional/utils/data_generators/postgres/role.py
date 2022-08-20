from ...fake_models.role import FakeRole
from .base import BasePostgresDataGenerator


class RoleDataGenerator(BasePostgresDataGenerator):
    table = 'roles'
    fake_model = FakeRole
