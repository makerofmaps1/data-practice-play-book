# Data Practice Play Book

A hands-on Python learning repository organized by topic.  
Each folder contains runnable, script-based examples demonstrating practical data engineering.

## What this project is

- A structured repo demonstrating core Python, pandas, SQL/database work, APIs, and ETL patterns.
- Script-first examples (not a packaged library), designed for quick experimentation.
- A practical reference you can return to when implementing real-world workflows.

## Repository structure

```
data-practice-play-book/
├── 01_core_python/
├── 02_pandas/
├── 03_databases/
├── 04_apis/
├── 05_etl_patterns/
├── 06_unit_tests/
└── README.md
```

### 01_core_python
Foundational Python topics and patterns:

- Data types and common operations
- Function basics and advanced function patterns
- OOP principles and patterns
- File I/O workflows
- Math/statistics examples

### 02_pandas
Data workflows using pandas (plus introductory GeoPandas):

- Data ingestion from multiple sources/formats
- Cleaning and validation
- Transformations and reshaping
- Time series operations
- End-to-end pipeline example

### 03_databases
Database skills in Python:

- SQL fundamentals in Python
- Shared `.env` config pattern for Postgres/MySQL/Snowflake credentials
- Bulk SQL operations
- SQLAlchemy ORM basics (`sqlalchemy_basic.py`)

### 04_apis
Planned API-focused examples (currently a placeholder).

### 05_etl_patterns
Planned ETL architecture and patterns (currently a placeholder).

### 06_unit_tests
Staged unit testing track for learning and teaching:

- `unittest` fundamentals
- `pytest` workflows
- Mocking and dependency isolation
- Test design and coverage
- Real project testing patterns

## Quick start

### 1) Create and activate a virtual environment

Recommended Python version: **3.12**

Windows (PowerShell):

```powershell
# Create with Python 3.12
py -3.12 -m venv .venv

# Activate
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
# Create with Python 3.12
python3.12 -m venv .venv

# Activate
source .venv/bin/activate
```

### 2) Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Optional extras

If you want to run every script (including heavier geo dependencies), install extras as needed:

```bash
pip install geopandas shapely
```

### 4) Database env setup (for external DB scripts)

```bash
copy 03_databases\.env.example 03_databases\.env
```

Then fill values in `03_databases/.env` for the database engines you want to run.

## Running examples

Run scripts from repository root:

```bash
python 01_core_python/core_data_types.py
python 01_core_python/functions_basics.py
python 01_core_python/functions_advanced.py
python 01_core_python/oop_patterns.py
python 01_core_python/file_io.py
python 01_core_python/math_and_statistics.py

python 02_pandas/data_ingestion.py
python 02_pandas/cleaning_and_validaion.py
python 02_pandas/transformations.py
python 02_pandas/time_series.py
python 02_pandas/geopandas_basic.py
python 02_pandas/pipeline_example.py

python 03_databases/sql_in_python_basic.py
python 03_databases/sqlalchemy_basic.py
python 03_databases/01_sqlite.py
python 03_databases/02_postgres.py
python 03_databases/03_mysql.py
python 03_databases/04_snowflake.py
```

## Suggested learning path

1. Start with `01_core_python` for language fundamentals.
2. Move to `02_pandas` for data wrangling and analysis patterns.
3. Continue with `03_databases` for SQL and production-minded DB workflows.
4. Use `04_apis` and `05_etl_patterns` as your next expansion tracks.
5. Follow `06_unit_tests` to build production-ready testing habits.

## Notes

- Most scripts are self-contained and print output directly to the console.
- Several modules intentionally demonstrate multiple approaches to the same task.
- `04_apis` and `05_etl_patterns` are currently placeholders and can be expanded as the next milestones.
- `06_unit_tests` is now a complete staged curriculum with runnable examples.

## Contributing ideas

Potential next additions:

- Unit tests for core examples
- A small capstone project combining pandas + SQL + API ingestion + ETL orchestration
