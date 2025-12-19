import streamlit as st
import pandas as pd

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Retail Analysis Dashboard",
    layout="wide"
)

# -----------------------------
# Title & subtitle
# -----------------------------
st.title("Retail Analysis Dashboard")
st.markdown(
    "Sales, revenue, and inventory insights across stores, products, and suppliers"
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# -----------------------------
# Dataset status message
# -----------------------------
st.success(
    "A sample dataset is preloaded for analysis. (2024-2025)"
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

# Store filter
store_options = sorted(df["store_id"].unique())
selected_stores = st.sidebar.multiselect(
    "Select Store(s)",
    options=store_options
)

# Date filters
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

# Supplier filter (OPTIONAL)
supplier_options = sorted(df["supplier"].unique())
selected_suppliers = st.sidebar.multiselect(
    "Select Supplier(s) (optional)",
    options=supplier_options
)

# Product filter (OPTIONAL)
product_options = sorted(df["product_name"].unique())
selected_products = st.sidebar.multiselect(
    "Select Product(s) (optional)",
    options=product_options
)

# -----------------------------
# Guidance message
# -----------------------------
if not selected_stores:
    st.info("Start by selecting one or more stores from the sidebar.")
    st.stop()

# -----------------------------
# Validation
# -----------------------------
if start_date is None or end_date is None:
    st.info("Please select both a start date and an end date.")
    st.stop()

if start_date > end_date:
    st.error("Start date cannot be after end date.")
    st.stop()

# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df[
    (df["store_id"].isin(selected_stores)) &
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date)
]

if selected_suppliers:
    filtered_df = filtered_df[
        filtered_df["supplier"].isin(selected_suppliers)
    ]

if selected_products:
    filtered_df = filtered_df[
        filtered_df["product_name"].isin(selected_products)
    ]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# -----------------------------
# Derived metric
# -----------------------------
filtered_df["revenue_calc"] = filtered_df["total_value"]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("Key Performance Indicators")

total_revenue = filtered_df["revenue_calc"].sum()
total_transactions = filtered_df["transaction_id"].nunique()
aov = total_revenue / total_transactions
reorder_rate = (filtered_df["reorder_flag"].sum() / total_transactions) * 100

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
k2.metric("Total Transactions", total_transactions)
k3.metric("Average Order Value (AOV)", f"₹{aov:,.2f}")
k4.metric("Reorder Rate (%)", f"{reorder_rate:.2f}")

# -----------------------------
# Revenue Trend
# -----------------------------
st.subheader("Revenue Trend Over Time")

daily_revenue = (
    filtered_df
    .groupby(filtered_df["date"].dt.date)["revenue_calc"]
    .sum()
)

st.line_chart(daily_revenue)

# -----------------------------
# Product-wise Revenue
# -----------------------------
st.subheader("Product-wise Revenue")

product_revenue = (
    filtered_df
    .groupby("product_name")["revenue_calc"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_revenue)

# -----------------------------
# Reorder / Low-stock Analysis
# -----------------------------
st.subheader("Reorder / Low-Stock Analysis")

reorder_count = filtered_df["reorder_flag"].sum()
st.metric("Reorder Transactions", reorder_count)

reorder_products = (
    filtered_df[filtered_df["reorder_flag"] == 1]
    .groupby("product_name")
    .size()
)

if not reorder_products.empty:
    st.markdown("**Products Frequently Needing Reorder**")
    st.bar_chart(reorder_products)
else:
    st.info("No reorder events for selected filters.")

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("Dataset Preview")
st.caption(f"Total rows after filters: {len(filtered_df)}")
st.dataframe(filtered_df.head(50))

# -----------------------------
# Download CSV (BOTTOM)
# -----------------------------
st.subheader("Download Filtered Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="filtered_retail_data.csv",
    mime="text/csv"
)