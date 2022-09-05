import hashlib
import uuid
from datetime import date, datetime, timedelta

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .base import CONFIG, BaseModel, db


class UserRole(BaseModel):
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.users.id', ondelete='CASCADE'), nullable=False
    )
    role_id = Column(
        UUID(as_uuid=True), ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.roles.id', ondelete='CASCADE'), nullable=False
    )


class RolePermission(BaseModel):
    role_id = Column(
        UUID(as_uuid=True), ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.roles.id', ondelete='CASCADE'), nullable=False
    )
    permission_id = Column(
        UUID(as_uuid=True), ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.permissions.id', ondelete='CASCADE'), nullable=False
    )


class User(BaseModel):
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    roles = relationship(
        'Role', secondary='join(Role, UserRole, Role.id == UserRole.role_id)', viewonly=True, backref=backref('users')
    )

    def __repr__(self):
        return f'<User {self.login}>'

    def __init__(self, id: uuid, login: str, password: str, email: str) -> None:
        self.id = id
        self.login = login
        self.password = self.encrypt_password(password)
        # TODO: mixin mail validator
        self.email = email

    @property
    def permissions(self) -> set:
        roles = self.roles
        return set([permission for role in roles for permission in role.permissions])

    @property
    def roles_with_permissions(self) -> list[str]:
        result = {'roles': set(), 'permissions': {}}

        _roles_with_permissions = (
            Role.query.with_entities(Role.title, Permission.url, Permission.http_method)
            .join(Permission, Role.permissions)
            .join(User, Role.users)
            .filter(User.id == self.id)
            .all()
        )

        for entity in _roles_with_permissions:
            result['roles'].add(entity.title)

            md5_hashed_url = hashlib.md5(entity.url.encode(), usedforsecurity=False).hexdigest()

            if md5_hashed_url in result['permissions'].keys():
                result['permissions'][md5_hashed_url].append(entity.http_method)
            else:
                result['permissions'][md5_hashed_url] = [entity.http_method]

        return result

    @staticmethod
    def encrypt_password(password: str) -> str:
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Role(BaseModel):
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(4096))

    permissions = relationship(
        'Permission',
        secondary='join(Permission, RolePermission, Permission.id == RolePermission.permission_id)',
        secondaryjoin='Role.id == RolePermission.role_id',
        viewonly=True,
    )

    @property
    def permissions_names(self) -> list[str]:
        return [perm.title for perm in self.permissions]

    def __repr__(self):
        return f'<Role {self.title}>'


class Permission(BaseModel):

    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(4096))
    http_method = Column(String(10))
    url = Column(String(4096))

    def __repr__(self):
        return f'<ACE {self.title}>'


class SignInHistory(BaseModel):
    __tablename__ = 'sign_in_history'
    __table_args__ = (
        UniqueConstraint('id', 'created_at'),
        {'schema': CONFIG.DB.SCHEMA_NAME, 'postgresql_partition_by': 'RANGE (created_at)', },
    )

    id: int = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, primary_key=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.users.id', ondelete='CASCADE'), nullable=False
    )
    os = Column(String(255))
    device = Column(String(255))
    browser = Column(String(255))

    user = relationship('User')

    @classmethod
    def create_partition(self, target_date: date) -> None:
        # Создание партиции таблицы входов пользователей.
        name = f'{CONFIG.DB.SCHEMA_NAME}.user_sign_in_{target_date.strftime("%m_%Y")}'

        start = datetime.strptime(
            f'{target_date.replace(day=1)}T{datetime.min.time()}', '%Y-%m-%dT%H:%M:%S'
        ).astimezone()

        end = datetime.strptime(
            f'{(target_date.replace(day=28) + timedelta(days=4)).replace(day=1)}T{datetime.min.time()}',
            '%Y-%m-%dT%H:%M:%S',
        ).astimezone()

        query = (
            'CREATE TABLE IF NOT EXISTS %(name)s '
            'PARTITION OF %(schema)s.sign_in_history '
            'FOR VALUES FROM ("%(start)s") TO ("%(end)s");'
        )

        params = {
            'name': name,
            'schema': CONFIG.DB.SCHEMA_NAME,
            'start': start,
            'end': end,
        }
        db.session.execute(query % params)
        db.session.commit()


class UserSocial(BaseModel):
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.users.id', ondelete='CASCADE'), nullable=False
    )
    user_service_id = Column(String(255))
    email = Column(String(255))
    service_name = Column(String(255))

    user = relationship('User')
