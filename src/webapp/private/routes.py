"""Route declaration."""
from flask import Blueprint, render_template

bp = Blueprint("private_bp", __name__, template_folder="templates")


@bp.route("/private")
def private() -> str:
    """Render the a private page of the website

    Returns
    -------
    str
        HTML of page to display at "/"
    """
    return render_template("secret.html", title="This is a protected page!")
