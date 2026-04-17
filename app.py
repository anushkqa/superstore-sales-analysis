import streamlit as st
import plotly.express as px
from analysis import load_data

# Page config
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("📊 Superstore Business Insights Dashboard")

# Load data
data = load_data()

# =======================
# 🔥 SIDEBAR FILTERS
# =======================
st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(data['Order Year'].unique())
)

category = st.sidebar.multiselect(
    "Select Category",
    data['Category'].unique(),
    default=data['Category'].unique()
)

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

# ❗ HANDLE EMPTY DATA (IMPORTANT)
if filtered_data.empty:
    st.warning("No data available for selected filters")
    st.stop()

# =======================
# 🔥 KPIs
# =======================
total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")

# =======================
# 📈 Monthly Sales
# =======================
st.subheader("Monthly Sales Analysis")

sales = filtered_data.groupby('Order Month')['Sales'].sum().reset_index()
sales = sales.sort_values(by='Order Month')  # FIX SORTING

fig1 = px.line(sales, x='Order Month', y='Sales', markers=True)
st.plotly_chart(fig1, use_container_width=True)

# =======================
# 📉 Monthly Profit
# =======================
st.subheader("Monthly Profit Analysis")

profit = filtered_data.groupby('Order Month')['Profit'].sum().reset_index()
profit = profit.sort_values(by='Order Month')  # FIX SORTING

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
    orientation='h',
    title="Top 5 Products"
)

st.plotly_chart(fig5, use_container_width=True)
st.subheader("Loss Making Products")

loss_data = filtered_data[filtered_data['Profit'] < 0]

if not loss_data.empty:
    loss_products = loss_data.groupby('Product Name')['Profit'].sum().reset_index()
    loss_products = loss_products.sort_values(by='Profit').head(5)

    fig6 = px.bar(
        loss_products,
        x='Profit',
        y='Product Name',
        orientation='h',
        title="Top Loss Making Products"
    )
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.info("No loss-making products in selected filters")

st.subheader("Discount vs Profit Analysis")

fig7 = px.scatter(
    filtered_data,
    x='Discount',
    y='Profit',
    color='Category',
    title="Impact of Discount on Profit"
)

st.plotly_chart(fig7, use_container_width=True)

st.subheader("Download Data")

csv = filtered_data.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv'
)