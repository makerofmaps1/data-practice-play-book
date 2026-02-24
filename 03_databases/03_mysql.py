"""
MySQL with Python

This script demonstrates working with MySQL from Python, including:
- Connecting via mysql-connector-python
- Schema and table creation
- Reading and writing data
- Pandas integration (query to DataFrame, write from DataFrame)

Requirements:
    pip install mysql-connector-python pandas

MySQL Docs:
    https://dev.mysql.com/doc/
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date

import mysql.connector
import pandas as pd

from db_config import get_mysql_config


# ============================================================
# CONNECTION CONFIGURATION
# ============================================================

MYSQL_CONFIG = get_mysql_config()


print("\n" + "=" * 60)
print("MYSQL WITH PYTHON")
print("=" * 60)


# ============================================================
# SECTION 1: CONNECTION
# ============================================================

print("\n" + "=" * 60)
print("SECTION 1: CONNECTION")
print("=" * 60)

# Ensure database exists before opening a DB-scoped connection
try:
    bootstrap_conn = mysql.connector.connect(
        host=MYSQL_CONFIG["host"],
        port=MYSQL_CONFIG["port"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
    )
    bootstrap_cursor = bootstrap_conn.cursor()
    bootstrap_cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4"
    )
    bootstrap_cursor.close()
    bootstrap_conn.close()
except Exception as e:
    print(f"Database bootstrap failed: {e}")

try:
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT CURRENT_USER(), DATABASE(), VERSION()")
    row = cursor.fetchone()
    print(f"Connected as: {row[0]}")
    print(f"Database:     {row[1]}")
    print(f"Version:      {row[2]}")

    cursor.close()
    conn.close()
    print("Connection closed")

except Exception as e:
    print(f"Connection failed: {e}")


@contextmanager
def get_mysql_connection():
    """Context manager for MySQL connections."""
    conn = None
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        if conn:
            conn.close()


try:
    with get_mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP()")
        ts = cursor.fetchone()[0]
        print(f"MySQL server time: {ts}")
        cursor.close()
    print("Context manager closed connection automatically")

except Exception as e:
    print(f"Context manager connection failed: {e}")


# ============================================================
# SECTION 2: TABLE CREATION
# ============================================================

print("\n" + "=" * 60)
print("SECTION 2: TABLE CREATION")
print("=" * 60)

try:
    with get_mysql_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id     INT AUTO_INCREMENT PRIMARY KEY,
                name           VARCHAR(200) NOT NULL,
                category       VARCHAR(100),
                price          DECIMAL(10, 2),
                in_stock       BOOLEAN DEFAULT TRUE,
                created_date   DATE DEFAULT (CURRENT_DATE)
            ) ENGINE=InnoDB
            """
        )
        print("Table products created / confirmed")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                sale_id         INT AUTO_INCREMENT PRIMARY KEY,
                product_id      INT NOT NULL,
                quantity        INT NOT NULL,
                sale_date       DATE DEFAULT (CURRENT_DATE),
                total_amount    DECIMAL(12, 2),
                CONSTRAINT fk_sales_product
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
            ) ENGINE=InnoDB
            """
        )
        print("Table sales created / confirmed")

        cursor.close()

except Exception as e:
    print(f"Table creation failed: {e}")


# ============================================================
# SECTION 3: DATA READ / WRITE
# ============================================================

print("\n" + "=" * 60)
print("SECTION 3: DATA READ / WRITE")
print("=" * 60)

sample_products = [
    ("Wireless Keyboard", "Electronics", 79.99, True),
    ("Standing Desk", "Furniture", 349.00, True),
    ("USB-C Hub", "Electronics", 49.99, True),
    ("Desk Lamp", "Furniture", 39.99, False),
    ("Laptop Stand", "Electronics", 29.99, True),
]

try:
    with get_mysql_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM sales")
        cursor.execute("ALTER TABLE sales AUTO_INCREMENT = 1")
        cursor.execute("DELETE FROM products")
        cursor.execute("ALTER TABLE products AUTO_INCREMENT = 1")

        cursor.executemany(
            """
            INSERT INTO products (name, category, price, in_stock)
            VALUES (%s, %s, %s, %s)
            """,
            sample_products,
        )
        print(f"Inserted {len(sample_products)} rows into products")

        cursor.execute("SELECT product_id, name, price, in_stock FROM products ORDER BY product_id")
        rows = cursor.fetchall()
        print("\nAll products:")
        for row in rows:
            stock = "in stock" if row[3] else "out of stock"
            print(f"  [{row[0]}] {row[1]:<25} ${row[2]:.2f}  ({stock})")

        cursor.execute(
            """
            SELECT name, price
            FROM products
            WHERE category = %s AND in_stock = TRUE
            ORDER BY price DESC
            """,
            ("Electronics",),
        )
        electronics = cursor.fetchall()
        print(f"\nIn-stock Electronics ({len(electronics)} items):")
        for row in electronics:
            print(f"  {row[0]:<25} ${row[1]:.2f}")

        cursor.execute(
            """
            SELECT
                category,
                COUNT(*)             AS item_count,
                ROUND(AVG(price), 2) AS avg_price,
                MIN(price)           AS min_price,
                MAX(price)           AS max_price
            FROM products
            GROUP BY category
            ORDER BY category
            """
        )
        print("\nCategory summary:")
        for row in cursor.fetchall():
            print(f"  {row[0]:<15} count={row[1]}  avg=${row[2]}  range=${row[3]}–${row[4]}")

        cursor.execute(
            """
            UPDATE products
            SET price = price * 0.90
            WHERE category = 'Electronics'
            """
        )
        print(f"\nApplied 10% discount to Electronics ({cursor.rowcount} rows updated)")

        cursor.execute("DELETE FROM products WHERE in_stock = FALSE")
        print(f"Removed out-of-stock items ({cursor.rowcount} rows deleted)")

        cursor.close()

except Exception as e:
    print(f"Read/write operations failed: {e}")


# ============================================================
# SECTION 4: PANDAS + MYSQL
# ============================================================

print("\n" + "=" * 60)
print("SECTION 4: PANDAS + MYSQL")
print("=" * 60)

try:
    with get_mysql_connection() as conn:
        df = pd.read_sql("SELECT * FROM products ORDER BY product_id", conn)

    print("Products loaded into DataFrame:")
    print(df.to_string(index=False))
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"dtypes:\n{df.dtypes}")

except Exception as e:
    print(f"Fetch to pandas failed: {e}")


try:
    sales_data = pd.DataFrame(
        {
            "product_id": [1, 2, 3, 1, 3],
            "quantity": [2, 1, 3, 1, 2],
            "sale_date": [date.today()] * 5,
            "total_amount": [159.98, 349.00, 149.97, 79.99, 99.98],
        }
    )

    print(f"\nSales DataFrame to write ({len(sales_data)} rows):")
    print(sales_data.to_string(index=False))

    with get_mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales")
        cursor.execute("ALTER TABLE sales AUTO_INCREMENT = 1")

        cursor.executemany(
            """
            INSERT INTO sales (product_id, quantity, sale_date, total_amount)
            VALUES (%s, %s, %s, %s)
            """,
            list(sales_data.itertuples(index=False, name=None)),
        )
        cursor.close()
        print(f"\nInserted {len(sales_data)} rows from DataFrame into sales")

    with get_mysql_connection() as conn:
        result_df = pd.read_sql(
            """
            SELECT
                s.sale_id,
                p.name AS product_name,
                s.quantity,
                s.total_amount,
                s.sale_date
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            ORDER BY s.sale_id
            """,
            conn,
        )

    print("\nSales joined with Products (read back from MySQL):")
    print(result_df.to_string(index=False))

    print(f"\nTotal revenue: ${result_df['total_amount'].sum():.2f}")
    print(f"Units sold:    {result_df['quantity'].sum()}")
    print(f"Top product:   {result_df.groupby('product_name')['total_amount'].sum().idxmax()}")

except Exception as e:
    print(f"Pandas write-back failed: {e}")


# ============================================================
# CLEAN UP (OPTIONAL)
# ============================================================

print("\n" + "=" * 60)
print("CLEAN UP")
print("=" * 60)

try:
    with get_mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS sales")
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.close()
    print("Dropped sales and products tables")

except Exception as e:
    print(f"Cleanup failed: {e}")


# ============================================================
# KEY TAKEAWAYS
# ============================================================

print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)

notes = """
1. mysql-connector-python follows Python DB-API style
   - cursor.execute() / fetchall() / fetchone()
   - %s placeholders for parameterized SQL

2. Create the database once, then connect to it
   - bootstrap connection helps keep setup predictable

3. Use InnoDB for relational tables
   - supports transactions and foreign keys

4. pandas fits naturally in the workflow
   - pd.read_sql() for reads
   - DataFrame tuples + executemany() for writes

5. Keep credentials in environment variables
   - avoid hardcoded secrets in source code
"""

print(notes)

print("\n" + "=" * 60)
print("END OF MYSQL DEMO")
print("=" * 60)
