import sqlite3
import pandas as pd
import os

def create_olist_db():
    db_name = 'olist_ecommerce.db'
    
    # Connection
    conn = sqlite3.connect(db_name)
    print(f"✅ Connecting to {db_name}...")

    # Olist Dataset ki saari 9 files ki list
    # Make sure ye files same folder mein hon
    olist_files = {
        'customers': '.csv/olist_customers_dataset.csv',
        'orders': '.csv/olist_orders_dataset.csv',
        'order_items': '.csv/olist_order_items_dataset.csv',
        'products': ',csv/olist_products_dataset.csv',
        'payments': '.csv/olist_order_payments_dataset.csv',
        'reviews': '.csv/olist_order_reviews_dataset.csv',
        'sellers': '.csv/olist_sellers_dataset.csv',
        'geolocation': '.csv/olist_geolocation_dataset.csv',
        'category_translation': '.csv/product_category_name_translation.csv'
    }

    print("🚀 Vertex Ingestion Engine: Starting CSV to SQL migration...")

    for table_name, csv_file in olist_files.items():
        if os.path.exists(csv_file):
            print(f"⏳ Processing {table_name}...")
            # Load CSV
            df = pd.read_csv(csv_file)
            
            # Data cleaning (Optional but good for quality score demo)
            # CSV ko SQL table mein convert karna
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"   - Successfully migrated {len(df)} rows.")
        else:
            print(f"❌ Warning: {csv_file} not found. Skip mapping.")

    conn.close()
    print("\n✅ Vertex Hub: Olist E-Commerce Database is Ready!")
    print("📊 Real-world scale: 100k+ orders and 9 interlinked tables.")

if __name__ == "__main__":
    create_olist_db()