from flask import Blueprint, current_app, make_response, redirect, request, url_for
from flask_awscognito import AWSCognitoAuthentication
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies

aws_auth = AWSCognitoAuthentication(current_app)


bp = Blueprint("auth_bp", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Redirect to the Cognito Hosted UI for login"""
    return redirect(aws_auth.get_sign_in_url())


@bp.route("/postlogin", methods=["GET"])
def postlogin():
    """After a successful login store the access token as a cookie and redirect"""
    access_token = aws_auth.get_access_token(request.args)
    resp = make_response(redirect(url_for("private_bp.private")))
    set_access_cookies(resp, access_token, max_age=30 * 60)  # 30 mins
    return resp


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    """Logout the user and delete their JWT cookie"""
    resp = make_response(redirect(url_for("home_bp.home")))
    unset_jwt_cookies(resp)
    return resp
