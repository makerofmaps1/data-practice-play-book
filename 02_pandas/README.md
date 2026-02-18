# Pandas

A collection of scripts demonstrating pandas and geopandas operations for data analysis workflows. Each script runs top-to-bottom with practical examples and clear section headers.

## Scripts

### data_ingestion.py
Loading data into pandas from multiple sources.
- Python objects (dict, list)
- CSV (string, file, with dtypes and parse_dates)
- JSON (standard and JSON Lines)
- Excel (xlsx with openpyxl)
- Parquet (with pyarrow/fastparquet)
- SQL (SQLite queries)
- Clipboard
- HTML tables
- Fixed-width files (FWF)

### cleaning_and_validaion.py
Data cleaning and validation techniques.
- Standardizing null representations (NaN, None, "NULL", "", etc.)
- Type conversion and datetime parsing (robust multi-format handling)
- Datetime normalization and timezone conversion
- Data quality checks (missing values, duplicates, range validation)
- Cleaning strategies (fill, drop, impute)
- Custom row-wise functions with lambda and apply
- Using declared functions with apply

### transformations.py
Core data transformation operations.
- GroupBy (aggregations, named aggs, transform, filter, apply)
- Merge/Join (inner, left, right, outer, with suffixes)
- Concatenation (vertical and horizontal)
- Pivot tables (simple, multi-agg, with margins)
- Reshape (melt wide→long, pivot long→wide, stack/unstack)
- Crosstab (frequency tables, value aggregation)
- Advanced transformations (rank, cumsum, shift within groups)

### time_series.py
Time series analysis and operations.
- Date/time component extraction and filtering
- Resampling (downsample and upsample with multiple frequencies)
- Rolling windows (simple, multi-agg, centered)
- **Rolling averages with 90% confidence intervals**
- Expanding windows (cumulative statistics)
- Exponentially weighted moving average (EWMA)
- Shifting and lagging (day-over-day changes)
- Datetime arithmetic and business day offsets
- Time-based grouping (month, quarter, day of week)
- Seasonality detection

### geopandas_basic.py
Geospatial operations with GeoPandas.
- Creating GeoDataFrames from scratch (Points, Polygons, LineStrings)
- Loading from CSV, GeoJSON, Shapefile, GeoPackage
- Coordinate reference system (CRS) conversions (WGS84, Web Mercator, UTM, Albers)
- Area calculations (geographic vs projected)
- Spatial operations (distance, buffer, centroid, bounds)
- Spatial joins and filtering
- Writing to GeoJSON, Shapefile, GeoPackage
- CRS information and common references

### pipeline_example.py
**Real-world end-to-end pipeline: E-Commerce Sales Analysis**

Integrates all concepts into a complete workflow:
- Multi-source ingestion (CSV, JSON, SQL)
- Data cleaning and validation (nulls, types, imputation)
- Data enrichment (merges, calculated fields, date components)
- Custom functions (lambda and apply)
- GroupBy aggregations (customer, product, region summaries)
- Time series analysis (resampling, rolling averages with CI)
- Pivot tables and cross-tabulation
- RFM customer segmentation (Recency, Frequency, Monetary)
- Business insights and key metrics
- Multi-format export (CSV, JSON, Excel)

## Requirements

- Python 3.11+
- pandas
- numpy
- scipy
- geopandas (for geopandas_basic.py)
- shapely (for geopandas_basic.py)
- openpyxl (optional, for Excel support)
- pyarrow or fastparquet (optional, for Parquet support)

## Installation

```bash
pip install pandas numpy scipy geopandas shapely openpyxl pyarrow
```

## Run

From the repository root:

```bash
python 02_pandas/data_ingestion.py
python 02_pandas/cleaning_and_validaion.py
python 02_pandas/transformations.py
python 02_pandas/time_series.py
python 02_pandas/geopandas_basic.py
python 02_pandas/pipeline_example.py
```

## Key Techniques Covered

- **Ingestion**: Multi-source, multi-format data loading
- **Cleaning**: Robust null handling, datetime parsing, validation
- **Transformation**: Merge, pivot, groupby, reshape operations
- **Time Series**: Resampling, rolling windows, confidence intervals
- **Geospatial**: CRS conversion, area calculation, spatial joins
- **Custom Logic**: Lambda functions, apply, custom aggregations
- **Pipeline**: Complete workflow from raw data to insights

Each script is self-contained and uses inline data so you can run them immediately without external files.
