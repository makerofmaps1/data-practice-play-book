"""
PostgreSQL with Python

This script demonstrates working with PostgreSQL from Python, including:
- Connecting via psycopg2
- Schema and table creation
- Reading and writing data
- Pandas integration (query to DataFrame, write from DataFrame)

Requirements:
    pip install psycopg2-binary pandas

PostgreSQL Docs:
    https://www.postgresql.org/docs/
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date

import pandas as pd
import psycopg2

from db_config import get_postgres_config


# ============================================================
# CONNECTION CONFIGURATION
# ============================================================

POSTGRES_CONFIG = get_postgres_config()


print("\n" + "=" * 60)
print("POSTGRESQL WITH PYTHON")
print("=" * 60)


# ============================================================
# SECTION 1: CONNECTION
# ============================================================

print("\n" + "=" * 60)
print("SECTION 1: CONNECTION")
print("=" * 60)

try:
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT current_user, current_database(), version()")
    row = cursor.fetchone()
    print(f"Connected as: {row[0]}")
    print(f"Database:     {row[1]}")
    print(f"Version:      {row[2].split(',')[0]}")

    cursor.close()
    conn.close()
    print("Connection closed")

except Exception as e:
    print(f"Connection failed: {e}")


@contextmanager
def get_postgres_connection():
    """Context manager for PostgreSQL connections."""
    conn = None
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
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
    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP")
        ts = cursor.fetchone()[0]
        print(f"PostgreSQL server time: {ts}")
        cursor.close()
    print("Context manager closed connection automatically")

except Exception as e:
    print(f"Context manager connection failed: {e}")


# ============================================================
# SECTION 2: SCHEMA AND TABLE CREATION
# ============================================================

print("\n" + "=" * 60)
print("SECTION 2: SCHEMA AND TABLE CREATION")
print("=" * 60)

try:
    with get_postgres_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("CREATE SCHEMA IF NOT EXISTS demo_schema")
        print("Schema demo_schema created / confirmed")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS demo_schema.products (
                product_id    SERIAL PRIMARY KEY,
                name          VARCHAR(200) NOT NULL,
                category      VARCHAR(100),
                price         NUMERIC(10, 2),
                in_stock      BOOLEAN DEFAULT TRUE,
                created_date  DATE DEFAULT CURRENT_DATE
            )
            """
        )
        print("Table products created / confirmed")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS demo_schema.sales (
                sale_id        SERIAL PRIMARY KEY,
                product_id     INTEGER NOT NULL REFERENCES demo_schema.products(product_id),
                quantity       INTEGER NOT NULL,
                sale_date      DATE DEFAULT CURRENT_DATE,
                total_amount   NUMERIC(12, 2)
            )
            """
        )
        print("Table sales created / confirmed")

        cursor.close()

except Exception as e:
    print(f"Schema/table creation failed: {e}")


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
    with get_postgres_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE demo_schema.sales RESTART IDENTITY")
        cursor.execute("TRUNCATE TABLE demo_schema.products RESTART IDENTITY CASCADE")

        cursor.executemany(
            """
            INSERT INTO demo_schema.products (name, category, price, in_stock)
            VALUES (%s, %s, %s, %s)
            """,
            sample_products,
        )
        print(f"Inserted {len(sample_products)} rows into products")

        cursor.execute(
            """
            SELECT product_id, name, price, in_stock
            FROM demo_schema.products
            ORDER BY product_id
            """
        )
        rows = cursor.fetchall()
        print("\nAll products:")
        for row in rows:
            stock = "in stock" if row[3] else "out of stock"
            print(f"  [{row[0]}] {row[1]:<25} ${row[2]:.2f}  ({stock})")

        cursor.execute(
            """
            SELECT name, price
            FROM demo_schema.products
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
                COUNT(*)              AS item_count,
                ROUND(AVG(price), 2)  AS avg_price,
                MIN(price)            AS min_price,
                MAX(price)            AS max_price
            FROM demo_schema.products
            GROUP BY category
            ORDER BY category
            """
        )
        print("\nCategory summary:")
        for row in cursor.fetchall():
            print(f"  {row[0]:<15} count={row[1]}  avg=${row[2]}  range=${row[3]}–${row[4]}")

        cursor.execute(
            """
            UPDATE demo_schema.products
            SET price = price * 0.90
            WHERE category = 'Electronics'
            """
        )
        print(f"\nApplied 10% discount to Electronics ({cursor.rowcount} rows updated)")

        cursor.execute("DELETE FROM demo_schema.products WHERE in_stock = FALSE")
        print(f"Removed out-of-stock items ({cursor.rowcount} rows deleted)")

        cursor.close()

except Exception as e:
    print(f"Read/write operations failed: {e}")


# ============================================================
# SECTION 4: PANDAS + POSTGRESQL
# ============================================================

print("\n" + "=" * 60)
print("SECTION 4: PANDAS + POSTGRESQL")
print("=" * 60)

try:
    with get_postgres_connection() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM demo_schema.products ORDER BY product_id",
            conn,
        )

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

    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE demo_schema.sales RESTART IDENTITY")

        cursor.executemany(
            """
            INSERT INTO demo_schema.sales (product_id, quantity, sale_date, total_amount)
            VALUES (%s, %s, %s, %s)
            """,
            list(sales_data.itertuples(index=False, name=None)),
        )
        cursor.close()
        print(f"\nInserted {len(sales_data)} rows from DataFrame into sales")

    with get_postgres_connection() as conn:
        result_df = pd.read_sql_query(
            """
            SELECT
                s.sale_id,
                p.name AS product_name,
                s.quantity,
                s.total_amount,
                s.sale_date
            FROM demo_schema.sales s
            JOIN demo_schema.products p ON s.product_id = p.product_id
            ORDER BY s.sale_id
            """,
            conn,
        )

    print("\nSales joined with Products (read back from PostgreSQL):")
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
    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP SCHEMA IF EXISTS demo_schema CASCADE")
        cursor.close()
    print("demo_schema dropped (CASCADE removes all tables inside it)")

except Exception as e:
    print(f"Cleanup failed: {e}")


# ============================================================
# KEY TAKEAWAYS
# ============================================================

print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)

notes = """
1. psycopg2 uses familiar DB-API patterns
   - cursor.execute() / fetchall() / fetchone()
   - %s placeholders for parameterized queries

2. PostgreSQL schemas are helpful
   - Keep demo or app objects grouped logically

3. pandas + PostgreSQL works cleanly
   - pd.read_sql_query() for DataFrame reads
   - Use executemany() for straightforward writes

4. Use transactions deliberately
   - commit on success, rollback on failure

5. Keep credentials out of code
   - environment variables locally
   - secrets manager in production
"""

print(notes)

print("\n" + "=" * 60)
print("END OF POSTGRESQL DEMO")
print("=" * 60)
