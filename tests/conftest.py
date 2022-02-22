import json
import logging
import os

import pytest

from webapp import create_app


@pytest.fixture
def app(mocker):
    """Create application for the tests."""
    # setup testing config
    os.environ["FLASK_APP"] = "webapp"
    os.environ["FLASK_ENV"] = "test"
    os.environ["FLASK_JWT_SECRET_KEY"] = "not-used"
    os.environ["FLASK_SITE_URL"] = "http://localhost:5000"

    os.environ["AWS_REGION"] = "na"
    os.environ["AWS_COGNITO_DOMAIN"] = "na"
    os.environ["AWS_COGNITO_USER_POOL_ID"] = "na"
    os.environ["AWS_COGNITO_USER_POOL_CLIENT_ID"] = "na"
    os.environ["AWS_COGNITO_USER_POOL_CLIENT_SECRET"] = "na"

    # patch the call to AWS Cognito
    mock_public_key = {
        "kty": "RSA",
        "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx",
        "e": "AQAB",
        "alg": "RS256",
        "kid": "2011-04-29",
    }

    mocker.patch(
        "webapp.auth.utils.get_cognito_public_keys",
        return_value=json.dumps(mock_public_key),
    )

    _app = create_app()
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    _app.config["TESTING"] = True
    _app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False

    _app.testing = True

    yield _app
    ctx.pop()


@pytest.fixture
def client(app):
    cl = app.test_client()
    yield cl
