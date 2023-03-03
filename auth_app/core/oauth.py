from authlib.integrations.flask_client import OAuth
from flask import Flask

oauth: OAuth | None = None


def create_oauth(app: Flask):
    global oauth
    oauth = OAuth(app)
    oauth.register(name='google')
    oauth.register(name='yandex')


def get_oauth_instance() -> OAuth:
    return oauth
