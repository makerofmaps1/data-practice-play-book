"""
Python Data Types Demonstration

This script demonstrates usage and manipulation of core Python data types:
- Strings (str)
- Integers (int)
- Floats (float)
- Lists (list)
- Dictionaries (dict)
"""

print("\n" + "="*60)
print("PYTHON DATA TYPES DEMONSTRATION")
print("="*60)


# ============================================================================
# STRING OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("STRING OPERATIONS")
print("="*60)

# Basic string creation and concatenation
first_name = "Python"
last_name = "Developer"
full_name = first_name + " " + last_name
print(f"Full name: {full_name}")

# String formatting methods
template = "Hello, {}! Welcome to {}"
formatted = template.format(full_name, "Data Science")
print(f"Formatted string: {formatted}")

# F-strings (modern approach)
age = 5
f_string = f"{first_name} is {age} years old"
print(f"F-string: {f_string}")

# String methods
sample_text = "  Data Analysis with Python  "
print(f"\nOriginal: '{sample_text}'")
print(f"Stripped: '{sample_text.strip()}'")
print(f"Uppercase: '{sample_text.upper()}'")
print(f"Lowercase: '{sample_text.lower()}'")
print(f"Title case: '{sample_text.title()}'")

# String slicing and indexing
message = "Python Programming"
print(f"\nOriginal message: {message}")
print(f"First 6 chars: {message[:6]}")
print(f"Last 11 chars: {message[-11:]}")
print(f"Every 2nd char: {message[::2]}")
print(f"Reversed: {message[::-1]}")

# String splitting and joining
csv_data = "apple,banana,cherry,date"
fruits = csv_data.split(",")
print(f"\nSplit CSV: {fruits}")
joined = " | ".join(fruits)
print(f"Joined with pipes: {joined}")

# String searching and replacing
text = "Python is powerful. Python is versatile."
print(f"\nOriginal: {text}")
print(f"Count 'Python': {text.count('Python')}")
print(f"Find 'powerful': {text.find('powerful')}")
replaced = text.replace("Python", "Programming")
print(f"Replaced: {replaced}")

# String validation methods
print(f"\n'12345'.isdigit(): {'12345'.isdigit()}")
print(f"'abc123'.isalnum(): {'abc123'.isalnum()}")
print(f"'Python'.isalpha(): {'Python'.isalpha()}")


# ============================================================================
# INTEGER OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("INTEGER OPERATIONS")
print("="*60)

# Basic arithmetic
a, b = 42, 7
print(f"\na = {a}, b = {b}")
print(f"Addition: {a} + {b} = {a + b}")
print(f"Subtraction: {a} - {b} = {a - b}")
print(f"Multiplication: {a} * {b} = {a * b}")
print(f"Division: {a} / {b} = {a / b}")
print(f"Floor division: {a} // {b} = {a // b}")
print(f"Modulo: {a} % {b} = {a % b}")
print(f"Exponentiation: {b} ** 2 = {b ** 2}")

# Bitwise operations
x, y = 12, 5  # 1100 and 0101 in binary
print(f"\nx = {x} (binary: {bin(x)}), y = {y} (binary: {bin(y)})")
print(f"AND: {x} & {y} = {x & y}")
print(f"OR: {x} | {y} = {x | y}")
print(f"XOR: {x} ^ {y} = {x ^ y}")
print(f"Left shift: {y} << 2 = {y << 2}")
print(f"Right shift: {x} >> 2 = {x >> 2}")

# Type conversion
float_num = 3.14159
from_float = int(float_num)
print(f"\nFloat to int: {float_num} -> {from_float}")

string_num = "1024"
from_string = int(string_num)
print(f"String to int: '{string_num}' -> {from_string}")

# Integer methods
number = -42
print(f"\nAbs value of {number}: {abs(number)}")
print(f"Max of 10, 25, 5: {max(10, 25, 5)}")
print(f"Min of 10, 25, 5: {min(10, 25, 5)}")
print(f"Sum of [1, 2, 3, 4, 5]: {sum([1, 2, 3, 4, 5])}")


# ============================================================================
# FLOAT OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("FLOAT OPERATIONS")
print("="*60)

# Basic float operations
pi = 3.14159265359
e = 2.71828182846

print(f"\nπ = {pi}")
print(f"e = {e}")
print(f"π + e = {pi + e}")
print(f"π * e = {pi * e}")

# Rounding and formatting
value = 123.456789
print(f"\nOriginal value: {value}")
print(f"Rounded to 2 decimals: {round(value, 2)}")
print(f"Rounded to nearest integer: {round(value)}")
print(f"Formatted to 3 decimals: {value:.3f}")
print(f"Scientific notation: {value:.2e}")

# Float precision and comparison
float_a = 0.1 + 0.2
float_b = 0.3
print(f"\n0.1 + 0.2 = {float_a}")
print(f"0.3 = {float_b}")
print(f"Are they equal? {float_a == float_b}")
print(f"Close enough (abs diff < 1e-9)? {abs(float_a - float_b) < 1e-9}")

# Converting between types
int_val = 42
float_val = float(int_val)
print(f"\nInt to float: {int_val} -> {float_val}")

string_float = "3.14159"
parsed_float = float(string_float)
print(f"String to float: '{string_float}' -> {parsed_float}")


# ============================================================================
# LIST OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("LIST OPERATIONS")
print("="*60)

# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, True, None]
nested = [[1, 2], [3, 4], [5, 6]]

print(f"\nNumbers list: {numbers}")
print(f"Mixed type list: {mixed}")
print(f"Nested list: {nested}")

# List indexing and slicing
fruits_list = ["apple", "banana", "cherry", "date", "elderberry"]
print(f"\nFruits: {fruits_list}")
print(f"First fruit: {fruits_list[0]}")
print(f"Last fruit: {fruits_list[-1]}")
print(f"First 3 fruits: {fruits_list[:3]}")
print(f"Middle fruits: {fruits_list[1:4]}")
print(f"Every other fruit: {fruits_list[::2]}")

# Adding elements
shopping = ["milk", "bread"]
print(f"\nOriginal shopping list: {shopping}")
shopping.append("eggs")
print(f"After append: {shopping}")
shopping.insert(1, "butter")
print(f"After insert at index 1: {shopping}")
shopping.extend(["cheese", "yogurt"])
print(f"After extend: {shopping}")

# Removing elements
items = ["a", "b", "c", "d", "e"]
print(f"\nOriginal items: {items}")
removed = items.pop()
print(f"After pop(): {items}, removed: {removed}")
items.remove("b")
print(f"After remove('b'): {items}")
del items[1]
print(f"After del items[1]: {items}")

# List methods
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
print(f"\nNumbers: {numbers}")
print(f"Count of 1: {numbers.count(1)}")
print(f"Index of 9: {numbers.index(9)}")

# Sorting and reversing
sorted_nums = sorted(numbers)
print(f"Sorted (new list): {sorted_nums}")
numbers.sort(reverse=True)
print(f"Sorted in-place (descending): {numbers}")
numbers.reverse()
print(f"Reversed: {numbers}")

# List comprehensions
squares = [x**2 for x in range(1, 6)]
print(f"\nSquares (1-5): {squares}")

evens = [x for x in range(1, 11) if x % 2 == 0]
print(f"Even numbers (1-10): {evens}")

matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
print(f"3x3 multiplication table: {matrix}")

# List operations
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2
repeated = list1 * 3
print(f"\n{list1} + {list2} = {combined}")
print(f"{list1} * 3 = {repeated}")

# Membership testing
print(f"\n2 in {list1}: {2 in list1}")
print(f"7 in {list1}: {7 in list1}")

# Unpacking
unpack_a, unpack_b, unpack_c = [10, 20, 30]
print(f"\nUnpacked: a={unpack_a}, b={unpack_b}, c={unpack_c}")

first, *middle, last = [1, 2, 3, 4, 5]
print(f"Extended unpacking: first={first}, middle={middle}, last={last}")


# ============================================================================
# DICTIONARY OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("DICTIONARY OPERATIONS")
print("="*60)

# Creating dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "occupation": "Data Scientist"
}
print(f"\nPerson dictionary: {person}")

# Alternative creation methods
dict_from_list = dict([("a", 1), ("b", 2), ("c", 3)])
print(f"Dict from list of tuples: {dict_from_list}")

dict_from_keywords = dict(x=10, y=20, z=30)
print(f"Dict from keywords: {dict_from_keywords}")

# Accessing values
print(f"\nName: {person['name']}")
print(f"Age: {person.get('age')}")
print(f"Email (with default): {person.get('email', 'Not provided')}")

# Adding and updating
person["email"] = "alice@example.com"
print(f"\nAfter adding email: {person}")

person.update({"age": 31, "phone": "555-1234"})
print(f"After update: {person}")

# Removing items
contacts = {"home": "555-0001", "work": "555-0002", "mobile": "555-0003"}
print(f"\nContacts: {contacts}")

removed = contacts.pop("work")
print(f"After pop('work'): {contacts}, removed: {removed}")

last_item = contacts.popitem()
print(f"After popitem(): {contacts}, removed: {last_item}")

# Dictionary methods
product = {"name": "Laptop", "price": 999.99, "brand": "TechCo"}
print(f"\nProduct: {product}")
print(f"Keys: {list(product.keys())}")
print(f"Values: {list(product.values())}")
print(f"Items: {list(product.items())}")

# Iterating through dictionaries
print("\nIterating through product:")
for key, value in product.items():
    print(f"  {key}: {value}")

# Dictionary comprehensions
squared_dict = {x: x**2 for x in range(1, 6)}
print(f"\nSquared dict: {squared_dict}")

filtered = {k: v for k, v in product.items() if isinstance(v, str)}
print(f"Filtered (strings only): {filtered}")

# Nested dictionaries
students = {
    "student1": {"name": "Bob", "grade": 85, "subjects": ["Math", "Science"]},
    "student2": {"name": "Carol", "grade": 92, "subjects": ["English", "History"]},
    "student3": {"name": "Dave", "grade": 78, "subjects": ["Math", "Art"]}
}
print(f"\nStudents database:")
for student_id, info in students.items():
    print(f"  {student_id}: {info['name']} - Grade: {info['grade']}")

# Merging dictionaries (Python 3.9+)
defaults = {"theme": "light", "language": "en", "notifications": True}
user_prefs = {"language": "es", "timezone": "UTC"}
merged = defaults | user_prefs
print(f"\nDefaults: {defaults}")
print(f"User preferences: {user_prefs}")
print(f"Merged (user overrides): {merged}")

# Membership testing
print(f"\n'name' in product: {'name' in product}")
print(f"'color' in product: {'color' in product}")

# setdefault method
config = {"host": "localhost"}
port = config.setdefault("port", 8080)
print(f"\nConfig: {config}")
print(f"Port (set with default): {port}")


# ============================================================================
# COMBINED OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("COMBINED OPERATIONS")
print("="*60)

# Processing a dataset
employees = [
    {"name": "Alice", "age": 30, "salary": 75000.50, "department": "Engineering"},
    {"name": "Bob", "age": 25, "salary": 65000.00, "department": "Marketing"},
    {"name": "Carol", "age": 35, "salary": 85000.75, "department": "Engineering"},
    {"name": "Dave", "age": 28, "salary": 70000.25, "department": "Sales"}
]

print("\nEmployee Database:")
for emp in employees:
    print(f"  {emp['name']:8} | Age: {emp['age']} | "
          f"Salary: ${emp['salary']:,.2f} | Dept: {emp['department']}")

# Aggregations
total_salary = sum(emp["salary"] for emp in employees)
avg_age = sum(emp["age"] for emp in employees) / len(employees)

print(f"\nTotal salary budget: ${total_salary:,.2f}")
print(f"Average age: {avg_age:.1f}")

# Filtering
eng_employees = [emp for emp in employees if emp["department"] == "Engineering"]
print(f"\nEngineering department: {[e['name'] for e in eng_employees]}")

high_earners = [emp["name"] for emp in employees if emp["salary"] > 70000]
print(f"Employees earning > $70,000: {high_earners}")

# Grouping
by_dept = {}
for emp in employees:
    dept = emp["department"]
    if dept not in by_dept:
        by_dept[dept] = []
    by_dept[dept].append(emp["name"])

print("\nGrouped by department:")
for dept, names in by_dept.items():
    print(f"  {dept}: {', '.join(names)}")

# Transformation
salary_adjustments = {emp["name"]: emp["salary"] * 1.05 for emp in employees}
print("\nProjected salaries (5% raise):")
for name, new_salary in salary_adjustments.items():
    print(f"  {name}: ${new_salary:,.2f}")


print("\n" + "="*60)
print("DEMONSTRATION COMPLETE")
print("="*60 + "\n")
