"""
SQL Queries in Python Demonstration

This script demonstrates SQL operations in Python using SQLite.
Covers fundamental SQL concepts including:
- CREATE, INSERT, SELECT, UPDATE, DELETE
- Parameterized queries (SQL injection prevention)
- WHERE clauses and filtering
- JOINs (INNER, LEFT, RIGHT)
- Aggregations (GROUP BY, COUNT, SUM, AVG)
- Subqueries
- ORDER BY and LIMIT

Uses in-memory SQLite database for demonstration.
"""

from __future__ import annotations

import sqlite3


print("\n" + "=" * 60)
print("SQL QUERIES IN PYTHON")
print("=" * 60)


# ============================================================
# CREATE DATABASE AND TABLES
# ============================================================

# simple but realistic e-commerce schema

print("\n" + "=" * 60)
print("CREATE DATABASE AND TABLES")
print("=" * 60)

# Create in-memory database
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row  # Return rows as dictionaries
cursor = conn.cursor()

# Create customers table
cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        city TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
print("Created table: customers")

# Create orders table
cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date DATE NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
""")
print("Created table: orders")

# Create order_items table
cursor.execute("""
    CREATE TABLE order_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
""")
print("Created table: order_items")

conn.commit()


# ============================================================
# INSERT DATA - PARAMETERIZED QUERIES
# ============================================================

print("\n" + "=" * 60)
print("INSERT WITH PARAMETERIZED QUERIES")
print("=" * 60)

print("""
IMPORTANT: Always use parameterized queries!

SQL Injection Example (NEVER DO THIS):
    user_input = "'; DROP TABLE customers; --"
    cursor.execute(f"SELECT * FROM customers WHERE name = '{user_input}'")
    # This could delete your entire table!

Safe Approach (ALWAYS DO THIS):
    cursor.execute("SELECT * FROM customers WHERE name = ?", (user_input,))
    # The ? placeholder prevents SQL injection by treating input as data, not code
""")

# Insert customers using parameterized queries
customers_data = [
    ("Alice Johnson", "alice@email.com", "New York"),
    ("Bob Smith", "bob@email.com", "Los Angeles"),
    ("Charlie Brown", "charlie@email.com", "Chicago"),
    ("Diana Prince", "diana@email.com", "New York"),
    ("Eve Davis", "eve@email.com", "Boston"),
]

cursor.executemany(
    "INSERT INTO customers (name, email, city) VALUES (?, ?, ?)",
    customers_data
)
conn.commit()
print(f"Inserted {cursor.rowcount} customers")

# Insert orders
orders_data = [
    (1, "2024-01-05", 299.99, "completed"),
    (1, "2024-01-15", 149.50, "completed"),
    (2, "2024-01-10", 599.00, "shipped"),
    (3, "2024-01-12", 89.99, "completed"),
    (4, "2024-01-18", 450.00, "pending"),
    (2, "2024-01-20", 199.99, "completed"),
]

cursor.executemany(
    "INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)",
    orders_data
)
conn.commit()
print(f"Inserted {cursor.rowcount} orders")

# Insert order items
items_data = [
    (1, "Laptop", 1, 299.99),
    (2, "Mouse", 2, 24.75),
    (2, "Keyboard", 1, 99.99),
    (3, "Monitor", 1, 599.00),
    (4, "USB Cable", 3, 9.99),
    (4, "Webcam", 1, 59.99),
    (5, "Headphones", 2, 225.00),
    (6, "Speakers", 1, 199.99),
]

cursor.executemany(
    "INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES (?, ?, ?, ?)",
    items_data
)
conn.commit()
print(f"Inserted {cursor.rowcount} order items")


# ============================================================
# SELECT - BASIC QUERIES
# ============================================================

print("\n" + "=" * 60)
print("SELECT - BASIC QUERIES")
print("=" * 60)

# Select all customers
cursor.execute("SELECT * FROM customers")
customers = cursor.fetchall()
print("\nAll customers:")
for customer in customers:
    print(f"  {customer['customer_id']}: {customer['name']} ({customer['email']})")

# Select specific columns
cursor.execute("SELECT name, city FROM customers")
print("\nCustomer names and cities:")
for row in cursor.fetchall():
    print(f"  {row['name']} - {row['city']}")

# Count rows
cursor.execute("SELECT COUNT(*) as total FROM customers")
total = cursor.fetchone()['total']
print(f"\nTotal customers: {total}")


# ============================================================
# WHERE CLAUSES - FILTERING
# ============================================================

print("\n" + "=" * 60)
print("WHERE CLAUSES - FILTERING")
print("=" * 60)

# Filter by city
city = "New York"
cursor.execute("SELECT * FROM customers WHERE city = ?", (city,))
print(f"\nCustomers in {city}:")
for row in cursor.fetchall():
    print(f"  {row['name']}")

# Multiple conditions (AND)
cursor.execute("""
    SELECT * FROM orders 
    WHERE total_amount > ? AND status = ?
""", (200, "completed"))
print("\nCompleted orders over $200:")
for row in cursor.fetchall():
    print(f"  Order {row['order_id']}: ${row['total_amount']} - {row['status']}")

# OR condition
cursor.execute("""
    SELECT * FROM orders 
    WHERE status = ? OR status = ?
""", ("pending", "shipped"))
print("\nPending or shipped orders:")
for row in cursor.fetchall():
    print(f"  Order {row['order_id']}: {row['status']}")

# IN operator
cities = ("New York", "Boston")
cursor.execute("""
    SELECT name, city FROM customers 
    WHERE city IN (?, ?)
""", cities)
print("\nCustomers in New York or Boston:")
for row in cursor.fetchall():
    print(f"  {row['name']} - {row['city']}")

# LIKE operator (pattern matching)
cursor.execute("SELECT name FROM customers WHERE name LIKE ?", ("%Smith%",))
print("\nCustomers with 'Smith' in name:")
for row in cursor.fetchall():
    print(f"  {row['name']}")

# BETWEEN operator
cursor.execute("""
    SELECT order_id, total_amount FROM orders 
    WHERE total_amount BETWEEN ? AND ?
""", (100, 500))
print("\nOrders between $100 and $500:")
for row in cursor.fetchall():
    print(f"  Order {row['order_id']}: ${row['total_amount']}")


# ============================================================
# JOINS
# ============================================================

print("\n" + "=" * 60)
print("JOINS")
print("=" * 60)

# INNER JOIN - customers with orders
cursor.execute("""
    SELECT 
        c.name,
        c.email,
        o.order_id,
        o.order_date,
        o.total_amount
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    ORDER BY c.name, o.order_date
""")
print("\nCustomers with orders (INNER JOIN):")
for row in cursor.fetchall():
    print(f"  {row['name']}: Order {row['order_id']} - ${row['total_amount']}")

# LEFT JOIN - all customers including those without orders
cursor.execute("""
    SELECT 
        c.name,
        c.city,
        COUNT(o.order_id) as order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name, c.city
    ORDER BY order_count DESC
""")
print("\nAll customers with order counts (LEFT JOIN):")
for row in cursor.fetchall():
    print(f"  {row['name']} ({row['city']}): {row['order_count']} orders")

# Multiple joins
cursor.execute("""
    SELECT 
        c.name as customer_name,
        o.order_id,
        oi.product_name,
        oi.quantity,
        oi.unit_price
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    WHERE c.name = ?
""", ("Alice Johnson",))
print("\nAlice Johnson's order details (Multiple JOINs):")
for row in cursor.fetchall():
    print(f"  Order {row['order_id']}: {row['product_name']} (qty: {row['quantity']}, price: ${row['unit_price']})")


# ============================================================
# AGGREGATIONS - GROUP BY
# ============================================================

print("\n" + "=" * 60)
print("AGGREGATIONS - GROUP BY")
print("=" * 60)

# Count orders by status
cursor.execute("""
    SELECT 
        status,
        COUNT(*) as count,
        SUM(total_amount) as total_revenue
    FROM orders
    GROUP BY status
    ORDER BY count DESC
""")
print("\nOrders by status:")
for row in cursor.fetchall():
    print(f"  {row['status']}: {row['count']} orders, ${row['total_revenue']:.2f} revenue")

# Customer spending summary
cursor.execute("""
    SELECT 
        c.name,
        COUNT(o.order_id) as order_count,
        SUM(o.total_amount) as total_spent,
        AVG(o.total_amount) as avg_order_value,
        MIN(o.total_amount) as min_order,
        MAX(o.total_amount) as max_order
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
    ORDER BY total_spent DESC
""")
print("\nCustomer spending summary:")
for row in cursor.fetchall():
    print(f"  {row['name']}:")
    print(f"    Orders: {row['order_count']}, Total: ${row['total_spent']:.2f}, Avg: ${row['avg_order_value']:.2f}")

# HAVING clause (filter after GROUP BY)
cursor.execute("""
    SELECT 
        c.city,
        COUNT(*) as customer_count,
        SUM(o.total_amount) as total_revenue
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.city
    HAVING SUM(o.total_amount) > ?
    ORDER BY total_revenue DESC
""", (300,))
print("\nCities with total revenue > $300:")
for row in cursor.fetchall():
    print(f"  {row['city']}: {row['customer_count']} customers, ${row['total_revenue']:.2f} revenue")


# ============================================================
# ORDER BY AND LIMIT
# ============================================================

print("\n" + "=" * 60)
print("ORDER BY AND LIMIT")
print("=" * 60)

# Order by single column
cursor.execute("SELECT name, city FROM customers ORDER BY name")
print("\nCustomers ordered by name:")
for row in cursor.fetchall():
    print(f"  {row['name']} - {row['city']}")

# Order by multiple columns
cursor.execute("""
    SELECT name, city FROM customers 
    ORDER BY city ASC, name DESC
""")
print("\nCustomers ordered by city (asc), then name (desc):")
for row in cursor.fetchall():
    print(f"  {row['city']}: {row['name']}")

# TOP N with LIMIT
cursor.execute("""
    SELECT order_id, total_amount, order_date
    FROM orders
    ORDER BY total_amount DESC
    LIMIT ?
""", (3,))
print("\nTop 3 orders by amount:")
for row in cursor.fetchall():
    print(f"  Order {row['order_id']}: ${row['total_amount']} ({row['order_date']})")

# LIMIT with OFFSET (pagination)
cursor.execute("""
    SELECT name, email FROM customers
    ORDER BY name
    LIMIT ? OFFSET ?
""", (2, 2))
print("\nCustomers (page 2, size 2):")
for row in cursor.fetchall():
    print(f"  {row['name']} - {row['email']}")


# ============================================================
# SUBQUERIES
# ============================================================

print("\n" + "=" * 60)
print("SUBQUERIES")
print("=" * 60)

# Subquery in WHERE clause
cursor.execute("""
    SELECT name, email
    FROM customers
    WHERE customer_id IN (
        SELECT customer_id 
        FROM orders 
        WHERE total_amount > 400
    )
""")
print("\nCustomers with orders over $400:")
for row in cursor.fetchall():
    print(f"  {row['name']}")

# Subquery in SELECT clause
cursor.execute("""
    SELECT 
        name,
        email,
        (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count
    FROM customers c
    ORDER BY order_count DESC
""")
print("\nCustomers with order counts (subquery in SELECT):")
for row in cursor.fetchall():
    print(f"  {row['name']}: {row['order_count']} orders")

# Subquery with EXISTS
cursor.execute("""
    SELECT name, city
    FROM customers c
    WHERE EXISTS (
        SELECT 1 
        FROM orders o 
        WHERE o.customer_id = c.customer_id 
        AND o.status = 'completed'
    )
""")
print("\nCustomers with at least one completed order:")
for row in cursor.fetchall():
    print(f"  {row['name']} ({row['city']})")


# ============================================================
# UPDATE
# ============================================================

print("\n" + "=" * 60)
print("UPDATE")
print("=" * 60)

# Update single row
cursor.execute("""
    UPDATE orders 
    SET status = ? 
    WHERE order_id = ?
""", ("delivered", 1))
conn.commit()
print(f"Updated {cursor.rowcount} order(s)")

# Update multiple rows
cursor.execute("""
    UPDATE orders 
    SET status = ? 
    WHERE status = ? AND total_amount < ?
""", ("completed", "pending", 200))
conn.commit()
print(f"Updated {cursor.rowcount} pending order(s) under $200 to completed")

# Verify updates
cursor.execute("SELECT order_id, status, total_amount FROM orders ORDER BY order_id")
print("\nOrders after update:")
for row in cursor.fetchall():
    print(f"  Order {row['order_id']}: {row['status']} (${row['total_amount']})")


# ============================================================
# DELETE
# ============================================================

print("\n" + "=" * 60)
print("DELETE")
print("=" * 60)

# Insert test data to delete
cursor.execute("""
    INSERT INTO customers (name, email, city) 
    VALUES (?, ?, ?)
""", ("Test User", "test@email.com", "Test City"))
test_id = cursor.lastrowid
conn.commit()
print(f"Inserted test customer with ID: {test_id}")

# Delete specific row
cursor.execute("DELETE FROM customers WHERE customer_id = ?", (test_id,))
conn.commit()
print(f"Deleted {cursor.rowcount} customer(s)")

# Verify deletion
cursor.execute("SELECT COUNT(*) as count FROM customers")
print(f"Remaining customers: {cursor.fetchone()['count']}")


# ============================================================
# TRANSACTIONS
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTIONS")
print("=" * 60)

try:
    # Start transaction (SQLite auto-begins on first statement)
    cursor.execute("""
        INSERT INTO customers (name, email, city) 
        VALUES (?, ?, ?)
    """, ("Transaction Test", "transaction@email.com", "Test City"))
    
    new_customer_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount, status)
        VALUES (?, ?, ?, ?)
    """, (new_customer_id, "2024-02-01", 999.99, "pending"))
    
    # Commit transaction
    conn.commit()
    print("Transaction committed successfully")
    
    # Clean up
    cursor.execute("DELETE FROM customers WHERE customer_id = ?", (new_customer_id,))
    conn.commit()
    
except Exception as e:
    # Rollback on error
    conn.rollback()
    print(f"Transaction rolled back due to error: {e}")


# ============================================================
# ADVANCED QUERIES
# ============================================================

print("\n" + "=" * 60)
print("ADVANCED QUERIES")
print("=" * 60)

# CASE statement
cursor.execute("""
    SELECT 
        name,
        total_amount,
        CASE 
            WHEN total_amount >= 500 THEN 'High'
            WHEN total_amount >= 200 THEN 'Medium'
            ELSE 'Low'
        END as order_tier
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    ORDER BY total_amount DESC
""")
print("\nOrders with tier classification:")
for row in cursor.fetchall():
    print(f"  {row['name']}: ${row['total_amount']} ({row['order_tier']})")

# Window functions (ROW_NUMBER)
cursor.execute("""
    SELECT 
        name,
        total_amount,
        order_date,
        ROW_NUMBER() OVER (ORDER BY total_amount DESC) as rank
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    ORDER BY rank
    LIMIT 5
""")
print("\nTop 5 orders ranked by amount:")
for row in cursor.fetchall():
    print(f"  #{row['rank']}: {row['name']} - ${row['total_amount']} ({row['order_date']})")


# ============================================================
# BEST PRACTICES SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("SQL BEST PRACTICES")
print("=" * 60)

best_practices = """
1. ALWAYS use parameterized queries
   - Prevents SQL injection attacks
   - SQLite: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
   - PostgreSQL: cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

2. Use appropriate JOIN types
   - INNER JOIN: Only matching rows
   - LEFT JOIN: All from left table, matches from right
   - Use explicit JOIN syntax (not WHERE for joins)

3. Index frequently queried columns
   - CREATE INDEX idx_customer_email ON customers(email)
   - Speeds up WHERE, JOIN, and ORDER BY operations

4. Use transactions for multi-step operations
   - Ensures data consistency
   - All-or-nothing execution

5. Close connections and cursors
   - Prevents resource leaks
   - Use context managers when possible

6. Limit result sets
   - Use LIMIT/OFFSET for pagination
   - Don't fetch all rows if you only need some

7. Use appropriate data types
   - INTEGER for IDs
   - REAL/DECIMAL for money
   - TEXT for strings
   - TIMESTAMP for dates

8. Avoid SELECT *
   - Specify only needed columns
   - Improves performance and clarity

9. Use EXPLAIN to analyze queries
   - cursor.execute("EXPLAIN QUERY PLAN SELECT ...")
   - Identifies performance bottlenecks

10. Sanitize all user input
    - Never trust user data
    - Always validate and use parameterized queries
"""

print(best_practices)

# Clean up
cursor.close()
conn.close()

print("\n" + "=" * 60)
print("END OF SQL QUERIES DEMO")
print("=" * 60)
