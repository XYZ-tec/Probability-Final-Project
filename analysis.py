import pandas as pd
import numpy as np
from scipy import stats
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
file_path = os.path.join('data', 'global_oc_index.xlsx')
df = pd.read_excel(file_path, sheet_name='2023_dataset')

# UPDATED: Matching your exact column names (note the commas!)
variables = [
    'Criminality avg,', 
    'Resilience avg,', 
    'Human trafficking', 
    'Cyber-dependent crimes', 
    'State-embedded actors'
]

# 1. Statistical Measures (Mean, Median, SD, Variance)
stats_summary = df[variables].agg(['mean', 'median', 'std', 'var'])
# Add Mode separately
stats_summary.loc['mode'] = df[variables].mode().iloc[0]

print("--- Descriptive Statistics for Project Report ---")
print(stats_summary)

# 2. 95% Confidence Interval for "Criminality avg,"
# Specific requirement for the Spring-2026 project
data = df['Criminality avg,'].dropna()
mean = np.mean(data)
sem = stats.sem(data)
ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)

print(f"\n--- 95% Confidence Interval for Global Criminality ---")
print(f"Lower Bound: {ci[0]:.4f}")
print(f"Upper Bound: {ci[1]:.4f}")
print(f"Mean Score: {mean:.4f}")

df[variables + ['Country']].to_csv('data/cleaned_crime_data.csv', index=False)

# Visualization for Probability Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Criminality avg,'], kde=True, color='blue')
plt.title('Probability Distribution of Global Criminality')
plt.savefig('distribution_plot.png')

# Normality Test
shapiro_test = stats.shapiro(df['Criminality avg,'].dropna())
print(f"Shapiro-Wilk Test P-value: {shapiro_test.pvalue}")




# Prepare data - Predicting Criminality based on Resilience
# Dropping NaNs is essential for the model to run
reg_data = df[['Resilience avg,', 'Criminality avg,']].dropna()
X = reg_data[['Resilience avg,']].values.reshape(-1, 1)
y = reg_data['Criminality avg,'].values

# Create and fit the model
model = LinearRegression()
model.fit(X, y)

# Get Results
intercept = model.intercept_
slope = model.coef_[0]
r_squared = model.score(X, y)

print(f"\n--- Regression Modeling ---")
print(f"Regression Equation: y = {slope:.4f}x + {intercept:.4f}")
print(f"R-squared (Accuracy): {r_squared:.4f}")

# Visualization of the Regression Line
plt.figure(figsize=(10, 6))
plt.scatter(X, y, alpha=0.5, label='Actual Data')
plt.plot(X, model.predict(X), color='red', linewidth=2, label='Regression Line')
plt.title('Predicting Criminality based on Resilience')
plt.xlabel('Resilience Score')
plt.ylabel('Criminality Score')
plt.legend()
plt.savefig('regression_analysis.png') # Save for the report!