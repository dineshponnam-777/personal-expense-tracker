import sqlite3
import os

# Get absolute project path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create db folder safely
DB_DIR = os.path.join(BASE_DIR, "db")
os.makedirs(DB_DIR, exist_ok=True)

# Full database path
DB_PATH = os.path.join(DB_DIR, "expenses.db")


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        amount REAL,
        payment TEXT,
        description TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS budgets(
        category TEXT PRIMARY KEY,
        amount REAL
    )
    """)

    con.commit()
    con.close()