import sqlite3

# Connection
conn = sqlite3.connect('my_business.db')
cursor = conn.cursor()

# Enable Foreign Key support in SQLite
cursor.execute("PRAGMA foreign_keys = ON")

# Clean up
cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute("DROP TABLE IF EXISTS customers")

# 1. Customers Table (Primary Entity)
# Adding some NULLs and varied dates to test 'Freshness' and 'Completeness'
cursor.execute('''CREATE TABLE customers (
    id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, 
    email TEXT, 
    region TEXT,
    join_date DATE
)''')

customers_data = [
    (1, 'Rahul Sharma', 'rahul@example.com', 'North', '2023-01-10'),
    (2, 'Anjali Gupta', 'anjali@test.com', 'South', '2023-02-15'),
    (3, 'Vikram Singh', None, 'West', '2023-05-20'), # Missing Email
    (4, 'Sanya Iyer', 'sanya@web.com', None, '2024-01-05') # Missing Region
]
cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers_data)

# 2. Sales Table (Transactional Entity)
# Added FOREIGN KEY constraint so Vertex can auto-detect the relationship
cursor.execute('''CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY, 
    item_name TEXT, 
    price REAL, 
    quantity INTEGER,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)''')

sales_data = [
    (101, 'Premium Laptop', 55000.0, 1, 1),
    (102, 'Wireless Phone', 25000.0, 2, 2),
    (103, 'Mechanical Keyboard', 4500.0, 1, 1),
    (104, 'Monitor 4K', 32000.0, 1, 3),
    (105, 'USB-C Cable', 1200.0, 5, 2),
    (106, 'Ergonomic Chair', 15000.0, 1, 1)
]
cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", sales_data)

conn.commit()
conn.close()

print("✅ Vertex Test Database Ready!")
print("📊 Included: Missing values for Quality Testing.")
print("🔗 Included: Foreign Key constraints for Lineage Testing.")