from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from pydantic import parse_obj_as

from core.jwt_factory import get_jwt_instance
from enumeration.errors import Errors
from enumeration.roles import RolesEnum
from schemas import RoleScheme
from services.decorators import access_permission_jwt, write_to_accout_history
from services.role_service import get_role_service


roles_v1 = Blueprint('roles_v1', __name__, url_prefix='/roles')
jwt = get_jwt_instance()


@roles_v1.route('/', methods=['GET'])
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@write_to_accout_history(action='get_roles')
def get_roles():
    service = get_role_service()
    roles = service.get_roles()
    roles_to_present = parse_obj_as(list[RoleScheme],
                                    [role.__dict__ for role in roles])
    response = [role.dict() for role in roles_to_present]
    return response


@roles_v1.route('/', methods=['POST'])
@validate()
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@write_to_accout_history(action='create_roles')
def create_role(body: RoleScheme):
    service = get_role_service()
    role = service.get_by_name(body.name)
    if role:
        return Errors.role_is_already_exists
    service.get_or_create_role(body.name, body.description)
    return jsonify({'msg': 'Role was created'})


@roles_v1.route('/<role_id>', methods=['GET'])
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@write_to_accout_history(action='get_role')
def get_role(role_id):
    service = get_role_service()
    role = service.get_by_id(role_id)
    if not role:
        return Errors.role_not_found
    return RoleScheme(**role.__dict__).dict()


@roles_v1.route('/<role_id>', methods=['PATCH'])
@validate()
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@write_to_accout_history(action='patch_role')
def patch_role(role_id: str, body: RoleScheme):
    service = get_role_service()
    role = service.change_role_data(role_id, body)
    if not role:
        return Errors.role_not_found
    return RoleScheme(**role.__dict__).dict()
