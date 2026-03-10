# Kalorien Zähler

## Overview

This is a web-application based on Python and Flask, made for making weight gain easier.
It is a calorie counting app with a vast database of different foods powered by Open Food Facts
It has a Simple UI/UX and is usable across devices.
This project idea came to me because i am myself very underweight, and to help me improve my health; i developed this app.

## Features

- Simple UI/UX
- Vast Database for food items powered by Open Food Facts
- Overview over past meals and daily calorie tracking

## Tech Stack

- Database: SQLite3
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript

## Installation & Running

Clone this repository `git clone`
Run `python init_db.py`
Create the `.env`
Then start with `run flask` or `python app.py`

## Project Structure

- `app.py` - Starts the Application
- `helpers.py` - Utility functions for ap.py
- `init_db.py` - Initialize database
- `templates/` - HTML templates for Flask/Jinja
  - `layout.html` - Base layout for Jinja and all HTML files
  - `index.html`, `login.html`, ...
- `static/` - Static files like images and css
  - `css/` - [Styles?]
- `requirements.txt` - Python dependencies
- `.env` - Stores environment variables

## Data Structure

|  |  |  |
|----------|----------|----------|
| users:  | email   | hash  |
| foods:  | name   | calories   | user_id   |
||

## Design Decisions

## Known Limitations / Future Work

## Academic Honesty & AI Usage

This project follows CS50's Academic Honesty guidelines.
See: `.github/prompts/honesty.prompt.md`.

## Video Demo
