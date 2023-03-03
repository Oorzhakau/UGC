from flask import Flask


def init_routes(app: Flask):
    from api.v1.role import roles_v1
    from api.v1.user import users_v1
    from api.v1.social import auth_socials_v1

    app.register_blueprint(users_v1, strict_slashes=False)
    app.register_blueprint(roles_v1, strict_slashes=False)
    app.register_blueprint(auth_socials_v1, strict_slashes=False)
