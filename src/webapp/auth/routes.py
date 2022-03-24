from flask import Blueprint, redirect, url_for
from flask_cognito_lib.decorators import (
    cognito_login,
    cognito_login_callback,
    cognito_logout,
)

bp = Blueprint("auth_bp", __name__)


@bp.route("/login", methods=["GET", "POST"])
@cognito_login
def login():
    """Redirect to the Cognito Hosted UI for login"""
    pass


@bp.route("/postlogin", methods=["GET"])
@cognito_login_callback
def postlogin():
    """After a successful login store the access token as a cookie and redirect"""
    return redirect(url_for("private_bp.private"))


@bp.route("/logout", methods=["GET", "POST"])
@cognito_logout
def logout():
    """Logout the user and delete their JWT cookie"""
    return redirect(url_for("home_bp.home"))
