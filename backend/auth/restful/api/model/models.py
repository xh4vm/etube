import uuid
from typing import Any

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .base import BaseModel, db


class UserRole(BaseModel):
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)


class RolePermission(BaseModel):
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False)


class User(BaseModel):
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    roles = relationship('Role', secondary='join(Role, UserRole, Role.id == UserRole.role_id)', viewonly=True)

    def __repr__(self):
        return f'<User {self.login}>'

    def __init__(self, id: uuid, login: str, password: str, email: str) -> None:
        self.id = id
        self.login = login
        self.password = self.encrypt_password(password)
        #TODO: mixin mail validator
        self.email = email

    @property
    def permissions(self) -> set:
        roles = self.roles
        return set([permission for role in roles for permission in role.permissions])

    @property
    def roles_names(self) -> list[str]:
        return [role.title for role in self.roles]

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

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    os = Column(String(255))
    device = Column(String(255))
    browser = Column(String(255))

    user = relationship('User')
