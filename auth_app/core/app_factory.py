from flask import Flask, request
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from api.v1.routers import init_routes
from core.swagger_factory import swagger_factory
from core.oauth import create_oauth
from core.tracer import configure_tracer
from db.db_factory import create_db
from db.cache_factory import create_cache
from settings.config import settings
from core.jwt_factory import create_jwt


def init_app(app: Flask) -> Flask:
    db_conf = (
        f'{settings.DB}://'
        f'{settings.DB_USER}:'
        f'{settings.DB_PASSWORD}@'
        f'{settings.DB_HOST}:'
        f'{settings.DB_PORT}/'
        f'{settings.DB_NAME}'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = db_conf
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = settings.PROJECT_SECRET

    swagger_blueprint = swagger_factory()
    app.register_blueprint(swagger_blueprint, url_prefix=swagger_blueprint.url_prefix)

    # database
    create_db(app)
    import models

    # cache
    create_cache(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    # jwt
    create_jwt(app)
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.ACCESS_TOKEN_EXPIRE

    # oauth
    app.config.update(settings.dict())
    create_oauth(app)

    # routes
    init_routes(app)

    # command
    from commands.create_superuser import createsuperuser
    app.cli.add_command(createsuperuser)

    if app.config['JAEGER_ACTIVATE']:
        @app.before_request
        def before_request():
            request_id = request.headers.get('X-Request-Id')
            if not request_id:
                raise RuntimeError('request id is required')
        # tracer
        configure_tracer(app=app)
        FlaskInstrumentor().instrument_app(app)
    return app
