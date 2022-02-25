import logging

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from jwt.algorithms import RSAAlgorithm
from jwt.exceptions import InvalidKeyError

from webapp.auth.utils import get_cognito_public_keys

__version__ = "0.1.0"
__all__ = ["__version__", "create_app"]


def create_app() -> Flask:
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object("webapp.config.Config")

    # Setup CORS middleware
    CORS(app)

    # Setup JWT
    try:
        app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(
            get_cognito_public_keys(
                region=app.config["AWS_REGION"],
                pool_id=app.config["AWS_COGNITO_USER_POOL_ID"],
            )
        )
    except InvalidKeyError:
        logging.warning(
            (
                "Could not verify Cognito public keys. "
                "Secure routes may not be accessible"
            )
        )

    JWTManager(app)

    with app.app_context():
        from .auth import routes as auth_routes  # noqa: F401
        from .home import routes as home_routes  # noqa: F401
        from .private import routes as private_routes  # noqa: F401

        # register blueprints
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(home_routes.bp)
        app.register_blueprint(private_routes.bp)

        return app
