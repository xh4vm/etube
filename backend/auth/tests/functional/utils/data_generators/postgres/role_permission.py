from ...fake_models.role_permission import FakeRolePermission
from .base import BasePostgresDataGenerator


class RolePermissionDataGenerator(BasePostgresDataGenerator):
    table = 'role_permissions'
    fake_model = FakeRolePermission
