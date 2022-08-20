from ...fake_models.permission import FakePermission
from .base import BasePostgresDataGenerator


class PermissionDataGenerator(BasePostgresDataGenerator):
    table = 'permissions'
    fake_model = FakePermission
