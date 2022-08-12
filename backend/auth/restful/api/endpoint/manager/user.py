import uuid
from flask import Blueprint
from flask_pydantic_spec import Response, Request

from ...app import spec
from ...schema.manager.user.set_role import UserSetRoleBodyParams, UserSetRoleHeader, UserSetRoleResponse
from ...schema.manager.user.retrive_role import UserRetriveRoleBodyParams, UserRetriveRoleHeader, UserRetriveRoleResponse
from ...utils.decorators import json_response, unpack_models


bp = Blueprint('user', __name__, url_prefix='/user')
TAG = 'Manager'


@bp.route('/role', methods=['POST'])
@spec.validate(
    body=Request(UserSetRoleBodyParams), 
    headers=UserSetRoleHeader, 
    resp=Response(HTTP_200=UserSetRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def set_role(body: UserSetRoleBodyParams, headers: UserSetRoleHeader) -> UserSetRoleResponse:
    """ Добавление роли пользователю
    ---
        Накидываем роль пользователю
    """
    return UserSetRoleResponse()


@bp.route('/role', methods=['DELETE'])
@spec.validate(
    body=Request(UserRetriveRoleBodyParams), 
    headers=UserRetriveRoleHeader, 
    resp=Response(HTTP_200=UserRetriveRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def retrive_role(body: UserRetriveRoleBodyParams, headers: UserRetriveRoleHeader) -> UserRetriveRoleResponse:
    """Отбираем роль у пользователя
    ---
        Отбираем роль у пользователя
    """
    return UserRetriveRoleResponse()
