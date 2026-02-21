import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Vertex | System Check", page_icon="✅")

st.title("💠 VertexLens: System Health Check")

# 1. Dataset Verification
olist_files = [
    'olist_customers_dataset.csv', 'olist_orders_dataset.csv', 
    'olist_order_items_dataset.csv', 'olist_products_dataset.csv',
    'olist_order_payments_dataset.csv', 'olist_order_reviews_dataset.csv',
    'olist_sellers_dataset.csv', 'olist_geolocation_dataset.csv',
    'product_category_name_translation.csv'
]

st.subheader("📦 Dataset Status")
missing_files = []
for file in olist_files:
    if os.path.exists(file):
        st.success(f"Found: {file}")
    else:
        st.error(f"Missing: {file}")
        missing_files.append(file)

# 2. Database Verification
st.subheader("🗄️ Database Status")
if os.path.exists('olist_ecommerce.db'):
    st.success("olist_ecommerce.db is ready and synced!")
else:
    st.warning("Database file not found. Please run 'setup_database.py' first.")

# 3. Quick Data Preview
if not missing_files:
    st.subheader("📊 Sample Data Preview (Orders)")
    df = pd.read_csv('olist_orders_dataset.csv')
    st.dataframe(df.head(5))
    
    st.info("Badhai ho! Sab kuch set hai. Ab 'app.py' chalao aur presentation phod do! 🚀")
else:
    st.error(f"Kaggle se ye files download karke folder mein daalo: {missing_files}")