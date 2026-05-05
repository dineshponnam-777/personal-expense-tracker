from src.db import get_conn
import pandas as pd

def load_csv(file):
    df = pd.read_csv(file)

    # Clean date
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df.dropna(subset=["Date"], inplace=True)

    return df


def save_to_db(df):
    # ✅ RENAME columns to match DB schema
    df = df.rename(columns={
        "Date": "date",
        "Category": "category",
        "Amount": "amount",
        "Payment Method": "payment",
        "Description": "description"
    })

    # Keep only required columns
    df = df[["date", "category", "amount", "payment", "description"]]

    con = get_conn()

    try:
        df.to_sql("transactions", con, if_exists="append", index=False)
        print("✅ Data inserted successfully")
    except Exception as e:
        print("❌ Insert failed:", e)

    con.close()