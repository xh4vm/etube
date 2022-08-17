from flask import Flask, Blueprint
from core.config import CONFIG, INTERACTION_CONFIG
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_jwt_extended import JWTManager
from flask_pydantic_spec import FlaskPydanticSpec

from .model.base import db
from .utils.system import json_abort
from .services.token.base import BaseTokenService

from .containers.storage import StorageResource, RedisStorageResource
from .containers.sign_in import ServiceContainer as SignInServiceContainer
from .containers.sign_up import ServiceContainer as SignUpServiceContainer
from .containers.token import ServiceContainer as TokenServiceContainer
from .containers.logout import ServiceContainer as LogoutServiceContainer
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
    LogoutServiceContainer(storage_svc=redis_resource)


def register_jwt_handelers():
    jwt.expired_token_loader(BaseTokenService.expired_token_callback)
    jwt.token_in_blocklist_loader(BaseTokenService.token_in_blocklist_callback)
    jwt.invalid_token_loader(BaseTokenService.invalid_token_callback)
    jwt.revoked_token_loader(BaseTokenService.revoked_token_callback)
    jwt.unauthorized_loader(BaseTokenService.unauthorized_callback)
    jwt.token_verification_failed_loader(BaseTokenService.token_verification_failed_callback)


def register_blueprints(app):
    root_bp = Blueprint('root', __name__, url_prefix=f'/api/{CONFIG.APP.API_VERSION}/auth')

    from .endpoint.action import bp as action_bp
    root_bp.register_blueprint(action_bp)

    from .endpoint.token import bp as token_bp
    root_bp.register_blueprint(token_bp)

    from .endpoint.manager import bp as manager_bp
    root_bp.register_blueprint(manager_bp)

    app.register_blueprint(root_bp)


def create_app(config_classes=[CONFIG.APP, INTERACTION_CONFIG]):
    app = Flask(__name__)
    
    [app.config.from_object(config_class) for config_class in config_classes]

    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    jwt.init_app(app)

    register_blueprints(app)
    register_di_containers()
    register_jwt_handelers()
    spec.register(app)

    app.app_context().push()

    return app
