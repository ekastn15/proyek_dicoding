import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load data
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("dashboard/all_data2.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    st.image("https://drive.google.com/file/d/18WPrT1KIWmb9eYtSKf0feuqC17twZa7j/view?usp=sharing")
    # Title
    st.title("Eka Sulistyaningsih")

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

# Header
st.header("E-Commerce Dashboard Dicoding")

# Daily Orders
st.subheader("Daily Orders")

col1, col2 = st.columns(2)

with col1:
    total_order = main_df.resample("D", on="order_approved_at")["order_id"].nunique().sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = format_currency(main_df.groupby(main_df["order_approved_at"].dt.date)["price"].sum().sum(), "IDR", locale="id_ID")
    st.markdown(f"Total Revenue: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(12, 6))
daily_orders = main_df.resample("D", on="order_approved_at")["order_id"].nunique()
ax.plot(
    daily_orders.index,
    daily_orders.values,
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = main_df.groupby("product_category_name_english")["order_item_id"].count().sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = main_df.groupby("product_category_name_english")["order_item_id"].count().mean()
    st.markdown(f"Average Items: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

colors = ["#3182bd", "#3182bd", "#3182bd", "#3182bd", "#3182bd"]

sns.barplot(x="order_item_id", y="product_category_name_english", data=main_df.groupby("product_category_name_english")["order_item_id"].count().reset_index().sort_values(by="order_item_id", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Penjualan Terbanyak", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)

sns.barplot(x="order_item_id", y="product_category_name_english", data=main_df.groupby("product_category_name_english")["order_item_id"].count().reset_index().sort_values(by="order_item_id").head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_yaxis() 
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Penjualan Sedikit", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.caption('Copyright (C) Eka Sulistyaningsih 2024')
