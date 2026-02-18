"""
Real-World Pandas Pipeline: E-Commerce Sales Analysis

This pipeline demonstrates a complete data analysis workflow incorporating:
- Multi-source data ingestion (CSV, JSON, SQL)
- Data cleaning and validation
- Type conversion and null handling
- Transformations (merge, groupby, pivot)
- Time series analysis (rolling averages, resampling)
- Custom functions with lambda and apply
- Data export and reporting

Scenario: Analyze e-commerce sales data to identify trends, customer segments,
and product performance.
"""

from __future__ import annotations

import io
import json
import sqlite3
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


print("\n" + "=" * 60)
print("E-COMMERCE SALES ANALYSIS PIPELINE")
print("=" * 60)


# ============================================================
# STEP 1: DATA INGESTION FROM MULTIPLE SOURCES
# ============================================================

print("\n" + "=" * 60)
print("STEP 1: DATA INGESTION")
print("=" * 60)

# Source 1: Sales transactions (CSV with messy data)
sales_csv = """transaction_id,customer_id,product_id,order_date,quantity,unit_price,region
1001,C001,P101,2024-01-05,2,29.99,East
1002,C002,P102,01/07/2024,1,49.99,West
1003,C001,P103,2024-01-08,3,NULL,East
1004,C003,P101,2024-01-10 14:30,1,29.99,North
1005,C002,P104,,,59.99,West
1006,C004,P102,2024-01-15,2,nan,South
1007,C003,P105,2024-01-18,1,89.99,North
1008,C001,P103,2024-01-20,2,19.99,East
1009,,P101,2024-01-22,1,29.99,
1010,C005,P104,2024-01-25,3,59.99,West
1011,C004,P102,2024-02-01,1,49.99,South
1012,C002,P105,2024-02-05,2,89.99,West
1013,C003,P103,2024-02-08,4,19.99,North
1014,C001,P101,2024-02-12,1,29.99,East
1015,C005,P104,2024-02-15,2,59.99,West
"""

df_sales_raw = pd.read_csv(io.StringIO(sales_csv))
print("Sales data (raw):")
print(df_sales_raw.head())
print(f"Shape: {df_sales_raw.shape}")

# Source 2: Customer data (JSON)
customers_json = """
[
    {"customer_id": "C001", "name": "Alice Johnson", "segment": "Premium", "join_date": "2023-05-12", "email": "alice@email.com"},
    {"customer_id": "C002", "name": "Bob Smith", "segment": "Standard", "join_date": "2023-08-20", "email": "bob@email.com"},
    {"customer_id": "C003", "name": "Charlie Brown", "segment": "Premium", "join_date": "2023-06-30", "email": "charlie@email.com"},
    {"customer_id": "C004", "name": "Diana Prince", "segment": "Standard", "join_date": "2023-11-15", "email": "diana@email.com"},
    {"customer_id": "C005", "name": "Eve Davis", "segment": "Premium", "join_date": "2023-09-08", "email": "eve@email.com"}
]
"""

df_customers_raw = pd.read_json(io.StringIO(customers_json))
print("\nCustomer data (raw):")
print(df_customers_raw)

# Source 3: Product data (SQL database)
product_data = {
    "product_id": ["P101", "P102", "P103", "P104", "P105"],
    "product_name": ["Widget A", "Gadget B", "Tool C", "Device D", "Equipment E"],
    "category": ["Electronics", "Electronics", "Hardware", "Electronics", "Hardware"],
    "cost": [15.00, 25.00, 10.00, 30.00, 45.00],
}

# Create temporary SQLite database
with sqlite3.connect(":memory:") as conn:
    df_products_temp = pd.DataFrame(product_data)
    df_products_temp.to_sql("products", conn, index=False, if_exists="replace")
    df_products_raw = pd.read_sql_query("SELECT * FROM products", conn)

print("\nProduct data (from SQL):")
print(df_products_raw)


# ============================================================
# STEP 2: DATA CLEANING AND VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2: DATA CLEANING AND VALIDATION")
print("=" * 60)

# Clean sales data
df_sales = df_sales_raw.copy()

# Standardize nulls
null_values = ["", " ", "NULL", "null", "nan", "NaN", "None"]
df_sales = df_sales.replace(null_values, np.nan)

print("\nNull counts before cleaning:")
print(df_sales.isna().sum())

# Type conversions
df_sales["quantity"] = pd.to_numeric(df_sales["quantity"], errors="coerce")
df_sales["unit_price"] = pd.to_numeric(df_sales["unit_price"], errors="coerce")
df_sales["order_date"] = pd.to_datetime(df_sales["order_date"], errors="coerce")

# Clean customer data
df_customers = df_customers_raw.copy()
df_customers["join_date"] = pd.to_datetime(df_customers["join_date"])

# Data quality checks
print("\nData Quality Issues:")
missing_customers = df_sales[df_sales["customer_id"].isna()]
print(f"  Transactions missing customer_id: {len(missing_customers)}")

missing_dates = df_sales[df_sales["order_date"].isna()]
print(f"  Transactions missing order_date: {len(missing_dates)}")

missing_prices = df_sales[df_sales["unit_price"].isna()]
print(f"  Transactions missing unit_price: {len(missing_prices)}")

# Imputation strategy
# Fill missing prices with product median from other transactions
for product_id in df_sales["product_id"].unique():
    product_median = df_sales[df_sales["product_id"] == product_id]["unit_price"].median()
    df_sales.loc[
        (df_sales["product_id"] == product_id) & (df_sales["unit_price"].isna()),
        "unit_price"
    ] = product_median

# Drop rows with missing critical fields
df_sales_clean = df_sales.dropna(subset=["customer_id", "order_date", "quantity"])

print(f"\nRows after cleaning: {len(df_sales_raw)} → {len(df_sales_clean)}")


# ============================================================
# STEP 3: DATA ENRICHMENT AND TRANSFORMATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 3: DATA ENRICHMENT")
print("=" * 60)

# Calculate total amount
df_sales_clean["total_amount"] = df_sales_clean["quantity"] * df_sales_clean["unit_price"]

# Merge with customer data
df_enriched = df_sales_clean.merge(
    df_customers,
    on="customer_id",
    how="left"
)

# Merge with product data
df_enriched = df_enriched.merge(
    df_products_raw,
    on="product_id",
    how="left"
)

# Calculate profit margin
df_enriched["profit_margin"] = df_enriched["total_amount"] - (df_enriched["quantity"] * df_enriched["cost"])

# Add date components
df_enriched["year"] = df_enriched["order_date"].dt.year
df_enriched["month"] = df_enriched["order_date"].dt.month
df_enriched["week"] = df_enriched["order_date"].dt.isocalendar().week
df_enriched["day_of_week"] = df_enriched["order_date"].dt.day_name()

print("Enriched data sample:")
print(df_enriched[["transaction_id", "name", "product_name", "total_amount", "profit_margin"]].head())


# ============================================================
# STEP 4: CUSTOM FUNCTIONS AND LAMBDA
# ============================================================

print("\n" + "=" * 60)
print("STEP 4: CUSTOM FUNCTIONS")
print("=" * 60)

# Apply lambda for customer value tier
df_enriched["value_tier"] = df_enriched["total_amount"].apply(
    lambda x: "High" if x >= 100 else ("Medium" if x >= 50 else "Low")
)

# Custom function for order complexity
def calculate_order_complexity(row):
    """Complex scoring based on multiple factors."""
    score = 0
    
    # Quantity factor
    score += row["quantity"] * 10
    
    # Premium customer bonus
    if row["segment"] == "Premium":
        score += 20
    
    # Category factor
    if row["category"] == "Electronics":
        score += 15
    
    return score

df_enriched["complexity_score"] = df_enriched.apply(calculate_order_complexity, axis=1)

print("\nCustomer value tiers:")
print(df_enriched[["transaction_id", "total_amount", "value_tier"]].head(10))


# ============================================================
# STEP 5: AGGREGATIONS AND GROUPBY
# ============================================================

print("\n" + "=" * 60)
print("STEP 5: AGGREGATIONS")
print("=" * 60)

# Customer-level aggregation
customer_summary = df_enriched.groupby("customer_id").agg(
    customer_name=("name", "first"),
    segment=("segment", "first"),
    total_orders=("transaction_id", "count"),
    total_spent=("total_amount", "sum"),
    avg_order_value=("total_amount", "mean"),
    total_items=("quantity", "sum"),
).reset_index()

print("Customer summary:")
print(customer_summary)

# Product performance
product_summary = df_enriched.groupby("product_id").agg(
    product_name=("product_name", "first"),
    category=("category", "first"),
    units_sold=("quantity", "sum"),
    revenue=("total_amount", "sum"),
    profit=("profit_margin", "sum"),
    avg_price=("unit_price", "mean"),
).reset_index()

product_summary["profit_margin_pct"] = (
    product_summary["profit"] / product_summary["revenue"] * 100
)

print("\nProduct performance:")
print(product_summary)

# Region analysis
region_summary = df_enriched.groupby("region").agg(
    orders=("transaction_id", "count"),
    revenue=("total_amount", "sum"),
    avg_order_value=("total_amount", "mean"),
).reset_index()

print("\nRegion performance:")
print(region_summary)


# ============================================================
# STEP 6: TIME SERIES ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 6: TIME SERIES ANALYSIS")
print("=" * 60)

# Set date as index for time series operations
df_ts = df_enriched.set_index("order_date").sort_index()

# Daily sales
daily_sales = df_ts.resample("D")["total_amount"].sum().fillna(0)
print("\nDaily sales (first 10 days):")
print(daily_sales.head(10))

# Weekly aggregation
weekly_sales = df_ts.resample("W").agg({
    "total_amount": "sum",
    "transaction_id": "count",
    "quantity": "sum",
})
weekly_sales.columns = ["revenue", "orders", "units"]

print("\nWeekly sales:")
print(weekly_sales)

# Rolling 7-day average
daily_sales_df = daily_sales.to_frame(name="daily_revenue")
daily_sales_df["rolling_7day_avg"] = daily_sales_df["daily_revenue"].rolling(window=7).mean()
daily_sales_df["rolling_7day_sum"] = daily_sales_df["daily_revenue"].rolling(window=7).sum()

print("\nRolling 7-day metrics:")
print(daily_sales_df.tail(10))

# Calculate rolling confidence intervals (90%)
window = 7
daily_sales_df["rolling_std"] = daily_sales_df["daily_revenue"].rolling(window=window).std()
daily_sales_df["rolling_std_error"] = daily_sales_df["rolling_std"] / np.sqrt(window)
z_score = stats.norm.ppf(0.95)
daily_sales_df["ci_lower_90"] = daily_sales_df["rolling_7day_avg"] - z_score * daily_sales_df["rolling_std_error"]
daily_sales_df["ci_upper_90"] = daily_sales_df["rolling_7day_avg"] + z_score * daily_sales_df["rolling_std_error"]

print("\nRolling average with 90% confidence intervals:")
print(daily_sales_df[["daily_revenue", "rolling_7day_avg", "ci_lower_90", "ci_upper_90"]].tail(10))


# ============================================================
# STEP 7: PIVOT TABLES AND CROSS-TABULATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 7: PIVOT ANALYSIS")
print("=" * 60)

# Category by region performance
category_region_pivot = df_enriched.pivot_table(
    values="total_amount",
    index="category",
    columns="region",
    aggfunc="sum",
    fill_value=0,
    margins=True,
)

print("\nRevenue by category and region:")
print(category_region_pivot)

# Customer segment by product category
segment_category = pd.crosstab(
    df_enriched["segment"],
    df_enriched["category"],
    values=df_enriched["total_amount"],
    aggfunc="sum",
    margins=True,
)

print("\nSegment × Category revenue:")
print(segment_category)


# ============================================================
# STEP 8: ADVANCED METRICS
# ============================================================

print("\n" + "=" * 60)
print("STEP 8: ADVANCED METRICS")
print("=" * 60)

# Customer lifetime value (total spend per customer)
customer_summary["customer_lifetime_value"] = customer_summary["total_spent"]

# Recency, Frequency, Monetary (RFM) Analysis
reference_date = df_enriched["order_date"].max()

rfm = df_enriched.groupby("customer_id").agg(
    recency=("order_date", lambda x: (reference_date - x.max()).days),
    frequency=("transaction_id", "count"),
    monetary=("total_amount", "sum"),
).reset_index()

# Score each dimension (1-5)
rfm["recency_score"] = pd.qcut(rfm["recency"], q=5, labels=[5, 4, 3, 2, 1], duplicates="drop")
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")
rfm["monetary_score"] = pd.qcut(rfm["monetary"], q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")

rfm["rfm_score"] = (
    rfm["recency_score"].astype(int) +
    rfm["frequency_score"].astype(int) +
    rfm["monetary_score"].astype(int)
)

# Segment customers
rfm["customer_segment"] = rfm["rfm_score"].apply(
    lambda x: "Champions" if x >= 12 else ("Loyal" if x >= 9 else ("At Risk" if x >= 6 else "Lost"))
)

rfm_with_names = rfm.merge(df_customers[["customer_id", "name"]], on="customer_id")

print("\nRFM Analysis:")
print(rfm_with_names[["customer_id", "name", "recency", "frequency", "monetary", "rfm_score", "customer_segment"]])

# Product rank by revenue
product_summary["revenue_rank"] = product_summary["revenue"].rank(ascending=False)
print("\nProduct ranking by revenue:")
print(product_summary[["product_name", "revenue", "revenue_rank"]].sort_values("revenue_rank"))


# ============================================================
# STEP 9: REPORTING AND INSIGHTS
# ============================================================

print("\n" + "=" * 60)
print("STEP 9: KEY INSIGHTS")
print("=" * 60)

total_revenue = df_enriched["total_amount"].sum()
total_profit = df_enriched["profit_margin"].sum()
total_orders = len(df_enriched)
total_customers = df_enriched["customer_id"].nunique()
avg_order_value = df_enriched["total_amount"].mean()

print(f"\nBusiness Metrics:")
print(f"  Total Revenue: ${total_revenue:,.2f}")
print(f"  Total Profit: ${total_profit:,.2f}")
print(f"  Profit Margin: {(total_profit / total_revenue * 100):.1f}%")
print(f"  Total Orders: {total_orders}")
print(f"  Total Customers: {total_customers}")
print(f"  Average Order Value: ${avg_order_value:.2f}")

print(f"\nTop Customer:")
top_customer = customer_summary.nlargest(1, "total_spent").iloc[0]
print(f"  {top_customer['customer_name']} ({top_customer['segment']})")
print(f"  Total Spent: ${top_customer['total_spent']:.2f}")
print(f"  Orders: {top_customer['total_orders']}")

print(f"\nTop Product:")
top_product = product_summary.nlargest(1, "revenue").iloc[0]
print(f"  {top_product['product_name']} ({top_product['category']})")
print(f"  Revenue: ${top_product['revenue']:.2f}")
print(f"  Units Sold: {top_product['units_sold']}")

print(f"\nBest Region:")
best_region = region_summary.nlargest(1, "revenue").iloc[0]
print(f"  {best_region['region']}")
print(f"  Revenue: ${best_region['revenue']:.2f}")
print(f"  Orders: {best_region['orders']}")


# ============================================================
# STEP 10: EXPORT RESULTS
# ============================================================

print("\n" + "=" * 60)
print("STEP 10: EXPORT RESULTS")
print("=" * 60)

with tempfile.TemporaryDirectory() as tmp_dir:
    tmp_path = Path(tmp_dir)
    
    # Export to CSV
    customer_summary.to_csv(tmp_path / "customer_summary.csv", index=False)
    product_summary.to_csv(tmp_path / "product_summary.csv", index=False)
    rfm_with_names.to_csv(tmp_path / "rfm_analysis.csv", index=False)
    
    # Export to JSON
    insights = {
        "total_revenue": float(total_revenue),
        "total_profit": float(total_profit),
        "total_orders": int(total_orders),
        "top_customer": top_customer['customer_name'],
        "top_product": top_product['product_name'],
    }
    
    (tmp_path / "insights.json").write_text(json.dumps(insights, indent=2))
    
    # Export pivot to Excel (if openpyxl available)
    try:
        with pd.ExcelWriter(tmp_path / "sales_analysis.xlsx") as writer:
            customer_summary.to_excel(writer, sheet_name="Customers", index=False)
            product_summary.to_excel(writer, sheet_name="Products", index=False)
            category_region_pivot.to_excel(writer, sheet_name="Category_Region")
            rfm_with_names.to_excel(writer, sheet_name="RFM", index=False)
        print("✓ Exported to Excel: sales_analysis.xlsx")
    except Exception as e:
        print(f"  Excel export skipped: {e}")
    
    print("✓ Exported to CSV: customer_summary.csv")
    print("✓ Exported to CSV: product_summary.csv")
    print("✓ Exported to CSV: rfm_analysis.csv")
    print("✓ Exported to JSON: insights.json")


print("\n" + "=" * 60)
print("PIPELINE COMPLETE")
print("=" * 60)
print("\nThis pipeline demonstrated:")
print("  ✓ Multi-source data ingestion (CSV, JSON, SQL)")
print("  ✓ Data cleaning and validation")
print("  ✓ Null handling and type conversion")
print("  ✓ Data enrichment with merges")
print("  ✓ Custom functions with lambda and apply")
print("  ✓ GroupBy aggregations")
print("  ✓ Time series analysis with rolling windows")
print("  ✓ Pivot tables and cross-tabulation")
print("  ✓ RFM customer segmentation")
print("  ✓ Multi-format data export")
