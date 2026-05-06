# Global Organized Crime Analytics 2023 - Interactive Dashboard

Welcome to the **Global Organized Crime Analytics Dashboard**. This project transforms raw global crime and resilience indices across 193 countries into a high-end, fully interactive web application. 

By migrating from a legacy static Flask/React implementation to an integrated **Plotly Dash** architecture, this project delivers a state-of-the-art "Glassmorphic" dark-mode analytical suite designed for researchers and policy-makers.

## ✨ Features

The application is structured into 5 comprehensive analytical tabs:

1. **🌍 Global Overview**
   - Interactive World Heatmap of Criminality scores.
   - Live Key Performance Indicators (KPIs) dynamically filtered by Continent/Region.
   - "Top 10" predictive breakdowns and pie chart compositions.

2. **📊 Distributions & Frequencies**
   - Select any of the 10 numerical or 5 categorical variables to instantly generate interactive Histograms and Barcharts.
   - Automatically generated Frequency Distribution tables displaying Relative and Cumulative frequencies.

3. **🔬 Exploratory Data Analysis (EDA)**
   - Outlier detection tools powered by Interactive Box Plots.
   - Real-time generation of 95% Confidence Intervals (CI) and exact statistical summaries (Mean, Median, Std Dev, IQR) for all numeric vectors.

4. **🎲 Probability Models**
   - Active Normal Distribution modeling engine.
   - Use sliders to shift Mean (μ), Standard Deviation (σ), and Thresholds (X) to visualize probability areas (Area Under the Curve) and compute Z-Scores instantly.

5. **📈 Prediction Engine & Regressions**
   - **Simple Linear Regression Explorer:** Pick any independent variable to chart against Global Criminality. Includes real-time mathematical equation rendering, R² Scores, and Line of Best Fit graphing.
   - **Multiple Linear Regression Predictor:** "Live Predictor" sliders. Slide input values for variables like *Human Trafficking* and *Cyber Crimes* and watch the Machine Learning module calculate the projected Criminality average in real-time.

## 🛠️ Technology Stack
* **Frontend UI/UX:** Plotly Dash core components wrapped in custom CSS (Responsive Flexbox, Glassmorphism `backdrop-filter`, dark-theme overrides, Google 'Inter' font).
* **Backend:** Python + Flask (integrated via Dash).
* **Data Processing:** Pandas & NumPy.
* **Statistics & Machine Learning:** SciPy (`scipy.stats`) and Scikit-Learn (`LinearRegression`).

## 🚀 Installation & Setup

Ensure you have Python 3.8+ installed.

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd "prob final project"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard server:**
   ```bash
   python app.py
   ```

4. **Access the Application:**
   Open your browser and navigate to: `http://127.0.0.1:8050/`

## 📂 File Structure

* `app.py` - The core application file managing both Frontend Layout and Backend Callbacks.
* `data/` - Contains the `processed_crime_data.csv` comprising 193 instances and 15 distinct variables (10 Numerical, 5 Categorical) including engineered columns.
* `requirements.txt` - Required python packages.

## 💎 Design & UI Notes
This project emphasizes rich visual aesthetics. It operates without external CSS frameworks to retain complete control over performance and theming. The dark mode (`#0B1120`), glowing gradient texts, and blur overlays create a premium interaction environment, ensuring all interactive dropdowns, slider tooltips, and data-tables seamlessly inherit the UI tokens.
