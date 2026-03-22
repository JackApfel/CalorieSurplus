# CS50 Final Project — Spickzettel

<!-- Assisted by GitHub Copilot while translating this reference guide to German. -->
<!-- Alle Beispiele sind allgemeine Muster — passe sie an dein eigenes Projekt an und stelle sicher, dass du sie verstehst. -->

> **Hinweis zur Academic Honesty:** Dieser Spickzettel ist eine *Lernhilfe*, keine Copy-Paste-Quelle.
> Verstehe jedes Snippet, bevor du es benutzt. Zitiere externen Code, den du einbaust.
> Siehe `.github/instructions/honesty.instructions.md` fuer die vollstaendige Richtlinie.

---

## Inhaltsverzeichnis

1. [Flask](#1-flask)
2. [Jinja2-Templating](#2-jinja2-templating)
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

> **Analogie:** Flask ist der *Kellner* im Restaurant. Ein Kunde (Browser) gibt eine Bestellung auf (HTTP-Request), der Kellner bringt sie in die Kueche (dein Python-Code) und bringt das Gericht zurueck (HTTP-Response).

### 1.1 Minimale App

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!"
```

- `Flask(__name__)` — erstellt die App. `__name__` sagt Flask, wo Templates/Static Files liegen.
- `@app.route("/")` — ein *Decorator*, der einen URL-Pfad auf eine Funktion mappt.

### 1.2 App starten

```bash
flask run          # produktionsnah
flask run --debug  # Auto-Reload + Debugger (nur Entwicklung)
```

### 1.3 Routen & Methoden

```python
@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # Formulardaten verarbeiten
        ...
    else:
        # Formular anzeigen
        return render_template("submit.html")
```

| Methode | Zweck | Analogie |
|--------|-------|----------|
| `GET` | Daten abrufen/lesen | "Zeig mir die Speisekarte" |
| `POST` | Daten senden/schreiben | "Hier ist meine Bestellung" |

### 1.4 `render_template`

Rendert eine HTML-Datei aus `templates/` und setzt Python-Variablen ein.

```python
from flask import render_template

@app.route("/greet")
def greet():
    name = "Alice"
    return render_template("greet.html", username=name)
```

In `greet.html` benutzt du `{{ username }}`, um "Alice" anzuzeigen.

### 1.5 `request`

Greift auf Daten zu, die der Browser gesendet hat.

```python
from flask import request

# Formularfeld (POST)
email = request.form.get("email")

# URL-Query-Parameter (GET)  — z. B. /search?q=apple
query = request.args.get("q")

# HTTP-Methode pruefen
if request.method == "POST":
    ...
```

### 1.6 `redirect`

Leitet den User auf eine andere URL um. Wie ein "go to" fuer den Browser.

```python
from flask import redirect

return redirect("/login")      # zu /login
return redirect("/")           # nach Hause
```

### 1.7 `flash`

Zeigt eine einmalige Nachricht auf der *naechsten* Seite an.

```python
from flask import flash

flash("Saved successfully!", "success")   # Kategorie = "success"
flash("Something went wrong.", "danger")  # Kategorie = "danger"
```

In Templates kannst du diese Meldungen ausgeben (siehe Jinja-Bereich).

### 1.8 `session`

Ein Cookie-basiertes Dictionary, das ueber Requests hinweg pro User erhalten bleibt.

> **Analogie:** Ein Festival-Armband — der Server erkennt dich wieder, ohne dass du dich bei jedem Schritt neu identifizieren musst.

```python
from flask import session

# Speichern
session["user_id"] = 42

# Lesen
uid = session.get("user_id")   # gibt None zurueck, wenn nicht vorhanden

# Alles loeschen
session.clear()
```

**Braucht einen Secret Key:**

```python
import os
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
```

### 1.9 Decorators (Routen schuetzen)

```python
from functools import wraps
from flask import session, redirect

def login_required(f):
    """Leitet auf /login um, falls der User nicht eingeloggt ist."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper
```

Nutzung:

```python
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
```

> **Analogie:** Ein Tuersteher im Club — er checkt deinen Ausweis (Session), bevor du rein darfst.

### 1.10 Umgebungsvariablen mit `python-dotenv`

```python
from dotenv import load_dotenv
import os

load_dotenv()                              # liest .env-Datei
secret = os.environ.get("SECRET_KEY")      # Wert verwenden
```

`.env`-Datei (niemals committen):

```
SECRET_KEY=some-random-string
```

---

## 2. Jinja2-Templating

> **Analogie:** Jinja ist wie ein *Serienbrief*. Du schreibst eine Vorlage mit Platzhaltern, und Jinja fuellt sie mit Daten aus Python.

### 2.1 Syntax-Ueberblick

| Syntax | Zweck | Beispiel |
|--------|------|----------|
| `{{ ... }}` | Wert ausgeben | `{{ username }}` |
| `{% ... %}` | Logik / Kontrollfluss | `{% if logged_in %}` |
| `{# ... #}` | Kommentar (wird nicht gerendert) | `{# TODO: fix later #}` |

### 2.2 Variablen & Filter

```html
<!-- Variable ausgeben -->
<p>Hello, {{ name }}!</p>

<!-- Filter transformieren Werte (mit |) -->
<p>{{ name | upper }}</p>              <!-- "ALICE" -->
<p>{{ price | round(2) }}</p>          <!-- 3.14 -->
<p>{{ description | default("N/A") }}</p>  <!-- Fallback bei None/leer -->
<p>{{ "<b>bold</b>" | e }}</p>         <!-- HTML-escaped Ausgabe -->
```

**Filter kombinieren:**

```html
{{ product_name | default("Unknown") | upper }}
```

### 2.3 Bedingungen

```html
{% if user %}
  <p>Welcome back, {{ user.name }}!</p>
{% elif guest %}
  <p>Hello, guest!</p>
{% else %}
  <p>Please log in.</p>
{% endif %}
```

### 2.4 Schleifen

```html
<ul>
{% for item in items %}
  <li>{{ item.name }} — {{ item.calories }} kcal</li>
{% endfor %}
</ul>
```

Nuetzliche Loop-Variablen:

| Variable | Bedeutung |
|----------|-----------|
| `loop.index` | Aktuelle Iteration (1-basiert) |
| `loop.index0` | Aktuelle Iteration (0-basiert) |
| `loop.first` | `True` in der ersten Iteration |
| `loop.last` | `True` in der letzten Iteration |
| `loop.length` | Gesamtanzahl der Elemente |

### 2.5 Template Inheritance

> **Analogie:** Ein *Bilderrahmen* (`layout`) mit austauschbaren *Bildern* (Seiteninhalt).

**layout.html** — der Rahmen:

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

**page.html** — das Bild:

```html
{% extends "layout.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
  <h1>Dashboard</h1>
  <p>Your daily calories: {{ total }}</p>
{% endblock %}
```

### 2.6 Flash-Messages im Template

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

### 2.7 Verschachtelte Daten (Dicts) ansprechen

```html
<!-- Python: item = {"product": {"nutriments": {"energy-kcal_100g": 250}}} -->

{{ item.product.nutriments['energy-kcal_100g'] | default('N/A') }}
```

Nutze Klammer-Syntax bei Schluesseln mit Bindestrich/Sonderzeichen.

---

## 3. Werkzeug Security

> **Analogie:** Die Passwort-Tools aus Werkzeug sind wie ein *Bankschliessfach*. `generate_password_hash` schliesst das Passwort sicher weg, `check_password_hash` prueft nur den passenden Schluessel.

### 3.1 Passwort hashen

```python
from werkzeug.security import generate_password_hash

hash_value = generate_password_hash("my_password")
# ergibt etwa "scrypt:32768:8:1$salt$hash..."
```

- **Nie Klartext-Passwoerter speichern.** Immer nur den Hash speichern.
- Jeder Aufruf erzeugt wegen Salt einen anderen Hash, das ist korrekt.

### 3.2 Passwort pruefen

```python
from werkzeug.security import check_password_hash

if check_password_hash(stored_hash, user_input):
    print("Password matches!")
else:
    print("Wrong password.")
```

### 3.3 Typischer Registrierungs-Flow

```python
password = request.form.get("password")
confirm  = request.form.get("confirm_password")

if password != confirm:
    flash("Passwords do not match.", "danger")
    return redirect("/register")

hashed = generate_password_hash(password)
db.execute("INSERT INTO users (email, hash) VALUES (?, ?)", email, hashed)
```

### 3.4 Typischer Login-Flow

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

> **Security-Tipp:** Fuer falsche E-Mail und falsches Passwort dieselbe Fehlermeldung zeigen.

---

## 4. CS50 Python Library

> **Analogie:** Die `cs50`-Library ist wie Stuetzraeder fuers Fahrrad. Du schreibst SQL-Strings, bekommst aber bequeme Python-Dicts zurueck.

### 4.1 Setup

```python
from cs50 import SQL

db = SQL("sqlite:///calories.db")
```

`sqlite:///` bedeutet Datei im aktuellen Verzeichnis (3 Slashes = relativ).

### 4.2 SELECT — Daten lesen

```python
# Gibt eine Liste von Dicts zurueck
rows = db.execute("SELECT * FROM users WHERE email = ?", email)
# z. B. [{"id": 1, "email": "a@b.com", "hash": "..."}]

# Einzelnes Element
if rows:
    user = rows[0]
    print(user["email"])
```

### 4.3 INSERT — Daten einfuegen

```python
db.execute(
    "INSERT INTO foods (name, calories, user_id) VALUES (?, ?, ?)",
    "Apple", 95, session["user_id"]
)
```

Gibt die `id` der neuen Zeile zurueck.

### 4.4 UPDATE — Daten aendern

```python
db.execute(
    "UPDATE foods SET calories = ? WHERE name = ? AND user_id = ?",
    100, "Apple", session["user_id"]
)
```

Gibt die Anzahl betroffener Zeilen zurueck.

### 4.5 DELETE — Daten loeschen

```python
db.execute(
    "DELETE FROM foods WHERE name = ? AND user_id = ?",
    "Apple", session["user_id"]
)
```

### 4.6 Parameterisierte Queries (Sicherheit!)

**Immer `?` Platzhalter verwenden** — niemals String-Konkatenation oder f-Strings fuer SQL-Werte.

```python
# SICHER — parameterisiert
db.execute("SELECT * FROM users WHERE email = ?", email)

# GEFAEHRLICH — SQL-Injection-Risiko!
# db.execute(f"SELECT * FROM users WHERE email = '{email}'")   # NIE SO
```

> **Analogie:** Platzhalter sind wie versiegelte Umschlaege. Die Datenbank trennt Struktur (Query) und Inhalt (Werte) sauber.

---

## 5. SQLite3

> **Analogie:** SQLite ist ein *Aktenschrank* in einer einzigen Datei. Jede Tabelle ist eine Schublade, jede Zeile ein Vorgang, jede Spalte ein Label.

### 5.1 Datentypen

| SQLite-Typ | Bedeutung | Beispiel |
|------------|-----------|----------|
| `INTEGER` | Ganze Zahl | `42` |
| `REAL` | Kommazahl | `3.14` |
| `TEXT` | String | `'Apple'` |
| `BLOB` | Binaerdaten | Bilder, Dateien |
| `NULL` | Kein Wert | `NULL` |

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

- `PRIMARY KEY AUTOINCREMENT` — erzeugt automatisch eindeutige IDs.
- `NOT NULL` — Spalte muss immer einen Wert haben.
- `FOREIGN KEY` — verknuepft Tabellen untereinander.

### 5.3 Haeufige Queries

```sql
-- Alle Foods eines Users, alphabetisch sortiert
SELECT * FROM foods WHERE user_id = 1 ORDER BY name ASC;

-- Gesamtkalorien heute
SELECT SUM(calories) AS total FROM foods WHERE user_id = 1;

-- Anzahl Eintraege
SELECT COUNT(*) AS entries FROM foods WHERE user_id = 1;

-- Teilstring-Suche
SELECT * FROM foods WHERE name LIKE '%apple%';

-- Wert updaten
UPDATE foods SET calories = 100 WHERE id = 5;

-- Zeile loeschen
DELETE FROM foods WHERE id = 5;

-- Tabelle droppen
DROP TABLE IF EXISTS foods;
```

### 5.4 Nuetzliche Clauses

| Clause | Zweck | Beispiel |
|--------|------|----------|
| `WHERE` | Zeilen filtern | `WHERE calories > 200` |
| `ORDER BY` | Ergebnisse sortieren | `ORDER BY name ASC` |
| `LIMIT` | Anzahl begrenzen | `LIMIT 10` |
| `GROUP BY` | Gruppen aggregieren | `GROUP BY user_id` |
| `HAVING` | Gruppen filtern | `HAVING SUM(calories) > 2000` |
| `DISTINCT` | Duplikate entfernen | `SELECT DISTINCT name` |

### 5.5 JOINs

```sql
-- Food-Eintraege mit User-E-Mail
SELECT foods.name, foods.calories, users.email
FROM foods
JOIN users ON foods.user_id = users.id
WHERE users.id = 1;
```

> **Analogie:** Ein JOIN ist wie zwei zusammengeheftete Formulare, wenn `user_id` und `id` zusammenpassen.

---

## 6. HTML

> **Analogie:** HTML ist das *Skelett* einer Webseite. CSS ist Aussehen/Kleidung, JavaScript ist Verhalten/Bewegung.

### 6.1 Dokument-Grundgeruest

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
</head>
<body>
    <!-- Sichtbarer Inhalt -->
</body>
</html>
```

### 6.2 Haeufige Elemente

| Element | Zweck | Beispiel |
|---------|-------|----------|
| `<h1>`–`<h6>` | Ueberschriften | `<h1>Welcome</h1>` |
| `<p>` | Absatz | `<p>Some text.</p>` |
| `<a>` | Link | `<a href="/about">About</a>` |
| `<img>` | Bild | `<img src="photo.jpg" alt="A photo">` |
| `<ul>`, `<ol>` | Unsortierte/sortierte Liste | `<ul><li>Item</li></ul>` |
| `<div>` | Generischer Block-Container | `<div>...</div>` |
| `<span>` | Generischer Inline-Container | `<span>...</span>` |
| `<table>` | Tabelle | siehe unten |
| `<form>` | Benutzereingaben | siehe unten |

### 6.3 Formulare

```html
<form action="/login" method="post">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required>

    <label for="password">Password</label>
    <input type="password" id="password" name="password" required>

    <button type="submit">Sign In</button>
</form>
```

Wichtige Attribute:
- `action` — URL fuer das Senden der Daten.
- `method` — `GET` (in URL) oder `POST` (im Body).
- `name` — Key fuer `request.form.get("name")`.
- `required` — Browser blockiert leeres Abschicken.

### 6.4 Input-Typen

| Typ | Darstellung | Beispiel |
|-----|-------------|----------|
| `text` | Textfeld | `<input type="text">` |
| `email` | E-Mail-Feld | `<input type="email">` |
| `password` | Verdeckte Zeichen | `<input type="password">` |
| `number` | Zahlenfeld | `<input type="number" min="0">` |
| `hidden` | Unsichtbares Feld | `<input type="hidden" name="id" value="5">` |
| `submit` | Senden-Button | `<input type="submit" value="Go">` |

### 6.5 Tabellen

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

### 6.6 Semantische Elemente

| Element | Bedeutung |
|---------|-----------|
| `<header>` | Kopfbereich |
| `<nav>` | Navigation |
| `<main>` | Hauptinhalt |
| `<section>` | Thematischer Abschnitt |
| `<article>` | Eigenstaendiger Inhalt |
| `<footer>` | Fussbereich |

---

## 7. CSS

> **Analogie:** Wenn HTML das Skelett ist, ist CSS die *Garderobe*. Es steuert Farben, Abstaende, Schrift und Layout.

### 7.1 Drei Wege, CSS einzubinden

```html
<!-- 1. Externe Datei (empfohlen) -->
<link rel="stylesheet" href="/static/css/layout.css">

<!-- 2. Intern (im <head>) -->
<style>
  body { margin: 0; }
</style>

<!-- 3. Inline (am Element — moeglichst vermeiden) -->
<p style="color: red;">Alert!</p>
```

### 7.2 Selektoren

```css
/* Element */
p { color: blue; }

/* Klasse (wiederverwendbar) */
.card { border: 1px solid #ccc; }

/* ID (einzigartig) */
#main-title { font-size: 2rem; }

/* Nachfahre */
nav a { text-decoration: none; }

/* Pseudoklasse */
a:hover { color: red; }
```

### 7.3 Box Model

Jedes Element ist eine Box:

```
+------- margin -------+
| +---- border ----+   |
| | +- padding -+ |    |
| | | CONTENT   | |    |
| | +-----------+ |    |
| +---------------+    |
+----------------------+
```

```css
.box {
    margin: 10px;       /* Abstand aussen */
    border: 1px solid;  /* sichtbarer Rand */
    padding: 15px;      /* Abstand innen */
    width: 200px;
}
```

### 7.4 Flexbox (1D-Layout)

> **Analogie:** Flexbox ist wie ein *Regal* — Elemente stehen in einer Reihe/Spalte, und du steuerst Ausrichtung/Abstand.

```css
.container {
    display: flex;
    justify-content: center;     /* horizontale Ausrichtung */
    align-items: center;         /* vertikale Ausrichtung */
    gap: 10px;                   /* Abstand zwischen Items */
}
```

| Property | Werte | Effekt |
|----------|-------|--------|
| `flex-direction` | `row`, `column` | Hauptrichtung |
| `justify-content` | `start`, `center`, `space-between`, `space-around` | Auf Hauptachse |
| `align-items` | `start`, `center`, `stretch` | Auf Querachse |
| `flex-wrap` | `nowrap`, `wrap` | Umbruch erlauben |

### 7.5 Haeufige CSS-Properties

```css
/* Typografie */
font-family: Arial, sans-serif;
font-size: 1rem;
font-weight: bold;
text-align: center;
color: #333;

/* Hintergruende */
background-color: #f5f5f5;
background: linear-gradient(135deg, #667eea, #764ba2);

/* Groesse */
width: 100%;
max-width: 600px;
min-height: 100vh;

/* Abgerundete Ecken & Schatten */
border-radius: 8px;
box-shadow: 0 2px 8px rgba(0,0,0,0.1);
```

---

## 8. Bootstrap 5

> **Analogie:** Bootstrap ist ein *Kleiderschrank mit fertigen Outfits*. Statt alles selbst zu stylen, nutzt du Klassen wie `btn btn-primary`.

### 8.1 Setup (CDN)

```html
<!-- CSS im <head> -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet">

<!-- JS vor </body> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js">
</script>
```

### 8.2 Grid-System

Das Bootstrap-Grid hat **12 Spalten**.

```html
<div class="container">
  <div class="row">
    <div class="col-md-6">Left half</div>
    <div class="col-md-6">Right half</div>
  </div>
</div>
```

| Klasse | Breite | Breakpoint |
|--------|--------|------------|
| `col` | gleichmaessig automatisch | alle |
| `col-6` | 50% (6/12) | alle |
| `col-sm-4` | 33% ab >=576px | Small |
| `col-md-6` | 50% ab >=768px | Medium |
| `col-lg-8` | 67% ab >=992px | Large |

### 8.3 Container

```html
<div class="container">       <!-- feste max-width, zentriert -->
<div class="container-fluid"> <!-- volle Breite -->
```

### 8.4 Buttons

```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-danger">Delete</button>
<button class="btn btn-outline-secondary">Cancel</button>
<button class="btn btn-success btn-sm">Small Green</button>
```

| Klasse | Farbe |
|--------|-------|
| `btn-primary` | Blau |
| `btn-secondary` | Grau |
| `btn-success` | Gruen |
| `btn-danger` | Rot |
| `btn-warning` | Gelb |
| `btn-info` | Cyan |
| `btn-light` | Hell |
| `btn-dark` | Dunkel |

### 8.5 Alerts

```html
<div class="alert alert-success alert-dismissible fade show" role="alert">
  Saved successfully!
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

### 8.6 Formulare

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

### 8.8a Card mit Bild

Mit `card-img-top` platzierst du ein Bild oben in der Card:

```html
<div class="card">
  <img src="https://example.com/foto.jpg" class="card-img-top" alt="Produktfoto">
  <div class="card-body">
    <h5 class="card-title">Banana</h5>
    <p class="card-text">105 kcal pro Portion</p>
    <a href="#" class="btn btn-primary">Hinzufuegen</a>
  </div>
</div>
```

- `card-img-top` — positioniert das Bild ueber dem Card-Body.
- Immer ein `alt`-Attribut fuer Barrierefreiheit setzen.
- Um Bilder gleich hoch zu halten, nutze CSS: `object-fit: contain; height: 200px;`.

### 8.8b Gleich hohe Cards

Wenn Cards im Grid unterschiedlich viel Text haben, werden sie verschieden hoch. Loesung:

1. **`h-100`** auf der `.card` — streckt die Card auf die volle Spaltenhoehe.
2. **`d-flex flex-column`** auf `.card-body` — macht den Body zur Flex-Spalte.
3. **`mt-auto`** auf dem Button — schiebt den Button nach unten.

```html
<div class="col">
  <div class="card h-100">
    <img src="..." class="card-img-top" alt="...">
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">Produktname</h5>
      <p class="card-text">Einige Details hier...</p>
      <a href="#" class="btn btn-primary mt-auto">Hinzufuegen</a>
    </div>
  </div>
</div>
```

> **Warum das funktioniert:** Bootstrap-Grid-Spalten sind standardmaessig gleich hoch (dank Flexbox). `h-100` laesst die Card diese Hoehe ausfuellen. `d-flex flex-column` + `mt-auto` drueckt den Button nach unten, sodass alle Buttons auf gleicher Linie stehen.

### 8.8c Responsives Card-Grid mit `row-cols-*`

Statt fixem `row-cols-4` nutze responsive Breakpoints, damit Cards auf dem Handy untereinander und auf dem Desktop nebeneinander stehen:

```html
<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-3">
  <!-- Cards hier -->
</div>
```

| Klasse | Breakpoint | Spalten | Bildschirm |
|--------|-----------|---------|------------|
| `row-cols-1` | Standard | 1 | Handys (< 576px) |
| `row-cols-sm-2` | >= 576px | 2 | Grosse Handys / kleine Tablets |
| `row-cols-md-3` | >= 768px | 3 | Tablets |
| `row-cols-lg-4` | >= 992px | 4 | Desktops |

- **`g-3`** fuegt gleichmaessige Abstaende (Gutters) zwischen Cards hinzu, horizontal und vertikal.
- `g-*` Werte gehen von `0` (kein Abstand) bis `5` (groesster Abstand).

### 8.9 Spacing-Utilities

Muster: `{property}{side}-{size}`

| Buchstabe | Property | Seiten | Groessen |
|-----------|----------|--------|----------|
| `m` | margin | `t` top, `b` bottom, `s` start, `e` end, `x` horizontal, `y` vertikal | `0`–`5`, `auto` |
| `p` | padding | wie oben | `0`–`5` |

```html
<div class="mt-3 mb-5 px-2">  <!-- margin-top 3, margin-bottom 5, padding-x 2 -->
```

### 8.10 Display- & Flex-Utilities

```html
<div class="d-flex justify-content-between align-items-center">
  <span>Left</span>
  <span>Right</span>
</div>

<div class="d-none d-md-block">  <!-- auf klein versteckt, ab md sichtbar -->
```

### 8.11 Tabellen

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

> **Analogie:** Wenn HTML das Skelett und CSS die Kleidung ist, ist JavaScript das *Nervensystem*.

### 9.1 Wo JavaScript hin soll

```html
<!-- Externe Datei (empfohlen) — vor </body> -->
<script src="/static/js/app.js"></script>

<!-- Inline -->
<script>
  console.log("Hello");
</script>
```

### 9.2 Variablen

```js
const name = "Alice";    // konstant — nicht neu zuweisen
let count = 0;           // veraenderbar — neu zuweisbar
// var ist aelter — lieber const/let
```

### 9.3 Funktionen

```js
// Deklaration
function greet(name) {
    return `Hello, ${name}!`;
}

// Arrow Function (kuerzer)
const greet = (name) => `Hello, ${name}!`;
```

### 9.4 DOM-Manipulation

```js
// Element auswaehlen
const btn = document.querySelector("#my-button");
const items = document.querySelectorAll(".item");

// Inhalt aendern
document.querySelector("#title").textContent = "New Title";
document.querySelector("#box").innerHTML = "<b>Bold</b>";

// Style aendern
document.querySelector("#box").style.display = "none";

// Klassen hinzufuegen/entfernen
document.querySelector("#box").classList.add("active");
document.querySelector("#box").classList.remove("active");
document.querySelector("#box").classList.toggle("active");
```

### 9.5 Event Listener

```js
document.querySelector("#my-button").addEventListener("click", function() {
    alert("Button clicked!");
});

// Mit Arrow Function
document.querySelector("form").addEventListener("submit", (event) => {
    event.preventDefault();   // normales Absenden stoppen
    // eigene Logik
});
```

### 9.6 Fetch API (AJAX)

> **Analogie:** `fetch` ist wie ein Bote: Anfrage zum Server, Antwort zurueck, ohne Seiten-Reload.

```js
// GET-Request
fetch("/api/foods")
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error("Error:", error);
    });

// POST-Request
fetch("/api/foods", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: "Apple", calories: 95 })
})
.then(response => response.json())
.then(data => console.log(data));
```

### 9.7 Async / Await

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

### 9.8 Nuetzliche Array-Methoden

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

> **Analogie:** Open Food Facts ist wie eine *freie Bibliothek fuer Lebensmitteletiketten*. Du gibst einen Barcode, und bekommst Naehrwertinformationen zum Produkt.

**Basis-URL:** `https://world.openfoodfacts.org/api/v2/`

**Dokumentation:** https://openfoodfacts.github.io/openfoodfacts-server/api/

### 10.1 Produkt per Barcode abrufen

```
GET https://world.openfoodfacts.org/api/v2/product/{barcode}.json
```

#### Python-Beispiel

```python
import requests

barcode = "3274080005003"
url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

headers = {
    "User-Agent": "YourAppName/0.1 your-email@example.com"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()  # Fehler bei 4xx/5xx werfen
data = response.json()
```

> **Wichtig:** Immer einen sinnvollen `User-Agent` mitsenden.

### 10.2 Response-Struktur

Die Antwort ist JSON. Wichtige Felder liegen unter `data["product"]`:

| Pfad | Beschreibung | Beispiel |
|------|--------------|----------|
| `product.product_name` | Produktname | `"Nutella"` |
| `product.product_name_en` | Name Englisch | `"Nutella"` |
| `product.brands` | Marke | `"Ferrero"` |
| `product.nutriments.energy-kcal_100g` | Kalorien pro 100g | `539` |
| `product.nutriments.fat_100g` | Fett pro 100g | `30.9` |
| `product.nutriments.carbohydrates_100g` | Kohlenhydrate pro 100g | `57.5` |
| `product.nutriments.proteins_100g` | Eiweiss pro 100g | `6.3` |
| `product.nutriments.sugars_100g` | Zucker pro 100g | `56.3` |
| `product.nutriments.salt_100g` | Salz pro 100g | `0.107` |
| `product.nutriments.fiber_100g` | Ballaststoffe pro 100g | `0` |
| `product.serving_size` | Portionsgroesse | `"15 g"` |
| `product.image_url` | Produktbild-URL | `"https://..."` |
| `product.image_front_small_url` | Kleines Vorschaubild-URL | `"https://..."` |
| `product.nutriscore_grade` | Nutri-Score (a-e) | `"e"` |
| `product.categories_tags` | Kategorien-Liste | `["en:spreads", ...]` |
| `status` | `1` = gefunden, `0` = nicht gefunden | `1` |

### 10.3 Suche nach Name

```
GET https://world.openfoodfacts.org/cgi/search.pl?search_terms=banana&json=true&page_size=5
```

#### Python-Beispiel

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

### 10.4 Fehlende Daten robust behandeln

Nicht jedes Produkt hat jedes Feld. Nutze `.get()` mit Defaults:

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

### 10.5 Pruefen, ob Produkt gefunden wurde

```python
data = response.json()

if data.get("status") == 1:
    product = data["product"]
    # Produktdaten verwenden
else:
    flash("Product not found.", "warning")
```

### 10.6 Fehlerbehandlung

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

### 10.7 Vollstaendiges Flask-Routen-Beispiel

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

## Schnellreferenz

| Aufgabe | Tool | Funktion / Syntax |
|---------|------|-------------------|
| Webseite rendern | Flask | `render_template("page.html", var=val)` |
| Formulardaten lesen | Flask | `request.form.get("field")` |
| URL-Parameter lesen | Flask | `request.args.get("key")` |
| User umleiten | Flask | `redirect("/path")` |
| Flash-Meldung zeigen | Flask | `flash("msg", "category")` |
| User merken | Flask | `session["user_id"] = id` |
| Passwort hashen | Werkzeug | `generate_password_hash(pw)` |
| Passwort pruefen | Werkzeug | `check_password_hash(hash, pw)` |
| SQL ausfuehren | CS50 | `db.execute("SELECT ...", param)` |
| Variable ausgeben | Jinja | `{{ variable }}` |
| Bedingung | Jinja | `{% if ... %}...{% endif %}` |
| Schleife | Jinja | `{% for x in items %}...{% endfor %}` |
| Layout erben | Jinja | `{% extends "layout.html" %}` |
| API-Daten holen | Python | `requests.get(url, headers=h, timeout=10)` |
| JSON parsen | Python | `response.json()` |
| Fehlende Keys abfangen | Python / Jinja | `.get("key", default)` / `\| default("N/A")` |

---

*Dieser Spickzettel wurde als Lernreferenz fuer das CS50 Final Project "Kalorien Zaehler" erstellt.*
*Assisted by GitHub Copilot. Alle Snippets sind allgemeine Muster — passe sie an und verstehe sie vor der Nutzung.*
