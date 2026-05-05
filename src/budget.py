from src.db import get_conn
import pandas as pd

def save_budget(category, amount):
    con = get_conn()
    con.execute(
        "INSERT OR REPLACE INTO budgets(category, amount) VALUES (?,?)",
        (category, amount)
    )
    con.commit()
    con.close()

def get_budgets():
    con = get_conn()
    df = pd.read_sql("SELECT * FROM budgets", con)
    con.close()
    return df