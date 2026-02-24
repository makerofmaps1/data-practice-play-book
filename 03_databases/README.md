# Database Operations

Hands-on database scripts for Python, from SQL basics to database-specific workflows.

## Overview

This folder focuses on practical patterns you will use often:

- Basic SQL execution from Python (`CREATE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`)
- Bulk operations and performance-minded query execution
- Engine-specific examples for SQLite, PostgreSQL, MySQL, and Snowflake
- Safe defaults like parameterized queries and transaction-aware code
- Shared `.env` + config helper pattern for connection settings

## Files

### `sql_in_python_basic.py`
Minimal SQL fundamentals using an **in-memory SQLite database**.

- Creates one table
- Inserts sample rows
- Reads rows with `SELECT`
- Updates rows with `UPDATE`
- Deletes rows with `DELETE`
- Uses parameterized queries (`?` placeholders)

Run:

```bash
python sql_in_python_basic.py
```

### `01_sqlite.py`
Template-style SQLite demo covering:

- Connection + context manager
- Table creation
- CRUD + simple analytics queries
- Pandas read/write flow
- Optional cleanup

Run:

```bash
python 01_sqlite.py
```

### `db_config.py`
Shared environment/config helper used by external database scripts.

- Loads `03_databases/.env`
- Builds connection config dictionaries for PostgreSQL, MySQL, and Snowflake
- Provides fail-fast validation for required credentials

### `02_postgres.py`
Template-style PostgreSQL demo with schema setup and SQL workflow.

Run:

```bash
python 02_postgres.py
```

### `03_mysql.py`
Template-style MySQL demo with database bootstrap and SQL workflow.

Run:

```bash
python 03_mysql.py
```

### `04_snowflake.py`
Simple Snowflake demo focused on connection config and basic SQL.

- Reads credentials from `.env`
- Uses configured warehouse/database/schema
- Runs `CREATE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`

Run:

```bash
python 04_snowflake.py
```

### `sqlalchemy_basic.py`
Beginner-friendly SQLAlchemy ORM demo (single engine: SQLite).

- Defines ORM models (`Product`, `Sale`)
- Uses ORM abstraction for `INSERT`, `SELECT`, `UPDATE`, `DELETE`
- Demonstrates relationships and joined queries
- Notes key differences for PostgreSQL, MySQL/MariaDB, and Snowflake

Run:

```bash
python sqlalchemy_basic.py
```

## Requirements

### Base

- Python 3.10+
- `pandas`
- `sqlalchemy`

### Database-specific drivers

Install only what you plan to run:

```bash
pip install pandas
pip install sqlalchemy
pip install psycopg2-binary
pip install mysql-connector-python
pip install "snowflake-connector-python[pandas]" snowpark
```

`sqlite3` is built into Python and does not require installation.

## Environment Variables (for external databases)

### PostgreSQL (`02_postgres.py`)

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

### MySQL (`03_mysql.py`)

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

### Snowflake (`04_snowflake.py`)

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`

### Setup Pattern (recommended)

1. Copy `.env.example` to `.env`
2. Fill in only the databases you are using
3. Run scripts from project root so each script can load `03_databases/.env`

```bash
python 03_databases/sqlalchemy_basic.py
python 03_databases/02_postgres.py
python 03_databases/03_mysql.py
python 03_databases/04_snowflake.py
```

## Notes

- `sql_in_python_basic.py` is intentionally minimal and beginner-focused.
- The `01`-`04` scripts share a similar structure so you can compare engines directly.
- `sqlalchemy_basic.py` keeps ORM teaching focused on one engine (SQLite), with portability notes for others.
- Keep credentials in environment variables rather than hardcoding them.
- For Snowflake, use a regular database name (for example `DEMO_DB`) instead of `USER$<username>` when creating tables.
