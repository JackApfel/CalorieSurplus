from cs50 import SQL

db = SQL("sqlite:///calories.db")

db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, hash TEXT NOT NULL)")

db.execute("EXECUTE TABLE IF NOT EXISTS foods (name TEXT NOT NULL, calories INTEGER NOT NULL)")

