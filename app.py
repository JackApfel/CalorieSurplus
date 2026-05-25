from datetime import datetime
import os
from functools import lru_cache
from time import strftime

import requests
from cs50 import SQL
from dotenv import load_dotenv
from email_validator import validate_email
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

cache_maxsize = int(os.environ.get("CACHE_MAXSIZE", 128))

db = SQL("sqlite:///calories.db")


# Source - https://stackoverflow.com/a/29516120
# Posted by lapinkoira, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-11, License - CC BY-SA 4.0
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/", methods=["GET", "POST"])
@helpers.login_required
def index():
    if request.method == "POST":
        # Get form data and validate it
        name = request.form.get("name")
        calories = request.form.get("product_calories")
        barcode = request.form.get("code")
        grams_consumed = request.form.get("grams")
        unit = request.form.get("unit")
        brand = request.form.get("brand")

        if not calories or not name or not barcode or not grams_consumed or not brand:
            flash("Fields cannot be empty!", "danger")
            return redirect("/")

        try:
            calories = int(round(float(calories)))
            grams_consumed = int(round(float(grams_consumed)))
        except ValueError:
            flash("Invalid input: calories/grams missing or not numeric", "danger")
            return redirect("/")

        if grams_consumed < 1 or calories < 1:
            flash("Values can not be Zero or less", "danger")
            return redirect("/catalog")

        try:
            grams_consumed = float(grams_consumed)
        except ValueError:
            flash("Invalid quantity input!", "danger")
            return redirect("/")
        if not unit:
            unit = ""
        # Normalize consumed quantity to base units (g or ml)
        grams_consumed, unit = helpers.norm_quantity(grams_consumed, unit)
        grams_consumed = int(round(grams_consumed))

        full_name = f"{name} - {brand}"

        # insert the new food entry into the database
        db.execute(
            "INSERT INTO foods (name, product_calories, consumed_calories, barcode, grams, user_id, calorie_goal) VALUES(?,?,?,?,?,?,?)",
            full_name,
            calories,
            round((calories / 100) * grams_consumed),
            barcode,
            grams_consumed,
            session["user_id"],
            session["calorie_goal"],
        )

        # Provide feedback to the user and redirect back to the main page
        flash("Entry Added!", "success")
        return redirect("/")

    else:
        daily_food_entries = db.execute(
            "SELECT * FROM foods WHERE user_id = ? AND DATE(created_at) = DATE('now') ORDER BY created_at DESC",
            session["user_id"],
        )

        daily_calories = db.execute(
            "SELECT SUM(consumed_calories) AS daily_calories FROM foods WHERE user_id = ? AND DATE(created_at) = DATE('now')",
            session["user_id"],
        )

        weekly_calories = db.execute(
            "SELECT SUM(consumed_calories) AS weekly_calories FROM foods WHERE user_id = ? AND DATE(created_at) >= DATE('now', '-7 days')",
            session["user_id"],
        )

        progress_percentage = (
            (daily_calories[0]["daily_calories"] / session["calorie_goal"]) * 100
            if daily_calories[0]["daily_calories"] and session["calorie_goal"]
            else 0
        )

        for entry in daily_food_entries:
            dt = datetime.fromisoformat(entry["created_at"])
            entry["format_created_at"] = dt.strftime("%H:%M")

        return render_template(
            "index.html",
            foods=daily_food_entries,
            daily_calories=daily_calories,
            weekly_calories=weekly_calories,
            progress_percentage=progress_percentage,
        )


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

        calorie_goal_row = db.execute(
            "SELECT calorie_goal FROM preferences WHERE user_id = ?", users[0]["id"]
        )

        if not calorie_goal_row:
            db.execute(
                "INSERT INTO preferences (user_id, calorie_goal) VALUES (?, ?)",
                users[0]["id"],
                2000,
            )
            calorie_goal_row = [{"calorie_goal": 2000}]

        session["calorie_goal"] = calorie_goal_row[0]["calorie_goal"]

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
            flash("Email, password, and confirmation are required.", "warning")
            return redirect("/register")

        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except:
            flash("Invalid email.", "warning")
            return redirect("/register")

        if password != confirm_password:
            flash("Passwords do not match.", "warning")
            return redirect("/register")

        if db.execute("SELECT * FROM users WHERE email = ?", email):
            flash("This email is already registered.", "warning")
            return redirect("/register")


        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (email, hash) VALUES(?,?)", email, hash)

        user_id = db.execute("SELECT id FROM users WHERE email = ?", email)[0]["id"]

        session["user_id"] = user_id

        db.execute("INSERT INTO preferences (user_id) VALUES(?);", session["user_id"])

        calorie_goal = db.execute(
            "SELECT calorie_goal FROM preferences WHERE user_id = ?", user_id
        )
        session["calorie_goal"] = calorie_goal[0]["calorie_goal"]

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


@lru_cache(maxsize=cache_maxsize)
def get_product(search_term):
    params = {
        "search_terms": search_term,
        "json": "true",
        "page_size": 8,
        # Only request the fields we actually need — massively reduces response size and latency
        "fields": "product_name,brands,nutriments,image_front_small_url,code,quantity,product_quantity,product_quantity_unit",
    }

    headers = {
        # Format: AppName/Version (contact-email) — no special chars in name, email in parentheses
        "User-Agent": "KalorienZaehler/0.1 (jack.apfel_dev@pm.me)"
    }

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    response = requests.get(url, params=params, headers=headers, timeout=32)
    response.raise_for_status()
    data = response.json()

    return data


@app.route("/catalog", methods=["GET", "POST"])
@helpers.login_required
def catalog():
    if request.method == "POST":
        search_term = request.form.get("search")
        search_term = (
            (search_term or "").strip().lower()
        )  # Copilot came up with the 'or' fix to handle None values
        if not search_term or search_term == "":
            flash("Please enter a product name.", "danger")
            return redirect("/catalog")
        try:
            data = get_product(search_term)
        except requests.exceptions.Timeout:
            flash(
                "The food database took too long to respond. Please try again.",
                "danger",
            )
            return redirect("/catalog")
        except requests.exceptions.HTTPError:
            flash(
                "Food database returned an error. Please try again later.",
                "danger",
            )
            return redirect("/catalog")
        except requests.exceptions.RequestException:
            flash(
                "Could not reach the food database. Please try again later.", "danger"
            )
            return redirect("/catalog")

        return render_template("catalog.html", item=data, search_term=search_term)
    else:
        return render_template("catalog.html")


@app.route("/history", methods=["GET", "POST"])
@helpers.login_required
def history():
    if request.method == "POST":
        date = request.form.get("date")

        try:
            products = db.execute(
                "SELECT * FROM foods WHERE user_id = ? AND date(created_at) = ?",
                session["user_id"],
                date,
            )

            total_calories = db.execute(
                "SELECT COALESCE(SUM(consumed_calories), 0) as total_calories FROM foods WHERE user_id = ? AND date(created_at) = ?",
                session["user_id"],
                date,
            )
        except Exception:
            flash(
                "Database encountered an error.",
                "danger",
            )
            return redirect("/history")

        for entry in products:
            dt = datetime.fromisoformat(entry["created_at"])
            entry["format_created_at"] = dt.strftime("%H:%M")

        return render_template(
            "history.html", foods=products, date=date, total_calories=total_calories
        )

    else:
        return render_template("history.html", total_calories=[{"total_calories": 0}])


@app.route("/preference", methods=["GET", "POST"])
@helpers.login_required
def preference():
    if request.method == "POST":
        daily_calorie_goal_form = request.form.get("daily_calorie_goal")
        if not daily_calorie_goal_form:
            flash("Error: Calorie goal is null", "danger")
            return redirect("/preference")
        try:
            daily_calorie_goal = int(round(float(daily_calorie_goal_form)))
        except ValueError:
            flash(
                "Input was not a number!",
                "danger",
            )
            return redirect("/preference")
        if daily_calorie_goal < 1:
            flash(
                "Calorie goal can not be Zero or less!",
                "warning",
            )
            return redirect("/preference")

        # Copilot helped with Syntax for ON CONFLICT and UPDATE
        db.execute(
            "UPDATE preferences SET calorie_goal = ? WHERE user_id = ?",
            daily_calorie_goal,
            session["user_id"],
        )
        session["calorie_goal"] = daily_calorie_goal

        return redirect("/preference")
    else:
        return render_template("preference.html")


@app.route("/delete_entry", methods=["POST"])
@helpers.login_required
def delete():
    db.execute(
        "DELETE FROM foods WHERE id = ? AND user_id = ?",
        request.form.get("entry_id"),
        session["user_id"],
    )

    allowed_redirects = {
        "/",
        "/history",
        "/catalog",
        "/preference",
        "/login",
        "/logout",
        "/register",
    }

    next_page = request.form.get("next")
    if next_page not in allowed_redirects:
        next_page = "/"

    flash("Entry Deleted", "success")
    return redirect(next_page)
