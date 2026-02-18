"""
File I/O Operations Demonstration
Author: Python Skills Portfolio
Date: February 2026

This script demonstrates file I/O operations:
- Reading and writing text files
- CSV file operations
- JSON file operations
- Pickle serialization
- File path operations
- Error handling
- Working with different encodings
- Binary file operations
"""

import os
import csv
import json
import pickle
from pathlib import Path

print("\n" + "="*60)
print("FILE I/O OPERATIONS DEMONSTRATION")
print("="*60)

# Create a data directory for examples
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


# ============================================================================
# TEXT FILE OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("TEXT FILE OPERATIONS")
print("="*60)

# Writing to a text file
text_file = os.path.join(data_dir, "sample.txt")

print(f"\nWriting to {text_file}...")
with open(text_file, 'w') as f:
    f.write("Hello, World!\n")
    f.write("This is a sample text file.\n")
    f.write("It demonstrates file I/O operations.\n")

# Reading entire file at once
print("Reading entire file:")
with open(text_file, 'r') as f:
    content = f.read()
    print(f"  Content: {repr(content)}")

# Reading line by line
print("\nReading line by line:")
with open(text_file, 'r') as f:
    for line_num, line in enumerate(f, 1):
        print(f"  Line {line_num}: {line.rstrip()}")

# Reading all lines as a list
print("\nReading as list:")
with open(text_file, 'r') as f:
    lines = f.readlines()
    print(f"  Lines: {lines}")

# Appending to file
print("\nAppending to file:")
with open(text_file, 'a') as f:
    f.write("This line was appended.\n")

# Modifying file content
print("Modifying file content (adding line numbers):")
with open(text_file, 'r') as f:
    lines = f.readlines()

modified_file = os.path.join(data_dir, "sample_modified.txt")
with open(modified_file, 'w') as f:
    for i, line in enumerate(lines, 1):
        f.write(f"{i}: {line}")

with open(modified_file, 'r') as f:
    print(f"  {f.read()}")


# ============================================================================
# CSV FILE OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("CSV FILE OPERATIONS")
print("="*60)

csv_file = os.path.join(data_dir, "employees.csv")

# Writing CSV file
print(f"\nWriting CSV file ({csv_file})...")
employees = [
    {"name": "Alice", "department": "Engineering", "salary": 90000, "years": 5},
    {"name": "Bob", "department": "Marketing", "salary": 70000, "years": 3},
    {"name": "Carol", "department": "Engineering", "salary": 95000, "years": 7},
    {"name": "Dave", "department": "Sales", "salary": 75000, "years": 4},
]

with open(csv_file, 'w', newline='') as f:
    fieldnames = ["name", "department", "salary", "years"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(employees)

# Reading CSV file with DictReader
print("Reading CSV as dictionaries:")
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']:8} - {row['department']:12} - ${row['salary']:>6} ({row['years']} years)")

# Reading CSV file with csv.reader
print("\nReading CSV as lists:")
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row_num, row in enumerate(reader):
        if row_num == 0:
            print(f"  Header: {row}")
        else:
            print(f"  Row {row_num}: {row}")

# Filtering CSV data
print("\nFiltering (Engineering department):")
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    engineers = [row for row in reader if row['department'] == 'Engineering']
    for eng in engineers:
        print(f"  {eng['name']:8} - ${eng['salary']}")

# Aggregating CSV data
print("\nAggregating data:")
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    total_salary = 0
    count = 0
    for row in reader:
        total_salary += int(row['salary'])
        count += 1
    avg_salary = total_salary / count
    print(f"  Total salary: ${total_salary:,}")
    print(f"  Average salary: ${avg_salary:,.2f}")


# ============================================================================
# JSON FILE OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("JSON FILE OPERATIONS")
print("="*60)

json_file = os.path.join(data_dir, "data.json")

# Creating data structures for JSON
data = {
    "project": "Python Skills",
    "version": "1.0",
    "author": "Developer",
    "modules": [
        {"name": "core_data_types", "status": "complete"},
        {"name": "functions_basics", "status": "complete"},
        {"name": "functions_advanced", "status": "complete"},
        {"name": "oop_patterns", "status": "complete"},
    ],
    "metadata": {
        "created": "2026-02-17",
        "last_updated": "2026-02-17",
        "tags": ["python", "educational", "skills"]
    }
}

# Writing JSON file
print(f"\nWriting JSON file ({json_file})...")
with open(json_file, 'w') as f:
    json.dump(data, f, indent=2)

# Reading JSON file
print("Reading JSON file:")
with open(json_file, 'r') as f:
    loaded_data = json.load(f)
    print(f"  Project: {loaded_data['project']} v{loaded_data['version']}")
    print(f"  Author: {loaded_data['author']}")
    print(f"  Created: {loaded_data['metadata']['created']}")
    print(f"  Tags: {', '.join(loaded_data['metadata']['tags'])}")

# Pretty printing JSON
print("\nJSON structure:")
print(json.dumps(loaded_data, indent=2))

# Working with JSON lists
json_list_file = os.path.join(data_dir, "students.json")

students = [
    {"id": 1, "name": "Alice", "grades": [85, 90, 88]},
    {"id": 2, "name": "Bob", "grades": [92, 88, 91]},
    {"id": 3, "name": "Carol", "grades": [78, 82, 80]},
]

with open(json_list_file, 'w') as f:
    json.dump(students, f, indent=2)

print(f"\nReading {json_list_file}:")
with open(json_list_file, 'r') as f:
    students_loaded = json.load(f)
    for student in students_loaded:
        avg_grade = sum(student['grades']) / len(student['grades'])
        print(f"  {student['name']:8} - Average: {avg_grade:.1f}")


# ============================================================================
# PICKLE SERIALIZATION
# ============================================================================

print("\n" + "="*60)
print("PICKLE SERIALIZATION")
print("="*60)

pickle_file = os.path.join(data_dir, "objects.pkl")

# Object to pickle
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
    
    def __repr__(self):
        return f"Person(name={self.name}, age={self.age}, email={self.email})"

people = [
    Person("Alice", 30, "alice@example.com"),
    Person("Bob", 25, "bob@example.com"),
    Person("Carol", 35, "carol@example.com"),
]

# Pickling objects
print(f"\nPickling objects to {pickle_file}...")
with open(pickle_file, 'wb') as f:
    pickle.dump(people, f)

# Unpickling objects
print("Unpickling objects:")
with open(pickle_file, 'rb') as f:
    loaded_people = pickle.load(f)
    for person in loaded_people:
        print(f"  {person}")


# ============================================================================
# FILE PATH OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("FILE PATH OPERATIONS")
print("="*60)

# Using pathlib for modern path handling
print("\nPathlib operations:")
sample_path = Path(data_dir) / "sample.txt"
print(f"  Path: {sample_path}")
print(f"  Absolute path: {sample_path.absolute()}")
print(f"  Parent: {sample_path.parent}")
print(f"  Name: {sample_path.name}")
print(f"  Stem: {sample_path.stem}")
print(f"  Suffix: {sample_path.suffix}")
print(f"  Exists: {sample_path.exists()}")
print(f"  Is file: {sample_path.is_file()}")
print(f"  Is dir: {sample_path.is_dir()}")

# Using os.path
print("\nos.path operations:")
print(f"  Basename: {os.path.basename(text_file)}")
print(f"  Dirname: {os.path.dirname(text_file)}")
print(f"  Splitext: {os.path.splitext(text_file)}")
print(f"  Exists: {os.path.exists(text_file)}")
print(f"  Is file: {os.path.isfile(text_file)}")
print(f"  File size: {os.path.getsize(text_file)} bytes")

# Listing directory contents
print(f"\nDirectory contents ({data_dir}):")
for item in os.listdir(data_dir):
    item_path = os.path.join(data_dir, item)
    size = os.path.getsize(item_path)
    print(f"  {item:30} ({size:6} bytes)")

# Using glob to find files
print("\nFinding .csv files:")
csv_files = list(Path(data_dir).glob("*.csv"))
for csv in csv_files:
    print(f"  {csv}")


# ============================================================================
# WORKING WITH DIFFERENT ENCODINGS
# ============================================================================

print("\n" + "="*60)
print("WORKING WITH DIFFERENT ENCODINGS")
print("="*60)

encoding_file = os.path.join(data_dir, "unicode.txt")

# Writing UTF-8 with special characters
print("\nWriting Unicode content (UTF-8)...")
content_utf8 = """English: Hello
French: Bonjour
Spanish: Hola
German: Guten Tag
Russian: Привет
Japanese: こんにちは
Emoji: 🎉 🐍 📚
"""

with open(encoding_file, 'w', encoding='utf-8') as f:
    f.write(content_utf8)

print("Reading Unicode content:")
with open(encoding_file, 'r', encoding='utf-8') as f:
    for line in f:
        print(f"  {line.rstrip()}")


# ============================================================================
# ERROR HANDLING
# ============================================================================

print("\n" + "="*60)
print("ERROR HANDLING")
print("="*60)

# File not found
print("\nHandling file not found:")
try:
    with open("nonexistent.txt", 'r') as f:
        content = f.read()
except FileNotFoundError:
    print("  Error: File not found")

# Permission error (simulated)
print("\nHandling generic file errors:")
try:
    with open(text_file, 'r') as f:
        content = f.read()
    print(f"  Successfully read {len(content)} characters")
except IOError as e:
    print(f"  Error: {e}")

# Using context manager for safe file handling
print("\nUsing context manager:")
try:
    with open(text_file, 'r') as f:
        lines = f.readlines()
        print(f"  Read {len(lines)} lines")
except (FileNotFoundError, IOError) as e:
    print(f"  Error: {e}")


# ============================================================================
# BATCH FILE OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("BATCH FILE OPERATIONS")
print("="*60)

# Process multiple CSV files
print("\nBatch processing CSV files:")
csv_files = Path(data_dir).glob("*.csv")
for csv_path in csv_files:
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"  {csv_path.name}: {len(rows)} rows")

# Finding and processing files by pattern
print("\nFinding Python files in seed directory:")
seed_dir = Path("01_core_python")
if seed_dir.exists():
    py_files = list(seed_dir.glob("*.py"))
    print(f"  Found {len(py_files)} Python files:")
    for py_file in py_files[:5]:  # Show first 5
        size = py_file.stat().st_size
        print(f"    {py_file.name:30} - {size:6} bytes")


# ============================================================================
# READING FILES IN CHUNKS
# ============================================================================

print("\n" + "="*60)
print("READING FILES IN CHUNKS")
print("="*60)

# Create a larger file
large_file = os.path.join(data_dir, "large.txt")
with open(large_file, 'w') as f:
    for i in range(1000):
        f.write(f"Line {i}: This is line number {i}\n")

# Reading in chunks
print("\nReading file in chunks (1024 bytes at a time):")
with open(large_file, 'rb') as f:
    chunk_size = 1024
    chunk_num = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        chunk_num += 1
        print(f"  Chunk {chunk_num}: {len(chunk)} bytes")
        if chunk_num >= 3:  # Show only first 3 chunks
            print("  ...")
            break

# Reading specific lines
print("\nReading specific lines:")
with open(large_file, 'r') as f:
    for line_num, line in enumerate(f, 1):
        if line_num >= 5 and line_num <= 7:
            print(f"  {line.rstrip()}")


# ============================================================================
# CONFIGURATION FILES
# ============================================================================

print("\n" + "="*60)
print("CONFIGURATION FILES")
print("="*60)

config_file = os.path.join(data_dir, "config.json")

config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb",
        "username": "admin"
    },
    "api": {
        "debug": True,
        "port": 8000,
        "workers": 4
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
}

# Write configuration
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print(f"\nConfiguration file created: {config_file}")

# Read and use configuration
with open(config_file, 'r') as f:
    loaded_config = json.load(f)
    print("\nDatabase configuration:")
    db_config = loaded_config['database']
    print(f"  Host: {db_config['host']}")
    print(f"  Port: {db_config['port']}")
    print(f"  Database: {db_config['name']}")
    print("\nAPI configuration:")
    api_config = loaded_config['api']
    print(f"  Debug: {api_config['debug']}")
    print(f"  Port: {api_config['port']}")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*60)
print("FILE I/O SUMMARY")
print("="*60)

print(f"\nAll files created in '{data_dir}' directory:")
for item in sorted(os.listdir(data_dir)):
    item_path = os.path.join(data_dir, item)
    size = os.path.getsize(item_path)
    print(f"  {item:30} {size:>8} bytes")

print("\n" + "="*60)
print("DEMONSTRATION COMPLETE")
print("="*60 + "\n")
