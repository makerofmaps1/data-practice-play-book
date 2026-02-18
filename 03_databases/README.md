# Database Operations

Comprehensive demonstrations of database operations in Python, covering raw SQL, connection management, and bulk operations. Includes both SQLite and PostgreSQL examples with production-grade patterns.

## Overview

This directory demonstrates professional database programming practices:

- **SQL Query Fundamentals**: CREATE, INSERT, SELECT, UPDATE, DELETE, JOINs, aggregations, subqueries, transactions
- **Connection Management**: Basic connections, context managers, connection pooling, thread safety
- **Bulk Operations**: executemany(), batch inserts, bulk updates/deletes, UPSERT patterns, performance optimization
- **Database Compatibility**: Cross-database patterns for SQLite, PostgreSQL, and MySQL

## Files

### `raw_sql/connection.py`
Database connection and pooling patterns. Covers:

- **Basic SQLite & PostgreSQL connections** - Simple connection establishment
- **Context managers** - Safe connection handling with automatic cleanup
- **Connection pooling** - SimpleConnectionPool and ThreadedConnectionPool for efficient resource management
- **Singleton pattern** - Application-wide shared database connection
- **Production best practices** - 10 key principles for reliable database operations

**Key Patterns:**
- 3 connection pool implementations
- PostgreSQL connection with local credentials (postgres/postgres)
- Thread-safe pooling for concurrent applications
- Error handling and resource cleanup

**Run:** `python raw_sql/connection.py`

### `sql_queries.py`
SQL fundamentals using in-memory SQLite. Covers:

- **CREATE TABLE** - Schema definitions with constraints and foreign keys
- **INSERT** - Single and parameterized inserts with SQL injection prevention
- **SELECT** - Basic queries, WHERE filtering, LIKE patterns, BETWEEN, IN clauses
- **JOINs** - INNER, LEFT, RIGHT, OUTER joins with multiple table examples
- **GROUP BY & HAVING** - Aggregations with COUNT, SUM, AVG, MIN, MAX
- **Subqueries** - WHERE, SELECT, and EXISTS subqueries
- **ORDER BY & LIMIT** - Sorting and pagination with OFFSET
- **UPDATE & DELETE** - Modifications and deletions with WHERE conditions
- **Transactions** - COMMIT and ROLLBACK for data consistency
- **Window Functions** - ROW_NUMBER, RANK, DENSE_RANK
- **CASE Statements** - Conditional logic in queries

**Key Patterns:**
- Parameterized queries to prevent SQL injection (with prominent warnings)
- E-commerce schema (products, orders, customers)
- Common query patterns for real applications
- Transaction examples for multi-statement operations

**Run:** `python sql_queries.py`

### `sql_bulk_operations.py`
Efficient bulk data operations and performance optimization. Covers:

- **executemany()** - Standard bulk insert method (cross-database compatible)
- **Batch processing** - Transaction batching for optimal performance
- **Multi-value INSERT** - Single SQL statement with multiple rows
- **Bulk UPDATE** - Updating many rows efficiently
- **Bulk DELETE** - Deleting multiple records with IN clauses
- **UPSERT** - INSERT OR REPLACE (SQLite) and ON CONFLICT (PostgreSQL)
- **Foreign key handling** - Maintaining referential integrity during bulk operations
- **Performance comparison** - 5 different insertion methods with metrics
- **Database-specific patterns** - PostgreSQL COPY, MySQL LOAD DATA INFILE

**Key Patterns:**
- Performance tuning: 506k rows/sec with executemany() vs 143k rows/sec with individual commits
- Batch size optimization (sweet spot: 500-5000 rows)
- Error handling during bulk operations
- Memory-efficient processing

**Performance Results (5000 records):**
- executemany with single commit: **506k rows/sec** ✓ Fastest
- Individual inserts + single commit: 332k rows/sec
- Batch commits (500 rows): 293k rows/sec
- Individual inserts + commit each: 143k rows/sec (very slow)

**Run:** `python sql_bulk_operations.py`

## Requirements

### Core Dependencies
```
sqlite3 (built-in)
psycopg2 (for PostgreSQL)
```

### Installation

```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Or if using conda
conda install psycopg2
```

## PostgreSQL Setup (Optional)

To run PostgreSQL examples in `raw_sql/connection.py`:

1. Have PostgreSQL server running locally
2. Default credentials: username=`postgres`, password=`postgres`
3. All examples will fall back to SQLite if PostgreSQL is unavailable

## Running the Examples

Each script is self-contained with inline data—no external files or databases required:

```bash
# View connection and pooling patterns
python raw_sql/connection.py

# Learn SQL fundamentals
python sql_queries.py

# Optimize bulk operations
python sql_bulk_operations.py
```

All output is printed to console with clear section headers.

## Key Concepts Demonstrated

### SQL Injection Prevention
```python
# WRONG - Vulnerable to SQL injection
query = f"SELECT * FROM users WHERE username = '{username}'"

# RIGHT - Use parameterized queries
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### Connection Pooling
```python
# Instead of creating new connection each time (slow and resource-intensive):
pool = psycopg2.pool.SimpleConnectionPool(1, 20, database="mydb")
conn = pool.getconn()
# ... use connection ...
pool.putconn(conn)
```

### Bulk Operations Performance
```python
# Slow: Individual inserts with commits (143k rows/sec)
for row in data:
    cursor.execute("INSERT INTO table VALUES (...)", row)
    conn.commit()

# Fast: executemany with single commit (506k rows/sec)
cursor.executemany("INSERT INTO table VALUES (...)", data)
conn.commit()
```

### Transaction Safety
```python
try:
    cursor.execute("INSERT INTO table VALUES (...)")
    # Do more work...
    conn.commit()
except Exception as e:
    conn.rollback()  # Undo all changes if error occurs
    raise
```

### Database-Specific Optimizations

**SQLite (In-memory testing):**
- INSERT OR REPLACE for upserts
- PRAGMA synchronous = OFF for speed (temp data only)

**PostgreSQL (Production):**
- COPY command for 10-100x faster bulk loads
- ON CONFLICT DO UPDATE for upserts
- RETURNING clause to retrieve inserted IDs
- Connection pooling with psycopg2.pool

**MySQL:**
- LOAD DATA INFILE for bulk loads
- INSERT IGNORE for duplicate handling
- ON DUPLICATE KEY UPDATE for upserts

## Best Practices

1. **Always use parameterized queries** - Prevents SQL injection attacks
2. **Use transactions** - Maintain data consistency and enable rollback
3. **Batch operations** - Much faster than individual inserts/updates
4. **Connection pooling** - Reuse connections in production applications
5. **Handle errors gracefully** - Use try/except and rollback on failures
6. **Monitor performance** - Profile bulk operations with different batch sizes
7. **Index strategically** - Speed up WHERE and JOIN clauses
8. **Defer foreign keys for bulk loads** - Turn off FK checks temporarily for speed
9. **Use database-specific features** - COPY, LOAD DATA, etc. for large datasets
10. **Validate data before insert** - Better to fail early than mid-operation

## Coming Soon

- **SQLAlchemy ORM** - Object-relational mapping for Pythonic database access
  - Session management
  - Relationship patterns
  - Query builder
  - Alembic migrations

---

**Note:** All scripts use SQLite with in-memory databases for portability. PostgreSQL examples are included as code patterns and will use local credentials if a server is running.
