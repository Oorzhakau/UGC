from flask import Blueprint, jsonify, request, url_for
from flask_pydantic import validate

from core.oauth import get_oauth_instance
from enumeration.oauths import SocialResourcesEnum
from enumeration.errors import Errors
from schemas import TokensResponse
from services.user_service import get_user_service
from services.oauth_service import get_social_auth_resource

auth_socials_v1 = Blueprint('auth_socials_v1', __name__, url_prefix='/oauth')

oauth = get_oauth_instance()


@auth_socials_v1.route('/<social_name>/login')
def socials_login(social_name: str):
    try:
        SocialResourcesEnum(social_name)
    except ValueError:
        return Errors.social_unsupported

    client = oauth.create_client(social_name)
    redirect_uri = url_for('auth_socials_v1.socials_auth',
                           social_name=social_name,
                           _external=True)

    uri = client.create_authorization_url(redirect_uri)
    client.save_authorize_data(redirect_uri=redirect_uri, **uri)
    return jsonify({'url': uri['url']})


@auth_socials_v1.route('/<social_name>/callback')
@validate()
def socials_auth(social_name: str) -> TokensResponse:
    service = get_user_service()
    try:
        resource = SocialResourcesEnum(social_name)
        user_data_kwargs = get_social_auth_resource(resource)()
    except (ValueError, TypeError):
        return Errors.social_unsupported

    account = service.get_social_account(
        social_id=user_data_kwargs.get('social_id'),
        social_name=social_name,
    )
    if not account:
        account = service.create_oauth_user(social_name=social_name,
                                            **user_data_kwargs)

    tokens = service.create_tokens(account.user)
    service.add_action_in_history(
        user=account.user,
        user_agent=request.headers.get('User-Agent'),
        action=f"OAuth2 {social_name}"
    )
    return tokens
