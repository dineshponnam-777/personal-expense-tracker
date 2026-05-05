import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------------
# STEP 1: CREATE SYNTHETIC DATA
# -------------------------------
def create_data():
    data = {
        # ✅ FIX: remove time from date
        "Date": pd.date_range(start="2025-01-01", periods=50).date,

        "Category": np.random.choice(
            ["Food", "Transport", "Rent", "Shopping", "Bills"], 50),

        "Amount": np.random.randint(100, 5000, 50),

        "Payment Method": np.random.choice(
            ["Cash", "UPI", "Card"], 50),

        "Description": np.random.choice(
            ["Groceries", "Uber", "Rent", "Amazon", "Electricity"], 50)
    }

    df = pd.DataFrame(data)

    # ✅ Save CSV (clean format)
    df.to_csv("data/expenses.csv", index=False)
    print("✅ Data Created")


# -------------------------------
# STEP 2: LOAD DATA
# -------------------------------
def load_data():
    df = pd.read_csv("data/expenses.csv")
    print("✅ Data Loaded")
    return df


# -------------------------------
# STEP 3: CLEAN DATA
# -------------------------------
def clean_data(df):
    # ✅ FIX: remove time & format properly
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    # Create Month column
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    print("✅ Data Cleaned")
    return df


# -------------------------------
# STEP 4: ANALYSIS
# -------------------------------
def analyze(df):
    category = df.groupby("Category")["Amount"].sum()
    monthly = df.groupby("Month")["Amount"].sum()
    payment = df.groupby("Payment Method")["Amount"].sum()

    # Extra KPIs
    avg_daily = df.groupby("Date")["Amount"].sum().mean()
    highest_day = df.groupby("Date")["Amount"].sum().idxmax()

    print("\n📊 Analysis Results:")
    print("Highest Spending Category:", category.idxmax())
    print("Total Spending:", df["Amount"].sum())
    print("Average Daily Spending:", round(avg_daily, 2))
    print("Highest Spending Day:", highest_day)

    return category, monthly, payment


# -------------------------------
# STEP 5: VISUALIZATION
# -------------------------------
def visualize(category, monthly, payment, df):

    # CATEGORY BAR CHART
    plt.figure(figsize=(8, 5))
    category.plot(kind='bar')
    plt.title("Category-wise Spending")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("outputs/category.png")
    plt.clf()

    # MONTHLY LINE CHART
    plt.figure(figsize=(8, 5))
    monthly.plot(kind='line', marker='o')
    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig("outputs/monthly.png")
    plt.clf()

    # PAYMENT PIE CHART
    plt.figure(figsize=(6, 6))
    payment.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Payment Method Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("outputs/payment.png")
    plt.clf()

    # DAILY TREND CHART
    daily = df.groupby("Date")["Amount"].sum()
    plt.figure(figsize=(8, 5))
    daily.plot(kind='line')
    plt.title("Daily Spending Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/daily.png")
    plt.clf()

    print("✅ Charts Created")


# -------------------------------
# STEP 6: REPORT GENERATION
# -------------------------------
def generate_report(df):

    # Amount Summary
    amount_summary = df["Amount"].describe()
    amount_summary.to_csv("reports/amount_summary.csv")

    # Date Summary (formatted for Excel)
    date_summary = {
        "Start Date": pd.to_datetime(df["Date"]).min().strftime("%d-%m-%Y"),
        "End Date": pd.to_datetime(df["Date"]).max().strftime("%d-%m-%Y"),
        "Total Days": df["Date"].nunique()
    }

    date_df = pd.DataFrame(list(date_summary.items()), columns=["Metric", "Value"])
    date_df.to_csv("reports/date_summary.csv", index=False)

    print("✅ Reports Generated")


# -------------------------------
# MAIN FUNCTION
# -------------------------------
if __name__ == "__main__":

    # Create folders
    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Run pipeline
    create_data()
    df = load_data()
    df = clean_data(df)

    category, monthly, payment = analyze(df)

    visualize(category, monthly, payment, df)
    generate_report(df)
