import os

import requests
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


@app.route("/", methods=["GET", "POST"])
@helpers.login_required
def index():
    if request.method == "POST":
        name = request.form.get("name")
        calories = request.form.get("product_calories")
        barcode = request.form.get("code")
        grams = request.form.get("grams")

        if not calories or not name or not barcode or not grams:
            flash("Fields cannot be empty!", "danger")
            return redirect("/")

        try:
            calories = int(float(calories))
            grams = int(float(grams))
        except ValueError:
            flash("Illegal Input! Must be type number.", "danger")
            return redirect("/")

        db.execute(
            "INSERT INTO foods (name, product_calories, consumed_calories, barcode, grams, user_id, calorie_goal) VALUES(?,?,?,?,?,?,?)",
            name,
            calories,
            (calories / 100) * grams,
            barcode,
            grams,
            session["user_id"],
            session["calorie_goal"],
        )
        flash("Entry Added!", "success")
        return redirect("/")
    else:
        foods = db.execute("SELECT * FROM foods WHERE user_id = ?", session["user_id"])

        # Calculate total calories for the day
        daily_calories = db.execute(
            "SELECT SUM(consumed_calories) AS daily_calories FROM foods WHERE user_id = ? AND DATE(created_at) = DATE('now')",
            session["user_id"],
        )

        weekly_calories = db.execute(
            "SELECT SUM(consumed_calories) AS weekly_calories FROM foods WHERE user_id = ? AND DATE(created_at) >= DATE('now', '-7 days')",
            session["user_id"],
        )

        return render_template(
            "index.html",
            foods=foods,
            daily_calories=daily_calories,
            weekly_calories=weekly_calories,
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

        calorie_goal = db.execute(
            "SELECT calorie_goal WHERE user_id = ?", users[0]["id"]
        )
        session["calorie_goal"] = calorie_goal[0]["calorie_goal"]
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
            flash("Email, password, and confirmation are required.", "waring")
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
            "fields": "product_name,brands,nutriments,image_front_small_url,code,quantity",
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
            flash(
                "The food database took too long to respond. Please try again.",
                "danger",
            )
            return redirect("/catalog")
        except requests.exceptions.HTTPError as e:
            flash(
                f"Food database returned an error (HTTP {e.response.status_code}). Please try again later.",
                "danger",
            )
            return redirect("/catalog")
        except requests.exceptions.RequestException:
            flash(
                "Could not reach the food database. Please try again later.", "danger"
            )
            return redirect("/catalog")

        print(f"Data: {data}")
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
                "SELECT sum(consumed_calories) as total_calories FROM foods WHERE user_id = ? AND date(created_at) = ?",
                session["user_id"],
                date,
            )

            if not total_calories:
                return render_template(
                    "history.html",
                    foods=products,
                    date=date,
                    total_calories=[{"total_calories": 0}],
                )

        except Exception as e:
            flash(
                f"Database encountered an error: {e}",
                "danger",
            )

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
            daily_calorie_goal = int(daily_calorie_goal_form)
        except ValueError:
            flash(
                "Input was not a number!",
                "danger",
            )
            return redirect("/preference")

        # Copilot helped with Syntax for ON CONFLICT and UPDATE
        db.execute(
            "UPDATE preferences SET calorie_goal = ? WHERE user_id = ?",
            daily_calorie_goal,
            session["user_id"],
        )
        session["calorie_goal"] = daily_calorie_goal

        print(session["calorie_goal"])

        return redirect("/preference")
    else:
        return render_template("preference.html")


@app.route("/delete_entry", methods=["POST"])
def delete():
    db.execute("DELETE FROM foods WHERE id = ?", request.form.get("entry_id"))
    flash("Entry Deleted", "success")
    next_page = request.form.get("next", "/")
    return redirect(next_page)
