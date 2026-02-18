# Data Practice Play Book
test

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
- Connections and pooling patterns
- Bulk SQL operations
- SQLAlchemy ORM folder scaffold

### 04_apis
Planned API-focused examples (currently a placeholder).

### 05_etl_patterns
Planned ETL architecture and patterns (currently a placeholder).

## Quick start

### 1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

Minimum useful set for most examples:

```bash
pip install numpy scipy pandas
```

Optional (used by specific scripts):

```bash
pip install geopandas shapely openpyxl pyarrow psycopg2-binary
```

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
python 03_databases/connections_and_pools.py
python 03_databases/sql_bulk_operations.py
```

## Suggested learning path

1. Start with `01_core_python` for language fundamentals.
2. Move to `02_pandas` for data wrangling and analysis patterns.
3. Continue with `03_databases` for SQL and production-minded DB workflows.
4. Use `04_apis` and `05_etl_patterns` as your next expansion tracks.

## Notes

- Most scripts are self-contained and print output directly to the console.
- Several modules intentionally demonstrate multiple approaches to the same task.
- `04_apis` and `05_etl_patterns` are currently placeholders and can be expanded as the next milestones.

## Contributing ideas

Potential next additions:

- Shared `requirements.txt` or per-track requirement files
- Unit tests for core examples
- A small capstone project combining pandas + SQL + API ingestion + ETL orchestration
