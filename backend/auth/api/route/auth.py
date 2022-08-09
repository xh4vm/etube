from flask import Blueprint


bp = Blueprint('action', __name__, url_prefix='/action')


@bp.route('/sign_in', methods=['POST'])
def sign_in():
    pass


@bp.route('/sign_up', methods=['POST'])
def sign_up():
    pass


@bp.route('/logout', methods=['POST'])
def logout():
    pass


@bp.route('/refresh', methods=['POST'])
def sign_in():
    pass
