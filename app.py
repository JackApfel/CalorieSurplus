import os

from cs50 import SQL
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

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


@app.route("/", methods=["GET", "POST"])
@helpers.login_required
def index():
    if request.method == "POST":
        name = request.form.get("name")
        calories = request.form.get("calories")
        barcode = request.form.get("code")

        db.execute("INSERT INTO foods (name, calories, barcode, user_id) VALUES(?,?,?,?)", name, calories, barcode, session["user_id"])
        return redirect("/")
    else:
        foods = db.execute("SELECT * FROM foods WHERE user_id = ?", session['user_id'])

        return render_template("index.html", foods=foods)

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



@app.route("/catalog", methods=["GET", "POST"])
@helpers.login_required
def catalog():

    if request.method == "POST":
        search_term = str(request.form.get("search"))
        params = {
            "search_terms": search_term,
            "json": "true",
            "page_size": 8,
            # Only request the fields we actually need — massively reduces response size and latency
            "fields": "product_name,brands,nutriments,image_front_small_url,code",
        }

        headers = {
            # Format: AppName/Version (contact-email) — no special chars in name, email in parentheses
            "User-Agent": "KalorienZaehler/0.1 (jack.apfel_dev@pm.me)"
        }

        url = "https://world.openfoodfacts.org/cgi/search.pl"

        try:
            response = requests.get(url, params=params, headers=headers, timeout=32)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout:
            flash("The food database took too long to respond. Please try again.", "danger")
            return redirect("/catalog")
        except requests.exceptions.HTTPError as e:
            flash(f"Food database returned an error (HTTP {e.response.status_code}). Please try again later.", "danger")
            return redirect("/catalog")
        except requests.exceptions.RequestException:
            flash("Could not reach the food database. Please try again later.", "danger")
            return redirect("/catalog")

        return render_template("catalog.html", item=data, search_term=search_term)
    else:
        return render_template("catalog.html")
