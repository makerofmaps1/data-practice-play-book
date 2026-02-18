"""
Math and Statistics Demonstration

This module demonstrates mathematical operations, linear algebra, and statistical analysis.
This code requires numpy and scipy to be installed.

Key covers:
- Basic math operations and functions
- Statistical analysis (descriptive and inferential)
- NumPy arrays and operations
- Matrix algebra and linear transformations
- Hypothesis testing (t-tests)
- A/B testing frameworks
"""

import math
import statistics
import numpy as np
from scipy import stats


# ============================================================
# BASIC MATH OPERATIONS
# ============================================================

print("\n" + "="*60)
print("BASIC MATH OPERATIONS")
print("="*60)

# Math constants
print(f"Pi: {math.pi}")
print(f"Euler's number (e): {math.e}")
print(f"Tau (2*pi): {math.tau}")

# Trigonometric functions
angle = math.pi / 4  # 45 degrees in radians
print(f"\nTrigonometric functions for 45°:")
print(f"  sin(45°) = {math.sin(angle):.4f}")
print(f"  cos(45°) = {math.cos(angle):.4f}")
print(f"  tan(45°) = {math.tan(angle):.4f}")

# Inverse trigonometric functions
value = 0.707
print(f"\nInverse trigonometric functions for {value}:")
print(f"  asin({value}) = {math.asin(value):.4f} radians")
print(f"  acos({value}) = {math.acos(value):.4f} radians")
print(f"  atan({value}) = {math.atan(value):.4f} radians")

# Logarithmic and exponential
print(f"\nLogarithmic and exponential:")
print(f"  log(100) = {math.log10(100):.4f}")
print(f"  ln(2.718) = {math.log(math.e):.4f}")
print(f"  e^2 = {math.exp(2):.4f}")
print(f"  2^10 = {math.pow(2, 10)}")

# Rounding and ceiling/floor
value = 3.7
print(f"\nRounding {value}:")
print(f"  floor({value}) = {math.floor(value)}")
print(f"  ceil({value}) = {math.ceil(value)}")
print(f"  round({value}) = {round(value)}")

# GCD and LCM
print(f"\nGCD and LCM:")
print(f"  GCD(12, 18) = {math.gcd(12, 18)}")
print(f"  LCM(12, 18) = {(12 * 18) // math.gcd(12, 18)}")

# Factorial
print(f"  Factorial(5) = {math.factorial(5)}")

# Square root and power
print(f"  sqrt(16) = {math.sqrt(16)}")
print(f"  sqrt(2) = {math.sqrt(2):.4f}")


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "="*60)
print("DESCRIPTIVE STATISTICS")
print("="*60)

# Sample data: test scores
scores = [85, 92, 78, 95, 88, 91, 82, 79, 93, 87]
print(f"\nTest Scores: {scores}")

# Central tendency
mean_score = statistics.mean(scores)
median_score = statistics.median(scores)
mode_score = statistics.mode(scores)

print(f"\nCentral Tendency:")
print(f"  Mean: {mean_score:.2f}")
print(f"  Median: {median_score:.2f}")
print(f"  Mode: {mode_score} (no repeating values)" if mode_score == None else f"  Mode: {mode_score}")

# Dispersion
variance = statistics.variance(scores)
stdev = statistics.stdev(scores)
range_val = max(scores) - min(scores)

print(f"\nDispersion:")
print(f"  Variance: {variance:.2f}")
print(f"  Std Dev: {stdev:.2f}")
print(f"  Range: {range_val}")

# Quartiles using quantiles
sorted_scores = sorted(scores)
q1 = statistics.quantiles(scores, n=4)[0]
q2 = statistics.quantiles(scores, n=4)[1]
q3 = statistics.quantiles(scores, n=4)[2]

print(f"\nQuartiles:")
print(f"  Q1 (25th percentile): {q1:.2f}")
print(f"  Q2 (50th percentile): {q2:.2f}")
print(f"  Q3 (75th percentile): {q3:.2f}")
print(f"  IQR: {q3 - q1:.2f}")


# ============================================================
# NUMPY BASICS
# ============================================================

print("\n" + "="*60)
print("NUMPY BASICS")
print("="*60)

# Creating arrays
arr1d = np.array([1, 2, 3, 4, 5])
arr2d = np.array([[1, 2, 3], [4, 5, 6]])

print(f"\n1D array:\n{arr1d}")
print(f"\n2D array:\n{arr2d}")
print(f"Shape: {arr2d.shape}, Type: {arr2d.dtype}")

# Array creation functions
zeros = np.zeros((3, 3))
ones = np.ones((2, 4))
linspace = np.linspace(0, 10, 5)
arange = np.arange(0, 10, 2)
random = np.random.rand(3, 3)

print(f"\nZeros (3x3):\n{zeros}")
print(f"\nOnes (2x4):\n{ones}")
print(f"\nLinspace (0 to 10, 5 points): {linspace}")
print(f"\nArange (0 to 10, step 2): {arange}")
print(f"\nRandom (3x3):\n{random}")

# Array operations
arr = np.array([1, 2, 3, 4, 5])
print(f"\nArray operations on {arr}:")
print(f"  Sum: {np.sum(arr)}")
print(f"  Mean: {np.mean(arr):.2f}")
print(f"  Std: {np.std(arr):.2f}")
print(f"  Max: {np.max(arr)}")
print(f"  Min: {np.min(arr)}")
print(f"  Sort: {np.sort(arr)}")

# Element-wise operations
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(f"\nElement-wise operations:")
print(f"  {a} + {b} = {a + b}")
print(f"  {a} * {b} = {a * b}")
print(f"  {a} / {b} = {a / b}")
print(f"  {a} ** 2 = {a ** 2}")
print(f"  sin({a}) = {np.sin(a)}")

# Indexing and slicing
matrix = np.arange(1, 10).reshape(3, 3)
print(f"\nMatrix:\n{matrix}")
print(f"Element at [0,1]: {matrix[0, 1]}")
print(f"Row 1: {matrix[1, :]}")
print(f"Column 2: {matrix[:, 2]}")
print(f"Last 2 rows:\n{matrix[-2:, :]}")


# ============================================================
# MATRIX ALGEBRA
# ============================================================

print("\n" + "="*60)
print("MATRIX ALGEBRA")
print("="*60)

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"\nMatrices:")
print(f"A =\n{A}")
print(f"B =\n{B}")

# Matrix addition and subtraction
print(f"\nA + B =\n{A + B}")
print(f"A - B =\n{A - B}")

# Matrix multiplication
print(f"\nA @ B (dot product) =\n{A @ B}")
print(f"A * B (element-wise) =\n{A * B}")

# Matrix transpose and determinant
print(f"\nA^T (transpose) =\n{A.T}")
print(f"det(A) = {np.linalg.det(A):.2f}")
print(f"rank(A) = {np.linalg.matrix_rank(A)}")
print(f"trace(A) = {np.trace(A)}")

# Inverse and solving
A_inv = np.linalg.inv(A)
print(f"\nA^-1 (inverse) =\n{A_inv}")
print(f"A @ A^-1 =\n{(A @ A_inv).round()}")

# Solving linear system Ax = b
print(f"\nSolving Ax = b:")
b = np.array([3, 7])
x = np.linalg.solve(A, b)
print(f"  b = {b}")
print(f"  x = {x}")
print(f"  Verification A @ x = {A @ x}")

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"\nEigenvalues of A: {eigenvalues}")
print(f"Eigenvectors of A:\n{eigenvectors}")


# ============================================================
# VECTOR OPERATIONS
# ============================================================

print("\n" + "="*60)
print("VECTOR OPERATIONS")
print("="*60)

u = np.array([1, 2, 3])
v = np.array([4, 5, 6])

# Dot product
dot_product = np.dot(u, v)
print(f"\nDot product of {u} and {v}: {dot_product}")

# Cross product
cross_product = np.cross(u, v)
print(f"Cross product: {cross_product}")

# Norms
print(f"\nNorms:")
print(f"  L1 norm: {np.linalg.norm(u, ord=1)}")
print(f"  L2 norm (Euclidean): {np.linalg.norm(u, ord=2):.4f}")
print(f"  L∞ norm (max): {np.linalg.norm(u, ord=np.inf)}")

# Angle between vectors
magnitude_u = np.linalg.norm(u)
magnitude_v = np.linalg.norm(v)
cos_angle = dot_product / (magnitude_u * magnitude_v)
angle_rad = np.arccos(cos_angle)
angle_deg = np.degrees(angle_rad)
print(f"\nAngle between u and v: {angle_deg:.2f}°")


# ============================================================
# MATRIX TRANSFORMATIONS
# ============================================================

print("\n" + "="*60)
print("MATRIX TRANSFORMATIONS")
print("="*60)

# Create points
points = np.array([[1, 0], [0, 1], [1, 1]])
print(f"\nOriginal points:\n{points}")

# Rotation matrix (45 degrees)
angle = np.radians(45)
rotation = np.array([
    [np.cos(angle), -np.sin(angle)],
    [np.sin(angle), np.cos(angle)]
])
rotated = points @ rotation.T
print(f"\nAfter 45° rotation:\n{rotated}")

# Scaling matrix
scale = np.array([[2, 0], [0, 3]])
scaled = points @ scale.T
print(f"\nAfter scaling (2x, 3y):\n{scaled}")

# Shearing matrix
shear = np.array([[1, 0.5], [0, 1]])
sheared = points @ shear.T
print(f"\nAfter shearing:\n{sheared}")


# ============================================================
# STATISTICAL OPERATIONS WITH NUMPY
# ============================================================

print("\n" + "="*60)
print("STATISTICAL OPERATIONS")
print("="*60)

# Generate sample data
np.random.seed(42)
data1 = np.random.normal(loc=100, scale=15, size=100)
data2 = np.random.normal(loc=105, scale=15, size=100)

print(f"\nData1 - Mean: {np.mean(data1):.2f}, Std: {np.std(data1):.2f}")
print(f"Data2 - Mean: {np.mean(data2):.2f}, Std: {np.std(data2):.2f}")

# Correlation
correlation = np.corrcoef(data1, data2)[0, 1]
print(f"\nCorrelation between data1 and data2: {correlation:.4f}")

# Multiple linear regression
X = np.array([[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]])
y = np.array([2, 3, 4, 5, 6])
coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
print(f"\nLinear regression y = {coeffs[0]:.2f} + {coeffs[1]:.2f}x")

# Calculate predictions and residuals
y_pred = X @ coeffs
residuals = y - y_pred
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y - np.mean(y))**2)
r_squared = 1 - (ss_res / ss_tot)
print(f"R² = {r_squared:.4f}")


# ============================================================
# T-TESTS (HYPOTHESIS TESTING)
# ============================================================

print("\n" + "="*60)
print("T-TESTS (HYPOTHESIS TESTING)")
print("="*60)

np.random.seed(42)

# One-sample t-test
# Test if sample mean is significantly different from 100
sample = np.random.normal(loc=102, scale=10, size=30)
t_stat, p_value = stats.ttest_1samp(sample, popmean=100)
print(f"\nOne-Sample T-Test:")
print(f"  Null hypothesis: Sample mean = 100")
print(f"  Sample mean: {np.mean(sample):.2f}")
print(f"  T-statistic: {t_stat:.4f}")
print(f"  P-value: {p_value:.4f}")
print(f"  Result: {'Reject H0 (significant difference)' if p_value < 0.05 else 'Fail to reject H0 (no significant difference)'}")

# Two-sample t-test (independent samples)
# Test if two groups have different means
group1 = np.random.normal(loc=100, scale=10, size=25)
group2 = np.random.normal(loc=105, scale=10, size=25)
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"\nTwo-Sample T-Test (Independent):")
print(f"  Group 1 mean: {np.mean(group1):.2f}")
print(f"  Group 2 mean: {np.mean(group2):.2f}")
print(f"  T-statistic: {t_stat:.4f}")
print(f"  P-value: {p_value:.4f}")
print(f"  Result: {'Reject H0 (groups differ significantly)' if p_value < 0.05 else 'Fail to reject H0 (no significant difference)'}")

# Paired t-test
# Test if there's a significant change before/after treatment
before = np.array([85, 88, 92, 78, 95, 81, 89, 84, 91, 87])
after = np.array([92, 95, 98, 85, 102, 88, 96, 91, 98, 93])
t_stat, p_value = stats.ttest_rel(before, after)
print(f"\nPaired T-Test (Before/After):")
print(f"  Before mean: {np.mean(before):.2f}")
print(f"  After mean: {np.mean(after):.2f}")
print(f"  Mean difference: {np.mean(after - before):.2f}")
print(f"  T-statistic: {t_stat:.4f}")
print(f"  P-value: {p_value:.4f}")
print(f"  Result: {'Reject H0 (significant change detected)' if p_value < 0.05 else 'Fail to reject H0 (no significant change)'}")


# ============================================================
# A/B TESTING
# ============================================================

print("\n" + "="*60)
print("A/B TESTING FRAMEWORK")
print("="*60)

# A/B Test 1: Conversion Rate Comparison (Chi-Square Test)
print(f"\nA/B Test: Conversion Rate (Chi-Square Test)")
print(f"  Testing if new design has different conversion rate")

# Contingency table: [conversions, non-conversions]
control = np.array([45, 955])      # 45 conversions out of 1000
treatment = np.array([60, 940])    # 60 conversions out of 1000

contingency_table = np.array([control, treatment])
print(f"  Control group: {control[0]}/{sum(control)} = {100*control[0]/sum(control):.2f}% conversion")
print(f"  Treatment group: {treatment[0]}/{sum(treatment)} = {100*treatment[0]/sum(treatment):.2f}% conversion")

chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
print(f"  Chi-square statistic: {chi2:.4f}")
print(f"  P-value: {p_value:.4f}")
print(f"  Result: {'Treatment has significantly different conversion rate' if p_value < 0.05 else 'No significant difference in conversion rates'}")

# A/B Test 2: Continuous Metric Comparison (T-Test)
print(f"\nA/B Test: Average Order Value (T-Test)")
print(f"  Testing if new design affects average order value")

control_aov = np.random.normal(loc=75, scale=20, size=100)
treatment_aov = np.random.normal(loc=82, scale=20, size=100)

t_stat, p_value = stats.ttest_ind(control_aov, treatment_aov)
print(f"  Control group avg: ${np.mean(control_aov):.2f}")
print(f"  Treatment group avg: ${np.mean(treatment_aov):.2f}")
print(f"  T-statistic: {t_stat:.4f}")
print(f"  P-value: {p_value:.4f}")
print(f"  Result: {'Treatment significantly affected AOV' if p_value < 0.05 else 'No significant effect on AOV'}")

# A/B Test 3: Sample Size Planning
print(f"\nSample Size Planning (Statistical Power)")

# For a one-sample t-test
effect_size = 0.5  # small effect
alpha = 0.05       # significance level
power = 0.80       # desired power

# Using power analysis (rough calculation)
# n ≈ (z_alpha + z_beta)² * 2 * σ² / effect_size²
z_alpha = 1.96     # for alpha=0.05
z_beta = 0.84      # for power=0.80
sigma = 1.0

sample_size = int((z_alpha + z_beta)**2 * 2 * sigma**2 / (effect_size**2))
print(f"  To detect effect size {effect_size} with 80% power:")
print(f"  Recommended sample size per group: {sample_size}")

# A/B Test 4: Effect Size and Confidence Intervals
print(f"\nEffect Size and Confidence Intervals")

control_metric = np.random.normal(loc=50, scale=10, size=50)
treatment_metric = np.random.normal(loc=55, scale=10, size=50)

# Cohen's d
mean_diff = np.mean(treatment_metric) - np.mean(control_metric)
pooled_std = np.sqrt((np.std(control_metric)**2 + np.std(treatment_metric)**2) / 2)
cohens_d = mean_diff / pooled_std

print(f"  Control mean: {np.mean(control_metric):.2f}")
print(f"  Treatment mean: {np.mean(treatment_metric):.2f}")
print(f"  Cohen's d (effect size): {cohens_d:.4f}")

# Confidence intervals
se_control = np.std(control_metric) / np.sqrt(len(control_metric))
se_treatment = np.std(treatment_metric) / np.sqrt(len(treatment_metric))
ci_control = (np.mean(control_metric) - 1.96*se_control, np.mean(control_metric) + 1.96*se_control)
ci_treatment = (np.mean(treatment_metric) - 1.96*se_treatment, np.mean(treatment_metric) + 1.96*se_treatment)

print(f"  Control 95% CI: [{ci_control[0]:.2f}, {ci_control[1]:.2f}]")
print(f"  Treatment 95% CI: [{ci_treatment[0]:.2f}, {ci_treatment[1]:.2f}]")

print(f"\n" + "="*60)
print("END OF MATH AND STATISTICS DEMONSTRATION")
print("="*60)
