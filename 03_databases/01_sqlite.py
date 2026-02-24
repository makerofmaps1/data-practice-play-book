"""
SQLite with Python

This script demonstrates working with SQLite from Python, including:
- Connecting via sqlite3 (built into Python)
- Table creation
- Reading and writing data
- Pandas integration (query to DataFrame, write from DataFrame)

Requirements:
    pip install pandas

SQLite Docs:
    https://docs.python.org/3/library/sqlite3.html
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import pandas as pd


# ============================================================
# CONNECTION CONFIGURATION
# ============================================================

DB_PATH = Path(__file__).with_name("sqlite_demo.db")


print("\n" + "=" * 60)
print("SQLITE WITH PYTHON")
print("=" * 60)


# ============================================================
# SECTION 1: CONNECTION
# ============================================================

print("\n" + "=" * 60)
print("SECTION 1: CONNECTION")
print("=" * 60)

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT sqlite_version()")
    row = cursor.fetchone()
    print(f"Connected to SQLite version: {row[0]}")
    print(f"Database file: {DB_PATH}")

    cursor.close()
    conn.close()
    print("Connection closed")

except Exception as e:
    print(f"Connection failed: {e}")


@contextmanager
def get_sqlite_connection():
    """Context manager for SQLite connections."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
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
    with get_sqlite_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT datetime('now')")
        ts = cursor.fetchone()[0]
        print(f"SQLite server time (UTC): {ts}")
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
    with get_sqlite_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS PRODUCTS (
                PRODUCT_ID   INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME         TEXT    NOT NULL,
                CATEGORY     TEXT,
                PRICE        REAL,
                IN_STOCK     INTEGER DEFAULT 1,
                CREATED_DATE TEXT    DEFAULT (date('now'))
            )
            """
        )
        print("Table PRODUCTS created / confirmed")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS SALES (
                SALE_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
                PRODUCT_ID    INTEGER NOT NULL,
                QUANTITY      INTEGER NOT NULL,
                SALE_DATE     TEXT    DEFAULT (date('now')),
                TOTAL_AMOUNT  REAL,
                FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCTS(PRODUCT_ID)
            )
            """
        )
        print("Table SALES created / confirmed")

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
    ("Wireless Keyboard", "Electronics", 79.99, 1),
    ("Standing Desk", "Furniture", 349.00, 1),
    ("USB-C Hub", "Electronics", 49.99, 1),
    ("Desk Lamp", "Furniture", 39.99, 0),
    ("Laptop Stand", "Electronics", 29.99, 1),
]

try:
    with get_sqlite_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM SALES")
        cursor.execute("DELETE FROM PRODUCTS")

        cursor.executemany(
            """
            INSERT INTO PRODUCTS (NAME, CATEGORY, PRICE, IN_STOCK)
            VALUES (?, ?, ?, ?)
            """,
            sample_products,
        )
        print(f"Inserted {len(sample_products)} rows into PRODUCTS")

        cursor.execute(
            "SELECT PRODUCT_ID, NAME, PRICE, IN_STOCK FROM PRODUCTS ORDER BY PRODUCT_ID"
        )
        rows = cursor.fetchall()
        print("\nAll products:")
        for row in rows:
            stock = "in stock" if row[3] == 1 else "out of stock"
            print(f"  [{row[0]}] {row[1]:<25} ${row[2]:.2f}  ({stock})")

        cursor.execute(
            """
            SELECT NAME, PRICE
            FROM PRODUCTS
            WHERE CATEGORY = ? AND IN_STOCK = 1
            ORDER BY PRICE DESC
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
                CATEGORY,
                COUNT(*)              AS ITEM_COUNT,
                ROUND(AVG(PRICE), 2)  AS AVG_PRICE,
                MIN(PRICE)            AS MIN_PRICE,
                MAX(PRICE)            AS MAX_PRICE
            FROM PRODUCTS
            GROUP BY CATEGORY
            ORDER BY CATEGORY
            """
        )
        print("\nCategory summary:")
        for row in cursor.fetchall():
            print(f"  {row[0]:<15} count={row[1]}  avg=${row[2]}  range=${row[3]}–${row[4]}")

        cursor.execute(
            """
            UPDATE PRODUCTS
            SET PRICE = PRICE * 0.90
            WHERE CATEGORY = 'Electronics'
            """
        )
        print(f"\nApplied 10% discount to Electronics ({cursor.rowcount} rows updated)")

        cursor.execute("DELETE FROM PRODUCTS WHERE IN_STOCK = 0")
        print(f"Removed out-of-stock items ({cursor.rowcount} rows deleted)")

        cursor.close()

except Exception as e:
    print(f"Read/write operations failed: {e}")


# ============================================================
# SECTION 4: PANDAS + SQLITE
# ============================================================

print("\n" + "=" * 60)
print("SECTION 4: PANDAS + SQLITE")
print("=" * 60)

try:
    with get_sqlite_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM PRODUCTS ORDER BY PRODUCT_ID", conn)

    print("Products loaded into DataFrame:")
    print(df.to_string(index=False))
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"dtypes:\n{df.dtypes}")

except Exception as e:
    print(f"Fetch to pandas failed: {e}")


try:
    sales_data = pd.DataFrame(
        {
            "PRODUCT_ID": [1, 2, 3, 1, 3],
            "QUANTITY": [2, 1, 3, 1, 2],
            "SALE_DATE": [date.today().isoformat()] * 5,
            "TOTAL_AMOUNT": [159.98, 349.00, 149.97, 79.99, 99.98],
        }
    )

    print(f"\nSales DataFrame to write ({len(sales_data)} rows):")
    print(sales_data.to_string(index=False))

    with get_sqlite_connection() as conn:
        sales_data.to_sql("SALES", conn, if_exists="append", index=False)
        print(f"\nWrote {len(sales_data)} rows from DataFrame into SALES")

    with get_sqlite_connection() as conn:
        result_df = pd.read_sql_query(
            """
            SELECT
                s.SALE_ID,
                p.NAME AS PRODUCT_NAME,
                s.QUANTITY,
                s.TOTAL_AMOUNT,
                s.SALE_DATE
            FROM SALES s
            JOIN PRODUCTS p ON s.PRODUCT_ID = p.PRODUCT_ID
            ORDER BY s.SALE_ID
            """,
            conn,
        )

    print("\nSales joined with Products (read back from SQLite):")
    print(result_df.to_string(index=False))

    print(f"\nTotal revenue: ${result_df['TOTAL_AMOUNT'].sum():.2f}")
    print(f"Units sold:    {result_df['QUANTITY'].sum()}")
    print(f"Top product:   {result_df.groupby('PRODUCT_NAME')['TOTAL_AMOUNT'].sum().idxmax()}")

except Exception as e:
    print(f"Pandas write-back failed: {e}")


# ============================================================
# CLEAN UP (OPTIONAL)
# ============================================================

print("\n" + "=" * 60)
print("CLEAN UP")
print("=" * 60)

try:
    with get_sqlite_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS SALES")
        cursor.execute("DROP TABLE IF EXISTS PRODUCTS")
        cursor.close()
    print("Dropped SALES and PRODUCTS tables")

except Exception as e:
    print(f"Cleanup failed: {e}")


# ============================================================
# KEY TAKEAWAYS
# ============================================================

print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)

notes = """
1. sqlite3 is built into Python
   - Great for local prototyping and tests
   - No external server required

2. SQLite placeholders use ? (not %s)
   - Keep parameterized queries to avoid SQL injection

3. pandas + SQLite is simple
   - pd.read_sql_query() for reads
   - DataFrame.to_sql() for quick writes

4. SQLite stores booleans as integers
   - Typically 1=True and 0=False

5. Keep schema small and explicit
   - SQLite is flexible with types, but clear definitions help consistency
"""

print(notes)

print("\n" + "=" * 60)
print("END OF SQLITE DEMO")
print("=" * 60)
