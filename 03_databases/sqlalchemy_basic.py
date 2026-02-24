"""
SQLAlchemy ORM Basics (Single Engine: SQLite)

This script demonstrates SQLAlchemy ORM with one local engine (SQLite)
and covers the same core operations as the raw SQL basics:
- Define ORM models
- Create tables
- Insert rows
- Query rows
- Update rows
- Delete rows

Requirements:
	pip install sqlalchemy
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Float, ForeignKey, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


print("\n" + "=" * 60)
print("SQLALCHEMY ORM BASICS")
print("=" * 60)


# ============================================================
# ORM MODELS
# ============================================================


class Base(DeclarativeBase):
	pass


class Product(Base):
	__tablename__ = "products"

	product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(200), nullable=False)
	category: Mapped[str] = mapped_column(String(100), nullable=False)
	price: Mapped[float] = mapped_column(Float, nullable=False)
	in_stock: Mapped[bool] = mapped_column(Boolean, default=True)

	sales: Mapped[list[Sale]] = relationship(back_populates="product")


class Sale(Base):
	__tablename__ = "sales"

	sale_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False)
	quantity: Mapped[int] = mapped_column(Integer, nullable=False)
	sale_date: Mapped[date] = mapped_column(Date, default=date.today)
	total_amount: Mapped[float] = mapped_column(Float, nullable=False)

	product: Mapped[Product] = relationship(back_populates="sales")


# ============================================================
# ENGINE + TABLE SETUP
# ============================================================

# In-memory SQLite keeps setup simple for teaching.
# Change to sqlite:///sqlalchemy_demo.db if you want persistence.
engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)

print("\nCreated ORM tables: products, sales")


# ============================================================
# INSERT (CREATE)
# ============================================================

print("\n" + "=" * 60)
print("INSERT (CREATE)")
print("=" * 60)

sample_products = [
	Product(name="Wireless Keyboard", category="Electronics", price=79.99, in_stock=True),
	Product(name="Standing Desk", category="Furniture", price=349.00, in_stock=True),
	Product(name="USB-C Hub", category="Electronics", price=49.99, in_stock=True),
	Product(name="Desk Lamp", category="Furniture", price=39.99, in_stock=False),
]

with Session(engine) as session:
	session.add_all(sample_products)
	session.commit()
	print(f"Inserted {len(sample_products)} products")


# ============================================================
# SELECT (READ)
# ============================================================

print("\n" + "=" * 60)
print("SELECT (READ)")
print("=" * 60)

with Session(engine) as session:
	all_products = session.scalars(select(Product).order_by(Product.product_id)).all()
	print("\nAll products:")
	for product in all_products:
		status = "in stock" if product.in_stock else "out of stock"
		print(f"  [{product.product_id}] {product.name:<20} ${product.price:.2f} ({status})")

	electronics = session.scalars(
		select(Product)
		.where(Product.category == "Electronics", Product.in_stock.is_(True))
		.order_by(Product.price.desc())
	).all()
	print(f"\nIn-stock Electronics ({len(electronics)} items):")
	for product in electronics:
		print(f"  {product.name:<20} ${product.price:.2f}")

	summary_stmt = (
		select(
			Product.category,
			func.count(Product.product_id),
			func.round(func.avg(Product.price), 2),
			func.min(Product.price),
			func.max(Product.price),
		)
		.group_by(Product.category)
		.order_by(Product.category)
	)

	print("\nCategory summary:")
	for category, count_value, avg_price, min_price, max_price in session.execute(summary_stmt):
		print(
			f"  {category:<12} count={count_value} avg=${avg_price} range=${min_price:.2f}–${max_price:.2f}"
		)


# ============================================================
# UPDATE
# ============================================================

print("\n" + "=" * 60)
print("UPDATE")
print("=" * 60)

with Session(engine) as session:
	electronics = session.scalars(select(Product).where(Product.category == "Electronics")).all()
	for product in electronics:
		product.price = round(product.price * 0.90, 2)

	session.commit()
	print(f"Applied 10% discount to Electronics ({len(electronics)} rows updated)")


# ============================================================
# DELETE
# ============================================================

print("\n" + "=" * 60)
print("DELETE")
print("=" * 60)

with Session(engine) as session:
	out_of_stock = session.scalars(select(Product).where(Product.in_stock.is_(False))).all()
	deleted_count = len(out_of_stock)
	for product in out_of_stock:
		session.delete(product)

	session.commit()
	print(f"Removed out-of-stock products ({deleted_count} rows deleted)")


# ============================================================
# RELATIONSHIP EXAMPLE (SALES)
# ============================================================

print("\n" + "=" * 60)
print("RELATIONSHIPS")
print("=" * 60)

with Session(engine) as session:
	keyboard = session.scalar(select(Product).where(Product.name == "Wireless Keyboard"))
	desk = session.scalar(select(Product).where(Product.name == "Standing Desk"))

	sales = [
		Sale(product_id=keyboard.product_id, quantity=2, total_amount=143.98),
		Sale(product_id=desk.product_id, quantity=1, total_amount=349.00),
	]
	session.add_all(sales)
	session.commit()

	sales_report = session.execute(
		select(Sale.sale_id, Product.name, Sale.quantity, Sale.total_amount, Sale.sale_date)
		.join(Sale.product)
		.order_by(Sale.sale_id)
	)

	print("Sales joined with products:")
	for sale_id, product_name, quantity, total_amount, sale_date in sales_report:
		print(f"  Sale {sale_id}: {product_name:<20} qty={quantity} amount=${total_amount:.2f} date={sale_date}")


# ============================================================
# ENGINE DIFFERENCES (IMPORTANT NOTES)
# ============================================================

print("\n" + "=" * 60)
print("IMPORTANT ENGINE DIFFERENCES")
print("=" * 60)

notes = """
This demo uses SQLite for simplicity. With other engines, the ORM code is mostly
the same, but the engine URL + installed driver changes:

1) PostgreSQL
   - URL: postgresql+psycopg2://user:password@host:5432/dbname
   - Driver: psycopg2-binary

2) MySQL / MariaDB
   - URL: mysql+mysqlconnector://user:password@host:3306/dbname
   - Driver: mysql-connector-python

3) Snowflake
   - SQLAlchemy support uses a separate dialect package (snowflake-sqlalchemy)
   - Connection URLs and type behavior are more warehouse-specific than OLTP databases

Practical rule:
- Keep ORM models database-agnostic where possible.
- Expect migrations/indexes and a few SQL types to be engine-specific in real projects.
"""

print(notes)

print("\n" + "=" * 60)
print("END OF SQLALCHEMY ORM BASICS")
print("=" * 60)

