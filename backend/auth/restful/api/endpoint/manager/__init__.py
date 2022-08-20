from flask import Blueprint

bp = Blueprint('manager', __name__, url_prefix='/manager')


from .user import bp as user_bp
bp.register_blueprint(user_bp)

from .role import bp as role_bp
bp.register_blueprint(role_bp)

from .permission import bp as permission_bp
bp.register_blueprint(permission_bp)
