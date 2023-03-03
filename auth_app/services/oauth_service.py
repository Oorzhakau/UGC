import json

from core.oauth import get_oauth_instance
from enumeration.oauths import SocialResourcesEnum

oauth = get_oauth_instance()


def get_userdata_from_google() -> dict:
    token = oauth.google.authorize_access_token()
    return {"email": token["userinfo"]["email"], "social_id": token["userinfo"]["sub"]}


def get_userdata_from_yandex() -> dict:
    oauth.yandex.authorize_access_token()
    user_data_response = oauth.yandex.get("info")
    user_data = json.loads(user_data_response.content)
    return {"email": user_data["default_email"], "social_id": user_data["id"]}


def get_social_auth_resource(key: str):
    socials_auth_mapping = {
        SocialResourcesEnum.GOOGLE: get_userdata_from_google,
        SocialResourcesEnum.YANDEX: get_userdata_from_yandex,
    }
    if key in socials_auth_mapping:
        return socials_auth_mapping[key]
