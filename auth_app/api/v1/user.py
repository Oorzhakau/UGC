from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, get_jwt, jwt_required
from flask_pydantic import validate
from pydantic import parse_obj_as

from core.jwt_factory import get_jwt_instance
from enumeration.errors import Errors
from enumeration.roles import RolesEnum
from models import User
from schemas import (AccountHistory, AccountScheme, Pagination,
                     PaginationResponse, PasswordChange, RoleScheme,
                     RolesRequest, TokensResponse, UserReduce,
                     UserSignInScheme, UserSignUpScheme)
from services.decorators import (access_permission_jwt, rate_limit,
                                 write_to_accout_history)
from services.user_service import UserService, get_user_service

users_v1 = Blueprint('users_v1', __name__, url_prefix='/users')
jwt = get_jwt_instance()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    user_id = jwt_payload['user_id']
    result = get_user_service().check_access_token_is_revoked(user_id, f"\"{jti}\"")
    return result


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']['user_id']
    return User.query.filter_by(id=identity).one_or_none()


@users_v1.route('/signup', methods=['POST'])
@validate()
@rate_limit
def registration(body: UserSignUpScheme):
    service = get_user_service()
    user = service.get_user_by_username(body.username)
    if user:
        return Errors.username_is_already_exists
    service.create_user(username=body.username,
                        password=body.password,
                        roles_name=[RolesEnum.BASE])
    return jsonify({'msg': 'Successful registration'})


@users_v1.route('/login', methods=['POST'])
@validate()
@rate_limit
def login(body: UserSignInScheme) -> TokensResponse:
    user = UserService.get_user_by_username(body.username)
    if not user:
        return Errors.user_not_found

    if not user.verify_password(body.password):
        return Errors.password_verification_failed
    service = get_user_service()
    tokens = service.create_tokens(user)
    service.add_action_in_history(
        user=user,
        user_agent=request.headers.get('User-Agent'),
        action='sign_in'
    )
    return tokens


@users_v1.route('/logout', methods=['POST'])
@jwt_required()
@rate_limit
@write_to_accout_history(action='sing_out')
def logout():
    jwt = get_jwt()
    jti = jwt['jti']
    service = get_user_service()
    service.logout_user(current_user.id, jti)
    return jsonify({'msg': 'User has been logged out'})


@users_v1.route('/refresh', methods=['POST'])
@validate()
@jwt_required(refresh=True)
@rate_limit
@write_to_accout_history(action='refresh_token')
def refresh() -> TokensResponse:
    refresh_token = request.headers.get('Authorization').split()[-1]
    service = get_user_service()
    compare_refresh_tokens = service.check_refresh_token(current_user.id, refresh_token)
    if not compare_refresh_tokens:
        return Errors.refresh_token_invalid

    access_token = get_jwt()['jti']
    service = get_user_service()
    service.revoke_access_token(current_user.id, access_token)
    tokens = service.create_tokens(current_user)
    return tokens


@users_v1.route('/logout/all', methods=['POST'])
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@rate_limit
def logout_all():
    service = get_user_service()
    service.logout_all_user()
    return jsonify({'msg': 'Revoked all refresh tokens'})


@users_v1.route('/password', methods=['POST'])
@validate()
@jwt_required()
@rate_limit
@write_to_accout_history(action='password_change')
def password_change(body: PasswordChange):
    if not current_user.verify_password(body.curr_password):
        return Errors.password_verification_failed
    get_user_service().change_password(current_user, body.new_password)
    return jsonify({'msg': 'Successful password change'})


@users_v1.route('/history', methods=['GET'])
@validate()
@jwt_required()
@write_to_accout_history(action='history')
@rate_limit
def history(body: Pagination) -> PaginationResponse:
    service = get_user_service()
    actions = service.get_account_history(current_user,
                                          page=body.page,
                                          per_page=body.per_page)
    data = parse_obj_as(list[AccountHistory], [action.__dict__ for action in actions.items])
    response = PaginationResponse(
        page=actions.page,
        pages=actions.pages,
        total=actions.total,
        prev_page=actions.prev_num,
        next_page=actions.next_num,
        has_next=actions.has_next,
        has_prev=actions.has_prev,
        results=data,
    )
    return response


@users_v1.route('/me', methods=['GET'])
@validate()
@jwt_required()
@rate_limit
@write_to_accout_history(action='account_get')
def get_me() -> AccountScheme:
    service = get_user_service()
    user = service.get_user_by_id(current_user.id)
    account = AccountScheme(**user.__dict__)
    roles = parse_obj_as(list[RoleScheme], [role.__dict__ for role in user.roles])
    account.roles = roles
    return account


@users_v1.route('/me', methods=['PATCH'])
@validate()
@jwt_required()
@rate_limit
@write_to_accout_history(action='account_patch')
def patch_me(body: AccountScheme) -> AccountScheme:
    service = get_user_service()
    user = service.get_user_by_id(current_user.id)
    if body.name:
        user.name = body.name
    if body.email:
        user.email = body.email
    account = AccountScheme(**user.__dict__)
    roles = parse_obj_as(list[RoleScheme], [role.__dict__ for role in user.roles])
    account.roles = roles
    user.save()
    return account


@users_v1.route('/', methods=['GET'])
@validate()
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@rate_limit
@write_to_accout_history(action='get_users')
def get_users(query: Pagination) -> PaginationResponse:
    service = get_user_service()
    users = service.get_users(page=query.page, per_page=query.per_page)
    data = []
    for user in users.items:
        account = AccountScheme(**user.__dict__)
        roles = parse_obj_as(list[RoleScheme], [role.__dict__ for role in user.roles])
        account.roles = roles
        data.append(account)
    response = PaginationResponse(
        page=users.page,
        pages=users.pages,
        total=users.total,
        prev_page=users.prev_num,
        next_page=users.next_num,
        has_next=users.has_next,
        has_prev=users.has_prev,
        results=data,
    )
    return response


@users_v1.route('/<user_id>', methods=['GET'])
@validate()
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@rate_limit
@write_to_accout_history(action='get_user')
def get_user(user_id: str):
    service = get_user_service()
    user = service.get_user_by_id(user_id)
    if not user:
        return Errors.user_not_found
    account = AccountScheme(**user.__dict__)
    roles = parse_obj_as(list[RoleScheme], [role.__dict__ for role in user.roles])
    account.roles = roles
    return account


@users_v1.route('/<user_id>/roles', methods=['POST'])
@validate()
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@rate_limit
@write_to_accout_history(action='patch_user_roles')
def set_user_role(user_id: str, body: RolesRequest) -> AccountScheme:
    service = get_user_service()
    user = service.change_roles_from_user(user_id, body)
    account = AccountScheme(**user.__dict__)
    roles = parse_obj_as(list[RoleScheme], [role.__dict__ for role in user.roles])
    account.roles = roles
    return account


@users_v1.route('/<user_id>/roles', methods=['DELETE'])
@validate()
@jwt_required()
@access_permission_jwt(roles=[RolesEnum.ADMIN])
@rate_limit
@write_to_accout_history(action='patch_user_roles')
def delete_role_from_user(user_id: str, body: RolesRequest) -> AccountScheme:
    service = get_user_service()
    user = service.remove_roles_from_user(user_id, body)
    account = AccountScheme(**user.__dict__)
    roles = parse_obj_as(list[RoleScheme], [role.__dict__ for role in user.roles])
    account.roles = roles
    return account


@users_v1.route('/verification_roles', methods=['GET'])
@validate()
@rate_limit
@jwt_required()
def verification() -> UserReduce:
    jwt = get_jwt()
    user_id = jwt['user_id']
    roles = jwt['roles']
    user_reduce = UserReduce(
        user_id=user_id,
        roles=roles
    )
    return user_reduce
