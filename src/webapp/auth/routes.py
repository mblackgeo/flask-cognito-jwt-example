from flask import (
    Blueprint,
    current_app,
    jsonify,
    make_response,
    redirect,
    request,
    url_for,
)
from flask_awscognito import AWSCognitoAuthentication
from flask_jwt_extended import JWTManager, get_jwt, jwt_required, set_access_cookies
from jwt.algorithms import RSAAlgorithm

from .utils import get_cognito_public_keys

aws_auth = AWSCognitoAuthentication(current_app)
current_app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(
    get_cognito_public_keys(
        region=current_app.config["AWS_DEFAULT_REGION"],
        pool_id=current_app.config["AWS_COGNITO_USER_POOL_ID"],
    )
)
jwt = JWTManager(current_app)
bp = Blueprint("auth_bp", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Redirect to the Cognito Hosted UI for login"""
    return redirect(aws_auth.get_sign_in_url())


@bp.route("/postlogin", methods=["GET"])
def postlogin():
    """After a successful loging store the access token as a cookie and redirect"""
    access_token = aws_auth.get_access_token(request.args)
    resp = make_response(redirect(url_for("private_bp.private")))
    set_access_cookies(resp, access_token, max_age=30 * 60)  # 30 mins
    return resp


@bp.route("/token")
@jwt_required(locations=["headers", "cookies"])
def token():
    """Show the JSON web token for the current authenticated user"""
    return jsonify(get_jwt())


# TODO logout function
