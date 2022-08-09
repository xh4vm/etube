from flask import Flask, Blueprint
from core.config import Config
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_jwt_extended import JWTManager

from .model.base import db


migrate = Migrate()
redis_client = FlaskRedis()
jwt = JWTManager()


def register_blueprints(app):
    root_bp = Blueprint('root', __name__, url_prefix='/auth')

    from .route.auth import bp as auth_bp
    root_bp.register_blueprint(auth_bp)

    from .route.role_manager import bp as role_manager_bp
    root_bp.register_blueprint(role_manager_bp)
    
    from .route.grant import bp as grant_bp
    root_bp.register_blueprint(grant_bp)

    app.register_blueprint(root_bp)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    jwt.init_app(app)

    register_blueprints(app)

    app.app_context().push()

    return app
