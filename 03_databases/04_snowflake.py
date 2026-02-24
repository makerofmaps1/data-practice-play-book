"""
Snowflake with Python (Simple)

Minimal demo of Snowflake connection and basic SQL using credentials from
03_databases/.env.

Covers:
- Connect with snowflake-connector-python
- Use warehouse/database/schema from config
- CREATE TABLE, INSERT, SELECT, UPDATE, DELETE

Requirements:
    pip install snowflake-connector-python
"""

from __future__ import annotations

from contextlib import contextmanager

import snowflake.connector

from db_config import get_snowflake_config, require_config


# ============================================================
# CONNECTION CONFIGURATION (.env)
# ============================================================

SNOWFLAKE_CONFIG = get_snowflake_config()
require_config(
    config=SNOWFLAKE_CONFIG,
    required_keys=("account", "user", "password", "warehouse", "database"),
    env_prefix="SNOWFLAKE",
)


print("\n" + "=" * 60)
print("SNOWFLAKE WITH PYTHON (SIMPLE)")
print("=" * 60)


@contextmanager
def get_snowflake_connection():
    """Context manager for Snowflake connections."""
    conn = None
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
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


# ============================================================
# SECTION 1: CONNECTION TEST
# ============================================================

print("\n" + "=" * 60)
print("SECTION 1: CONNECTION TEST")
print("=" * 60)

try:
    with get_snowflake_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(f"USE WAREHOUSE {SNOWFLAKE_CONFIG['warehouse']}")
        cursor.execute(f"USE DATABASE {SNOWFLAKE_CONFIG['database']}")
        cursor.execute(f"USE SCHEMA {SNOWFLAKE_CONFIG['schema']}")

        cursor.execute("SELECT CURRENT_USER(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
        user_name, warehouse, database_name, schema_name = cursor.fetchone()

        print(f"Connected as: {user_name}")
        print(f"Warehouse:    {warehouse}")
        print(f"Database:     {database_name}")
        print(f"Schema:       {schema_name}")

        cursor.close()

except Exception as e:
    print(f"Connection setup failed: {e}")
    print("Hint: Use a regular database like DEMO_DB. USER$<username> cannot create tables.")
    raise SystemExit(1)


# ============================================================
# SECTION 2: BASIC SQL (CREATE / INSERT / SELECT / UPDATE / DELETE)
# ============================================================

print("\n" + "=" * 60)
print("SECTION 2: BASIC SQL")
print("=" * 60)

sample_rows = [
    ("Keyboard", 79.99, True),
    ("Mouse", 29.99, True),
    ("Desk Lamp", 39.99, False),
]

try:
    with get_snowflake_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(f"USE WAREHOUSE {SNOWFLAKE_CONFIG['warehouse']}")
        cursor.execute(f"USE DATABASE {SNOWFLAKE_CONFIG['database']}")
        cursor.execute(f"USE SCHEMA {SNOWFLAKE_CONFIG['schema']}")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS DEMO_PRODUCTS (
                PRODUCT_ID INTEGER AUTOINCREMENT PRIMARY KEY,
                NAME VARCHAR(100) NOT NULL,
                PRICE NUMBER(10, 2),
                IN_STOCK BOOLEAN
            )
            """
        )
        print("Created/confirmed table: DEMO_PRODUCTS")

        cursor.execute("TRUNCATE TABLE DEMO_PRODUCTS")

        cursor.executemany(
            """
            INSERT INTO DEMO_PRODUCTS (NAME, PRICE, IN_STOCK)
            VALUES (%s, %s, %s)
            """,
            sample_rows,
        )
        print(f"Inserted {len(sample_rows)} rows")

        cursor.execute("SELECT PRODUCT_ID, NAME, PRICE, IN_STOCK FROM DEMO_PRODUCTS ORDER BY PRODUCT_ID")
        print("\nSELECT result:")
        for product_id, name, price, in_stock in cursor.fetchall():
            status = "in stock" if in_stock else "out of stock"
            print(f"  [{product_id}] {name:<12} ${price:.2f} ({status})")

        cursor.execute("UPDATE DEMO_PRODUCTS SET PRICE = PRICE * 0.90 WHERE IN_STOCK = TRUE")
        print(f"\nUpdated {cursor.rowcount} row(s) (10% discount)")

        cursor.execute("DELETE FROM DEMO_PRODUCTS WHERE IN_STOCK = FALSE")
        print(f"Deleted {cursor.rowcount} row(s) (out-of-stock)")

        cursor.execute("SELECT COUNT(*) FROM DEMO_PRODUCTS")
        remaining = cursor.fetchone()[0]
        print(f"Remaining rows: {remaining}")

        cursor.close()

except Exception as e:
    print(f"Basic SQL demo failed: {e}")


print("\n" + "=" * 60)
print("END OF SIMPLE SNOWFLAKE DEMO")
print("=" * 60)
