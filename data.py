import pandas as pd
from sklearn.linear_model import LinearRegression

# Load Data
df = pd.read_csv('data/processed_crime_data.csv')

NUMERIC_VARS = [
    'Criminality avg', 'Resilience avg', 'Human trafficking',
    'Cyber-dependent crimes', 'State-embedded actors', 'Criminal markets avg',
    'Criminal actors avg', 'Anti-money laundering', 'Financial crimes',
    'Extortion and protection racketeering'
]

CAT_VARS = ['Continent', 'Region', 'Country', 'Crime_Level', 'Resilience_Level']

# Multiple Linear Regression Pre-training
MLR_FEATURES = [
    'Resilience avg', 'Human trafficking', 'Cyber-dependent crimes',
    'State-embedded actors', 'Financial crimes', 'Anti-money laundering'
]
TARGET = 'Criminality avg'
df_mlr = df[MLR_FEATURES + [TARGET]].dropna()
X_all = df_mlr[MLR_FEATURES]
y_all = df_mlr[TARGET]
reg_model = LinearRegression().fit(X_all, y_all)
