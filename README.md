# CalorieSurplus

#### Description

This project is a web application built with Flask and SQLite, created as my Final Project for Harvard's CS50x course.

The app is for people who want to track their calorie intake and set a daily calorie goal.

Product search is powered by Open Food Facts.

It provides a basic overview of daily progress.

It was built as a learning project and as my final project for Harvard's CS50x course.

## Features

- Register to create an account and log in at any time.
- Search products by name with automatic caching to reduce API requests.
- Calories are automatically calculated and summarized.
- Set a personal calorie goal on the preferences page.
- Check your meal history.

## Tech Stack

This project uses:

- Flask (backend framework)

- SQLite (database)

- HTML/CSS/JavaScript (frontend)

- Open Food Facts API (product data)

I used Flask because it is lightweight and beginner-friendly.

SQLite is a good fit for this project because it is simple and portable.

The frontend is built with HTML, CSS, and JavaScript to keep pages simple and responsive.

External data is fetched via HTTP requests to Open Food Facts.

## Installation & Running

**Requirements:**

- Python 3.14.4
- pip

**Installation:**

- Clone this repository: `git clone https://github.com/JackApfel/CalorieSurplus.git`
- Navigate into the directory: `cd CalorieSurplus`
- Create a virtual environment: `python3.14 -m venv .venv`
- Activate the virtual environment:
  - Linux/macOS: `source .venv/bin/activate`
  - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
  - Windows (CMD): `.venv\Scripts\activate.bat`
- Install dependencies: `pip install -r requirements.txt`
- Create the `.env` file from the example:
  - Linux/macOS: `cp .env.example .env`
  - Windows: `copy .env.example .env`
- Open the `.env` file and set your `SECRET_KEY`
- Create the database: `python init_db.py -c`
- Start the app: `flask run`

## Project Structure

- `app.py` - Contains routes and core app logic
- `helpers.py` - Contains utility functions, decorators, and unit conversion logic
- `init_db.py` - Creates and resets the database schema
- `requirements.txt` - Python dependencies
- `.env` - Stores environment variables (see `.env.example`)
- `templates/` - Contains Jinja HTML pages
  - `layout.html` - Base layout for Jinja and all HTML files
  - `index.html`, `login.html`, `register.html`, `logout.html`, `catalog.html`, `history.html`, `preference.html`, `404.html`
- `static/` - Contains CSS and JavaScript assets
  - `css/layout.css` - Main stylesheet
  - `js/` - JavaScript utilities

## Data Structure

This project uses a small SQLite database with three main tables: users, foods, and preferences.
The schema is designed for simplicity and readability because this is a learning project.
Each user can log many food entries, and each user has one preference record with a personal calorie goal.

### users

Purpose: Stores account and authentication data.

- id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique user id
- email (TEXT UNIQUE NOT NULL): User email address
- hash (TEXT NOT NULL): Password hash
- created_at (TEXT DEFAULT CURRENT_TIMESTAMP): Account creation time

### foods

Purpose: Stores each food entry a user logs.

- id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique food entry id
- name (TEXT NOT NULL): Product name
- product_calories (INTEGER NOT NULL): Calories per 100g
- consumed_calories (INTEGER NOT NULL): Calculated calories for consumed grams
- user_id (INTEGER NOT NULL): Owner of this food entry
- barcode (INTEGER NOT NULL): Product barcode
- grams (INTEGER NOT NULL): Consumed amount in grams
- created_at (TEXT DEFAULT CURRENT_TIMESTAMP): Entry creation time
- calorie_goal (INTEGER NOT NULL): Snapshot of user calorie goal at entry time
- Foreign Key: user_id references users.id

### preferences

Purpose: Stores user-specific app preferences.

- id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique preference id
- user_id (INTEGER NOT NULL UNIQUE): User id linked to this preference row
- calorie_goal (INTEGER NOT NULL DEFAULT 2000): Daily calorie target
- Foreign Key: user_id references users.id

### Relationships

- One user can have many food entries (1:N)
- One user has one preferences row (1:1)

## Design Decisions

### Database

I decided to use SQLite for its simplicity and portability. The schema is intentionally compact, with users, foods, and preferences, to keep development and debugging manageable.

The foods table stores a snapshot of the current calorie goal when each row is created.
This preserves historical context for future features and analysis.

### Authentication & Security

I used `werkzeug.security` for password hashing, as learned in Week 9. It is easy to use and secure, which made it a good choice for this project.

Variables like `SECRET_KEY` are stored and loaded from `.env`. This is safer than hardcoding secrets in the application and is easier to configure.

All database queries use parameterized statements via `cs50.SQL` to reduce SQL injection risk.

### External API

Product lookup is provided by Open Food Facts, which fits this project very well.

Requests to the Open Food Facts API include a descriptive `User-Agent`, only required fields to reduce payload size, and robust timeout/error handling for better user feedback.

**Caching:** OFF search results are cached using Python's `lru_cache` decorator (configured via `CACHE_MAXSIZE` environment variable). This significantly reduces API requests for frequently searched items and improves response times.

### Input Validation & UX

Numeric inputs such as calories, grams, and goals are validated and cast to integers for more reliable handling and cleaner display.

The app follows the POST-Redirect-GET pattern to improve user flow and uses flash messages for clear feedback.

### Simplicity & Portability

Flask and SQLite minimize dependency and setup complexity, making the project easier to develop and test.
The lightweight stack is portable, and there is no external database server required.

I kept the UI as simple as possible because I am not a designer, and a simpler layout improves readability and usability across devices.

## Known Limitations / Future Work

**Limitations:**

- The Open Food Facts (OFF) API does not cover all products or home-cooked meals.
- The app caches OFF results in memory; cache is cleared when the application restarts.
- The Open Food Facts API has strict request limits.

**Future Work:**

- Improve the visual design to make the interface more polished and appealing.
- Tidy up the database schema.
- Address frequent 503 errors.
- Support for barcode scanning on mobile devices.

## Academic Honesty & AI Usage

This project follows CS50's Academic Honesty guidelines.

AI was used selectively to improve productivity without compromising understanding. Specific uses include:

- Secure configuration management setup with `python-dotenv`
- Flask decorator pattern implementation
- Syntax assistance for SQL UPDATE statements
- Code review and refactoring of `layout.html`
- Formalization of documentation

AI-assisted code is marked via comments in the source files.
