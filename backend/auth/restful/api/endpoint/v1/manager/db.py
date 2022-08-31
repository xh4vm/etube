from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.model.models import SignInHistory
from api.schema.manager.db.create import DbBodyParams, DbResponse
from api.utils.decorators import json_response, unpack_models


bp = Blueprint('db', __name__, url_prefix='/db')
TAG = 'DB'


@bp.route('', methods=['POST'])
@spec.validate(
    body=DbBodyParams,
    resp=Response(HTTP_200=DbResponse),
    tags=[TAG],
)
@unpack_models
@json_response
def create_table(
    body: DbBodyParams,
):
    """ Создании партиции
    ---
    """

    target_date = body.target_date
    SignInHistory.create_partition(target_date)

    return DbResponse(message='Таблица создана.')
