import pandas as pd
import numpy as np
from scipy import stats
import os
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