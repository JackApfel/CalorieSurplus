from functools import wraps

from flask import redirect, session


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
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
