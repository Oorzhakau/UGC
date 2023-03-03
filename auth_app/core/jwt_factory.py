from flask import Flask
from flask_jwt_extended import JWTManager

jwt: JWTManager | None = None


def create_jwt(app: Flask):
    global jwt
    if jwt is None:
        jwt = JWTManager(app)


def get_jwt_instance() -> JWTManager:
    return jwt
