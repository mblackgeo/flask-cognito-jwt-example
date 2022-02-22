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
from flask_jwt_extended import (
    JWTManager,
    get_jwt_identity,
    set_access_cookies,
    verify_jwt_in_request,
)

aws_auth = AWSCognitoAuthentication(current_app)
jwt = JWTManager(current_app)
bp = Blueprint("auth_bp", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Redirect to the Cognito Hosted UI for login"""
    return redirect(aws_auth.get_sign_in_url())


@bp.route("/postlogin", methods=["GET"])
def postlogin():
    """After a successful loging store the access token as a cookie"""
    access_token = aws_auth.get_access_token(request.args)
    resp = make_response(redirect(url_for("private_bp.private")))
    set_access_cookies(resp, access_token, max_age=30 * 60)  # 30 mins
    return resp


@bp.route("/claims")
def claims():
    """Show the Authenticated user claims granted from Cognito"""
    verify_jwt_in_request(optional=True)
    if get_jwt_identity():
        return jsonify({"claims": aws_auth.claims})
    return redirect(aws_auth.get_sign_in_url())


# TODO logout function
