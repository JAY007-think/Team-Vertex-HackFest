import sqlite3

# Naya database file: enterprise_data.db
conn = sqlite3.connect('enterprise_data.db')
cursor = conn.cursor()

# 1. Employees Table
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute('''CREATE TABLE employees 
               (emp_id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary REAL)''')
cursor.execute("INSERT INTO employees VALUES (101, 'Amit', 'Engineering', 85000)")
cursor.execute("INSERT INTO employees VALUES (102, 'Suman', 'HR', 60000)")

# 2. Inventory Table
cursor.execute("DROP TABLE IF EXISTS inventory")
cursor.execute('''CREATE TABLE inventory 
               (prod_id INTEGER PRIMARY KEY, prod_name TEXT, stock_count INTEGER)''')
cursor.execute("INSERT INTO inventory VALUES (501, 'Keyboard', 25)")
cursor.execute("INSERT INTO inventory VALUES (502, 'Monitor', 10)")

conn.commit()
conn.close()
print("✅ Doosra Database 'enterprise_data.db' ready hai!")