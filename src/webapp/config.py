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
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    AWS_DEFAULT_REGION = environ.get("AWS_DEFAULT_REGION")
    AWS_COGNITO_DOMAIN = environ.get("AWS_COGNITO_DOMAIN")
    AWS_COGNITO_USER_POOL_ID = environ.get("AWS_COGNITO_USER_POOL_ID")
    AWS_COGNITO_USER_POOL_CLIENT_ID = environ.get("AWS_COGNITO_USER_POOL_CLIENT_ID")
    AWS_COGNITO_USER_POOL_CLIENT_SECRET = environ.get(
        "AWS_COGNITO_USER_POOL_CLIENT_SECRET"
    )
    AWS_COGNITO_REDIRECT_URL = environ.get("AWS_COGNITO_REDIRECT_URL")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
