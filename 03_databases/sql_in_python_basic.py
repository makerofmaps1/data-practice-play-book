"""
SQL in Python (Basics)

Minimal demo of writing and executing basic SQL using an in-memory SQLite database.
Covers:
- CREATE TABLE
- INSERT
- SELECT
- UPDATE
- DELETE
- Parameterized queries
"""

from __future__ import annotations

import sqlite3


print("\n" + "=" * 60)
print("SQL IN PYTHON - BASICS")
print("=" * 60)

# In-memory SQLite database (exists only while script runs)
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()


# ============================================================
# 1) CREATE TABLE
# ============================================================

print("\n1) CREATE TABLE")
cursor.execute(
    """
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        in_stock INTEGER NOT NULL
    )
    """
)
print("Created table: products")


# ============================================================
# 2) INSERT DATA
# ============================================================

print("\n2) INSERT DATA")

products = [
    ("Keyboard", 79.99, 1),
    ("Mouse", 29.99, 1),
    ("Desk Lamp", 39.99, 0),
]

cursor.executemany(
    "INSERT INTO products (name, price, in_stock) VALUES (?, ?, ?)",
    products,
)
conn.commit()
print(f"Inserted {cursor.rowcount} rows")


# ============================================================
# 3) SELECT DATA
# ============================================================

print("\n3) SELECT DATA")

cursor.execute("SELECT product_id, name, price, in_stock FROM products ORDER BY product_id")
rows = cursor.fetchall()

print("All products:")
for product_id, name, price, in_stock in rows:
    status = "in stock" if in_stock == 1 else "out of stock"
    print(f"  [{product_id}] {name:<12} ${price:.2f} ({status})")

# Parameterized filter query
min_price = 30
cursor.execute(
    "SELECT name, price FROM products WHERE price >= ? ORDER BY price DESC",
    (min_price,),
)
print(f"\nProducts with price >= ${min_price}:")
for name, price in cursor.fetchall():
    print(f"  {name:<12} ${price:.2f}")


# ============================================================
# 4) UPDATE DATA
# ============================================================

print("\n4) UPDATE DATA")

cursor.execute(
    "UPDATE products SET price = price * 0.90 WHERE in_stock = ?",
    (1,),
)
conn.commit()
print(f"Updated {cursor.rowcount} row(s)")

cursor.execute("SELECT name, price FROM products ORDER BY product_id")
print("Prices after update:")
for name, price in cursor.fetchall():
    print(f"  {name:<12} ${price:.2f}")


# ============================================================
# 5) DELETE DATA
# ============================================================

print("\n5) DELETE DATA")

cursor.execute("DELETE FROM products WHERE in_stock = ?", (0,))
conn.commit()
print(f"Deleted {cursor.rowcount} row(s)")

cursor.execute("SELECT COUNT(*) FROM products")
remaining = cursor.fetchone()[0]
print(f"Remaining rows: {remaining}")


# Cleanup
cursor.close()
conn.close()

print("\n" + "=" * 60)
print("END OF BASICS DEMO")
print("=" * 60)
