"""
Object-Oriented Programming Patterns Demonstration
Author: Python Skills Portfolio
Date: February 2026

This script demonstrates OOP concepts and design patterns:
- Classes and objects
- Instance and class variables
- Methods (instance, class, static)
- Inheritance and polymorphism
- Encapsulation and property decorators
- Abstract base classes
- Composition vs inheritance
- Mixins
- Design patterns (singleton, factory, observer)
- Exception handling in OOP
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum
from copy import deepcopy

print("\n" + "="*60)
print("OOP PATTERNS DEMONSTRATION")
print("="*60)


# ============================================================================
# BASIC CLASS DEFINITION
# ============================================================================

print("\n" + "="*60)
print("BASIC CLASS DEFINITION")
print("="*60)

class Animal:
    """Basic class with __init__ and instance methods."""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def speak(self):
        return f"{self.name} makes a sound"
    
    def __str__(self):
        return f"Animal(name={self.name}, species={self.species})"

dog = Animal("Buddy", "Dog")
print(f"\nBasic class: {dog}")
print(f"Method: {dog.speak()}")


# ============================================================================
# INSTANCE AND CLASS VARIABLES
# ============================================================================

print("\n" + "="*60)
print("INSTANCE AND CLASS VARIABLES")
print("="*60)

class Counter:
    """Demonstrates instance and class variables."""
    
    total_count = 0  # Class variable
    
    def __init__(self, name):
        self.name = name  # Instance variable
        self.count = 0  # Instance variable
        Counter.total_count += 1
    
    def increment(self):
        self.count += 1
        Counter.total_count += 1
    
    def __str__(self):
        return f"{self.name}: self.count={self.count}, class.total={Counter.total_count}"

counter1 = Counter("Counter1")
counter2 = Counter("Counter2")

print(f"\nInitial state:")
print(f"  {counter1}")
print(f"  {counter2}")

counter1.increment()
counter1.increment()
counter2.increment()

print(f"\nAfter incrementing:")
print(f"  {counter1}")
print(f"  {counter2}")


# ============================================================================
# INSTANCE, CLASS, AND STATIC METHODS
# ============================================================================

print("\n" + "="*60)
print("INSTANCE, CLASS, AND STATIC METHODS")
print("="*60)

class MathOperations:
    """Demonstrates different method types."""
    
    pi = 3.14159
    instances_created = 0
    
    def __init__(self, value):
        self.value = value
        MathOperations.instances_created += 1
    
    def instance_method(self):
        """Instance method - has access to self and instance variables."""
        return f"Instance value: {self.value}"
    
    @classmethod
    def create_from_string(cls, value_str):
        """Class method - takes cls instead of self."""
        value = float(value_str)
        return cls(value)
    
    @classmethod
    def get_instances_created(cls):
        """Class methods can access class variables."""
        return cls.instances_created
    
    @staticmethod
    def static_method(a, b):
        """Static method - no access to instance or class."""
        return a + b

print("\nInstance method:")
obj = MathOperations(10)
print(f"  {obj.instance_method()}")

print("\nClass method:")
obj2 = MathOperations.create_from_string("25.5")
print(f"  Created from string: {obj2.value}")
print(f"  Instances created: {MathOperations.get_instances_created()}")

print("\nStatic method:")
print(f"  add(5, 3) = {MathOperations.static_method(5, 3)}")


# ============================================================================
# INHERITANCE
# ============================================================================

print("\n" + "="*60)
print("INHERITANCE")
print("="*60)

class Animal2:
    """Parent class."""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self):
        return f"{self.name} makes a sound"
    
    def info(self):
        return f"{self.name} is {self.age} years old"

class Dog(Animal2):
    """Child class that inherits from Animal2."""
    
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # Call parent constructor
        self.breed = breed
    
    def speak(self):  # Override parent method
        return f"{self.name} barks"
    
    def fetch(self):
        return f"{self.name} fetches the ball"

class Cat(Animal2):
    """Another child class."""
    
    def speak(self):
        return f"{self.name} meows"

print("\nInheritance and method override:")
dog = Dog("Max", 3, "Golden Retriever")
cat = Cat("Whiskers", 2)

print(f"Dog: {dog.speak()}")
print(f"Dog fetch: {dog.fetch()}")
print(f"Dog info: {dog.info()}")
print(f"Cat: {cat.speak()}")
print(f"Cat info: {cat.info()}")


# ============================================================================
# POLYMORPHISM
# ============================================================================

print("\n" + "="*60)
print("POLYMORPHISM")
print("="*60)

class Shape:
    """Base class for shapes."""
    
    def area(self):
        raise NotImplementedError("Subclass must implement area()")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height

class Cylinder(Shape):
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height
    
    def area(self):
        # Calculate surface area: 2πr² + 2πrh
        return 2 * 3.14159 * self.radius ** 2 + 2 * 3.14159 * self.radius * self.height

print("\nPolymorphism - same method, different implementations:")
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4), Cylinder(3, 8)]
for shape in shapes:
    print(f"  {shape.__class__.__name__} area: {shape.area():.2f}")


# ============================================================================
# ENCAPSULATION AND PROPERTIES
# ============================================================================

print("\n" + "="*60)
print("ENCAPSULATION AND PROPERTIES")
print("="*60)

class BankAccount:
    """Demonstrates encapsulation with properties."""
    
    def __init__(self, account_number, initial_balance=0):
        self._account_number = account_number  # Protected
        self.__balance = initial_balance  # Private (name mangling)
    
    @property
    def balance(self):
        """Getter property."""
        return self.__balance
    
    @balance.setter
    def balance(self, amount):
        """Setter property with validation."""
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = amount
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        return f"Deposited ${amount}. New balance: ${self.__balance}"
    
    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        return f"Withdrew ${amount}. New balance: ${self.__balance}"

print("\nEncapsulation with properties:")
account = BankAccount("12345", 1000)
print(f"Initial balance: ${account.balance}")
print(account.deposit(500))
print(account.withdraw(200))
print(f"Final balance: ${account.balance}")

try:
    account.balance = -100  # Validation in setter
except ValueError as e:
    print(f"Error: {e}")


# ============================================================================
# ABSTRACT BASE CLASSES
# ============================================================================

print("\n" + "="*60)
print("ABSTRACT BASE CLASSES")
print("="*60)

class Vehicle(ABC):
    """Abstract base class."""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    @abstractmethod
    def start(self):
        """Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def stop(self):
        """Must be implemented by subclasses."""
        pass
    
    def info(self):
        """Concrete method in abstract class."""
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    """Concrete implementation of Vehicle."""
    
    def start(self):
        return "Car engine started"
    
    def stop(self):
        return "Car engine stopped"

class Motorcycle(Vehicle):
    """Another concrete implementation."""
    
    def start(self):
        return "Motorcycle engine roared to life"
    
    def stop(self):
        return "Motorcycle engine silenced"

print("\nAbstract base classes:")
car = Car("Toyota", "Camry")
moto = Motorcycle("Harley-Davidson", "Street 750")

print(f"Car: {car.info()} - {car.start()}")
print(f"Moto: {moto.info()} - {moto.start()}")

# This would raise an error (cannot instantiate abstract class):
# vehicle = Vehicle("Generic", "Model")


# ============================================================================
# COMPOSITION VS INHERITANCE
# ============================================================================

print("\n" + "="*60)
print("COMPOSITION VS INHERITANCE")
print("="*60)

# Composition approach
class Engine:
    def start(self):
        return "Engine started"
    
    def stop(self):
        return "Engine stopped"

class Transmission:
    def shift(self, gear):
        return f"Shifted to {gear}"

class CompositionCar:
    """Uses composition instead of inheritance."""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.engine = Engine()
        self.transmission = Transmission()
    
    def start(self):
        return self.engine.start()
    
    def stop(self):
        return self.engine.stop()
    
    def drive(self, gear):
        return self.transmission.shift(gear)

print("\nComposition approach:")
car = CompositionCar("Ford", "Mustang")
print(f"  {car.start()}")
print(f"  {car.drive('D')}")
print(f"  {car.stop()}")


# ============================================================================
# MIXINS
# ============================================================================

print("\n" + "="*60)
print("MIXINS")
print("="*60)

class TimestampMixin:
    """Mixin that adds timestamp functionality."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = None
        self.modified_at = None
    
    def mark_created(self):
        self.created_at = "2026-02-17 10:00:00"
    
    def mark_modified(self):
        self.modified_at = "2026-02-17 10:05:00"

class SerializableMixin:
    """Mixin that adds serialization."""
    
    def to_dict(self):
        return self.__dict__.copy()
    
    def from_dict(self, data):
        self.__dict__.update(data)

class Document(TimestampMixin, SerializableMixin):
    """Class using multiple mixins."""
    
    def __init__(self, title, content):
        super().__init__()
        self.title = title
        self.content = content

print("\nMixins:")
doc = Document("My Document", "This is the content")
doc.mark_created()
doc.mark_modified()
print(f"  Title: {doc.title}")
print(f"  Created: {doc.created_at}")
print(f"  Modified: {doc.modified_at}")
print(f"  As dict: {doc.to_dict()}")


# ============================================================================
# SINGLETON PATTERN
# ============================================================================

print("\n" + "="*60)
print("SINGLETON PATTERN")
print("="*60)

class Singleton:
    """Singleton pattern - only one instance exists."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.value = 0
            self.initialized = True

singleton1 = Singleton()
singleton2 = Singleton()

singleton1.value = 42
print(f"\nSingleton pattern:")
print(f"  singleton1.value = {singleton1.value}")
print(f"  singleton2.value = {singleton2.value}")
print(f"  Are they the same object? {singleton1 is singleton2}")


# ============================================================================
# FACTORY PATTERN
# ============================================================================

print("\n" + "="*60)
print("FACTORY PATTERN")
print("="*60)

class Transport(ABC):
    """Abstract transport."""
    @abstractmethod
    def deliver(self):
        pass

class Truck(Transport):
    def deliver(self):
        return "Delivering by truck"

class Ship(Transport):
    def deliver(self):
        return "Delivering by ship"

class Plane(Transport):
    def deliver(self):
        return "Delivering by plane"

class TransportFactory:
    """Factory for creating transport objects."""
    
    _transports = {
        'truck': Truck,
        'ship': Ship,
        'plane': Plane
    }
    
    @classmethod
    def create_transport(cls, transport_type):
        transport_class = cls._transports.get(transport_type.lower())
        if transport_class is None:
            raise ValueError(f"Unknown transport type: {transport_type}")
        return transport_class()

print("\nFactory pattern:")
transports = ['truck', 'ship', 'plane']
for transport_type in transports:
    transport = TransportFactory.create_transport(transport_type)
    print(f"  {transport_type}: {transport.deliver()}")


# ============================================================================
# OBSERVER PATTERN
# ============================================================================

print("\n" + "="*60)
print("OBSERVER PATTERN")
print("="*60)

class Observable:
    """Subject that notifies observers of changes."""
    
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        """Attach an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Detach an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event):
        """Notify all observers."""
        for observer in self._observers:
            observer.update(event)

class Observer(ABC):
    """Observer interface."""
    
    @abstractmethod
    def update(self, event):
        pass

class EmailNotifier(Observer):
    def update(self, event):
        print(f"  Email: {event}")

class SMSNotifier(Observer):
    def update(self, event):
        print(f"  SMS: {event}")

class LogNotifier(Observer):
    def update(self, event):
        print(f"  Log: {event}")

class UserAccount(Observable):
    """Example observable class."""
    
    def __init__(self, username):
        super().__init__()
        self.username = username
    
    def login(self):
        event = f"User {self.username} logged in"
        self.notify(event)
    
    def logout(self):
        event = f"User {self.username} logged out"
        self.notify(event)

print("\nObserver pattern:")
account = UserAccount("alice")
account.attach(EmailNotifier())
account.attach(SMSNotifier())
account.attach(LogNotifier())

print("On login:")
account.login()

print("\nOn logout:")
account.logout()


# ============================================================================
# CUSTOM ITERATORS
# ============================================================================

print("\n" + "="*60)
print("CUSTOM ITERATORS")
print("="*60)

class CountUp:
    """Custom iterator that counts up to a limit."""
    
    def __init__(self, max_value):
        self.max_value = max_value
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.max_value:
            self.current += 1
            return self.current
        else:
            raise StopIteration

print("\nCustom iterator:")
counter = CountUp(5)
print(f"  Counting: {list(counter)}")

# Using in a for loop
counter = CountUp(5)
print(f"  In loop: ", end="")
for num in counter:
    print(num, end=" ")
print()


# ============================================================================
# CONTEXT MANAGERS
# ============================================================================

print("\n" + "="*60)
print("CONTEXT MANAGERS")
print("="*60)

class FileManager:
    """Context manager for file operations."""
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"  Opening {self.filename}")
        self.file = f"<file object: {self.filename}>"
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Closing {self.filename}")
        if exc_type:
            print(f"  Exception occurred: {exc_type.__name__}")
        return False

print("\nContext manager with statement:")
with FileManager("data.txt", "r") as file:
    print(f"  Working with: {file}")


# ============================================================================
# EXCEPTION HANDLING IN OOP
# ============================================================================

print("\n" + "="*60)
print("EXCEPTION HANDLING IN OOP")
print("="*60)

class CustomError(Exception):
    """Custom exception class."""
    pass

class DataValidator:
    """Validates data and raises custom exceptions."""
    
    @staticmethod
    def validate_age(age):
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")
        return True
    
    @staticmethod
    def validate_email(email):
        if '@' not in email or '.' not in email:
            raise CustomError("Invalid email format")
        return True

print("\nException handling:")
validator = DataValidator()

try:
    validator.validate_age(30)
    print("  Age 30: Valid")
except (TypeError, ValueError) as e:
    print(f"  Error: {e}")

try:
    validator.validate_age("not a number")
except (TypeError, ValueError) as e:
    print(f"  Error: {e}")

try:
    validator.validate_email("invalid-email")
except CustomError as e:
    print(f"  Error: {e}")

try:
    validator.validate_email("user@example.com")
    print("  Email: Valid")
except CustomError as e:
    print(f"  Error: {e}")


# ============================================================================
# PRACTICAL EXAMPLE: COMPLETE SYSTEM
# ============================================================================

print("\n" + "="*60)
print("PRACTICAL EXAMPLE: USER MANAGEMENT SYSTEM")
print("="*60)

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class User:
    """User class with roles and permissions."""
    
    _user_count = 0
    
    def __init__(self, username, email, role=Role.USER):
        self.username = username
        self.email = email
        self.role = role
        self._active = True
        User._user_count += 1
        self.user_id = User._user_count
    
    def deactivate(self):
        self._active = False
        return f"User {self.username} deactivated"
    
    def has_permission(self, permission):
        permissions = {
            Role.ADMIN: ['read', 'write', 'delete', 'manage_users'],
            Role.MODERATOR: ['read', 'write', 'delete'],
            Role.USER: ['read', 'write']
        }
        return permission in permissions.get(self.role, [])
    
    def __str__(self):
        return f"User({self.user_id}, {self.username}, {self.role.value})"

class UserManager:
    """Manages users in the system."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
    
    def add_user(self, user):
        self.users[user.username] = user
        return f"Added user: {user}"
    
    def remove_user(self, username):
        if username in self.users:
            del self.users[username]
            return f"Removed user: {username}"
        return f"User not found: {username}"
    
    def get_user(self, username):
        return self.users.get(username)
    
    def list_users_by_role(self, role):
        return [user for user in self.users.values() if user.role == role]

print("\nUser management system:")
manager = UserManager()

# Create users
user1 = User("alice", "alice@example.com", Role.ADMIN)
user2 = User("bob", "bob@example.com", Role.USER)
user3 = User("carol", "carol@example.com", Role.MODERATOR)

manager.add_user(user1)
manager.add_user(user2)
manager.add_user(user3)

print(f"\nAll users:")
for username, user in manager.users.items():
    print(f"  {user}")

print(f"\nPermissions:")
print(f"  alice can delete? {user1.has_permission('delete')}")
print(f"  bob can delete? {user2.has_permission('delete')}")
print(f"  carol can manage_users? {user3.has_permission('manage_users')}")

print(f"\nAdmins:")
admins = manager.list_users_by_role(Role.ADMIN)
for admin in admins:
    print(f"  {admin}")


print("\n" + "="*60)
print("DEMONSTRATION COMPLETE")
print("="*60 + "\n")
