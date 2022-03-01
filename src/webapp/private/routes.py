"""Route declaration."""
from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import get_jwt

from webapp.auth.utils import login_required

bp = Blueprint("private_bp", __name__, template_folder="templates")


@bp.route("/private")
@login_required()
def private() -> str:
    """Render the a private page of the website

    Returns
    -------
    str
        HTML of page to display at "/"
    """
    return render_template("secret.html", title="This is a protected page!")


@bp.route("/token")
@login_required()
def token():
    """Show the JSON web token for the current authenticated user"""
    return jsonify(get_jwt())
