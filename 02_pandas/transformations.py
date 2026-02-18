"""
Pandas Transformations Demonstration

This script demonstrates common data transformation operations including
groupby, merge, pivot, and reshape operations.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


print("\n" + "=" * 60)
print("PANDAS TRANSFORMATIONS")
print("=" * 60)


# ============================================================
# SAMPLE DATA
# ============================================================

print("\n" + "=" * 60)
print("SAMPLE DATA")
print("=" * 60)

# Sales data
sales = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "customer_id": [101, 102, 101, 103, 102, 101, 104, 103],
    "product": ["A", "B", "A", "C", "B", "C", "A", "B"],
    "region": ["East", "West", "East", "North", "West", "East", "South", "North"],
    "amount": [250, 300, 150, 400, 350, 200, 275, 425],
    "quantity": [5, 3, 2, 8, 4, 3, 5, 6],
})

print("Sales data:")
print(sales)

# Customer data
customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 104, 105],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "segment": ["Premium", "Standard", "Premium", "Standard", "Premium"],
})

print("\nCustomer data:")
print(customers)


# ============================================================
# GROUPBY OPERATIONS
# ============================================================

print("\n" + "=" * 60)
print("GROUPBY OPERATIONS")
print("=" * 60)

# Simple aggregation
grouped_region = sales.groupby("region")["amount"].sum()
print("\nTotal amount by region:")
print(grouped_region)

# Multiple aggregations
grouped_multi = sales.groupby("product").agg({
    "amount": ["sum", "mean", "count"],
    "quantity": "sum"
})
print("\nMultiple aggregations by product:")
print(grouped_multi)

# Named aggregations (cleaner column names)
grouped_named = sales.groupby("region").agg(
    total_amount=("amount", "sum"),
    avg_amount=("amount", "mean"),
    order_count=("order_id", "count"),
    total_quantity=("quantity", "sum"),
)
print("\nNamed aggregations by region:")
print(grouped_named)

# GroupBy with multiple columns
grouped_multi_cols = sales.groupby(["region", "product"])["amount"].sum()
print("\nAmount by region and product:")
print(grouped_multi_cols)

# Transform (broadcast aggregated values back to original shape)
sales["region_total"] = sales.groupby("region")["amount"].transform("sum")
sales["region_avg"] = sales.groupby("region")["amount"].transform("mean")
print("\nSales with region totals and averages:")
print(sales[["order_id", "region", "amount", "region_total", "region_avg"]])

# Filter groups
high_volume_regions = sales.groupby("region").filter(lambda x: x["amount"].sum() > 500)
print("\nOrders from high-volume regions (total > 500):")
print(high_volume_regions)

# Apply custom function to groups
def top_order(group):
    return group.nlargest(1, "amount")

top_by_region = sales.groupby("region").apply(top_order)
print("\nTop order by region:")
print(top_by_region)


# ============================================================
# MERGE OPERATIONS (JOINS)
# ============================================================

print("\n" + "=" * 60)
print("MERGE OPERATIONS")
print("=" * 60)

# Inner join (default)
merged_inner = sales.merge(customers, on="customer_id", how="inner")
print("\nInner join (sales with customer info):")
print(merged_inner[["order_id", "customer_id", "name", "product", "amount"]])

# Left join (keep all sales)
merged_left = sales.merge(customers, on="customer_id", how="left")
print("\nLeft join (all sales, with customer info where available):")
print(merged_left[["order_id", "customer_id", "name", "product", "amount"]])

# Right join (keep all customers)
merged_right = sales.merge(customers, on="customer_id", how="right")
print("\nRight join (all customers, with sales where available):")
print(merged_right[["customer_id", "name", "order_id", "amount"]])

# Outer join (keep everything)
merged_outer = sales.merge(customers, on="customer_id", how="outer")
print("\nOuter join (all sales and all customers):")
print(merged_outer[["order_id", "customer_id", "name", "amount"]])

# Merge with different column names
products = pd.DataFrame({
    "prod_code": ["A", "B", "C"],
    "prod_name": ["Widget", "Gadget", "Doohickey"],
    "cost": [50, 75, 100],
})

merged_diff_cols = sales.merge(
    products,
    left_on="product",
    right_on="prod_code",
    how="left"
)
print("\nMerge with different column names:")
print(merged_diff_cols[["order_id", "product", "prod_name", "amount", "cost"]])

# Merge with suffixes for overlapping columns
sales2 = pd.DataFrame({
    "order_id": [1, 2, 3],
    "amount": [260, 310, 160],  # updated amounts
    "status": ["shipped", "pending", "shipped"],
})

merged_suffix = sales.merge(
    sales2,
    on="order_id",
    how="left",
    suffixes=("_original", "_updated")
)
print("\nMerge with suffixes:")
print(merged_suffix[["order_id", "amount_original", "amount_updated", "status"]])


# ============================================================
# CONCATENATION
# ============================================================

print("\n" + "=" * 60)
print("CONCATENATION")
print("=" * 60)

# Vertical concatenation (stack rows)
sales_q1 = sales.iloc[:4]
sales_q2 = sales.iloc[4:]

sales_combined = pd.concat([sales_q1, sales_q2], ignore_index=True)
print("\nVertical concatenation (Q1 + Q2):")
print(sales_combined)

# Horizontal concatenation (add columns)
extra_info = pd.DataFrame({
    "discount": [0.1, 0.0, 0.15, 0.0, 0.05, 0.1, 0.0, 0.2],
    "shipping": [10, 15, 10, 20, 15, 10, 12, 18],
})

sales_with_extra = pd.concat([sales.reset_index(drop=True), extra_info], axis=1)
print("\nHorizontal concatenation (add columns):")
print(sales_with_extra[["order_id", "amount", "discount", "shipping"]])


# ============================================================
# PIVOT TABLES
# ============================================================

print("\n" + "=" * 60)
print("PIVOT TABLES")
print("=" * 60)

# Simple pivot
pivot_simple = sales.pivot_table(
    values="amount",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)
print("\nPivot: Amount by region and product:")
print(pivot_simple)

# Pivot with multiple aggregations
pivot_multi = sales.pivot_table(
    values="amount",
    index="region",
    columns="product",
    aggfunc=["sum", "mean"],
    fill_value=0
)
print("\nPivot with multiple aggregations:")
print(pivot_multi)

# Pivot with margins (totals)
pivot_margins = sales.pivot_table(
    values="amount",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="Total"
)
print("\nPivot with margins (totals):")
print(pivot_margins)


# ============================================================
# RESHAPE: MELT (WIDE TO LONG)
# ============================================================

print("\n" + "=" * 60)
print("MELT (WIDE TO LONG)")
print("=" * 60)

# Wide format data
wide_data = pd.DataFrame({
    "customer": ["Alice", "Bob", "Charlie"],
    "2023_sales": [1000, 1500, 1200],
    "2024_sales": [1200, 1800, 1300],
})

print("\nWide format:")
print(wide_data)

# Melt to long format
long_data = wide_data.melt(
    id_vars=["customer"],
    value_vars=["2023_sales", "2024_sales"],
    var_name="year",
    value_name="sales"
)

# Clean up year column
long_data["year"] = long_data["year"].str.replace("_sales", "")

print("\nLong format (melted):")
print(long_data)


# ============================================================
# RESHAPE: PIVOT (LONG TO WIDE)
# ============================================================

print("\n" + "=" * 60)
print("PIVOT (LONG TO WIDE)")
print("=" * 60)

# Convert back to wide
wide_again = long_data.pivot(
    index="customer",
    columns="year",
    values="sales"
)

print("\nWide format (pivoted back):")
print(wide_again)


# ============================================================
# STACK AND UNSTACK
# ============================================================

print("\n" + "=" * 60)
print("STACK AND UNSTACK")
print("=" * 60)

# Create multi-index data
multi_data = sales.groupby(["region", "product"])["amount"].sum()
print("\nMulti-index data:")
print(multi_data)

# Unstack (pivot innermost level to columns)
unstacked = multi_data.unstack(fill_value=0)
print("\nUnstacked (product as columns):")
print(unstacked)

# Stack (pivot columns to index)
stacked = unstacked.stack()
print("\nStacked back:")
print(stacked)


# ============================================================
# CROSSTAB
# ============================================================

print("\n" + "=" * 60)
print("CROSSTAB")
print("=" * 60)

# Frequency table
crosstab = pd.crosstab(sales["region"], sales["product"])
print("\nCrosstab (frequency of region x product):")
print(crosstab)

# Crosstab with values
crosstab_values = pd.crosstab(
    sales["region"],
    sales["product"],
    values=sales["amount"],
    aggfunc="sum",
    margins=True
)
print("\nCrosstab with values (sum of amount):")
print(crosstab_values)


# ============================================================
# ADVANCED TRANSFORMATIONS
# ============================================================

print("\n" + "=" * 60)
print("ADVANCED TRANSFORMATIONS")
print("=" * 60)

# Rank within groups
sales["rank_in_region"] = sales.groupby("region")["amount"].rank(
    ascending=False,
    method="dense"
)
print("\nRank within region:")
print(sales[["order_id", "region", "amount", "rank_in_region"]].sort_values(["region", "rank_in_region"]))

# Cumulative sum within groups
sales_sorted = sales.sort_values(["customer_id", "order_id"])
sales_sorted["cumulative_amount"] = sales_sorted.groupby("customer_id")["amount"].cumsum()
print("\nCumulative amount by customer:")
print(sales_sorted[["customer_id", "order_id", "amount", "cumulative_amount"]])

# Shift (lag/lead) within groups
sales_sorted["prev_amount"] = sales_sorted.groupby("customer_id")["amount"].shift(1)
sales_sorted["next_amount"] = sales_sorted.groupby("customer_id")["amount"].shift(-1)
print("\nShift (previous and next amounts):")
print(sales_sorted[["customer_id", "order_id", "prev_amount", "amount", "next_amount"]])


print("\n" + "=" * 60)
print("END OF TRANSFORMATIONS DEMO")
print("=" * 60)
