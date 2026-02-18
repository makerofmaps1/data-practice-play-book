"""
Database Connection Demonstration

This script demonstrates database connection patterns including:
- Basic psycopg2 connection to PostgreSQL
- Connection pooling for performance
- Context managers for safe connection handling
- Error handling and connection management

Requirements:
- PostgreSQL installed locally with username=postgres, password=postgres
- Database 'test_db' created (or script will create it)

PostgreSQL Setup Tutorial:
https://www.postgresql.org/docs/current/tutorial-install.html
or video: https://www.youtube.com/watch?v=qw--VYLpxG4 (PostgreSQL Setup)

"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor


print("\n" + "=" * 60)
print("DATABASE CONNECTION PATTERNS")
print("=" * 60)


# ============================================================
# BASIC SQLITE CONNECTION (FOR DEMONSTRATION)
# ============================================================

print("\n" + "=" * 60)
print("BASIC SQLITE CONNECTION")
print("=" * 60)

# Simple connection
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create sample table
cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Insert data
cursor.execute(
    "INSERT INTO users (username, email) VALUES (?, ?)",
    ("alice", "alice@email.com")
)
conn.commit()

# Query data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print(f"Users: {rows}")

# Clean up
cursor.close()
conn.close()
print("Connection closed")


# ============================================================
# CONNECTION WITH CONTEXT MANAGER
# ============================================================

print("\n" + "=" * 60)
print("CONNECTION WITH CONTEXT MANAGER")
print("=" * 60)

# SQLite context manager (auto-commits and closes)
with sqlite3.connect(":memory:") as conn:
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL
        )
    """)
    
    cursor.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        ("Widget", 29.99)
    )
    
    cursor.execute("SELECT * FROM products")
    print(f"Products: {cursor.fetchall()}")
    
print("Connection auto-closed by context manager")


# ============================================================
# CUSTOM CONNECTION MANAGER
# ============================================================

print("\n" + "=" * 60)
print("CUSTOM CONNECTION MANAGER")
print("=" * 60)

@contextmanager
def get_db_connection(db_path=":memory:"):
    """Context manager for database connections."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
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

# Use custom connection manager
with get_db_connection() as conn:
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            total REAL
        )
    """)
    
    cursor.execute(
        "INSERT INTO orders (customer_id, total) VALUES (?, ?)",
        (1, 99.99)
    )
    
    cursor.execute("SELECT * FROM orders")
    row = cursor.fetchone()
    print(f"Order (as dict): customer_id={row['customer_id']}, total={row['total']}")


# ============================================================
# SIMPLE CONNECTION POOL (SQLITE)
# ============================================================

print("\n" + "=" * 60)
print("SIMPLE CONNECTION POOL")
print("=" * 60)

class SimpleConnectionPool:
    """Basic connection pool implementation."""
    
    def __init__(self, db_path, pool_size=5):
        self.db_path = db_path
        self.pool_size = pool_size
        self.pool = []
        self.in_use = set()
        
        # Initialize pool
        for _ in range(pool_size):
            conn = sqlite3.connect(db_path, check_same_thread=False)
            self.pool.append(conn)
    
    def get_connection(self):
        """Get a connection from the pool."""
        if not self.pool:
            raise Exception("No connections available in pool")
        
        conn = self.pool.pop()
        self.in_use.add(conn)
        return conn
    
    def return_connection(self, conn):
        """Return a connection to the pool."""
        if conn in self.in_use:
            self.in_use.remove(conn)
            self.pool.append(conn)
    
    def close_all(self):
        """Close all connections."""
        for conn in self.pool:
            conn.close()
        for conn in self.in_use:
            conn.close()
        self.pool.clear()
        self.in_use.clear()

# Use connection pool
pool = SimpleConnectionPool(":memory:", pool_size=3)
print(f"Pool created with {pool.pool_size} connections")
print(f"Available connections: {len(pool.pool)}")

# Get connection from pool
conn1 = pool.get_connection()
print(f"Got connection 1. Available: {len(pool.pool)}")

conn2 = pool.get_connection()
print(f"Got connection 2. Available: {len(pool.pool)}")

# Return connection to pool
pool.return_connection(conn1)
print(f"Returned connection 1. Available: {len(pool.pool)}")

pool.close_all()
print("Pool closed")


# ============================================================
# POSTGRESQL CONNECTION
# ============================================================

print("\n" + "=" * 60)
print("POSTGRESQL CONNECTION")
print("=" * 60)

try:
    # Basic PostgreSQL connection
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",  # Connect to default postgres database
        user="postgres",
        password="postgres",
        port=5432
    )

    cursor = conn.cursor()

    # Execute query
    cursor.execute("SELECT version()")
    version = cursor.fetchone()
    print(f"PostgreSQL version: {version[0][:50]}...")

    # Create test database if it doesn't exist
    conn.autocommit = True
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='test_db'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE test_db")
        print("Created database: test_db")
    else:
        print("Database test_db already exists")

    cursor.close()
    conn.close()
    print("Connection closed successfully")

except Exception as e:
    print(f"PostgreSQL connection failed: {e}")
    print("Make sure PostgreSQL is running with user=postgres, password=postgres")


# ============================================================
# POSTGRESQL CONNECTION POOLING
# ============================================================

print("\n" + "=" * 60)
print("POSTGRESQL CONNECTION POOLING")
print("=" * 60)

try:
    # Create connection pool
    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )

    print(f"Connection pool created (min=1, max=10)")

    # Get connection from pool
    conn = connection_pool.getconn()
    print("Got connection from pool")

    try:
        cursor = conn.cursor()
        
        # Create sample table
        cursor.execute("""
            CREATE TEMPORARY TABLE pool_test (
                id SERIAL PRIMARY KEY,
                name TEXT
            )
        """)
        
        # Insert data
        cursor.execute("INSERT INTO pool_test (name) VALUES (%s)", ("Test User",))
        conn.commit()
        
        # Query data
        cursor.execute("SELECT * FROM pool_test")
        rows = cursor.fetchall()
        print(f"Query result: {rows}")
        
        cursor.close()
    finally:
        # Return connection to pool
        connection_pool.putconn(conn)
        print("Returned connection to pool")

    # Close all connections when done
    connection_pool.closeall()
    print("Connection pool closed")

except Exception as e:
    print(f"PostgreSQL pooling failed: {e}")


# ============================================================
# POSTGRESQL WITH CONTEXT MANAGER
# ============================================================

print("\n" + "=" * 60)
print("POSTGRESQL CONTEXT MANAGER")
print("=" * 60)

@contextmanager
def get_pg_connection():
    """Context manager for PostgreSQL connections."""
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

try:
    # Use the context manager
    with get_pg_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Create temporary table
        cursor.execute("""
            CREATE TEMPORARY TABLE context_test (
                id SERIAL PRIMARY KEY,
                username TEXT,
                score INTEGER
            )
        """)
        
        # Insert data
        cursor.execute(
            "INSERT INTO context_test (username, score) VALUES (%s, %s) RETURNING id",
            ("alice", 95)
        )
        user_id = cursor.fetchone()["id"]
        print(f"Inserted user with ID: {user_id}")
        
        # Query with dict cursor
        cursor.execute("SELECT * FROM context_test WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        print(f"User: {user['username']}, Score: {user['score']}")
        
        cursor.close()
    
    print("Context manager auto-committed and closed connection")

except Exception as e:
    print(f"PostgreSQL context manager failed: {e}")


# ============================================================
# CONNECTION POOL CLASS (PSYCOPG2 EXAMPLE)
# ============================================================

print("\n" + "=" * 60)
print("ADVANCED POOLING CLASS (SINGLETON)")
print("=" * 60)

class DatabasePool:
    """Singleton connection pool for PostgreSQL."""
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self, minconn=1, maxconn=10, **kwargs):
        if self._pool is None:
            self._pool = pool.ThreadedConnectionPool(
                minconn=minconn,
                maxconn=maxconn,
                **kwargs
            )
    
    @contextmanager
    def get_connection(self):
        conn = self._pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)
    
    def close_all(self):
        if self._pool:
            self._pool.closeall()

try:
    # Initialize pool (once at application startup)
    db_pool = DatabasePool()
    db_pool.initialize(
        minconn=2,
        maxconn=10,
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )
    print("Database pool initialized (singleton pattern)")

    # Use pool throughout application
    with db_pool.get_connection() as conn:
        cursor = conn.cursor()
        
        # Create temporary table
        cursor.execute("""
            CREATE TEMPORARY TABLE pool_class_test (
                id SERIAL PRIMARY KEY,
                value TEXT
            )
        """)
        cursor.execute("INSERT INTO pool_class_test (value) VALUES (%s)", ("test",))
        cursor.execute("SELECT COUNT(*) FROM pool_class_test")
        count = cursor.fetchone()[0]
        print(f"Record count: {count}")
        cursor.close()
    
    print("Connection returned to pool")
    
    # Clean up
    db_pool.close_all()
    print("Pool closed")

except Exception as e:
    print(f"Advanced pooling failed: {e}")


# ============================================================
# BEST PRACTICES SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("BEST PRACTICES")
print("=" * 60)

best_practices = """
1. Always use connection pooling in production
   - Reduces connection overhead
   - Improves performance under load
   - Limits concurrent connections

2. Use context managers for automatic cleanup
   - Ensures connections are closed
   - Handles commits/rollbacks automatically
   - Prevents connection leaks

3. Use parameterized queries (ALWAYS)
   - Prevents SQL injection
   - PostgreSQL: cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
   - SQLite: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

4. Handle errors gracefully
   - Try/except blocks around DB operations
   - Rollback on errors
   - Log errors for debugging

5. Connection pool sizing
   - Min connections: 2-5 (keep warm connections)
   - Max connections: Based on load (10-50 typical)
   - Monitor pool exhaustion

6. Use appropriate cursor types
   - RealDictCursor for dict-like results
   - ServerSideCursor for large result sets
   - Named cursors for scrollable results

7. Close cursors when done
   - Frees up server resources
   - Prevents cursor leaks

8. Set appropriate timeouts
   - Connection timeout
   - Statement timeout
   - Idle connection timeout

9. Use connection URI for configuration
   - postgresql://user:password@host:port/database
   - Easier to manage in environment variables

10. Monitor connection health
    - Check connection before use
    - Implement connection validation
    - Handle stale connections
"""

print(best_practices)


print("\n" + "=" * 60)
print("END OF CONNECTION DEMO")
print("=" * 60)
