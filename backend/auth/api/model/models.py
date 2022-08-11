from .base import BaseModel, db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(BaseModel):
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    roles = relationship('UserRole')
    permissions = relationship('UserPermission')

    def __repr__(self):
        return f'<User {self.login}>'


class Role(BaseModel):
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Role {self.title}>'


class UserRole(BaseModel):
    user_id = db.Column(ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(ForeignKey('roles.id'), primary_key=True)


class Permission(BaseModel):
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    expiration_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Permission {self.title}>'


class UserPermission(BaseModel):
    user_id = db.Column(ForeignKey('users.id'), primary_key=True)
    permission_id = db.Column(ForeignKey('permissions.id'), primary_key=True)


class SignInHistory(BaseModel):
    user_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), ForeignKey('users.id'))
    user = relationship('User')
    user_agent = db.Column(db.String)
