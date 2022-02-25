import json
import logging

import requests
from urllib3.exceptions import LocationParseError


def get_cognito_public_keys(region: str, pool_id: str) -> str:
    try:
        url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"  # noqa: E501

        resp = requests.get(url)
        return json.dumps(json.loads(resp.text)["keys"][1])

    except (KeyError, LocationParseError):
        logging.warning("Could not load public keys from Cognito User Pool")
