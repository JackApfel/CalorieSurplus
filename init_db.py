import sys
from pathlib import Path

from cs50 import SQL

# Copilot provided Syntax for file creation
Path("calories.db").touch(exist_ok=True)

db = SQL("sqlite:///calories.db")

if len(sys.argv) < 2:
    print(
        "-h --help for this text\n-c --create will create the .db file and setup Tables\n-d --drop will drop and create entirely new tables (all information WILL be lost!)"
    )
    sys.exit()


def create():
    db.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "email TEXT UNIQUE NOT NULL, "
        "hash TEXT NOT NULL, "
        "created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS foods ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, "
        "product_calories INTEGER NOT NULL, "
        "consumed_calories INTEGER NOT NULL, "
        "user_id INTEGER NOT NULL, "
        "barcode INTEGER NOT NULL, "
        "grams INTEGER NOT NULL, "
        "created_at TEXT DEFAULT CURRENT_TIMESTAMP, "
        "calorie_goal INTEGER NOT NULL, "
        "FOREIGN KEY(user_id) REFERENCES users(id))"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS preferences ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL UNIQUE, "
        "calorie_goal INTEGER NOT NULL DEFAULT 2000, "
        "FOREIGN KEY(user_id) REFERENCES users(id))"
    )


def drop():
    db.execute("DROP TABLE IF EXISTS foods")
    db.execute("DROP TABLE IF EXISTS preferences")
    db.execute("DROP TABLE IF EXISTS users")

    create()


# match syntax was found on StackOverflow when searching for a switch like statement in Python
match sys.argv[1]:
    case "-h" | "--help":
        print(
            "-h --help for this text\n-c --create will create the .db file and setup Tables\n-d --drop will drop and create entirely new tables (ALL information will be LOST!)"
        )

    case "-c" | "--create":
        create()
        print("Done!")
    case "-d" | "--drop":
        prompt = input("are you sure? y/n ")
        match prompt:
            case "y" | "Y":
                drop()
                print("Done!")
            case "n" | "N":
                print("Aborting...")
                sys.exit()
            case _:
                sys.exit()
    case _:
        print("use -h or --help for more information")
