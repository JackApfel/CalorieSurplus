from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash

import helpers

app = Flask(__name__)

db = SQL("sqlite:///calories.db")


@app.route("/")
def index():
    helpers.login_required()
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template(
                "error.html", error="Must provide email and password"
            )

        hash = generate_password_hash(password)

        print(db.execute("SELECT * FROM users WHERE email = ?", email))
        print(
            db.execute("SELECT * FROM users WHERE email = ? AND hash = ?", email, hash)
        )

        # users = db.execute("SELECT * FROM users WHERE email = ?", email)

        # for user in users:
        #     if email == user['email']:
        #         return render_template("error.html", error="Email already exists")
        # check email with db query

        return redirect("/")
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
