import os

from cs50 import SQL
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

import helpers

# Load environment variables from .env file (for local development)
# Assisted by GitHub Copilot while setting up secure configuration management
load_dotenv()

app = Flask(__name__)

# Configure Flask secret key from environment variable
# This is required for session management (signing cookies securely)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise ValueError("No SECRET_KEY set in the environment. Check your .env file.")

db = SQL("sqlite:///calories.db")


@app.route("/")
@helpers.login_required
def index():
    return render_template("index.html", user_id=session.get("user_id"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()

        password = request.form.get("password")
        email = request.form.get("email")
        if not password or not email:
            flash("Email and password are required.", "danger")
            return redirect("/login")

        users = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get("email")
        )

        if not users:
            flash("Invalid email or password.", "danger")
            return redirect("/login")

        if check_password_hash(users[0]["hash"], password):
            session["user_id"] = users[0]["id"]
            flash("Signed in successfully!", "success")
        else:
            flash("Invalid email or password.", "danger")
            return redirect("/login")

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not email or not password or not confirm_password:
            flash("Email, password, and confirmation are required.", "danger")
            return redirect("/register")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect("/register")

        if db.execute("SELECT * FROM users WHERE email = ?", email):
            flash("This email is already registered.", "danger")
            return redirect("/register")

        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (email, hash) VALUES(?,?)", email, hash)

        user_id = db.execute("SELECT id FROM users WHERE email = ?", email)[0]["id"]

        session["user_id"] = user_id
        flash("Registration successful. Welcome!", "success")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout", methods=["GET", "POST"])
@helpers.login_required
def logout():
    """Log user out by clearing session"""
    if request.method == "POST":
        session.clear()
        flash("Logged out successfully!", "success")
        return redirect("/login")
    else:
        return render_template("logout.html")


if __name__ == "__main__":
    app.run(debug=True)
