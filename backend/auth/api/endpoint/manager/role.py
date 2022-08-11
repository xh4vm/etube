from flask import Blueprint
from flask_pydantic_spec import Response, Request

from ...app import spec
from ...schema.manager.role.get import GetRoleBodyParams, GetRoleHeader, GetRoleResponse
from ...schema.manager.role.create import CreateRoleBodyParams, CreateRoleHeader, CreateRoleResponse
from ...schema.manager.role.update import UpdateRoleBodyParams, UpdateRoleHeader, UpdateRoleResponse
from ...schema.manager.role.delete import DeleteRoleBodyParams, DeleteRoleHeader, DeleteRoleResponse
from ...schema.manager.role.set import SetRoleBodyParams, SetRoleHeader, SetRoleResponse
from ...schema.manager.role.retrive import RetriveRoleBodyParams, RetriveRoleHeader, RetriveRoleResponse
from ...schema.manager.role.base import Role
from ...utils.decorators import json_response, unpack_models


bp = Blueprint('role', __name__, url_prefix='/role')
TAG = 'Manager'

@bp.route('', methods=['GET'])
@spec.validate(
    body=Request(GetRoleBodyParams), 
    headers=GetRoleHeader,
    resp=Response(HTTP_200=GetRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def get_Roles():
    return GetRoleResponse(Roles=[])


@bp.route('', methods=['POST'])
@spec.validate(
    body=Request(CreateRoleBodyParams), 
    headers=CreateRoleHeader, 
    resp=Response(HTTP_200=CreateRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def create_Role() -> CreateRoleResponse:
    return CreateRoleResponse(id=uuid.uuid4())


@bp.route('', methods=['PUT'])
@spec.validate(
    body=Request(UpdateRoleBodyParams), 
    headers=UpdateRoleHeader, 
    resp=Response(HTTP_200=UpdateRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def update_Role() -> UpdateRoleResponse:
    UpdateRoleResponse(id=uuid.uuid4(), title='')


@bp.route('', methods=['DELETE'])
@spec.validate(
    body=Request(DeleteRoleBodyParams), 
    headers=DeleteRoleHeader, 
    resp=Response(HTTP_200=DeleteRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def delete_Role() -> DeleteRoleResponse:
    return DeleteRoleResponse()


@bp.route('', methods=['POST'])
@spec.validate(
    body=Request(SetRoleBodyParams), 
    headers=SetRoleHeader, 
    resp=Response(HTTP_200=SetRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def set_Role() -> SetRoleResponse:
    return SetRoleResponse()


@bp.route('', methods=['DELETE'])
@spec.validate(
    body=Request(RetriveRoleBodyParams), 
    headers=RetriveRoleHeader, 
    resp=Response(HTTP_200=RetriveRoleResponse, HTTP_403=None), 
    tags=[TAG]
)
@unpack_models
@json_response
def retrive_Role() -> RetriveRoleResponse:
    return RetriveRoleResponse()
