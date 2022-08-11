from flask import Blueprint


bp = Blueprint('manager_role', __name__, url_prefix='/manager/role')


@bp.route('', methods=['GET'])
def get_roles():
    pass


@bp.route('', methods=['POST'])
def create_role():
    pass


@bp.route('', methods=['PUT'])
def update_role():
    pass


@bp.route('', methods=['DELETE'])
def delete_role():
    pass
