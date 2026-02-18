"""
Advanced Python Functions Demonstration
Author: Python Skills Portfolio
Date: February 2026

This script demonstrates advanced function concepts:
- Logging decorators
- Retry decorators
- Caching/memoization decorators
- Validation decorators
- Context managers as decorators
- Partial functions
- Descriptor protocol
- Generator functions
- Coroutines
"""

import functools
import logging
import time
from typing import Any, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

print("\n" + "="*60)
print("ADVANCED PYTHON FUNCTIONS DEMONSTRATION")
print("="*60)


# ============================================================================
# LOGGING DECORATORS
# ============================================================================

print("\n" + "="*60)
print("LOGGING DECORATORS")
print("="*60)

def log_execution(func):
    """Decorator that logs function execution time and result."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info(f"Starting {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Completed {func.__name__} successfully")
            return result
        except Exception as e:
            logger.error(f"Failed {func.__name__}: {e}")
            raise
    return wrapper

@log_execution
def process_data(data):
    """Example function that processes data."""
    time.sleep(0.1)  # Simulate processing
    return [x * 2 for x in data]

print("\nExecuting logged function:")
result = process_data([1, 2, 3, 4, 5])
print(f"Result: {result}")


def log_with_params(func):
    """Decorator that logs function parameters and return value."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_with_params
def calculate_sum(a, b, c=0):
    return a + b + c

print("\nExecuting function with parameter logging:")
result = calculate_sum(10, 20, c=5)
print(f"Result: {result}")


# ============================================================================
# RETRY DECORATORS
# ============================================================================

print("\n" + "="*60)
print("RETRY DECORATORS")
print("="*60)

def retry(max_attempts=3, delay=1):
    """Decorator that retries a function if it raises an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts")
                        raise
                    logger.warning(f"{func.__name__} attempt {attempts} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

# Counter to simulate failures
attempt_counter = 0

@retry(max_attempts=3, delay=0.1)
def unreliable_function():
    """Simulates a function that fails twice then succeeds."""
    global attempt_counter
    attempt_counter += 1
    if attempt_counter < 3:
        raise ConnectionError("Network timeout")
    return "Success!"

print("\nExecuting unreliable function with retry:")
attempt_counter = 0  # Reset counter
result = unreliable_function()
print(f"Final result: {result}")


# ============================================================================
# CACHING/MEMOIZATION DECORATORS
# ============================================================================

print("\n" + "="*60)
print("CACHING/MEMOIZATION DECORATORS")
print("="*60)

def manual_cache(func):
    """Custom caching decorator."""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"  Cache hit for {args}")
            return cache[args]
        print(f"  Cache miss for {args}, computing...")
        result = func(*args)
        cache[args] = result
        return result
    
    return wrapper

@manual_cache
def fibonacci(n):
    """Calculate Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("\nManual cache demonstration:")
print(f"fibonacci(10) = {fibonacci(10)}")
print(f"fibonacci(10) again = {fibonacci(10)}")  # Should hit cache


# Using functools.lru_cache
@functools.lru_cache(maxsize=128)
def expensive_calculation(n):
    """Simulates an expensive calculation."""
    time.sleep(0.01)  # Simulate work
    return n ** 2 + n ** 3

print("\nLRU cache demonstration:")
start = time.time()
result1 = expensive_calculation(100)
time1 = time.time() - start

start = time.time()
result2 = expensive_calculation(100)  # Should be cached
time2 = time.time() - start

print(f"First call: {result1} (took {time1*1000:.2f}ms)")
print(f"Second call: {result2} (took {time2*1000:.2f}ms)")
print(f"Cache info: {expensive_calculation.cache_info()}")


# ============================================================================
# VALIDATION DECORATORS
# ============================================================================

print("\n" + "="*60)
print("VALIDATION DECORATORS")
print("="*60)

def validate_types(**type_constraints):
    """Decorator that validates argument types."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate types
            for param_name, expected_type in type_constraints.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Parameter '{param_name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int, salary=float)
def create_employee(name, age, salary):
    return f"Employee: {name}, Age: {age}, Salary: ${salary:,.2f}"

print("\nType validation decorator:")
print(create_employee("Alice", 30, 75000.50))

try:
    print(create_employee("Bob", "thirty", 65000.00))  # Should fail
except TypeError as e:
    print(f"Validation error: {e}")


def validate_range(param_name, min_val=None, max_val=None):
    """Decorator that validates numeric ranges."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            if param_name in bound_args.arguments:
                value = bound_args.arguments[param_name]
                if min_val is not None and value < min_val:
                    raise ValueError(f"{param_name} must be >= {min_val}")
                if max_val is not None and value > max_val:
                    raise ValueError(f"{param_name} must be <= {max_val}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_range("age", min_val=0, max_val=120)
@validate_range("score", min_val=0, max_val=100)
def record_student(name, age, score):
    return f"Student: {name}, Age: {age}, Score: {score}"

print("\nRange validation decorator:")
print(record_student("Carol", 20, 85))

try:
    print(record_student("Dave", 150, 95))  # Should fail
except ValueError as e:
    print(f"Validation error: {e}")


# ============================================================================
# TIMING AND PROFILING DECORATORS
# ============================================================================

print("\n" + "="*60)
print("TIMING AND PROFILING DECORATORS")
print("="*60)

def timing_decorator(func):
    """Decorator that measures execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        print(f"{func.__name__} executed in {execution_time:.2f}ms")
        return result
    return wrapper

@timing_decorator
def slow_computation(n):
    """Simulates a slow computation."""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

print("\nTiming decorator:")
result = slow_computation(100000)
print(f"Result: {result}")


def count_calls(func):
    """Decorator that counts how many times a function is called."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        print(f"{func.__name__} has been called {wrapper.call_count} time(s)")
        return func(*args, **kwargs)
    
    wrapper.call_count = 0
    return wrapper

@count_calls
def greet(name):
    return f"Hello, {name}!"

print("\nCall counting decorator:")
greet("Alice")
greet("Bob")
greet("Carol")


# ============================================================================
# PARTIAL FUNCTIONS
# ============================================================================

print("\n" + "="*60)
print("PARTIAL FUNCTIONS")
print("="*60)

def power(base, exponent):
    """Calculate base raised to exponent."""
    return base ** exponent

# Create specialized functions using partial
square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)

print("\nPartial functions:")
print(f"square(5) = {square(5)}")
print(f"cube(5) = {cube(5)}")

# Practical example: logging with fixed level
def log_message(message, level="INFO", module="app"):
    """Log a message with specified level and module."""
    return f"[{level}] {module}: {message}"

# Create specialized loggers
error_logger = functools.partial(log_message, level="ERROR")
debug_logger = functools.partial(log_message, level="DEBUG", module="debug")

print(f"\n{error_logger('Something went wrong')}")
print(f"{debug_logger('Debugging information')}")


# ============================================================================
# GENERATOR FUNCTIONS
# ============================================================================

print("\n" + "="*60)
print("GENERATOR FUNCTIONS")
print("="*60)

def simple_generator(n):
    """Generate numbers from 0 to n-1."""
    for i in range(n):
        yield i

print("\nSimple generator:")
gen = simple_generator(5)
print(f"Generator object: {gen}")
print(f"Generated values: {list(simple_generator(5))}")


def fibonacci_generator(limit):
    """Generate Fibonacci numbers up to limit."""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

print("\nFibonacci generator:")
fibs = list(fibonacci_generator(100))
print(f"Fibonacci numbers < 100: {fibs}")


def infinite_counter(start=0):
    """Infinite counter generator."""
    count = start
    while True:
        yield count
        count += 1

print("\nInfinite counter (first 10 values):")
counter = infinite_counter(100)
first_ten = [next(counter) for _ in range(10)]
print(f"Values: {first_ten}")


# Generator expression
print("\nGenerator expression:")
squared_gen = (x**2 for x in range(10))
print(f"Generator: {squared_gen}")
print(f"First 5 squared: {[next(squared_gen) for _ in range(5)]}")


# ============================================================================
# ADVANCED GENERATOR PATTERNS
# ============================================================================

print("\n" + "="*60)
print("ADVANCED GENERATOR PATTERNS")
print("="*60)

def chunk_data(data, chunk_size):
    """Yield data in chunks."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

print("\nData chunking:")
data = list(range(20))
print(f"Original: {data}")
print("Chunks of 5:")
for chunk in chunk_data(data, 5):
    print(f"  {chunk}")


def pipeline(*functions):
    """Create a data processing pipeline."""
    def process(data):
        for item in data:
            value = item
            for func in functions:
                value = func(value)
            yield value
    return process

# Pipeline functions
add_10 = lambda x: x + 10
multiply_2 = lambda x: x * 2
subtract_5 = lambda x: x - 5

print("\nGenerator pipeline:")
data = [1, 2, 3, 4, 5]
processor = pipeline(add_10, multiply_2, subtract_5)
results = list(processor(data))
print(f"Input: {data}")
print(f"After pipeline: {results}")


# ============================================================================
# FUNCTION FACTORIES
# ============================================================================

print("\n" + "="*60)
print("FUNCTION FACTORIES")
print("="*60)

def create_multiplier_factory(base_multiplier):
    """Factory that creates multiplier functions."""
    def create_multiplier(multiplier):
        def multiply(x):
            return x * base_multiplier * multiplier
        return multiply
    return create_multiplier

# Create factory with base multiplier of 10
factory = create_multiplier_factory(10)

# Create specific multipliers
times_20 = factory(2)  # 10 * 2 = 20x
times_50 = factory(5)  # 10 * 5 = 50x

print("\nFunction factory:")
print(f"times_20(3) = {times_20(3)}")
print(f"times_50(3) = {times_50(3)}")


def create_validator_factory(validation_type):
    """Factory that creates different types of validators."""
    validators = {
        'email': lambda x: '@' in x and '.' in x,
        'phone': lambda x: x.replace('-', '').replace(' ', '').isdigit(),
        'positive': lambda x: x > 0,
        'even': lambda x: x % 2 == 0
    }
    
    def validate(value):
        validator = validators.get(validation_type)
        if validator is None:
            raise ValueError(f"Unknown validation type: {validation_type}")
        return validator(value)
    
    return validate

print("\nValidator factory:")
email_validator = create_validator_factory('email')
phone_validator = create_validator_factory('phone')
positive_validator = create_validator_factory('positive')

print(f"email_validator('test@example.com'): {email_validator('test@example.com')}")
print(f"email_validator('invalid'): {email_validator('invalid')}")
print(f"phone_validator('555-1234'): {phone_validator('555-1234')}")
print(f"positive_validator(10): {positive_validator(10)}")
print(f"positive_validator(-5): {positive_validator(-5)}")


# ============================================================================
# PRACTICAL EXAMPLE: API ENDPOINT DECORATOR
# ============================================================================

print("\n" + "="*60)
print("PRACTICAL EXAMPLE: API ENDPOINT DECORATOR")
print("="*60)

def api_endpoint(method="GET", auth_required=True):
    """Decorator for API endpoints with authentication and method validation."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request_data):
            logger = logging.getLogger(func.__module__)
            
            # Validate HTTP method
            request_method = request_data.get('method', 'GET')
            if request_method != method:
                logger.error(f"Method not allowed: {request_method}")
                return {"error": "Method not allowed", "status": 405}
            
            # Check authentication
            if auth_required and not request_data.get('auth_token'):
                logger.error("Authentication required")
                return {"error": "Authentication required", "status": 401}
            
            # Execute endpoint
            try:
                logger.info(f"Processing {method} request to {func.__name__}")
                result = func(request_data)
                return {"data": result, "status": 200}
            except Exception as e:
                logger.error(f"Request failed: {e}")
                return {"error": str(e), "status": 500}
        
        return wrapper
    return decorator

@api_endpoint(method="POST", auth_required=True)
def create_user(request_data):
    """API endpoint to create a user."""
    user_data = request_data.get('body', {})
    return f"Created user: {user_data.get('name')}"

@api_endpoint(method="GET", auth_required=False)
def get_status(request_data):
    """API endpoint to get system status."""
    return "System is running"

print("\nAPI endpoint decorators:")

# Valid request
response = create_user({
    'method': 'POST',
    'auth_token': 'abc123',
    'body': {'name': 'Alice'}
})
print(f"Valid POST: {response}")

# Invalid method
response = create_user({
    'method': 'GET',
    'auth_token': 'abc123',
    'body': {'name': 'Bob'}
})
print(f"Wrong method: {response}")

# Missing auth
response = create_user({
    'method': 'POST',
    'body': {'name': 'Carol'}
})
print(f"No auth: {response}")

# Public endpoint
response = get_status({'method': 'GET'})
print(f"Public endpoint: {response}")


print("\n" + "="*60)
print("DEMONSTRATION COMPLETE")
print("="*60 + "\n")
