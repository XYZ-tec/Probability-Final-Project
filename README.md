# Global Organized Crime Analytics 2023 

Welcome to the **Global Organized Crime Analytics Dashboard**. This project transforms raw global crime and resilience indices across 193 countries into a high-end, fully interactive web application. 

By migrating from a legacy static Flask/React implementation to an integrated **Plotly Dash** architecture, this project delivers a state-of-the-art "Glassmorphic" dark-mode analytical suite designed for researchers and policy-makers.

##  Features

The application is structured into 5 comprehensive analytical tabs:

1. ** Global Overview**
   - Interactive World Heatmap of Criminality scores.
   - Live Key Performance Indicators (KPIs) dynamically filtered by Continent/Region.
   - "Top 10" predictive breakdowns and pie chart compositions.

2. ** Distributions & Frequencies**
   - Select any of the 10 numerical or 5 categorical variables to instantly generate interactive Histograms and Barcharts.
   - Automatically generated Frequency Distribution tables displaying Relative and Cumulative frequencies.

3. ** Exploratory Data Analysis (EDA)**
   - Outlier detection tools powered by Interactive Box Plots.
   - Real-time generation of 95% Confidence Intervals (CI) and exact statistical summaries (Mean, Median, Std Dev, IQR) for all numeric vectors.

4. ** Probability Models**
   - Active Normal Distribution modeling engine.
   - Use sliders to shift Mean (μ), Standard Deviation (σ), and Thresholds (X) to visualize probability areas (Area Under the Curve) and compute Z-Scores instantly.

5. ** Prediction Engine & Regressions**
   - **Simple Linear Regression Explorer:** Pick any independent variable to chart against Global Criminality. Includes real-time mathematical equation rendering, R² Scores, and Line of Best Fit graphing.
   - **Multiple Linear Regression Predictor:** "Live Predictor" sliders. Slide input values for variables like *Human Trafficking* and *Cyber Crimes* and watch the Machine Learning module calculate the projected Criminality average in real-time.

##  Technology Stack
* **Frontend UI/UX:** Plotly Dash core components wrapped in custom CSS (Responsive Flexbox, Glassmorphism `backdrop-filter`, dark-theme overrides, Google 'Inter' font).
* **Backend:** Python + Flask (integrated via Dash).
* **Data Processing:** Pandas & NumPy.
* **Statistics & Machine Learning:** SciPy (`scipy.stats`) and Scikit-Learn (`LinearRegression`).

##  Installation & Setup

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

##  File Structure

The dashboard operates on a professional, modular Model-View-Controller style architecture:

* `app.py` - The application entry point. Simply boots the Plotly Dash server.
* `app_instance.py` - Core instance initialization, resolving circular imports.
* `config.py` - Master styling tokens, graph templates, and CSS themes.
* `data.py` - Loads `processed_crime_data.csv` and executes preliminary Machine Learning `.fit()` actions.
* `layout.py` - Formats the DOM skeleton across the 5 independent analytical tabs.
* `components.py` - Abstraction layer containing reusable UI elements (glassmorphic cards, tables).
* `callbacks.py` - The logic routing module that calculates visualizations based on inputs.
* `data/` - Holds the processed DataFrame of 193 instances and 15 distinct variables.
* `requirements.txt` - Required python dependencies.