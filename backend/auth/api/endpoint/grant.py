from flask import Blueprint


bp = Blueprint('grant', __name__, url_prefix='/grant')


@bp.route('', methods=['POST'])
def grant_permission():
    pass