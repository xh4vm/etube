"""

Создание суперпользователя со всеми имеющимися разрешениями.

"""

import uuid
from datetime import datetime
from getpass import getpass

import psycopg2
from psycopg2.extras import execute_values
from pydantic import BaseSettings, Field
from werkzeug.security import generate_password_hash


class Settings(BaseSettings):
    user: str = Field('auth', env='AUTH_DB_USER')
    password: str = Field('123qwe', env='AUTH_DB_PASSWORD')
    host: str = Field('localhost', env='AUTH_DB_HOST')
    port: int = Field('5432', env='AUTH_DB_PORT')
    dbname: str = Field('auth_database', env='AUTH_DB_NAME')


class SuperUser:
    def __init__(self):
        self.user_id = str(uuid.uuid4())
        self.role_id = str(uuid.uuid4())
        self.login = None
        self.email = None
        self.password = None
        self.conn = psycopg2.connect(**Settings().dict())
        self.curs = self.conn.cursor()

    def set_user_data(self):
        # Данные пользователя, принмиаемые через терминал.
        self.login = input('Login: ')
        self.email = input('Email: ')
        password = getpass('Password: ')
        password2 = getpass('Password again: ')
        while password != password2:
            print('Пароли не совпадают.')
            password = getpass('Password: ')
            password2 = getpass('Password again: ')
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def executor(self, query: str, data: list):
        execute_values(self.curs, query, data)
        self.conn.commit()

    def create_role(self):
        # Создание роли админа.
        query = """
            INSERT INTO auth_etube.roles (id,title,description,created_at,updated_at)
            VALUES %s;
            """
        data = [(self.role_id, 'admin', '', datetime.utcnow(), datetime.utcnow())]
        self.executor(query, data)

    def set_permissions(self):
        # Назначение админу всех разрешений.
        self.curs.execute("""SELECT id FROM auth_etube.permissions;""")
        data = [
            (str(uuid.uuid4()), self.role_id, permission[0], datetime.utcnow(), datetime.utcnow(),)
            for permission in self.curs.fetchall()
        ]
        query = """
            INSERT INTO auth_etube.role_permissions (id,role_id,permission_id,created_at,updated_at)
            VALUES %s;
            """
        self.executor(query, data)

    def create_user(self):
        # Создание пользователя-админа.
        query = """
            INSERT INTO auth_etube.users (id,login,email,password,created_at,updated_at)
            VALUES %s;
            """
        data = [(self.user_id, self.login, self.email, self.password, datetime.utcnow(), datetime.utcnow())]
        self.executor(query, data)

    def set_role(self):
        # Назначение пользователю роли админа.
        query = """
            INSERT INTO auth_etube.user_roles (id,user_id,role_id,created_at,updated_at)
            VALUES %s;
            """
        data = [(str(uuid.uuid4()), self.user_id, self.role_id, datetime.utcnow(), datetime.utcnow())]
        self.executor(query, data)


if __name__ == '__main__':
    super_user = SuperUser()
    super_user.create_role()
    super_user.set_permissions()
    super_user.set_user_data()
    super_user.create_user()
    super_user.set_role()
    super_user.conn.close()
