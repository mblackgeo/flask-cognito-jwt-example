import serverless_wsgi
from flask import Flask
from flask_cors import CORS

__version__ = "0.1.0"
__all__ = ["__version__", "create_app"]


def create_app() -> Flask:
    """Construct the core application."""
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("webapp.config.Config")

    with app.app_context():
        from .auth import routes as auth_routes  # noqa: F401
        from .home import routes as home_routes  # noqa: F401
        from .private import routes as private_routes  # noqa: F401

        # register blueprints
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(home_routes.bp)
        app.register_blueprint(private_routes.bp)

        return app


def handler(event, context):
    """Handler for AWS Lambda"""
    app = create_app()
    return serverless_wsgi.handle_request(app.wsgi_app, event, context)
