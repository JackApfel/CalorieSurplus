from functools import wraps

from cs50 import SQL
from flask import redirect, session

db = SQL("sqlite:///calories.db")


def login_required(f):
    """
    Decorator to require login for a route.
    Wraps a route function and checks if user is logged in before executing it.

    Usage:
        @app.route("/protected")
        @login_required
        def protected_page():
            return "You can only see this if logged in"

    Assisted by GitHub Copilot while implementing Flask decorator pattern.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = db.execute(
            "SELECT id FROM users WHERE id = ?", session.get("user_id")
        )
        if not user_id:
            return redirect("/login")
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def norm_quantity(quantity: float, unit: str):
    match unit:
        case "g":
            return (quantity, "g")
        case "kg":
            return (quantity * 1000, "g")
        case "mg":
            return (quantity / 1000, "g")
        case "lb":
            return (quantity * 453.5924, "g")
        case "oz":
            return (quantity * 28.34952, "g")
        case "ml":
            return (quantity, "ml")
        case "l":
            return (quantity * 1000, "ml")
        case "cl":
            return (quantity * 10, "ml")
        case _:
            return quantity, unit
