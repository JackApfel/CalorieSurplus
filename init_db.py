from cs50 import SQL

db = SQL("sqlite:///calories.db")

db.execute("DROP TABLE IF EXISTS users")
db.execute("DROP TABLE IF EXISTS foods")

db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, hash TEXT NOT NULL)")

db.execute("CREATE TABLE IF NOT EXISTS foods (name TEXT NOT NULL, calories INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")

