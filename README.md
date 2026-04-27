# Kalorien Zähler

#### a CS50x Final Project

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

- Clone this repository `git clone https://github.com/JackApfel/Kalorien-Z-hler.git`
- Install dependencies `pip install -r requirements.txt`
- Run `python init_db.py`
- Create the `.env`
- Then start with `run flask`

## Project Structure

- `app.py` - Starts the Application
- `helpers.py` - Utility functions for app.py
- `init_db.py` - Initialize database
- `templates/` - HTML templates for Flask/Jinja
  - `layout.html` - Base layout for Jinja and all HTML files
  - `index.html`, `login.html`, ...
- `static/` - Static files like images and css
  - `css/` - [Styles?]
- `requirements.txt` - Python dependencies
- `.env` - Stores environment variables

## Data Structure

This Project uses a very simple SQLite database

- users (Stores user specific information)
  - **id** (INTEGER PRIMARY KEY, unique users id)
  - **email** (TEXT, the email of the user)
  - **hash** (TEXT, password hash of the users password)
  - **created_at** (TEXT, entry creation date)

- foods (Stores product specific information)
  - **name** (TEXT, name of the product)
  - **product_calories** (INTEGER, products kcal per 100g)
  - **consumed_calories** (INTEGER, calories consumed by the user)
  - **user_id** (INTEGER, the user_id of the corresponding user)
  - **barcode** (INTEGER, the barcode of product)
  - **grams** (INTEGER, the number of grams consumed from the user)
  - **created_at** (TEXT, entry creation date)
  - **user_id** (FOREIGN KEY, references the `users` tables `id` field)

- preferences (Stores preferences set by the user)
  - **id** (INTEGER PRIMARY KEY, unique id of the preference set)
  - **user_id** (INTEGER UNIQUE, id of the user this preferences belong to)
  - **calorie_goal** (INTEGER DEFAULT 2000, daily calorie goal for the user)
  - **(reference) user_id** (TODO)

## Design Decisions

TODO

## Known Limitations / Future Work

**Limitation:**

- The Open Food Facts (OFF) API does not cover all products or self cooked meals.
  
- The Open Food Facts API does often return error 503

**Future Work:**

- The current design of the application is not sightly and is plain looking, a more appealing design is planned.

- Addressing the frequent 503 errors

## Academic Honesty & AI Usage

This project follows CS50's Academic Honesty guidelines.

I did first use AI when starting this project, but soon enough i did realize that it was more of a hindrance then it was helping.

I minimized my AI usage to mostly just be help with Syntax i had forgotten.

AI assisted code is marked via comment.

when AI was used it was this this used with this prompt.md, the prompt file was created by Github Copilot.
See: `.github/prompts/honesty.prompt.md`.

## Video Demo

**TODO**
