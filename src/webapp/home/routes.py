"""Route declaration."""
from flask import Blueprint, Response, jsonify, render_template

bp = Blueprint("home_bp", __name__)


@bp.route("/health")
def health() -> Response:
    """Return a JSON response containing status OK. Used for automatic health checks
    Returns
    -------
    flask.Response
        200 OK response
    """
    return jsonify({"status": "ok"})


@bp.route("/")
def home() -> str:
    """Render the homepage of the website

    Returns
    -------
    str
        HTML of page to display at "/"
    """
    return render_template("index.html", title="Welcome!")


@bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Handover to Coginito for login

    Returns
    -------
    str
        HTML of page to display at "/"
    """
    return "ok"
