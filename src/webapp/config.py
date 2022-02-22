"""App configuration."""
from os import environ, path, urandom

from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "..", "..", ".env"))


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY", urandom(32))
    FLASK_APP = environ["FLASK_APP"]
    FLASK_ENV = environ["FLASK_ENV"]
    FLASK_SITE_URL = environ["FLASK_SITE_URL"]

    # Cognito
    AWS_DEFAULT_REGION = environ["AWS_DEFAULT_REGION"]
    AWS_COGNITO_DOMAIN = environ["AWS_COGNITO_DOMAIN"]
    AWS_COGNITO_USER_POOL_ID = environ["AWS_COGNITO_USER_POOL_ID"]
    AWS_COGNITO_USER_POOL_CLIENT_ID = environ["AWS_COGNITO_USER_POOL_CLIENT_ID"]
    AWS_COGNITO_USER_POOL_CLIENT_SECRET = environ["AWS_COGNITO_USER_POOL_CLIENT_SECRET"]
    AWS_COGNITO_REDIRECT_URL = path.join(FLASK_SITE_URL, "postlogin")

    # JWT
    JWT_ALGORITHM = "RS256"
    # JWT_TOKEN_LOCATION = ["cookies"]
    # JWT_COOKIE_SECURE = FLASK_ENV == "prod"  # True in prod

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
