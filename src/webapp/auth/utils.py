import json

import requests


def get_cognito_public_keys(region: str, pool_id: str) -> str:
    url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"

    resp = requests.get(url)
    return json.dumps(json.loads(resp.text)["keys"][1])
