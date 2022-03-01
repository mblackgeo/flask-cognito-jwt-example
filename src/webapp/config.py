"""App configuration."""
import logging
from os import environ, path, urandom

from dotenv import load_dotenv
from jwt.algorithms import RSAAlgorithm
from jwt.exceptions import InvalidKeyError

from webapp.auth.utils import get_cognito_public_keys

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "..", "..", ".env"))


class Config:
    """Set Flask configuration vars from .env file."""

    # TODO replace this with pydantic
    # General Config
    SECRET_KEY = environ.get("SECRET_KEY", urandom(32))
    FLASK_APP = environ["FLASK_APP"]
    FLASK_ENV = environ["FLASK_ENV"]
    FLASK_SITE_URL = environ["FLASK_SITE_URL"]

    # Cognito
    AWS_REGION = environ["AWS_REGION"]
    AWS_DEFAULT_REGION = AWS_REGION
    AWS_COGNITO_DOMAIN = environ["AWS_COGNITO_DOMAIN"]
    AWS_COGNITO_USER_POOL_ID = environ["AWS_COGNITO_USER_POOL_ID"]
    AWS_COGNITO_USER_POOL_CLIENT_ID = environ["AWS_COGNITO_USER_POOL_CLIENT_ID"]
    AWS_COGNITO_USER_POOL_CLIENT_SECRET = environ["AWS_COGNITO_USER_POOL_CLIENT_SECRET"]
    AWS_COGNITO_REDIRECT_URL = path.join(FLASK_SITE_URL, "postlogin")

    # JWT
    FLASK_JWT_SECRET_KEY = environ.get("FLASK_JWT_SECRET_KEY", urandom(32))
    JWT_ALGORITHM = "RS256"

    # CSRF protection
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT = False  # TODO is this required?
    JWT_COOKIE_SECURE = True

    try:
        JWT_PUBLIC_KEY = RSAAlgorithm.from_jwk(
            get_cognito_public_keys(
                region=AWS_REGION,
                pool_id=AWS_COGNITO_USER_POOL_ID,
            )
        )
    except InvalidKeyError:
        logging.warning(
            "Could not access Cognito public keys. Secure routes may not be accessible"
        )

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
