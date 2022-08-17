from typing import Any
import uuid
from flask import Flask, Blueprint
from core.config import CONFIG, SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_jwt_extended import JWTManager
from flask_pydantic_spec import FlaskPydanticSpec

from .model.base import db

from .containers.storage import StorageResource, RedisStorageResource
from .containers.sign_in import ServiceContainer as SignInServiceContainer
from .containers.sign_up import ServiceContainer as SignUpServiceContainer
from .containers.token import ServiceContainer as TokenServiceContainer
from .containers.permissions import ServiceContainer as PermissionsServiceContainer



migrate = Migrate()
redis_client = FlaskRedis()
jwt = JWTManager()
spec = FlaskPydanticSpec("flask", title="Auth API", version=CONFIG.APP.API_VERSION, path=CONFIG.APP.SWAGGER_PATH)


def register_di_containers():
    redis_resource = StorageResource(RedisStorageResource)

    SignInServiceContainer(storage_svc=redis_resource)
    SignUpServiceContainer()
    TokenServiceContainer(storage_svc=redis_resource)
    PermissionsServiceContainer()


def register_blueprints(app):
    root_bp = Blueprint('root', __name__, url_prefix=f'/api/{CONFIG.APP.API_VERSION}/auth')

    from .endpoint.action import bp as action_bp
    root_bp.register_blueprint(action_bp)

    from .endpoint.token import bp as token_bp
    root_bp.register_blueprint(token_bp)

    from .endpoint.manager import bp as manager_bp
    root_bp.register_blueprint(manager_bp)

    app.register_blueprint(root_bp)


@jwt.additional_claims_loader
def add_claims(user) -> dict[str, Any]:
    return {
        'login': user.login,
        'email': user.email,
        # 'roles': user.roles,
        # 'permissions': user.permissions
    }

@jwt.user_identity_loader
def add_identity(user) -> uuid.UUID:
    return user.id


def create_app(config_class=CONFIG.APP):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    jwt.init_app(app)

    register_blueprints(app)
    register_di_containers()
    spec.register(app)

    app.app_context().push()

    return app