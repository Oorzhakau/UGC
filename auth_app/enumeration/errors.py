from http import HTTPStatus


class Errors:
    user_not_found = {'msg': 'User not found'}, HTTPStatus.NOT_FOUND
    username_is_already_exists = {'msg': 'Username is already exists'}, HTTPStatus.CONFLICT
    role_is_already_exists = {'msg': 'Role is already exists'}, HTTPStatus.CONFLICT
    role_not_found = {'msg': 'Role not found'}, HTTPStatus.NOT_FOUND
    password_verification_failed = {'msg': 'Invalid password'}, HTTPStatus.UNAUTHORIZED
    refresh_token_invalid = {'msg': 'Invalid refresh token'}, HTTPStatus.UNAUTHORIZED
    permission_denied = {'msg': 'Permission denied'}, HTTPStatus.FORBIDDEN
    id_not_valid = {'msg': 'Incorrect id'}, HTTPStatus.BAD_REQUEST
    social_unsupported = {"msg": "Unsupported social name"}, HTTPStatus.UNPROCESSABLE_ENTITY
