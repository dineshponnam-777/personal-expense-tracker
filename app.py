import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.db import init_db
from src.ingest import load_csv, save_to_db
from src.analyze import fetch_data
from src.budget import save_budget, get_budgets

# -------------------------------
# INIT DB
# -------------------------------
init_db()

st.set_page_config(layout="wide")
st.title("💼 Industry-Level Expense Tracker")

# -------------------------------
# UPLOAD
# -------------------------------
uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    df_new = load_csv(uploaded)
    save_to_db(df_new)
    st.success("Data saved to database!")

# -------------------------------
# LOAD DATA
# -------------------------------
df = fetch_data()

if df.empty:
    st.warning("No data available")
    st.stop()

# -------------------------------
# FILTERS
# -------------------------------
st.sidebar.header("Filters")

month = st.sidebar.selectbox("Month", ["All"] + sorted(df["Month"].unique()))
category_filter = st.sidebar.multiselect("Category", df["category"].unique(), default=df["category"].unique())

filtered = df.copy()

if month != "All":
    filtered = filtered[filtered["Month"] == month]

filtered = filtered[filtered["category"].isin(category_filter)]

# -------------------------------
# KPIs
# -------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total", f"₹{filtered['amount'].sum():.0f}")
col2.metric("Avg", f"₹{filtered['amount'].mean():.0f}")
col3.metric("Max", f"₹{filtered['amount'].max():.0f}")

# -------------------------------
# CATEGORY CHART
# -------------------------------
st.subheader("Category Spending")
cat = filtered.groupby("category")["amount"].sum()

fig, ax = plt.subplots()
cat.plot(kind="bar", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------------
# BUDGET SYSTEM (PERSISTENT)
# -------------------------------
st.subheader("💰 Budget System")

budgets = get_budgets()

for c in cat.index:
    existing = budgets[budgets["category"] == c]["amount"]
    default_val = float(existing.values[0]) if not existing.empty else 1000

    val = st.number_input(f"{c}", value=default_val)
    save_budget(c, val)

# Compare
budgets = get_budgets()
merged = pd.merge(cat.reset_index(), budgets, on="category", how="left")
merged.columns = ["Category","Actual","Budget"]
merged["Diff"] = merged["Actual"] - merged["Budget"]

st.dataframe(merged)

# Alerts
for _, r in merged.iterrows():
    if r["Diff"] > 0:
        st.error(f"{r['Category']} exceeded by ₹{r['Diff']:.0f}")

# -------------------------------
# EXPORT REPORT
# -------------------------------
st.subheader("📥 Download Report")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV Report",
    data=csv,
    file_name="expense_report.csv",
    mime="text/csv"
)