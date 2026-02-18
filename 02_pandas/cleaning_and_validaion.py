"""
Pandas Cleaning and Validation Demonstration

This script demonstrates common data-cleaning steps, with special focus on
handling multiple null representations and robust datetime parsing.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


print("\n" + "=" * 60)
print("PANDAS CLEANING AND VALIDATION")
print("=" * 60)


# ============================================================
# RAW DATA WITH MIXED NULLS AND MESSY DATES
# ============================================================

print("\n" + "=" * 60)
print("RAW DATA")
print("=" * 60)

raw_data = {
	"user_id": ["001", "002", "003", "004", None, "006", "007"],
	"name": ["Ava", "nan", "Liam", "NULL", "", "Noah", None],
	"age": [25, "N/A", 31, None, "", "27", "NaN"],
	"join_date": [
		"2024-01-05",
		"01/07/2024",
		"2024-02-30",  # invalid date
		"2024-03-15 14:30",
		"March 22, 2024",
		"",
		None,
	],
	"last_active": [
		"2024-04-01T09:15:00Z",
		"2024-04-02 10:05",
		"04-03-2024",
		"2024/04/04",
		"2024-13-01",  # invalid month
		"nan",
		"NULL",
	],
	"score": [88, 92, "nan", 85, None, "", "NULL"],
}

df_raw = pd.DataFrame(raw_data)
print(df_raw)


# ============================================================
# STANDARDIZE NULL REPRESENTATIONS
# ============================================================

print("\n" + "=" * 60)
print("STANDARDIZE NULLS")
print("=" * 60)

null_like = [
	"",
	" ",
	"NA",
	"N/A",
	"na",
	"n/a",
	"NULL",
	"null",
	"NaN",
	"nan",
	"None",
]

df_clean = df_raw.replace(null_like, np.nan)
print(df_clean)

print("\nNull counts:")
print(df_clean.isna().sum())


# ============================================================
# TYPE CONVERSION AND VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("TYPE CONVERSION")
print("=" * 60)

# Convert age and score to numeric
df_clean["age"] = pd.to_numeric(df_clean["age"], errors="coerce")
df_clean["score"] = pd.to_numeric(df_clean["score"], errors="coerce")

print(df_clean[["age", "score"]])

print("\nData types:")
print(df_clean.dtypes)


# ============================================================
# ROBUST DATETIME PARSING
# ============================================================

print("\n" + "=" * 60)
print("DATETIME PARSING")
print("=" * 60)

# Parse join_date with multiple formats and coerce invalids to NaT
df_clean["join_date"] = pd.to_datetime(
	df_clean["join_date"],
	errors="coerce",
)

# Parse last_active with timezone handling
df_clean["last_active"] = pd.to_datetime(
	df_clean["last_active"],
	errors="coerce",
	utc=True,
)

print(df_clean[["join_date", "last_active"]])
print("\nDatetime dtypes:")
print(df_clean[["join_date", "last_active"]].dtypes)


# ============================================================
# NORMALIZE DATETIME OUTPUTS
# ============================================================

print("\n" + "=" * 60)
print("DATETIME NORMALIZATION")
print("=" * 60)

# Convert to date only
df_clean["join_date_date"] = df_clean["join_date"].dt.date

# Convert to local timezone (example: US/Eastern) then strip tz info
df_clean["last_active_local"] = (
	df_clean["last_active"].dt.tz_convert("US/Eastern").dt.tz_localize(None)
)

print(df_clean[["join_date_date", "last_active_local"]])


# ============================================================
# DATA QUALITY CHECKS
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY CHECKS")
print("=" * 60)

# Required fields: user_id and name
missing_required = df_clean[df_clean[["user_id", "name"]].isna().any(axis=1)]
print("\nRows missing required fields:")
print(missing_required)

# Valid ranges for age and score
invalid_age = df_clean[(df_clean["age"] < 0) | (df_clean["age"] > 120)]
invalid_score = df_clean[(df_clean["score"] < 0) | (df_clean["score"] > 100)]

print("\nInvalid age rows:")
print(invalid_age)
print("\nInvalid score rows:")
print(invalid_score)

# Duplicate check
duplicates = df_clean[df_clean.duplicated(subset=["user_id"], keep=False)]
print("\nDuplicate user_id rows:")
print(duplicates)


# ============================================================
# CLEANING STRATEGIES
# ============================================================

print("\n" + "=" * 60)
print("CLEANING STRATEGIES")
print("=" * 60)

# Drop rows missing required fields
df_required = df_clean.dropna(subset=["user_id", "name"])

# Fill missing numeric values with median
df_required["age"] = df_required["age"].fillna(df_required["age"].median())
df_required["score"] = df_required["score"].fillna(df_required["score"].median())

# Fill missing join_date with a placeholder date
df_required["join_date"] = df_required["join_date"].fillna(pd.Timestamp("2024-01-01"))

print(df_required)


# ============================================================
# CUSTOM ROW-WISE FUNCTIONS WITH LAMBDA
# ============================================================

print("\n" + "=" * 60)
print("CUSTOM ROW-WISE FUNCTIONS")
print("=" * 60)

# Apply lambda to create derived column
df_required["score_category"] = df_required["score"].apply(
    lambda x: "High" if x >= 90 else ("Medium" if x >= 80 else "Low")
)

print("\nScore categories:")
print(df_required[["name", "score", "score_category"]])

# Apply lambda row-wise across multiple columns
df_required["user_status"] = df_required.apply(
    lambda row: "Active" if pd.notna(row["last_active"]) and row["score"] > 85 else "Inactive",
    axis=1,
)

print("\nUser status (based on last_active and score):")
print(df_required[["name", "score", "last_active", "user_status"]])

# Clean name field with lambda
df_required["name_clean"] = df_required["name"].apply(
    lambda x: x.strip().title() if isinstance(x, str) else x
)

print("\nCleaned names:")
print(df_required[["name", "name_clean"]])

# Create age_group using lambda with apply
df_required["age_group"] = df_required["age"].apply(
    lambda x: "18-25" if x <= 25 else ("26-35" if x <= 35 else "36+")
)

print("\nAge groups:")
print(df_required[["name", "age", "age_group"]])

# Using declared function with apply
def calculate_engagement_score(row):
    """Complex logic using multiple columns."""
    score = 0
    
    # Points for score
    if row["score"] >= 90:
        score += 50
    elif row["score"] >= 80:
        score += 30
    else:
        score += 10
    
    # Points for recent activity
    if pd.notna(row["last_active"]):
        score += 30
    
    # Bonus for young users
    if row["age"] < 30:
        score += 20
    
    return score

df_required["engagement_score"] = df_required.apply(calculate_engagement_score, axis=1)

print("\nEngagement scores (using declared function):")
print(df_required[["name", "score", "age", "engagement_score"]])


# ============================================================
# FINAL VALIDATION SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL VALIDATION SUMMARY")
print("=" * 60)

print("Null counts after cleaning:")
print(df_required.isna().sum())

print("\nData types after cleaning:")
print(df_required.dtypes)

print("\nSample data:")
print(df_required.head())


print("\n" + "=" * 60)
print("END OF CLEANING AND VALIDATION DEMO")
print("=" * 60)
