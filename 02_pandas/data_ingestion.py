"""
Pandas Data Ingestion Demonstration

This script shows common ways to load data into pandas. It uses small inline
examples so it can run top-to-bottom without external files.

Some formats require optional dependencies:
- Excel: openpyxl
- Parquet: pyarrow or fastparquet
- HTML: lxml or html5lib
"""

from __future__ import annotations

import io
import json
import sqlite3
import tempfile
from pathlib import Path

import pandas as pd


print("\n" + "=" * 60)
print("PANDAS DATA INGESTION")
print("=" * 60)


# ============================================================
# FROM PYTHON OBJECTS (DICT / LIST)
# ============================================================

print("\n" + "=" * 60)
print("FROM PYTHON OBJECTS")
print("=" * 60)

records = [
	{"id": 1, "name": "Ava", "score": 88},
	{"id": 2, "name": "Noah", "score": 93},
	{"id": 3, "name": "Liam", "score": 79},
]
df_from_records = pd.DataFrame.from_records(records)
print(df_from_records)

data_dict = {"id": [1, 2, 3], "dept": ["Sales", "Eng", "Ops"]}
df_from_dict = pd.DataFrame(data_dict)
print("\nFrom dict:")
print(df_from_dict)


# ============================================================
# CSV (STRING, FILE PATH, OPTIONS)
# ============================================================

print("\n" + "=" * 60)
print("CSV INGESTION")
print("=" * 60)

csv_text = """id,name,score\n1,Ava,88\n2,Noah,93\n3,Liam,79\n"""
df_csv_string = pd.read_csv(io.StringIO(csv_text))
print("From CSV string:")
print(df_csv_string)

csv_with_types = """id,joined,active\n1,2024-01-05,True\n2,2024-02-10,False\n"""
df_csv_types = pd.read_csv(
	io.StringIO(csv_with_types),
	parse_dates=["joined"],
	dtype={"id": "int64", "active": "boolean"},
)
print("\nCSV with parse_dates and dtypes:")
print(df_csv_types)
print(df_csv_types.dtypes)

with tempfile.TemporaryDirectory() as tmp_dir:
	csv_path = Path(tmp_dir) / "people.csv"
	csv_path.write_text(csv_text, encoding="utf-8")
	df_csv_file = pd.read_csv(csv_path)
	print("\nFrom CSV file path:")
	print(df_csv_file)


# ============================================================
# JSON (STRING, LINES, FILE)
# ============================================================

print("\n" + "=" * 60)
print("JSON INGESTION")
print("=" * 60)

json_text = json.dumps(records)
df_json_string = pd.read_json(io.StringIO(json_text))
print("From JSON string:")
print(df_json_string)

json_lines = """{"id": 1, "name": "Ava"}\n{"id": 2, "name": "Noah"}\n"""
df_json_lines = pd.read_json(io.StringIO(json_lines), lines=True)
print("\nFrom JSON Lines:")
print(df_json_lines)

with tempfile.TemporaryDirectory() as tmp_dir:
	json_path = Path(tmp_dir) / "people.json"
	json_path.write_text(json_text, encoding="utf-8")
	df_json_file = pd.read_json(json_path)
	print("\nFrom JSON file path:")
	print(df_json_file)


# ============================================================
# EXCEL (OPTIONAL DEPENDENCY)
# ============================================================

print("\n" + "=" * 60)
print("EXCEL INGESTION")
print("=" * 60)

try:
	with tempfile.TemporaryDirectory() as tmp_dir:
		xlsx_path = Path(tmp_dir) / "people.xlsx"
		df_from_records.to_excel(xlsx_path, index=False, sheet_name="people")
		df_excel = pd.read_excel(xlsx_path, sheet_name="people")
		print("From Excel file:")
		print(df_excel)
except Exception as exc:  # openpyxl missing or other engine errors
	print(f"Excel read skipped: {exc}")


# ============================================================
# PARQUET (OPTIONAL DEPENDENCY)
# ============================================================

print("\n" + "=" * 60)
print("PARQUET INGESTION")
print("=" * 60)

try:
	with tempfile.TemporaryDirectory() as tmp_dir:
		parquet_path = Path(tmp_dir) / "people.parquet"
		df_from_records.to_parquet(parquet_path, index=False)
		df_parquet = pd.read_parquet(parquet_path)
		print("From Parquet file:")
		print(df_parquet)
except Exception as exc:  # pyarrow/fastparquet missing
	print(f"Parquet read skipped: {exc}")


# ============================================================
# SQL (SQLITE DATABASE)
# ============================================================

print("\n" + "=" * 60)
print("SQL INGESTION")
print("=" * 60)

with sqlite3.connect(":memory:") as conn:
	df_from_records.to_sql("people", conn, index=False, if_exists="replace")
	df_sql = pd.read_sql_query("SELECT * FROM people WHERE score >= 85", conn)
	print("From SQL query:")
	print(df_sql)


# ============================================================
# CLIPBOARD (OPTIONAL, MAY FAIL IN SOME ENVIRONMENTS)
# ============================================================

print("\n" + "=" * 60)
print("CLIPBOARD INGESTION")
print("=" * 60)

try:
	clipboard_text = """id\tname\n1\tAva\n2\tNoah\n"""
	pd.DataFrame({"clipboard": [clipboard_text]}).to_clipboard(index=False)
	df_clipboard = pd.read_clipboard()
	print("From clipboard:")
	print(df_clipboard)
except Exception as exc:
	print(f"Clipboard read skipped: {exc}")


# ============================================================
# HTML TABLES (OPTIONAL DEPENDENCY)
# ============================================================

print("\n" + "=" * 60)
print("HTML TABLE INGESTION")
print("=" * 60)

html_text = """
<table>
  <thead><tr><th>id</th><th>name</th></tr></thead>
  <tbody>
	<tr><td>1</td><td>Ava</td></tr>
	<tr><td>2</td><td>Noah</td></tr>
  </tbody>
</table>
"""

try:
	df_html = pd.read_html(io.StringIO(html_text))[0]
	print("From HTML table:")
	print(df_html)
except Exception as exc:
	print(f"HTML read skipped: {exc}")


# ============================================================
# FIXED-WIDTH FILES (FWF)
# ============================================================

print("\n" + "=" * 60)
print("FIXED-WIDTH FILE INGESTION")
print("=" * 60)

fwf_text = """1 Ava  088\n2 Noah 093\n3 Liam 079\n"""
df_fwf = pd.read_fwf(io.StringIO(fwf_text), widths=[2, 6, 4], names=["id", "name", "score"])
print("From fixed-width text:")
print(df_fwf)


print("\n" + "=" * 60)
print("END OF DATA INGESTION DEMO")
print("=" * 60)
