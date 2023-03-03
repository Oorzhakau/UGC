from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint


def swagger_factory(swagger_url: str = '/swagger',
                    api_url: str = '/static/swagger.json') -> Blueprint:
    swagger_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': 'Auth app'
        }
    )
    return swagger_blueprint
