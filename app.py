import os

from cs50 import SQL
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash

import helpers

# Load environment variables from .env file (for local development)
# Assisted by GitHub Copilot while setting up secure configuration management
load_dotenv()

app = Flask(__name__)

# Configure Flask secret key from environment variable
# This is required for session management (signing cookies securely)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise ValueError("No SECRET_KEY set in environment. Check your .env file.")

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
