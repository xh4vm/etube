from http import HTTPStatus
import backoff
from core.config import CONFIG, INTERACTION_CONFIG, BACKOFF_CONFIG, auth_logger
from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_pydantic_spec import FlaskPydanticSpec
from flask_redis import FlaskRedis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .containers.logout import ServiceContainer as LogoutServiceContainer
from .containers.permissions import \
    ServiceContainer as PermissionsServiceContainer
from .containers.roles import ServiceContainer as RolesServiceContainer
from .containers.oauth import YandexAuthContainer, VKAuthContainer
from .containers.sign_in import ServiceContainer as SignInServiceContainer
from .containers.sign_up import ServiceContainer as SignUpServiceContainer
from .containers.storage import RedisStorageResource, StorageResource
from .containers.token import ServiceContainer as TokenServiceContainer
from .containers.user import ServiceContainer as UserServiceContainer
from .model.base import db
from .services.storage.redis import BaseStorage, RedisStorage
from .services.token.handler import TokenHandlerService
from .utils.error_handlers import many_requests
from .utils.rate_limit import check_bots

migrate = Migrate()
redis_client = FlaskRedis()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
spec = FlaskPydanticSpec('flask', title='Auth API', version=CONFIG.APP.API_VERSION, path=CONFIG.APP.SWAGGER_PATH)


def register_di_containers():
    redis_resource = StorageResource(RedisStorageResource)

    SignInServiceContainer(storage_svc=redis_resource)
    SignUpServiceContainer(storage_svc=redis_resource)
    TokenServiceContainer(storage_svc=redis_resource)
    UserServiceContainer(storage_svc=redis_resource)
    RolesServiceContainer(storage_svc=redis_resource)
    PermissionsServiceContainer(storage_svc=redis_resource)
    LogoutServiceContainer(storage_svc=redis_resource)
    YandexAuthContainer(storage_svc=redis_resource)
    VKAuthContainer(storage_svc=redis_resource)


def register_jwt_handelers(storage_service: BaseStorage):
    token_handelr_service = TokenHandlerService(storage_service)

    jwt.expired_token_loader(token_handelr_service.expired_token_callback)
    jwt.token_in_blocklist_loader(token_handelr_service.token_in_blocklist_callback)
    jwt.invalid_token_loader(token_handelr_service.invalid_token_callback)
    jwt.revoked_token_loader(token_handelr_service.revoked_token_callback)
    jwt.unauthorized_loader(token_handelr_service.unauthorized_callback)
    jwt.token_verification_failed_loader(token_handelr_service.token_verification_failed_callback)


def register_error_handlers(app: Flask):
    app.register_error_handler(HTTPStatus.TOO_MANY_REQUESTS, many_requests)


def register_blueprints(app: Flask):
    root_bp = Blueprint('root', __name__, url_prefix=f'/api/{CONFIG.APP.API_VERSION}/auth')
    limiter.limit('3/second')(root_bp)
    limiter.limit('1/hour', exempt_when=lambda: not check_bots(), override_defaults=False)(root_bp)

    from .endpoint.v1.action import bp as action_bp

    root_bp.register_blueprint(action_bp)
    limiter.limit('15/minute')(action_bp)

    from .endpoint.v1.token import bp as token_bp

    root_bp.register_blueprint(token_bp)
    limiter.exempt(token_bp)

    from .endpoint.v1.manager import bp as manager_bp

    root_bp.register_blueprint(manager_bp)
    limiter.exempt(manager_bp)

    from .endpoint.v1.manager.db import bp as db_bp

    root_bp.register_blueprint(db_bp)

    from .utils.superuser_cli import bp as superuser_bp

    app.register_blueprint(superuser_bp)

    app.register_blueprint(root_bp)


def create_db_schema(db, schema_name=CONFIG.DB.SCHEMA_NAME):
    db.engine.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name};')


@backoff.on_exception(**BACKOFF_CONFIG, logger=auth_logger)
def create_app(config_classes=[CONFIG.APP, INTERACTION_CONFIG]):
    app = Flask(__name__)

    [app.config.from_object(config_class) for config_class in config_classes]

    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    register_blueprints(app)
    register_error_handlers(app)
    register_di_containers()

    redis_storage = RedisStorage(redis=redis_client)
    register_jwt_handelers(storage_service=redis_storage)

    spec.register(app)
    app.app_context().push()

    create_db_schema(db)

    return app
