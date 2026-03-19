from cs50 import SQL
import sys
from pathlib import Path


if len(sys.argv) < 2:
    print("-h --help for this text\n-c --create will create the .db file and setup Tables\n-d --drop will drop and create entirely new tables (all information WILL be lost!)")
    sys.exit()





def create():
    # Copilot provided Syntax for file creation
    Path("calories.db").touch(exist_ok=True)

    db = SQL("sqlite:///calories.db")

    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, hash TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS foods (name TEXT NOT NULL, calories INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")

def drop():
    Path("calories.db").touch(exist_ok=True)
    db = SQL("sqlite:///calories.db")

    db.execute("DROP TABLE IF EXISTS users")
    db.execute("DROP TABLE IF EXISTS foods")

    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, hash TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS foods (name TEXT NOT NULL, calories INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")


# match syntax was found on StackOverflow when searching for a switch like statement in Python 
match sys.argv[1]:
    case "-h" | "--help":
        print("-h --help for this text\n-c --create will create the .db file and setup Tables\n-d --drop will drop and create entirely new tables (all information WILL be lost!)")

    case "-c" | "--create":
        create()
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
