from flask import Flask

__version__ = "0.1.0"
__all__ = ["__version__", "create_app"]


def create_app() -> Flask:
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object("webapp.config.Config")

    with app.app_context():
        from .home import routes as home_routes  # noqa: F401
        from .private import routes as private_routes  # noqa: F401

        # register blueprints
        app.register_blueprint(home_routes.bp)
        app.register_blueprint(private_routes.bp)

        return app
