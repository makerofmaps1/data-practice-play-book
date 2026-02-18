"""
Pandas Time Series Operations Demonstration

This script demonstrates time series operations including resampling, rolling windows,
date operations, and confidence interval calculations.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


print("\n" + "=" * 60)
print("PANDAS TIME SERIES OPERATIONS")
print("=" * 60)


# ============================================================
# SAMPLE TIME SERIES DATA
# ============================================================

print("\n" + "=" * 60)
print("SAMPLE TIME SERIES DATA")
print("=" * 60)

# Create daily sales data
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
sales = 1000 + np.cumsum(np.random.randn(len(dates)) * 50)  # Random walk
temperature = 20 + 15 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365) + np.random.randn(len(dates)) * 3

df = pd.DataFrame({
    "date": dates,
    "sales": sales,
    "temperature": temperature,
})

df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

print("Daily data (first 10 rows):")
print(df.head(10))


# ============================================================
# DATE/TIME OPERATIONS
# ============================================================

print("\n" + "=" * 60)
print("DATE/TIME OPERATIONS")
print("=" * 60)

# Extract date components
df["year"] = df.index.year
df["month"] = df.index.month
df["day"] = df.index.day
df["day_of_week"] = df.index.dayofweek
df["day_name"] = df.index.day_name()
df["week_of_year"] = df.index.isocalendar().week
df["quarter"] = df.index.quarter

print("\nDate components:")
print(df[["year", "month", "day", "day_of_week", "day_name", "week_of_year", "quarter"]].head(10))

# Filter by date range
jan_data = df.loc["2024-01"]
print("\nJanuary data:")
print(jan_data.head())

q1_data = df.loc["2024-01":"2024-03"]
print(f"\nQ1 data: {len(q1_data)} rows")

# Boolean date filtering
summer_data = df[(df["month"] >= 6) & (df["month"] <= 8)]
print(f"\nSummer data (Jun-Aug): {len(summer_data)} rows")

weekdays = df[df["day_of_week"] < 5]
print(f"\nWeekday data: {len(weekdays)} rows")


# ============================================================
# RESAMPLING (CHANGE FREQUENCY)
# ============================================================

print("\n" + "=" * 60)
print("RESAMPLING")
print("=" * 60)

# Downsample: Daily to Weekly (sum)
weekly_sales = df["sales"].resample("W").sum()
print("\nWeekly sales (sum):")
print(weekly_sales.head(10))

# Downsample: Daily to Monthly (mean)
monthly_avg = df.resample("M").mean()
print("\nMonthly averages:")
print(monthly_avg.head())

# Downsample with multiple aggregations
monthly_agg = df.resample("M").agg({
    "sales": ["sum", "mean", "min", "max"],
    "temperature": "mean"
})
print("\nMonthly aggregations:")
print(monthly_agg.head())

# Upsample: Daily to Hourly (forward fill)
hourly_sample = df.loc["2024-01-01":"2024-01-03"].resample("H").ffill()
print("\nUpsampled to hourly (first 24 hours):")
print(hourly_sample.head(24))


# ============================================================
# ROLLING WINDOWS
# ============================================================

print("\n" + "=" * 60)
print("ROLLING WINDOWS")
print("=" * 60)

# Simple rolling average
df["sales_7day_avg"] = df["sales"].rolling(window=7).mean()
df["sales_30day_avg"] = df["sales"].rolling(window=30).mean()

print("\nRolling averages:")
print(df[["sales", "sales_7day_avg", "sales_30day_avg"]].tail(10))

# Rolling with multiple aggregations
rolling_stats = df["sales"].rolling(window=7).agg(["mean", "std", "min", "max"])
print("\n7-day rolling statistics:")
print(rolling_stats.tail(10))

# Rolling sum
df["sales_7day_sum"] = df["sales"].rolling(window=7).sum()
print("\n7-day rolling sum:")
print(df[["sales", "sales_7day_sum"]].tail(5))

# Centered rolling window
df["sales_7day_centered"] = df["sales"].rolling(window=7, center=True).mean()
print("\nCentered vs standard rolling average:")
print(df[["sales", "sales_7day_avg", "sales_7day_centered"]].iloc[3:10])


# ============================================================
# ROLLING AVERAGE WITH CONFIDENCE INTERVALS
# ============================================================

print("\n" + "=" * 60)
print("ROLLING AVERAGE WITH 90% CONFIDENCE INTERVALS")
print("=" * 60)

# Calculate rolling mean and std
window = 30
df["rolling_mean"] = df["sales"].rolling(window=window).mean()
df["rolling_std"] = df["sales"].rolling(window=window).std()

# Calculate 90% confidence intervals (z-score = 1.645 for one-tailed 90%)
z_score = stats.norm.ppf(0.95)  # 90% CI = ±1.645 standard errors
df["rolling_std_error"] = df["rolling_std"] / np.sqrt(window)
df["ci_lower_90"] = df["rolling_mean"] - z_score * df["rolling_std_error"]
df["ci_upper_90"] = df["rolling_mean"] + z_score * df["rolling_std_error"]

print(f"\n30-day rolling average with 90% confidence intervals:")
print(df[["sales", "rolling_mean", "ci_lower_90", "ci_upper_90"]].tail(15))

# Check how many actual values fall within CI
within_ci = df["sales"].between(df["ci_lower_90"], df["ci_upper_90"])
print(f"\nPercentage of values within 90% CI: {within_ci.mean() * 100:.1f}%")


# ============================================================
# EXPANDING WINDOWS (CUMULATIVE)
# ============================================================

print("\n" + "=" * 60)
print("EXPANDING WINDOWS (CUMULATIVE)")
print("=" * 60)

# Cumulative statistics from start of time series
df["cumulative_mean"] = df["sales"].expanding().mean()
df["cumulative_std"] = df["sales"].expanding().std()
df["cumulative_max"] = df["sales"].expanding().max()

print("\nExpanding (cumulative) statistics:")
print(df[["sales", "cumulative_mean", "cumulative_std", "cumulative_max"]].iloc[::30])


# ============================================================
# EXPONENTIALLY WEIGHTED MOVING AVERAGE (EWMA)
# ============================================================

print("\n" + "=" * 60)
print("EXPONENTIALLY WEIGHTED MOVING AVERAGE")
print("=" * 60)

# EWMA gives more weight to recent observations
df["ewma_7"] = df["sales"].ewm(span=7).mean()
df["ewma_30"] = df["sales"].ewm(span=30).mean()

print("\nEWMA vs simple moving average:")
print(df[["sales", "sales_7day_avg", "ewma_7", "sales_30day_avg", "ewma_30"]].tail(10))


# ============================================================
# SHIFTING AND LAGGING
# ============================================================

print("\n" + "=" * 60)
print("SHIFTING AND LAGGING")
print("=" * 60)

# Lag (shift forward)
df["sales_lag_1"] = df["sales"].shift(1)
df["sales_lag_7"] = df["sales"].shift(7)

# Lead (shift backward)
df["sales_lead_1"] = df["sales"].shift(-1)

print("\nShifted values:")
print(df[["sales", "sales_lag_1", "sales_lag_7", "sales_lead_1"]].iloc[7:12])

# Calculate day-over-day change
df["sales_change"] = df["sales"] - df["sales_lag_1"]
df["sales_pct_change"] = df["sales"].pct_change() * 100

print("\nDay-over-day changes:")
print(df[["sales", "sales_change", "sales_pct_change"]].tail(10))


# ============================================================
# DATETIME ARITHMETIC
# ============================================================

print("\n" + "=" * 60)
print("DATETIME ARITHMETIC")
print("=" * 60)

# Create events dataframe
events = pd.DataFrame({
    "event": ["Launch", "Promo", "Holiday"],
    "event_date": pd.to_datetime(["2024-03-15", "2024-06-20", "2024-12-25"]),
})

print("\nEvents:")
print(events)

# Calculate days until next event
reference_date = pd.Timestamp("2024-01-01")
events["days_from_ref"] = (events["event_date"] - reference_date).dt.days
print("\nDays from reference date:")
print(events)

# Add business days
start = pd.Timestamp("2024-01-01")
future = start + pd.Timedelta(days=10)
business_days_ahead = start + pd.offsets.BDay(10)

print(f"\nStart date: {start.date()}")
print(f"10 calendar days ahead: {future.date()}")
print(f"10 business days ahead: {business_days_ahead.date()}")


# ============================================================
# TIME-BASED GROUPING
# ============================================================

print("\n" + "=" * 60)
print("TIME-BASED GROUPING")
print("=" * 60)

# Group by month
monthly_sales = df.groupby(df.index.to_period("M"))["sales"].agg(["sum", "mean", "count"])
print("\nMonthly sales summary:")
print(monthly_sales)

# Group by day of week
dow_sales = df.groupby("day_name")["sales"].mean()
print("\nAverage sales by day of week:")
print(dow_sales)

# Group by quarter
quarterly = df.groupby("quarter")["sales"].agg(["sum", "mean"])
print("\nQuarterly sales:")
print(quarterly)


# ============================================================
# SEASONALITY DETECTION
# ============================================================

print("\n" + "=" * 60)
print("SEASONALITY DETECTION")
print("=" * 60)

# Compare same month across time
jan_sales = df[df["month"] == 1]["sales"].mean()
jul_sales = df[df["month"] == 7]["sales"].mean()

print(f"\nAverage sales in January: {jan_sales:.2f}")
print(f"Average sales in July: {jul_sales:.2f}")
print(f"Difference: {jul_sales - jan_sales:.2f}")

# Month-over-month comparison
monthly_comparison = df.groupby("month")["temperature"].mean()
print("\nAverage temperature by month:")
print(monthly_comparison)


print("\n" + "=" * 60)
print("END OF TIME SERIES DEMO")
print("=" * 60)
