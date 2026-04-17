import streamlit as st
import plotly.express as px
from analysis import load_data

# Page config
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("📊 Superstore Sales Dashboard")

# Load data
data = load_data()

# =======================
# 🔥 SIDEBAR FILTERS
# =======================
st.sidebar.header("Filters")

# Year filter
year = st.sidebar.selectbox(
    "Select Year",
    sorted(data['Order Year'].unique())
)

# Category filter
category = st.sidebar.multiselect(
    "Select Category",
    data['Category'].unique(),
    default=data['Category'].unique()
)

# Region filter
region = st.sidebar.multiselect(
    "Select Region",
    data['Region'].unique(),
    default=data['Region'].unique()
)

# Apply filters
filtered_data = data[
    (data['Order Year'] == year) &
    (data['Category'].isin(category)) &
    (data['Region'].isin(region))
]

# =======================
# 🔥 KPIs
# =======================
total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")

# =======================
# 📈 Monthly Sales
# =======================
st.subheader("Monthly Sales Analysis")
sales = filtered_data.groupby('Order Month')['Sales'].sum().reset_index()
fig1 = px.line(sales, x='Order Month', y='Sales', markers=True)
st.plotly_chart(fig1, use_container_width=True)

# =======================
# 📉 Monthly Profit
# =======================
st.subheader("Monthly Profit Analysis")
profit = filtered_data.groupby('Order Month')['Profit'].sum().reset_index()
fig2 = px.line(profit, x='Order Month', y='Profit', markers=True)
st.plotly_chart(fig2, use_container_width=True)

# =======================
# 🥧 Category Sales
# =======================
st.subheader("Sales by Category")
cat_sales = filtered_data.groupby('Category')['Sales'].sum().reset_index()
fig3 = px.pie(cat_sales, values='Sales', names='Category')
st.plotly_chart(fig3, use_container_width=True)

# =======================
# 🥧 Category Profit
# =======================
st.subheader("Profit by Category")
cat_profit = filtered_data.groupby('Category')['Profit'].sum().reset_index()
fig4 = px.pie(cat_profit, values='Profit', names='Category')
st.plotly_chart(fig4, use_container_width=True)

# =======================
# 🔥 Top 5 Products
# =======================
st.subheader("Top 5 Products by Sales")

top_products = filtered_data.groupby('Product Name')['Sales'].sum().reset_index()
top_products = top_products.sort_values(by='Sales', ascending=False).head(5)

fig5 = px.bar(
    top_products,
    x='Sales',
    y='Product Name',
    orientation='h'
)

st.plotly_chart(fig5, use_container_width=True)