"""Route declaration."""
from flask import Blueprint, jsonify, render_template, session
from flask_cognito_lib.decorators import auth_required

bp = Blueprint("private_bp", __name__, template_folder="templates")


@bp.route("/private")
@auth_required()
def private() -> str:
    """Render the a private page of the website

    Returns
    -------
    str
        HTML of page to display at "/"
    """
    return render_template("secret.html", title="This is a protected page!")


@bp.route("/token")
@auth_required()
def token():
    """Show the JSON web token for the current authenticated user"""
    return jsonify(session)
