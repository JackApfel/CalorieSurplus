# CS50 Final Project — Cheat Sheet

<!-- Assisted by GitHub Copilot while compiling this reference guide. -->
<!-- All examples are original patterns — adapt them to your own project and make sure you understand each one. -->

> **Academic Honesty Reminder:** This cheat sheet is a *learning aid*, not a copy-paste source.
> Understand every snippet before using it. Cite any external code you incorporate.
> See `.github/instructions/honesty.instructions.md` for the full policy.

---

## Table of Contents

1. [Flask](#1-flask)
2. [Jinja2 Templating](#2-jinja2-templating)
3. [Werkzeug Security](#3-werkzeug-security)
4. [CS50 Python Library](#4-cs50-python-library)
5. [SQLite3](#5-sqlite3)
6. [HTML](#6-html)
7. [CSS](#7-css)
8. [Bootstrap 5](#8-bootstrap-5)
9. [JavaScript](#9-javascript)
10. [Open Food Facts API](#10-open-food-facts-api)

---

## 1. Flask

> **Analogy:** Flask is the *waiter* in a restaurant. A customer (browser) places an order (HTTP request), the waiter carries it to the kitchen (your Python code), and brings back the dish (HTTP response).

### 1.1 Minimal App

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!"
```

- `Flask(__name__)` — creates the app. `__name__` tells Flask where to find templates/static files.
- `@app.route("/")` — a *decorator* that maps a URL path to a function.

### 1.2 Running the App

```bash
flask run          # production-like
flask run --debug  # auto-reload + debugger (development only)
```

### 1.3 Routes & Methods

```python
@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # handle form data
        ...
    else:
        # show the form
        return render_template("submit.html")
```

| Method | Purpose | Analogy |
|--------|---------|---------|
| `GET` | Fetch / read data | "Show me the menu" |
| `POST` | Send / write data | "Here's my order" |

### 1.4 `render_template`

Renders an HTML file from `templates/` and injects Python variables into it.

```python
from flask import render_template

@app.route("/greet")
def greet():
    name = "Alice"
    return render_template("greet.html", username=name)
```

Inside `greet.html` you'd use `{{ username }}` to display "Alice".

### 1.5 `request`

Access data the browser sent.

```python
from flask import request

# Form field (POST)
email = request.form.get("email")

# URL query parameter (GET)  — e.g. /search?q=apple
query = request.args.get("q")

# Check the HTTP method
if request.method == "POST":
    ...
```

### 1.6 `redirect`

Send the user to a different URL. Think of it as a "go to" for the browser.

```python
from flask import redirect

return redirect("/login")      # go to /login
return redirect("/")           # go home
```

### 1.7 `flash`

Show a one-time message on the *next* page the user sees — like a post-it note slipped into their pocket.

```python
from flask import flash

flash("Saved successfully!", "success")   # category = "success"
flash("Something went wrong.", "danger")  # category = "danger"
```

Retrieve them in templates (see Jinja section below).

### 1.8 `session`

A cookie-based dictionary that persists across requests for one user.

> **Analogy:** A wristband at a festival — the server recognizes you by it without you re-identifying yourself every time.

```python
from flask import session

# Store
session["user_id"] = 42

# Read
uid = session.get("user_id")   # returns None if missing

# Delete everything
session.clear()
```

**Requires a secret key:**

```python
import os
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
```

### 1.9 Decorators (protecting routes)

```python
from functools import wraps
from flask import session, redirect

def login_required(f):
    """Redirect to /login if the user is not signed in."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper
```

Usage:

```python
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
```

> **Analogy:** A bouncer at a club door — checks your ID (session) before letting you in.

### 1.10 Environment Variables with `python-dotenv`

```python
from dotenv import load_dotenv
import os

load_dotenv()                              # reads .env file
secret = os.environ.get("SECRET_KEY")      # use the value
```

`.env` file (never commit this):

```
SECRET_KEY=some-random-string
```

---

## 2. Jinja2 Templating

> **Analogy:** Jinja is a *mail merge* tool — you write a letter template with blanks, and Jinja fills in the blanks with data from Python.

### 2.1 Syntax Overview

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ ... }}` | Output a value | `{{ username }}` |
| `{% ... %}` | Logic / control flow | `{% if logged_in %}` |
| `{# ... #}` | Comment (not rendered) | `{# TODO: fix later #}` |

### 2.2 Variables & Filters

```html
<!-- Display a variable -->
<p>Hello, {{ name }}!</p>

<!-- Filters transform values (piped with |) -->
<p>{{ name | upper }}</p>              <!-- "ALICE" -->
<p>{{ price | round(2) }}</p>          <!-- 3.14 -->
<p>{{ description | default("N/A") }}</p>  <!-- fallback if None/empty -->
<p>{{ "<b>bold</b>" | e }}</p>         <!-- HTML-escaped output -->
```

**Chaining filters:**

```html
{{ product_name | default("Unknown") | upper }}
```

### 2.3 Conditionals

```html
{% if user %}
  <p>Welcome back, {{ user.name }}!</p>
{% elif guest %}
  <p>Hello, guest!</p>
{% else %}
  <p>Please log in.</p>
{% endif %}
```

### 2.4 Loops

```html
<ul>
{% for item in items %}
  <li>{{ item.name }} — {{ item.calories }} kcal</li>
{% endfor %}
</ul>
```

Useful loop variables:

| Variable | Meaning |
|----------|---------|
| `loop.index` | Current iteration (1-based) |
| `loop.index0` | Current iteration (0-based) |
| `loop.first` | `True` on first iteration |
| `loop.last` | `True` on last iteration |
| `loop.length` | Total number of items |

### 2.5 Template Inheritance

> **Analogy:** A *picture frame* (layout) that you can swap different *photos* (pages) into.

**layout.html** — the frame:

```html
<!doctype html>
<html>
<head>
  <title>{% block title %}My App{% endblock %}</title>
</head>
<body>
  <nav>...</nav>
  <main>
    {% block content %}{% endblock %}
  </main>
  <footer>...</footer>
</body>
</html>
```

**page.html** — the photo:

```html
{% extends "layout.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
  <h1>Dashboard</h1>
  <p>Your daily calories: {{ total }}</p>
{% endblock %}
```

### 2.6 Flash Messages in Templates

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">
        {{ message }}
      </div>
    {% endfor %}
  {% endif %}
{% endwith %}
```

### 2.7 Accessing Nested Data (Dicts)

```html
<!-- Python: item = {"product": {"nutriments": {"energy-kcal_100g": 250}}} -->

{{ item.product.nutriments['energy-kcal_100g'] | default('N/A') }}
```

Use bracket notation for keys containing hyphens or special characters.

---

## 3. Werkzeug Security

> **Analogy:** Werkzeug's password tools are like a *safe deposit box*. `generate_password_hash` locks the password away; `check_password_hash` verifies the key fits — but you can never open the box to read the password back.

### 3.1 Hashing a Password

```python
from werkzeug.security import generate_password_hash

hash_value = generate_password_hash("my_password")
# returns something like "scrypt:32768:8:1$salt$hash..."
```

- **Never store plain-text passwords.** Always store the hash.
- Each call produces a *different* hash (random salt), and that's fine.

### 3.2 Checking a Password

```python
from werkzeug.security import check_password_hash

if check_password_hash(stored_hash, user_input):
    print("Password matches!")
else:
    print("Wrong password.")
```

### 3.3 Typical Registration Flow

```python
password = request.form.get("password")
confirm  = request.form.get("confirm_password")

if password != confirm:
    flash("Passwords do not match.", "danger")
    return redirect("/register")

hashed = generate_password_hash(password)
db.execute("INSERT INTO users (email, hash) VALUES (?, ?)", email, hashed)
```

### 3.4 Typical Login Flow

```python
users = db.execute("SELECT * FROM users WHERE email = ?", email)

if not users:
    flash("Invalid email or password.", "danger")
    return redirect("/login")

if check_password_hash(users[0]["hash"], password):
    session["user_id"] = users[0]["id"]
    flash("Signed in!", "success")
    return redirect("/")
else:
    flash("Invalid email or password.", "danger")
    return redirect("/login")
```

> **Security tip:** Always give the same error for wrong email *and* wrong password — don't reveal which one was incorrect.

---

## 4. CS50 Python Library

> **Analogy:** The `cs50` library wraps SQLite in a user-friendly coat — like training wheels on a bicycle. You write SQL strings, but get Python dicts back instead of raw tuples.

### 4.1 Setup

```python
from cs50 import SQL

db = SQL("sqlite:///calories.db")
```

The `sqlite:///` prefix means "file in the current directory."  Three slashes = relative path.

### 4.2 SELECT — reading data

```python
# Returns a list of dicts
rows = db.execute("SELECT * FROM users WHERE email = ?", email)
# e.g. [{"id": 1, "email": "a@b.com", "hash": "..."}]

# Single item
if rows:
    user = rows[0]
    print(user["email"])
```

### 4.3 INSERT — adding data

```python
db.execute(
    "INSERT INTO foods (name, calories, user_id) VALUES (?, ?, ?)",
    "Apple", 95, session["user_id"]
)
```

Returns the `id` of the newly inserted row.

### 4.4 UPDATE — modifying data

```python
db.execute(
    "UPDATE foods SET calories = ? WHERE name = ? AND user_id = ?",
    100, "Apple", session["user_id"]
)
```

Returns the number of rows affected.

### 4.5 DELETE — removing data

```python
db.execute(
    "DELETE FROM foods WHERE name = ? AND user_id = ?",
    "Apple", session["user_id"]
)
```

### 4.6 Parameterized Queries (Security!)

**Always use `?` placeholders** — NEVER string concatenation or f-strings for SQL values.

```python
# SAFE — parameterized
db.execute("SELECT * FROM users WHERE email = ?", email)

# DANGEROUS — SQL injection risk!
# db.execute(f"SELECT * FROM users WHERE email = '{email}'")   # NEVER DO THIS
```

> **Analogy:** Placeholders are like sealed envelopes — the database reads the address on the outside (your query structure) and only opens the envelope (your data) safely inside, so nobody can tamper with the instructions.

---

## 5. SQLite3

> **Analogy:** SQLite is a *filing cabinet* stored in a single file on disk. Each *drawer* is a table, each *folder* is a row, and each *label* is a column.

### 5.1 Data Types

| SQLite Type | Meaning | Example |
|-------------|---------|---------|
| `INTEGER` | Whole number | `42` |
| `REAL` | Decimal | `3.14` |
| `TEXT` | String | `'Apple'` |
| `BLOB` | Binary data | images, files |
| `NULL` | No value | `NULL` |

### 5.2 CREATE TABLE

```sql
CREATE TABLE IF NOT EXISTS users (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT    NOT NULL,
    hash  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS foods (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT    NOT NULL,
    calories INTEGER NOT NULL,
    user_id  INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

- `PRIMARY KEY AUTOINCREMENT` — auto-generates a unique ID.
- `NOT NULL` — column must always have a value.
- `FOREIGN KEY` — links one table to another (like a cross-reference).

### 5.3 Common Queries

```sql
-- All foods for a user, sorted by name
SELECT * FROM foods WHERE user_id = 1 ORDER BY name ASC;

-- Total calories today
SELECT SUM(calories) AS total FROM foods WHERE user_id = 1;

-- Count of entries
SELECT COUNT(*) AS entries FROM foods WHERE user_id = 1;

-- Search by partial name
SELECT * FROM foods WHERE name LIKE '%apple%';

-- Update a value
UPDATE foods SET calories = 100 WHERE id = 5;

-- Delete a row
DELETE FROM foods WHERE id = 5;

-- Drop (destroy) a table
DROP TABLE IF EXISTS foods;
```

### 5.4 Useful Clauses

| Clause | Purpose | Example |
|--------|---------|---------|
| `WHERE` | Filter rows | `WHERE calories > 200` |
| `ORDER BY` | Sort results | `ORDER BY name ASC` |
| `LIMIT` | Cap results | `LIMIT 10` |
| `GROUP BY` | Aggregate groups | `GROUP BY user_id` |
| `HAVING` | Filter groups | `HAVING SUM(calories) > 2000` |
| `DISTINCT` | Remove duplicates | `SELECT DISTINCT name` |

### 5.5 JOINs

```sql
-- Get food entries with user email
SELECT foods.name, foods.calories, users.email
FROM foods
JOIN users ON foods.user_id = users.id
WHERE users.id = 1;
```

> **Analogy:** A JOIN is like stapling two related forms together — one from the "foods" drawer and one from the "users" drawer — wherever the user_id matches.

---

## 6. HTML

> **Analogy:** HTML is the *skeleton* of a web page — it defines the structure and bones. CSS adds the skin and clothes, JavaScript adds the muscles and movement.

### 6.1 Document Skeleton

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
</head>
<body>
    <!-- Visible content goes here -->
</body>
</html>
```

### 6.2 Common Elements

| Element | Purpose | Example |
|---------|---------|---------|
| `<h1>`–`<h6>` | Headings (1 = largest) | `<h1>Welcome</h1>` |
| `<p>` | Paragraph | `<p>Some text.</p>` |
| `<a>` | Link | `<a href="/about">About</a>` |
| `<img>` | Image | `<img src="photo.jpg" alt="A photo">` |
| `<ul>`, `<ol>` | Unordered / ordered list | `<ul><li>Item</li></ul>` |
| `<div>` | Generic block container | `<div>...</div>` |
| `<span>` | Generic inline container | `<span>...</span>` |
| `<table>` | Table | see below |
| `<form>` | User input form | see below |

### 6.3 Forms

```html
<form action="/login" method="post">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required>

    <label for="password">Password</label>
    <input type="password" id="password" name="password" required>

    <button type="submit">Sign In</button>
</form>
```

Key attributes:
- `action` — URL to send data to.
- `method` — `GET` (in URL) or `POST` (in body).
- `name` — the key used in `request.form.get("name")`.
- `required` — browser won't submit if empty.

### 6.4 Input Types

| Type | Renders | Example |
|------|---------|---------|
| `text` | Plain text box | `<input type="text">` |
| `email` | Email field (validated) | `<input type="email">` |
| `password` | Hidden characters | `<input type="password">` |
| `number` | Numeric spinner | `<input type="number" min="0">` |
| `hidden` | Invisible field | `<input type="hidden" name="id" value="5">` |
| `submit` | Submit button | `<input type="submit" value="Go">` |

### 6.5 Tables

```html
<table>
  <thead>
    <tr><th>Food</th><th>Calories</th></tr>
  </thead>
  <tbody>
    <tr><td>Apple</td><td>95</td></tr>
    <tr><td>Banana</td><td>105</td></tr>
  </tbody>
</table>
```

### 6.6 Semantic Elements

| Element | Meaning |
|---------|---------|
| `<header>` | Top section (logo, nav) |
| `<nav>` | Navigation links |
| `<main>` | Primary content |
| `<section>` | Thematic group |
| `<article>` | Self-contained content |
| `<footer>` | Bottom section |

---

## 7. CSS

> **Analogy:** If HTML is the skeleton, CSS is the *wardrobe*. It controls colors, spacing, fonts, and layout — how the skeleton is dressed up.

### 7.1 Three Ways to Add CSS

```html
<!-- 1. External file (recommended) -->
<link rel="stylesheet" href="/static/css/layout.css">

<!-- 2. Internal (in <head>) -->
<style>
  body { margin: 0; }
</style>

<!-- 3. Inline (on an element — avoid if possible) -->
<p style="color: red;">Alert!</p>
```

### 7.2 Selectors

```css
/* Element */
p { color: blue; }

/* Class (reusable) */
.card { border: 1px solid #ccc; }

/* ID (unique) */
#main-title { font-size: 2rem; }

/* Descendant */
nav a { text-decoration: none; }

/* Pseudo-class */
a:hover { color: red; }
```

### 7.3 Box Model

Every element is a box:

```
┌─────── margin ───────┐
│ ┌──── border ────┐   │
│ │ ┌─ padding ─┐  │   │
│ │ │  CONTENT   │  │   │
│ │ └────────────┘  │   │
│ └─────────────────┘   │
└───────────────────────┘
```

```css
.box {
    margin: 10px;       /* space outside */
    border: 1px solid;  /* the visible edge */
    padding: 15px;      /* space inside */
    width: 200px;
}
```

### 7.4 Flexbox (1D Layout)

> **Analogy:** Flexbox is a *shelf* — items line up in a row (or column) and you control spacing and alignment.

```css
.container {
    display: flex;
    justify-content: center;     /* horizontal alignment */
    align-items: center;         /* vertical alignment */
    gap: 10px;                   /* space between items */
}
```

| Property | Values | Effect |
|----------|--------|--------|
| `flex-direction` | `row`, `column` | Main axis direction |
| `justify-content` | `start`, `center`, `space-between`, `space-around` | Along main axis |
| `align-items` | `start`, `center`, `stretch` | Along cross axis |
| `flex-wrap` | `nowrap`, `wrap` | Allow wrapping |

### 7.5 Common Properties Quick Reference

```css
/* Typography */
font-family: Arial, sans-serif;
font-size: 1rem;
font-weight: bold;
text-align: center;
color: #333;

/* Backgrounds */
background-color: #f5f5f5;
background: linear-gradient(135deg, #667eea, #764ba2);

/* Sizing */
width: 100%;
max-width: 600px;
min-height: 100vh;

/* Rounded corners & shadow */
border-radius: 8px;
box-shadow: 0 2px 8px rgba(0,0,0,0.1);
```

---

## 8. Bootstrap 5

> **Analogy:** Bootstrap is a *wardrobe of pre-made outfits*. Instead of sewing CSS from scratch, you pick class names like `btn btn-primary` and the styling is done for you.

### 8.1 Setup (CDN)

```html
<!-- CSS in <head> -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet">

<!-- JS before </body> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js">
</script>
```

### 8.2 Grid System

Bootstrap's grid has **12 columns**. Think of it as slicing a pizza into 12 pieces.

```html
<div class="container">
  <div class="row">
    <div class="col-md-6">Left half</div>
    <div class="col-md-6">Right half</div>
  </div>
</div>
```

| Class | Width | Breakpoint |
|-------|-------|------------|
| `col` | Equal auto-width | All |
| `col-6` | 50% (6/12) | All |
| `col-sm-4` | 33% on ≥576px | Small |
| `col-md-6` | 50% on ≥768px | Medium |
| `col-lg-8` | 67% on ≥992px | Large |

### 8.3 Containers

```html
<div class="container">      <!-- fixed max-width, centered -->
<div class="container-fluid"> <!-- full-width -->
```

### 8.4 Buttons

```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-danger">Delete</button>
<button class="btn btn-outline-secondary">Cancel</button>
<button class="btn btn-success btn-sm">Small Green</button>
```

| Class | Color |
|-------|-------|
| `btn-primary` | Blue |
| `btn-secondary` | Gray |
| `btn-success` | Green |
| `btn-danger` | Red |
| `btn-warning` | Yellow |
| `btn-info` | Cyan |
| `btn-light` | Light |
| `btn-dark` | Dark |

### 8.5 Alerts

```html
<div class="alert alert-success alert-dismissible fade show" role="alert">
  Saved successfully!
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

### 8.6 Forms

```html
<form>
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control" id="email" name="email">
  </div>
  <div class="mb-3">
    <label for="pw" class="form-label">Password</label>
    <input type="password" class="form-control" id="pw" name="password">
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### 8.7 Navbar

```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">My App</a>
    <button class="navbar-toggler" type="button"
            data-bs-toggle="collapse" data-bs-target="#navContent">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navContent">
      <ul class="navbar-nav me-auto">
        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="/catalog">Catalog</a></li>
      </ul>
    </div>
  </div>
</nav>
```

### 8.8 Cards

```html
<div class="card" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">Apple</h5>
    <p class="card-text">95 kcal per serving</p>
    <a href="#" class="btn btn-primary">Add</a>
  </div>
</div>
```

### 8.8a Card with Image

Use `card-img-top` to place an image at the top of a card:

```html
<div class="card">
  <img src="https://example.com/photo.jpg" class="card-img-top" alt="Product photo">
  <div class="card-body">
    <h5 class="card-title">Banana</h5>
    <p class="card-text">105 kcal per serving</p>
    <a href="#" class="btn btn-primary">Add</a>
  </div>
</div>
```

- `card-img-top` — positions the image above the card body.
- Always include an `alt` attribute for accessibility.
- To keep images the same height, use CSS: `object-fit: contain; height: 200px;`.

### 8.8b Equal-Height Cards

When cards are in a grid, different content lengths make them unequal. Fix this with:

1. **`h-100`** on the `.card` — stretches the card to the full column height.
2. **`d-flex flex-column`** on `.card-body` — makes the body a flex column.
3. **`mt-auto`** on the button — pushes the button to the bottom.

```html
<div class="col">
  <div class="card h-100">
    <img src="..." class="card-img-top" alt="...">
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">Product Name</h5>
      <p class="card-text">Some details here...</p>
      <a href="#" class="btn btn-primary mt-auto">Add</a>
    </div>
  </div>
</div>
```

> **Why it works:** Bootstrap grid columns are equal height by default (Flexbox). `h-100` makes the card fill that height. `d-flex flex-column` + `mt-auto` pushes the button down so all buttons line up.

### 8.8c Responsive Card Grid with `row-cols-*`

Instead of fixed `row-cols-4`, use responsive breakpoints so cards stack on mobile and spread on desktop:

```html
<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-3">
  <!-- cards here -->
</div>
```

| Class | Breakpoint | Columns | Screen |
|-------|-----------|---------|--------|
| `row-cols-1` | default | 1 | Phones (< 576px) |
| `row-cols-sm-2` | >= 576px | 2 | Large phones / small tablets |
| `row-cols-md-3` | >= 768px | 3 | Tablets |
| `row-cols-lg-4` | >= 992px | 4 | Desktops |

- **`g-3`** adds a uniform gap (gutter) between cards both horizontally and vertically.
- `g-*` values go from `0` (no gap) to `5` (largest gap).

### 8.9 Spacing Utilities

Pattern: `{property}{side}-{size}`

| Letter | Property | Sides | Sizes |
|--------|----------|-------|-------|
| `m` | margin | `t` top, `b` bottom, `s` start, `e` end, `x` horizontal, `y` vertical | `0`–`5`, `auto` |
| `p` | padding | same as above | `0`–`5` |

```html
<div class="mt-3 mb-5 px-2">  <!-- margin-top 3, margin-bottom 5, padding-x 2 -->
```

### 8.10 Display & Flex Utilities

```html
<div class="d-flex justify-content-between align-items-center">
  <span>Left</span>
  <span>Right</span>
</div>

<div class="d-none d-md-block">  <!-- hidden on small, visible on medium+ -->
```

### 8.11 Tables

```html
<table class="table table-striped table-hover">
  <thead>
    <tr><th>Food</th><th>Calories</th></tr>
  </thead>
  <tbody>
    <tr><td>Banana</td><td>105</td></tr>
  </tbody>
</table>
```

---

## 9. JavaScript

> **Analogy:** If HTML is the skeleton and CSS is the clothing, JavaScript is the *nervous system* — it makes the page react to user input, fetch data, and update itself without reloading.

### 9.1 Where to Put It

```html
<!-- External file (recommended) — before </body> -->
<script src="/static/js/app.js"></script>

<!-- Inline -->
<script>
  console.log("Hello");
</script>
```

### 9.2 Variables

```js
const name = "Alice";    // constant — cannot reassign
let count = 0;           // mutable — can reassign
// var is older — prefer const/let
```

### 9.3 Functions

```js
// Declaration
function greet(name) {
    return `Hello, ${name}!`;
}

// Arrow function (shorter)
const greet = (name) => `Hello, ${name}!`;
```

### 9.4 DOM Manipulation

```js
// Select an element
const btn = document.querySelector("#my-button");
const items = document.querySelectorAll(".item");

// Change content
document.querySelector("#title").textContent = "New Title";
document.querySelector("#box").innerHTML = "<b>Bold</b>";

// Change style
document.querySelector("#box").style.display = "none";

// Add / remove classes
document.querySelector("#box").classList.add("active");
document.querySelector("#box").classList.remove("active");
document.querySelector("#box").classList.toggle("active");
```

### 9.5 Event Listeners

```js
document.querySelector("#my-button").addEventListener("click", function() {
    alert("Button clicked!");
});

// With arrow function
document.querySelector("form").addEventListener("submit", (event) => {
    event.preventDefault();   // stop normal form submission
    // do something custom
});
```

### 9.6 Fetch API (AJAX)

> **Analogy:** `fetch` is like sending a messenger to the server and getting a reply — all without reloading the page.

```js
// GET request
fetch("/api/foods")
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error("Error:", error);
    });

// POST request
fetch("/api/foods", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: "Apple", calories: 95 })
})
.then(response => response.json())
.then(data => console.log(data));
```

### 9.7 Async / Await (cleaner fetch)

```js
async function loadFoods() {
    try {
        const response = await fetch("/api/foods");
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Error:", error);
    }
}
```

### 9.8 Useful Array Methods

```js
const nums = [1, 2, 3, 4, 5];

nums.forEach(n => console.log(n));           // loop
const doubled = nums.map(n => n * 2);        // [2, 4, 6, 8, 10]
const even = nums.filter(n => n % 2 === 0);  // [2, 4]
const sum = nums.reduce((a, b) => a + b, 0); // 15
const found = nums.find(n => n > 3);         // 4
```

### 9.9 Template Literals

```js
const name = "Apple";
const cal = 95;
const msg = `${name} has ${cal} calories.`;  // "Apple has 95 calories."
```

---

## 10. Open Food Facts API

> **Analogy:** Open Food Facts is a *free public library of food labels*. You give it a barcode (library card number) and it returns the nutrition facts page for that product.

**Base URL:** `https://world.openfoodfacts.org/api/v2/`

**Docs:** https://openfoodfacts.github.io/openfoodfacts-server/api/

### 10.1 Get a Product by Barcode

```
GET https://world.openfoodfacts.org/api/v2/product/{barcode}.json
```

#### Python Example

```python
import requests

barcode = "3274080005003"
url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

headers = {
    "User-Agent": "YourAppName/0.1 your-email@example.com"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()  # raise an error on 4xx/5xx
data = response.json()
```

> **Important:** Always include a descriptive `User-Agent` header — it's required by the API's terms.

### 10.2 Response Structure

The response is a JSON object. Key fields live under `data["product"]`:

| Path | Description | Example |
|------|-------------|---------|
| `product.product_name` | Product name | `"Nutella"` |
| `product.product_name_en` | English name | `"Nutella"` |
| `product.brands` | Brand | `"Ferrero"` |
| `product.nutriments.energy-kcal_100g` | Calories per 100g | `539` |
| `product.nutriments.fat_100g` | Fat per 100g | `30.9` |
| `product.nutriments.carbohydrates_100g` | Carbs per 100g | `57.5` |
| `product.nutriments.proteins_100g` | Protein per 100g | `6.3` |
| `product.nutriments.sugars_100g` | Sugars per 100g | `56.3` |
| `product.nutriments.salt_100g` | Salt per 100g | `0.107` |
| `product.nutriments.fiber_100g` | Fiber per 100g | `0` |
| `product.serving_size` | Serving size string | `"15 g"` |
| `product.image_url` | Product photo URL | `"https://..."` |
| `product.image_front_small_url` | Small thumbnail URL | `"https://..."` |
| `product.nutriscore_grade` | Nutri-Score (a–e) | `"e"` |
| `product.categories_tags` | Categories list | `["en:spreads", ...]` |
| `status` | `1` = found, `0` = not found | `1` |

### 10.3 Search by Name

```
GET https://world.openfoodfacts.org/cgi/search.pl?search_terms=banana&json=true&page_size=5
```

#### Python Example

```python
params = {
    "search_terms": "banana",
    "json": "true",
    "page_size": 5
}
url = "https://world.openfoodfacts.org/cgi/search.pl"

response = requests.get(url, params=params, headers=headers, timeout=10)
data = response.json()

for product in data.get("products", []):
    name = product.get("product_name", "Unknown")
    kcal = product.get("nutriments", {}).get("energy-kcal_100g", "N/A")
    print(f"{name}: {kcal} kcal/100g")
```

### 10.4 Handling Missing Data Safely

Not every product has every field. Always use `.get()` with defaults:

```python
product = data.get("product", {})
name    = product.get("product_name", "Unknown")
kcal    = product.get("nutriments", {}).get("energy-kcal_100g", 0)
brand   = product.get("brands", "Unknown brand")
```

In Jinja:

```html
{{ item.product.product_name | default("Unknown") }}
{{ item.product.nutriments['energy-kcal_100g'] | default('N/A') }}
```

### 10.5 Checking If a Product Was Found

```python
data = response.json()

if data.get("status") == 1:
    product = data["product"]
    # use product data
else:
    flash("Product not found.", "warning")
```

### 10.6 Error Handling

```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    flash("The request timed out. Try again.", "danger")
except requests.exceptions.HTTPError as e:
    flash(f"API error: {e}", "danger")
except requests.exceptions.RequestException as e:
    flash(f"Network error: {e}", "danger")
```

### 10.7 Full Flask Route Example

```python
@app.route("/lookup")
@login_required
def lookup():
    barcode = request.args.get("barcode", "").strip()
    if not barcode:
        flash("Please enter a barcode.", "warning")
        return redirect("/catalog")

    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    headers = {"User-Agent": "KalorienZaehler/0.1 your-email@example.com"}

    try:
        api_resp = requests.get(url, headers=headers, timeout=10)
        api_resp.raise_for_status()
        data = api_resp.json()
    except requests.exceptions.RequestException:
        flash("Could not reach the food database.", "danger")
        return redirect("/catalog")

    if data.get("status") != 1:
        flash("Product not found.", "warning")
        return redirect("/catalog")

    return render_template("product.html", product=data["product"])
```

---

## Quick Reference Card

| Task | Tool | Key Function / Syntax |
|------|------|-----------------------|
| Serve a web page | Flask | `render_template("page.html", var=val)` |
| Read form input | Flask | `request.form.get("field")` |
| Read URL params | Flask | `request.args.get("key")` |
| Redirect user | Flask | `redirect("/path")` |
| Show flash message | Flask | `flash("msg", "category")` |
| Remember user | Flask | `session["user_id"] = id` |
| Hash password | Werkzeug | `generate_password_hash(pw)` |
| Verify password | Werkzeug | `check_password_hash(hash, pw)` |
| Run a SQL query | CS50 | `db.execute("SELECT ...", param)` |
| Output variable | Jinja | `{{ variable }}` |
| Conditional | Jinja | `{% if ... %}...{% endif %}` |
| Loop | Jinja | `{% for x in items %}...{% endfor %}` |
| Inherit layout | Jinja | `{% extends "layout.html" %}` |
| Fetch API data | Python | `requests.get(url, headers=h, timeout=10)` |
| Parse JSON | Python | `response.json()` |
| Handle missing keys | Python / Jinja | `.get("key", default)` / `\| default("N/A")` |

---

*This cheat sheet was compiled as a learning reference for the CS50 final project "Kalorien Zähler."*
*Assisted by GitHub Copilot. All snippets are generic patterns — adapt and understand them before use.*
