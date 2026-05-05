import pandas as pd
from src.db import get_conn

def fetch_data():
    con = get_conn()
    df = pd.read_sql("SELECT * FROM transactions", con)
    con.close()

    df["Date"] = pd.to_datetime(df["date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    return df