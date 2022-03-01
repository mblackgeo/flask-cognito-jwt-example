import json
import logging
from functools import wraps

import requests
from flask import current_app, redirect
from flask_awscognito import AWSCognitoAuthentication
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from urllib3.exceptions import LocationParseError


def get_cognito_public_keys(region: str, pool_id: str) -> str:
    try:
        url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"  # noqa: E501

        resp = requests.get(url)
        return json.dumps(json.loads(resp.text)["keys"][1])

    except (KeyError, LocationParseError, requests.exceptions.ConnectionError):
        logging.warning("Could not load public keys from Cognito User Pool")


def login_required():
    """If a user is not logged, redirect them to the Cognito UI"""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(optional=True)
            if get_jwt_identity():
                return fn(*args, **kwargs)
            else:
                aws_auth = AWSCognitoAuthentication(current_app)
                return redirect(aws_auth.get_sign_in_url())

        return decorator

    return wrapper
