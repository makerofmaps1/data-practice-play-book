"""
SQL Bulk Operations Demonstration

This script demonstrates efficient bulk data operations across database engines.
Covers:
- executemany() for batch inserts (SQLite, PostgreSQL, MySQL compatible)
- Batch insert strategies and performance
- Transaction batching
- COPY operations (PostgreSQL specific)
- Bulk update and delete patterns

Uses SQLite for working examples with PostgreSQL patterns shown for reference.
"""

from __future__ import annotations

import sqlite3
import time


print("\n" + "=" * 60)
print("SQL BULK OPERATIONS")
print("=" * 60)


# ============================================================
# SETUP DATABASE AND SCHEMA
# ============================================================

print("\n" + "=" * 60)
print("SETUP")
print("=" * 60)

# Create single shared in-memory database
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        transaction_date DATE NOT NULL,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
""")

cursor.execute("""
    CREATE INDEX idx_user_email ON users(email)
""")

cursor.execute("""
    CREATE INDEX idx_transaction_user ON transactions(user_id)
""")

conn.commit()
print("Tables and indexes created")


# ============================================================
# INDIVIDUAL INSERTS (SLOW - FOR COMPARISON)
# ============================================================

print("\n" + "=" * 60)
print("INDIVIDUAL INSERTS (BASELINE)")
print("=" * 60)

num_records = 1000

start_time = time.time()

for i in range(num_records):
    cursor.execute(
        "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
        (f"user_{i}", f"user_{i}@email.com", 20 + (i % 50))
    )
    conn.commit()  # Commit each insert (very slow!)

elapsed = time.time() - start_time
print(f"Inserted {num_records} records individually: {elapsed:.3f} seconds")
print(f"Rate: {num_records / elapsed:.0f} records/second")


# ============================================================
# EXECUTEMANY - STANDARD BULK INSERT
# ============================================================

print("\n" + "=" * 60)
print("EXECUTEMANY - STANDARD BULK INSERT")
print("=" * 60)

# Clear for next test
cursor.execute("DELETE FROM transactions")
cursor.execute("DELETE FROM users")
conn.commit()

num_records = 10000
users_data = [
    (f"user_{i}", f"user_{i}@email.com", 20 + (i % 50))
    for i in range(num_records)
]

start_time = time.time()

# executemany() - works on SQLite, PostgreSQL, MySQL
cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    users_data
)
conn.commit()

elapsed = time.time() - start_time
print(f"Inserted {num_records} records with executemany(): {elapsed:.3f} seconds")
print(f"Rate: {num_records / elapsed:.0f} records/second")

# Verify
cursor.execute("SELECT COUNT(*) as count FROM users")
count = cursor.fetchone()['count']
print(f"Total users in database: {count}")


# ============================================================
# BATCH INSERTS WITH TRANSACTION CONTROL
# ============================================================

print("\n" + "=" * 60)
print("BATCH INSERTS WITH TRANSACTION CONTROL")
print("=" * 60)

cursor.execute("DELETE FROM users")
conn.commit()

num_records = 10000
batch_size = 500

users_data = [
    (f"user_{i}", f"user_{i}@email.com", 20 + (i % 50))
    for i in range(num_records)
]

start_time = time.time()

# Process in batches
for i in range(0, len(users_data), batch_size):
    batch = users_data[i:i + batch_size]
    cursor.executemany(
        "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
        batch
    )
    conn.commit()  # Commit each batch

elapsed = time.time() - start_time
print(f"Inserted {num_records} records in batches of {batch_size}: {elapsed:.3f} seconds")
print(f"Rate: {num_records / elapsed:.0f} records/second")


# ============================================================
# MULTI-VALUE INSERT (SINGLE STATEMENT)
# ============================================================

print("\n" + "=" * 60)
print("MULTI-VALUE INSERT (SINGLE STATEMENT)")
print("=" * 60)

cursor.execute("DELETE FROM users")
conn.commit()

num_records = 1000
users_data = [
    (f"user_{i}", f"user_{i}@email.com", 20 + (i % 50))
    for i in range(num_records)
]

start_time = time.time()

# Build multi-value INSERT statement
placeholders = ", ".join(["(?, ?, ?)"] * len(users_data))
query = f"INSERT INTO users (username, email, age) VALUES {placeholders}"

# Flatten the data list
flat_data = [item for row in users_data for item in row]

cursor.execute(query, flat_data)
conn.commit()

elapsed = time.time() - start_time
print(f"Inserted {num_records} records with multi-value INSERT: {elapsed:.3f} seconds")
print(f"Rate: {num_records / elapsed:.0f} records/second")


# ============================================================
# BULK INSERT WITH RETURNING (PostgreSQL Pattern)
# ============================================================

print("\n" + "=" * 60)
print("BULK INSERT WITH RETURNING")
print("=" * 60)

print("""
PostgreSQL supports RETURNING clause to get inserted IDs:

# PostgreSQL example (requires psycopg2)
cursor.executemany(
    '''
    INSERT INTO users (username, email, age)
    VALUES (%s, %s, %s)
    RETURNING user_id
    ''',
    users_data
)
inserted_ids = [row[0] for row in cursor.fetchall()]
""")

# SQLite equivalent using lastrowid
cursor.execute("DELETE FROM users")
conn.commit()

users_data = [
    (f"batch_user_{i}", f"batch_user_{i}@email.com", 25)
    for i in range(5)
]

inserted_ids = []
for username, email, age in users_data:
    cursor.execute(
        "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
        (username, email, age)
    )
    inserted_ids.append(cursor.lastrowid)

conn.commit()

print(f"\nSQLite - Inserted user IDs: {inserted_ids}")


# ============================================================
# POSTGRESQL COPY PATTERN
# ============================================================

print("\n" + "=" * 60)
print("POSTGRESQL COPY PATTERN")
print("=" * 60)

print("""
PostgreSQL COPY is the fastest bulk load method:

# Method 1: COPY from CSV file
import io
from psycopg2 import sql

csv_data = io.StringIO()
for user in users_data:
    csv_data.write(f"{user[0]},{user[1]},{user[2]}\\n")
csv_data.seek(0)

cursor.copy_expert(
    '''
    COPY users (username, email, age)
    FROM STDIN WITH CSV
    ''',
    csv_data
)

# Method 2: COPY with custom delimiter
cursor.copy_from(
    csv_data,
    'users',
    columns=('username', 'email', 'age'),
    sep=','
)

# Can load millions of rows per second with COPY
""")


# ============================================================
# BULK UPDATE
# ============================================================

print("\n" + "=" * 60)
print("BULK UPDATE")
print("=" * 60)

# Clear and insert test data
cursor.execute("DELETE FROM users")
conn.commit()

users_data = [
    (f"update_user_{i}", f"update_user_{i}@email.com", 25)
    for i in range(100)
]
cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    users_data
)
conn.commit()

# Method 1: Update all matching rows at once
start_time = time.time()
cursor.execute("UPDATE users SET age = age + 1 WHERE age < 30")
conn.commit()
elapsed = time.time() - start_time
print(f"Bulk updated {cursor.rowcount} rows: {elapsed:.4f} seconds")

# Method 2: Batch updates with executemany
updates_data = [
    (i + 100, f"update_user_{i}")  # new age, username
    for i in range(50)
]

start_time = time.time()
cursor.executemany(
    "UPDATE users SET age = ? WHERE username = ?",
    updates_data
)
conn.commit()
elapsed = time.time() - start_time
print(f"Batch updated {len(updates_data)} rows with executemany: {elapsed:.4f} seconds")


# ============================================================
# BULK DELETE
# ============================================================

print("\n" + "=" * 60)
print("BULK DELETE")
print("=" * 60)

# Insert test data
cursor.execute("DELETE FROM users")
conn.commit()

users_data = [
    (f"delete_user_{i}", f"delete_user_{i}@email.com", 25)
    for i in range(1000)
]
cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    users_data
)
conn.commit()

# Method 1: Delete all matching rows
start_time = time.time()
cursor.execute("DELETE FROM users WHERE username LIKE 'delete_user_%'")
conn.commit()
elapsed = time.time() - start_time
print(f"Bulk deleted {cursor.rowcount} rows: {elapsed:.4f} seconds")

# Method 2: Delete with IN clause (for specific IDs)
cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    [(f"temp_{i}", f"temp_{i}@email.com", 25) for i in range(10)]
)
conn.commit()

# Get IDs to delete
cursor.execute("SELECT user_id FROM users WHERE username LIKE 'temp_%'")
ids_to_delete = [row['user_id'] for row in cursor.fetchall()]

# Delete using IN clause with placeholders
placeholders = ', '.join(['?'] * len(ids_to_delete))
cursor.execute(f"DELETE FROM users WHERE user_id IN ({placeholders})", ids_to_delete)
conn.commit()
print(f"Deleted {len(ids_to_delete)} specific rows using IN clause")


# ============================================================
# UPSERT OPERATIONS (INSERT OR UPDATE)
# ============================================================

print("\n" + "=" * 60)
print("UPSERT OPERATIONS")
print("=" * 60)

# Clear and insert initial data
cursor.execute("DELETE FROM users")
conn.commit()

users_data = [
    ("alice", "alice@email.com", 30),
    ("bob", "bob@email.com", 25),
    ("charlie", "charlie@email.com", 35),
]

cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    users_data
)
conn.commit()
print("Inserted initial users")

# Get IDs
cursor.execute("SELECT user_id, username FROM users WHERE username IN ('alice', 'bob', 'charlie')")
user_map = {row['username']: row['user_id'] for row in cursor.fetchall()}

# SQLite: INSERT OR REPLACE
upsert_data = [
    (user_map['alice'], "alice", "alice_new@email.com", 31),  # Update
    (None, "diana", "diana@email.com", 28),  # Insert new
]

cursor.executemany(
    """
    INSERT OR REPLACE INTO users (user_id, username, email, age)
    VALUES (?, ?, ?, ?)
    """,
    upsert_data
)
conn.commit()
print(f"Upserted {len(upsert_data)} rows (SQLite INSERT OR REPLACE)")

# Verify
cursor.execute("SELECT username, email, age FROM users WHERE username IN ('alice', 'diana')")
for row in cursor.fetchall():
    print(f"  {row['username']}: {row['email']}, age {row['age']}")

print("""
PostgreSQL UPSERT (ON CONFLICT):

cursor.executemany(
    '''
    INSERT INTO users (username, email, age)
    VALUES (%s, %s, %s)
    ON CONFLICT (username)
    DO UPDATE SET email = EXCLUDED.email, age = EXCLUDED.age
    ''',
    users_data
)
""")


# ============================================================
# BULK INSERT WITH FOREIGN KEYS
# ============================================================

print("\n" + "=" * 60)
print("BULK INSERT WITH FOREIGN KEYS")
print("=" * 60)

# Clear all
cursor.execute("DELETE FROM transactions")
cursor.execute("DELETE FROM users")
conn.commit()

# Insert users first
users_data = [
    (f"fk_user_{i}", f"fk_user_{i}@email.com", 25)
    for i in range(10)
]

cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    users_data
)
conn.commit()

# Get inserted user IDs
cursor.execute("SELECT user_id FROM users WHERE username LIKE 'fk_user_%'")
user_ids = [row['user_id'] for row in cursor.fetchall()]

# Bulk insert transactions with foreign keys
import random
transactions_data = [
    (random.choice(user_ids), round(random.uniform(10, 1000), 2), "2024-01-15", "completed")
    for _ in range(50)
]

cursor.executemany(
    """
    INSERT INTO transactions (user_id, amount, transaction_date, status)
    VALUES (?, ?, ?, ?)
    """,
    transactions_data
)
conn.commit()

print(f"Inserted {len(transactions_data)} transactions for {len(user_ids)} users")

# Verify with JOIN
cursor.execute("""
    SELECT 
        u.username,
        COUNT(t.transaction_id) as transaction_count,
        SUM(t.amount) as total_amount
    FROM users u
    LEFT JOIN transactions t ON u.user_id = t.user_id
    WHERE u.username LIKE 'fk_user_%'
    GROUP BY u.user_id, u.username
    ORDER BY total_amount DESC
    LIMIT 5
""")

print("\nTop 5 users by transaction amount:")
for row in cursor.fetchall():
    print(f"  {row['username']}: {row['transaction_count']} transactions, ${row['total_amount']:.2f}")


# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

print("\n" + "=" * 60)
print("PERFORMANCE COMPARISON")
print("=" * 60)

cursor.execute("DELETE FROM transactions")
cursor.execute("DELETE FROM users")
conn.commit()

num_records = 5000
results = {}

# Test 1: Individual inserts with commits
start = time.time()
for i in range(num_records):
    cursor.execute(
        "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
        (f"perf_user_{i}", f"perf_{i}@email.com", 25)
    )
    conn.commit()
results['Individual + commit each'] = time.time() - start

# Test 2: Individual inserts, single commit
cursor.execute("DELETE FROM users")
conn.commit()

start = time.time()
for i in range(num_records):
    cursor.execute(
        "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
        (f"perf_user_{i}", f"perf_{i}@email.com", 25)
    )
conn.commit()
results['Individual + single commit'] = time.time() - start

# Test 3: executemany
cursor.execute("DELETE FROM users")
conn.commit()

data = [(f"perf_user_{i}", f"perf_{i}@email.com", 25) for i in range(num_records)]
start = time.time()
cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    data
)
conn.commit()
results['executemany'] = time.time() - start

# Test 4: Batch commits
cursor.execute("DELETE FROM users")
conn.commit()

data = [(f"perf_user_{i}", f"perf_{i}@email.com", 25) for i in range(num_records)]
batch_size = 500
start = time.time()
for i in range(0, len(data), batch_size):
    cursor.executemany(
        "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
        data[i:i + batch_size]
    )
    conn.commit()
results['Batch commits (500)'] = time.time() - start

print(f"\nPerformance for {num_records} records:")
for method, elapsed in sorted(results.items(), key=lambda x: x[1]):
    rate = num_records / elapsed
    print(f"  {method:30s}: {elapsed:6.3f}s ({rate:8.0f} rows/sec)")


# ============================================================
# BEST PRACTICES
# ============================================================

print("\n" + "=" * 60)
print("BULK OPERATIONS BEST PRACTICES")
print("=" * 60)

best_practices = """
1. Use executemany() for cross-database compatibility
   - Works on SQLite, PostgreSQL, MySQL, etc.
   - Faster than individual inserts
   - Maintains parameterized query safety

2. Control transaction commits
   - Don't commit after each record (very slow)
   - Commit in batches (balance between speed and safety)
   - Use single commit for entire bulk operation when possible

3. Use database-specific optimizations when available
   - PostgreSQL: COPY for fastest bulk loads (millions of rows/sec)
   - MySQL: LOAD DATA INFILE
   - SQLite: Disable synchronous mode for temp data

4. Batch size considerations
   - Too small: Slower due to overhead
   - Too large: Memory issues, long locks
   - Typical sweet spot: 500-5000 rows per batch

5. Use indexes wisely
   - Drop indexes before bulk insert, rebuild after (for large loads)
   - Keep indexes for smaller bulk operations
   - Consider deferring foreign key checks for large loads

6. Handle errors gracefully
   - Use transactions for rollback capability
   - Log failed batches
   - Consider continuing on error vs. failing fast

7. Monitor memory usage
   - Don't load all data into memory at once
   - Use generators or iterators for large datasets
   - Process in chunks

8. Database-specific patterns:
   
   SQLite:
   - BEGIN TRANSACTION / COMMIT for speed
   - PRAGMA synchronous = OFF (for temp data only)
   - INSERT OR REPLACE for upserts
   
   PostgreSQL:
   - COPY for fastest bulk load
   - ON CONFLICT for upserts
   - RETURNING clause to get inserted IDs
   - Use UNLOGGED tables for temp data
   
   MySQL:
   - LOAD DATA INFILE for bulk loads
   - INSERT IGNORE for duplicate handling
   - ON DUPLICATE KEY UPDATE for upserts

9. Validate data before bulk insert
   - Check constraints, types, nullability
   - Better to fail early than mid-batch

10. Use bulk operations for updates/deletes too
    - UPDATE with WHERE clause instead of row-by-row
    - DELETE with IN clause for specific records
    - Use executemany for batched updates
"""

print(best_practices)

# Clean up
cursor.close()
conn.close()

print("\n" + "=" * 60)
print("END OF BULK OPERATIONS DEMO")
print("=" * 60)
