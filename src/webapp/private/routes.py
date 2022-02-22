"""Route declaration."""
from typing import Union

from flask import Blueprint, Response, render_template
from flask_jwt_extended import jwt_required

bp = Blueprint("private_bp", __name__, template_folder="templates")


@bp.route("/private")
@jwt_required(locations=["headers", "cookies"])
def private() -> Union[Response, str]:
    """Render the a private page of the website

    Returns
    -------
    str
        HTML of page to display at "/"
    """
    return render_template("secret.html", title="This is a protected page!")
