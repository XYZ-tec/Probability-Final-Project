from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

app = Flask(__name__)
CORS(app)  # Allow React (port 3000) to talk to Flask (port 5000)

# ─────────────────────────────────────────────
# LOAD DATA ONCE WHEN SERVER STARTS
# ─────────────────────────────────────────────

df = pd.read_csv('data/cleaned_crime_data.csv')

# Clean column names (remove trailing commas/spaces)
df.columns = df.columns.str.strip().str.rstrip(',')
df = df.rename(columns={
    'Criminality avg': 'Criminality',
    'Resilience avg': 'Resilience'
})

print("✅ Data loaded successfully!")
print(f"   Columns: {list(df.columns)}")
print(f"   Countries: {len(df)}")

# ─────────────────────────────────────────────
# ROUTE 1: GET ALL DATA
# ─────────────────────────────────────────────

@app.route('/api/data', methods=['GET'])
def get_data():
    """Return the full dataset as JSON."""
    return jsonify({
        "status": "success",
        "total_countries": len(df),
        "data": df.fillna(0).to_dict(orient='records')
    })

# ─────────────────────────────────────────────
# ROUTE 2: DESCRIPTIVE STATISTICS
# ─────────────────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return descriptive statistics for all numeric columns."""
    numeric_cols = ['Criminality', 'Resilience', 'Human trafficking',
                    'Cyber-dependent crimes', 'State-embedded actors']
    available = [c for c in numeric_cols if c in df.columns]

    result = {}
    for col in available:
        data = df[col].dropna()
        result[col] = {
            "mean":     round(float(data.mean()), 4),
            "median":   round(float(data.median()), 4),
            "std":      round(float(data.std()), 4),
            "variance": round(float(data.var()), 4),
            "min":      round(float(data.min()), 4),
            "max":      round(float(data.max()), 4),
            "skewness": round(float(data.skew()), 4),
            "count":    int(data.count())
        }

    return jsonify({
        "status": "success",
        "statistics": result
    })

# ─────────────────────────────────────────────
# ROUTE 3: CONFIDENCE INTERVALS
# ─────────────────────────────────────────────

@app.route('/api/confidence', methods=['GET'])
def get_confidence():
    """Return 95% confidence intervals for Criminality overall
       and broken down by top/bottom resilience groups."""

    # Overall CI for Criminality
    data = df['Criminality'].dropna()
    mean = float(data.mean())
    se = float(stats.sem(data))
    ci = stats.t.interval(0.95, df=len(data)-1, loc=mean, scale=se)

    overall = {
        "variable": "Criminality",
        "n": int(len(data)),
        "mean": round(mean, 4),
        "std": round(float(data.std()), 4),
        "ci_lower": round(float(ci[0]), 4),
        "ci_upper": round(float(ci[1]), 4),
        "confidence": "95%"
    }

    # CI by Resilience Group (Low / Medium / High)
    df['Resilience_Group'] = pd.cut(
        df['Resilience'],
        bins=[0, 3.5, 6.0, 10],
        labels=['Low Resilience', 'Medium Resilience', 'High Resilience']
    )

    groups = []
    for group_name, group_data in df.groupby('Resilience_Group', observed=True):
        g_data = group_data['Criminality'].dropna()
        if len(g_data) < 2:
            continue
        g_mean = float(g_data.mean())
        g_se = float(stats.sem(g_data))
        g_ci = stats.t.interval(0.95, df=len(g_data)-1, loc=g_mean, scale=g_se)
        groups.append({
            "group": str(group_name),
            "n": int(len(g_data)),
            "mean": round(g_mean, 3),
            "ci_lower": round(float(g_ci[0]), 3),
            "ci_upper": round(float(g_ci[1]), 3)
        })

    return jsonify({
        "status": "success",
        "overall": overall,
        "by_group": groups
    })

# ─────────────────────────────────────────────
# ROUTE 4: PROBABILITY DISTRIBUTION
# ─────────────────────────────────────────────

@app.route('/api/distribution', methods=['GET'])
def get_distribution():
    """Return histogram data + normal distribution fit parameters."""
    col = request.args.get('variable', 'Criminality')

    if col not in df.columns:
        return jsonify({"status": "error", "message": f"Column '{col}' not found"}), 400

    data = df[col].dropna()

    # Fit normal distribution
    mu, sigma = stats.norm.fit(data)

    # Shapiro-Wilk normality test
    shapiro_stat, shapiro_p = stats.shapiro(data)

    # Build histogram bins for chart
    counts, bin_edges = np.histogram(data, bins=15)
    histogram = []
    for i in range(len(counts)):
        histogram.append({
            "bin_start": round(float(bin_edges[i]), 3),
            "bin_end":   round(float(bin_edges[i+1]), 3),
            "count":     int(counts[i]),
            "label":     f"{bin_edges[i]:.1f}–{bin_edges[i+1]:.1f}"
        })

    # Normal curve points for overlay
    x_vals = np.linspace(float(data.min()), float(data.max()), 100)
    y_vals = stats.norm.pdf(x_vals, mu, sigma)
    normal_curve = [
        {"x": round(float(x), 3), "y": round(float(y), 6)}
        for x, y in zip(x_vals, y_vals)
    ]

    return jsonify({
        "status": "success",
        "variable": col,
        "mu": round(float(mu), 4),
        "sigma": round(float(sigma), 4),
        "shapiro_stat": round(float(shapiro_stat), 4),
        "shapiro_p": round(float(shapiro_p), 4),
        "is_normal": bool(shapiro_p > 0.05),
        "histogram": histogram,
        "normal_curve": normal_curve
    })

# ─────────────────────────────────────────────
# ROUTE 5: REGRESSION MODEL
# ─────────────────────────────────────────────

@app.route('/api/regression', methods=['GET'])
def get_regression():
    """Multiple linear regression: predict Criminality."""
    feature_cols = ['Resilience', 'Human trafficking',
                    'Cyber-dependent crimes', 'State-embedded actors']
    available = [c for c in feature_cols if c in df.columns]
    target = 'Criminality'

    model_df = df[available + [target, 'Country']].dropna()
    X = model_df[available]
    y = model_df[target]

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    r2   = round(float(r2_score(y, y_pred)), 4)
    rmse = round(float(np.sqrt(mean_squared_error(y, y_pred))), 4)

    # Scatter data: actual vs predicted
    scatter = [
        {
            "country": str(row['Country']),
            "actual": round(float(row[target]), 3),
            "predicted": round(float(pred), 3)
        }
        for (_, row), pred in zip(model_df.iterrows(), y_pred)
    ]

    coefficients = [
        {"feature": feat, "coefficient": round(float(coef), 4)}
        for feat, coef in zip(available, model.coef_)
    ]

    return jsonify({
        "status": "success",
        "r2": r2,
        "rmse": rmse,
        "intercept": round(float(model.intercept_), 4),
        "coefficients": coefficients,
        "features_used": available,
        "scatter_data": scatter
    })

# ─────────────────────────────────────────────
# ROUTE 6: PREDICT (POST)
# ─────────────────────────────────────────────

@app.route('/api/predict', methods=['POST'])
def predict():
    """Accept input values and return a predicted criminality score."""
    body = request.get_json()

    feature_cols = ['Resilience', 'Human trafficking',
                    'Cyber-dependent crimes', 'State-embedded actors']
    available = [c for c in feature_cols if c in df.columns]
    target = 'Criminality'

    model_df = df[available + [target]].dropna()
    X = model_df[available]
    y = model_df[target]

    model = LinearRegression()
    model.fit(X, y)

    # Extract input values from POST body
    try:
        input_values = [[float(body.get(feat, df[feat].mean())) for feat in available]]
        prediction = float(model.predict(input_values)[0])
        prediction = round(max(0, min(10, prediction)), 3)  # clamp between 0-10

        if prediction >= 7:
            level = "High"
            color = "red"
        elif prediction >= 5:
            level = "Moderate"
            color = "orange"
        else:
            level = "Low"
            color = "green"

        return jsonify({
            "status": "success",
            "predicted_criminality": prediction,
            "level": level,
            "color": color,
            "inputs": body
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# ─────────────────────────────────────────────
# ROUTE 7: OVERVIEW METRICS (for Home page)
# ─────────────────────────────────────────────

@app.route('/api/overview', methods=['GET'])
def get_overview():
    """Return summary metrics for the home page."""
    top5 = df.nlargest(5, 'Criminality')[['Country', 'Criminality']].to_dict(orient='records')
    bottom5 = df.nsmallest(5, 'Criminality')[['Country', 'Criminality']].to_dict(orient='records')

    return jsonify({
        "status": "success",
        "total_countries": int(len(df)),
        "global_mean_criminality": round(float(df['Criminality'].mean()), 4),
        "global_mean_resilience": round(float(df['Resilience'].mean()), 4),
        "highest_crime_country": str(df.loc[df['Criminality'].idxmax(), 'Country']),
        "lowest_crime_country": str(df.loc[df['Criminality'].idxmin(), 'Country']),
        "top5_highest": top5,
        "top5_lowest": bottom5
    })

# ─────────────────────────────────────────────
# RUN SERVER
# ─────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5000)