"""
Python Functions and Closures Demonstration
Author: Python Skills Portfolio
Date: February 2026

This script demonstrates Python functions and closures:
- Function definitions and parameters
- Return values and multiple returns
- Default arguments, *args, and **kwargs
- Lambda functions
- Nested functions and closures
- Scope (local, global, nonlocal)
- Decorators
- Higher-order functions
"""

print("\n" + "="*60)
print("PYTHON FUNCTIONS AND CLOSURES DEMONSTRATION")
print("="*60)


# ============================================================================
# BASIC FUNCTION DEFINITIONS
# ============================================================================

print("\n" + "="*60)
print("BASIC FUNCTION DEFINITIONS")
print("="*60)

# Simple function with no parameters
def greet():
    return "Hello, World!"

result = greet()
print(f"\nSimple function: {result}")

# Function with parameters
def greet_person(name):
    return f"Hello, {name}!"

result = greet_person("Alice")
print(f"Function with parameter: {result}")

# Function with multiple parameters
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(f"Add 5 + 3 = {result}")

# Function with default parameters
def greet_with_title(name, title="Mr."):
    return f"Hello, {title} {name}"

print(f"\nWith title: {greet_with_title('Smith')}")
print(f"Custom title: {greet_with_title('Johnson', 'Dr.')}")

# Function with multiple return values
def calculate(a, b):
    return a + b, a - b, a * b, a / b

add, sub, mul, div = calculate(10, 2)
print(f"\nMultiple returns: add={add}, sub={sub}, mul={mul}, div={div}")


# ============================================================================
# POSITIONAL AND KEYWORD ARGUMENTS
# ============================================================================

print("\n" + "="*60)
print("POSITIONAL AND KEYWORD ARGUMENTS")
print("="*60)

def create_profile(name, age, city, occupation):
    return f"{name}, {age}, from {city}, works as {occupation}"

# Positional arguments
profile1 = create_profile("Alice", 30, "New York", "Engineer")
print(f"\nPositional: {profile1}")

# Keyword arguments
profile2 = create_profile(city="Boston", name="Bob", occupation="Designer", age=25)
print(f"Keyword: {profile2}")

# Mixed (positional must come first)
profile3 = create_profile("Carol", 35, city="Chicago", occupation="Manager")
print(f"Mixed: {profile3}")


# ============================================================================
# *ARGS AND **KWARGS
# ============================================================================

print("\n" + "="*60)
print("*ARGS AND **KWARGS")
print("="*60)

# *args - variable number of positional arguments
def sum_all(*args):
    total = sum(args)
    return total

print(f"\nsum_all(1, 2, 3): {sum_all(1, 2, 3)}")
print(f"sum_all(1, 2, 3, 4, 5): {sum_all(1, 2, 3, 4, 5)}")
print(f"sum_all(10, 20): {sum_all(10, 20)}")

# **kwargs - variable number of keyword arguments
def print_info(**kwargs):
    info_list = []
    for key, value in kwargs.items():
        info_list.append(f"{key}={value}")
    return ", ".join(info_list)

result = print_info(name="Alice", age=30, city="NYC")
print(f"\nprint_info: {result}")

result = print_info(language="Python", version=3.11, type="interpreted")
print(f"print_info: {result}")

# Combining regular args, *args, and **kwargs
def complex_function(required, *args, default="value", **kwargs):
    result = f"Required: {required}\n"
    result += f"Args: {args}\n"
    result += f"Default: {default}\n"
    result += f"Kwargs: {kwargs}"
    return result

print(f"\nComplex function:")
print(complex_function("must_have", 1, 2, 3, default="custom", x=10, y=20))


# ============================================================================
# LAMBDA FUNCTIONS
# ============================================================================

print("\n" + "="*60)
print("LAMBDA FUNCTIONS")
print("="*60)

# Simple lambda
square = lambda x: x ** 2
print(f"\nLambda square(5): {square(5)}")

# Lambda with multiple parameters
multiply = lambda x, y: x * y
print(f"Lambda multiply(4, 3): {multiply(4, 3)}")

# Lambda in sorting
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Carol", "grade": 78}
]
sorted_students = sorted(students, key=lambda x: x["grade"], reverse=True)
print(f"\nSorted by grade (descending):")
for student in sorted_students:
    print(f"  {student['name']}: {student['grade']}")

# Lambda in filtering
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"\nFiltered evens: {evens}")

# Lambda in mapping
squared = list(map(lambda x: x ** 2, numbers))
print(f"Mapped squares: {squared}")


# ============================================================================
# NESTED FUNCTIONS
# ============================================================================

print("\n" + "="*60)
print("NESTED FUNCTIONS")
print("="*60)

# Function containing another function
def outer_function(text):
    def inner_function():
        return text.upper()
    
    result = inner_function()
    return f"Outer got: {result}"

print(f"\nNested function: {outer_function('hello')}")

# Helper function inside
def process_data(data):
    def validate(item):
        return item > 0
    
    def transform(item):
        return item * 2
    
    validated = [x for x in data if validate(x)]
    transformed = [transform(x) for x in validated]
    return transformed

result = process_data([-2, -1, 0, 1, 2, 3, 4])
print(f"Process data [-2, -1, 0, 1, 2, 3, 4]: {result}")


# ============================================================================
# CLOSURES
# ============================================================================

print("\n" + "="*60)
print("CLOSURES")
print("="*60)

# Basic closure - inner function remembers outer function's variables
def make_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

times_2 = make_multiplier(2)
times_5 = make_multiplier(5)

print(f"\nClosure times_2(10): {times_2(10)}")
print(f"Closure times_5(10): {times_5(10)}")

# Closure with state
def make_counter():
    count = 0
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    return increment

counter1 = make_counter()
counter2 = make_counter()

print(f"\nCounter1 first call: {counter1()}")
print(f"Counter1 second call: {counter1()}")
print(f"Counter1 third call: {counter1()}")
print(f"Counter2 first call: {counter2()}")
print(f"Counter2 second call: {counter2()}")

# Closure for encapsulation
def create_account(initial_balance):
    balance = initial_balance
    
    def deposit(amount):
        nonlocal balance
        balance += amount
        return f"Deposited ${amount}. New balance: ${balance}"
    
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return f"Insufficient funds. Balance: ${balance}"
        balance -= amount
        return f"Withdrew ${amount}. New balance: ${balance}"
    
    def get_balance():
        return f"Current balance: ${balance}"
    
    return deposit, withdraw, get_balance

deposit, withdraw, get_balance = create_account(1000)
print(f"\n{get_balance()}")
print(deposit(500))
print(withdraw(200))
print(get_balance())


# ============================================================================
# SCOPE: LOCAL, GLOBAL, NONLOCAL
# ============================================================================

print("\n" + "="*60)
print("SCOPE: LOCAL, GLOBAL, NONLOCAL")
print("="*60)

# Global variable
global_var = "I am global"

def show_global():
    print(f"Inside function: {global_var}")

print(f"\nOutside function: {global_var}")
show_global()

# Local variable
def local_scope():
    local_var = "I am local"
    return local_var

result = local_scope()
print(f"\nLocal variable returned: {result}")

# Modifying global variable
counter = 0

def increment_global():
    global counter
    counter += 1
    return counter

print(f"\nInitial counter: {counter}")
print(f"After increment: {increment_global()}")
print(f"After increment: {increment_global()}")
print(f"Global counter now: {counter}")

# Nonlocal in nested functions
def outer():
    x = "outer"
    
    def inner():
        nonlocal x
        x = "modified by inner"
        return x
    
    print(f"  Before inner: x = '{x}'")
    result = inner()
    print(f"  After inner: x = '{x}'")
    return result

print("\nNonlocal example:")
outer()


# ============================================================================
# DECORATORS
# ============================================================================

print("\n" + "="*60)
print("DECORATORS")
print("="*60)

# Simple decorator
def uppercase_decorator(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@uppercase_decorator
def say_hello():
    return "hello, world"

print(f"\nDecorated function: {say_hello()}")

# Decorator with arguments
def repeat_decorator(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat_decorator(3)
def greet_simple(name):
    return f"Hello, {name}!"

result = greet_simple("Bob")
print(f"\nRepeated 3 times: {result}")

# Timing decorator
def timer_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        execution_time = (end - start) * 1000  # Convert to milliseconds
        return result, execution_time
    return wrapper

@timer_decorator
def slow_function():
    total = 0
    for i in range(100000):
        total += i
    return total

result, time_taken = slow_function()
print(f"\nTimed function result: {result}")
print(f"Execution time: {time_taken:.2f}ms")


# ============================================================================
# HIGHER-ORDER FUNCTIONS
# ============================================================================

print("\n" + "="*60)
print("HIGHER-ORDER FUNCTIONS")
print("="*60)

# Function that takes another function as argument
def apply_operation(numbers, operation):
    return [operation(x) for x in numbers]

def double(x):
    return x * 2

def square_func(x):
    return x ** 2

numbers = [1, 2, 3, 4, 5]
print(f"\nOriginal: {numbers}")
print(f"Doubled: {apply_operation(numbers, double)}")
print(f"Squared: {apply_operation(numbers, square_func)}")
print(f"With lambda (x + 10): {apply_operation(numbers, lambda x: x + 10)}")

# Function that returns a function
def create_adder(n):
    def adder(x):
        return x + n
    return adder

add_5 = create_adder(5)
add_10 = create_adder(10)

print(f"\nadd_5(20): {add_5(20)}")
print(f"add_10(20): {add_10(20)}")

# Built-in higher-order functions
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map
squared_map = list(map(lambda x: x ** 2, numbers))
print(f"\nmap (squared): {squared_map}")

# filter
evens_filter = list(filter(lambda x: x % 2 == 0, numbers))
print(f"filter (evens): {evens_filter}")

# reduce
from functools import reduce
sum_reduce = reduce(lambda x, y: x + y, numbers)
print(f"reduce (sum): {sum_reduce}")

product_reduce = reduce(lambda x, y: x * y, [1, 2, 3, 4, 5])
print(f"reduce (product): {product_reduce}")


# ============================================================================
# RECURSIVE FUNCTIONS
# ============================================================================

print("\n" + "="*60)
print("RECURSIVE FUNCTIONS")
print("="*60)

# Factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"\nfactorial(5): {factorial(5)}")
print(f"factorial(7): {factorial(7)}")

# Fibonacci
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"\nFibonacci sequence (first 10):")
fib_sequence = [fibonacci(i) for i in range(10)]
print(f"  {fib_sequence}")

# Sum of list (recursive)
def sum_list(lst):
    if not lst:
        return 0
    return lst[0] + sum_list(lst[1:])

print(f"\nsum_list([1, 2, 3, 4, 5]): {sum_list([1, 2, 3, 4, 5])}")


# ============================================================================
# PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "="*60)
print("PRACTICAL EXAMPLES")
print("="*60)

# Closure for creating validators
def create_validator(min_value, max_value):
    def validate(value):
        if value < min_value:
            return False, f"Value {value} is below minimum {min_value}"
        if value > max_value:
            return False, f"Value {value} is above maximum {max_value}"
        return True, f"Value {value} is valid"
    return validate

age_validator = create_validator(0, 120)
score_validator = create_validator(0, 100)

print(f"\nAge validation:")
print(f"  {age_validator(25)}")
print(f"  {age_validator(150)}")

print(f"\nScore validation:")
print(f"  {score_validator(85)}")
print(f"  {score_validator(105)}")

# Function composition
def compose(*functions):
    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return inner

def add_10(x):
    return x + 10

def multiply_by_2(x):
    return x * 2

def subtract_5(x):
    return x - 5

composed = compose(subtract_5, multiply_by_2, add_10)
print(f"\nFunction composition (add 10, multiply by 2, subtract 5):")
print(f"  Input: 5, Output: {composed(5)}")
print(f"  Calculation: ((5 + 10) * 2) - 5 = {composed(5)}")

# Memoization using closure
def memoize(func):
    cache = {}
    
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    
    return wrapper

@memoize
def expensive_fibonacci(n):
    if n <= 1:
        return n
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2)

print(f"\nMemoized Fibonacci:")
print(f"  fibonacci(30): {expensive_fibonacci(30)}")
print(f"  fibonacci(35): {expensive_fibonacci(35)}")


print("\n" + "="*60)
print("DEMONSTRATION COMPLETE")
print("="*60 + "\n")
