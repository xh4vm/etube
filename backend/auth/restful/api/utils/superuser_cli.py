import click
from flask import Blueprint
from werkzeug.security import generate_password_hash

from .superuser import SuperUser

bp = Blueprint('superuser', __name__)

@bp.cli.command('create')
@click.argument('login')
@click.argument('email')
@click.argument('password')
def create(login, email, password):
    super_user = SuperUser()
    super_user.create_role()
    super_user.set_permissions()
    super_user.login = login
    super_user.email = email
    super_user.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    super_user.create_user()
    super_user.set_role()
    super_user.conn.close()
