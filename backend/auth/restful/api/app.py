from flask import Flask, Blueprint
from core.config import CONFIG
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_jwt_extended import JWTManager
from flask_pydantic_spec import FlaskPydanticSpec

from .model.base import db

migrate = Migrate()
redis_client = FlaskRedis()
jwt = JWTManager()
spec = FlaskPydanticSpec("flask", title="Auth API", version=CONFIG.APP.API_VERSION, path=CONFIG.APP.SWAGGER_PATH)


def register_blueprints(app):
    root_bp = Blueprint('root', __name__, url_prefix='/auth')

    from .endpoint.action import bp as action_bp
    root_bp.register_blueprint(action_bp)

    from .endpoint.token import bp as token_bp
    root_bp.register_blueprint(token_bp)

    from .endpoint.manager import bp as manager_bp
    root_bp.register_blueprint(manager_bp)

    app.register_blueprint(root_bp)


def create_app(config_class=CONFIG):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    jwt.init_app(app)

    register_blueprints(app)
    spec.register(app)

    app.app_context().push()

    return app