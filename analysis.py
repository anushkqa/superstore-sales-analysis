import pandas as pd

def load_data():
    data = pd.read_csv("data/Sample - Superstore.csv", encoding='latin-1')
    
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Ship Date'] = pd.to_datetime(data['Ship Date'])

    data['Order Month'] = data['Order Date'].dt.month
    data['Order Year'] = data['Order Date'].dt.year
    
    return data

def sales_by_month(data):
    return data.groupby('Order Month')['Sales'].sum().reset_index()

def profit_by_month(data):
    return data.groupby('Order Month')['Profit'].sum().reset_index()

def category_sales(data):
    return data.groupby('Category')['Sales'].sum().reset_index()

def category_profit(data):
    return data.groupby('Category')['Profit'].sum().reset_index()