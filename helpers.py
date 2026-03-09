from flask import session, redirect

def login_required():
    if session.get("user_id") is None:
        return redirect("/login")
