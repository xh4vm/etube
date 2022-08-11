from flask import Blueprint


bp = Blueprint('permission', __name__, url_prefix='/permission')


@bp.route('', methods=['GET'])
def get_permissions():
    pass


@bp.route('', methods=['POST'])
def create_permission():
    pass


@bp.route('', methods=['PUT'])
def update_permission():
    pass


@bp.route('', methods=['DELETE'])
def delete_permission():
    pass
