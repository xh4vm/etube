from .base import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, Integer, String, Date
from werkzeug.security import generate_password_hash, check_password_hash


class UserRole(BaseModel):
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    role_id = Column(ForeignKey('roles.id'), primary_key=True)


class RolePermission(BaseModel):
    role_id = Column(ForeignKey('users.id'), primary_key=True)
    permission_id = Column(ForeignKey('permissions.id'), primary_key=True)


class User(BaseModel):
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    roles = relationship('Role', secondary=UserRole)

    def __repr__(self):
        return f'<User {self.login}>'

    @staticmethod
    def encrypt_password(password: str) -> str:
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    @staticmethod
    def check_password(pwhash: str, password: str) -> bool:
        return check_password_hash(pwhash, password)


class Role(BaseModel):
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(4096))
    permissions = relationship('Permission', secondary=RolePermission)

    def __repr__(self):
        return f'<Role {self.title}>'


class Permission(BaseModel):
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(4096))
    http_method = Column(String(10))
    url = Column(String(255))

    def __repr__(self):
        return f'<Permission {self.title}>'


class SignInHistory(BaseModel):
    user_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('users.id'))
    user = relationship('User')
    device = Column(String(255))
    browser = Column(String(255))
