from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as scipy_stats
from scipy.stats import norm
from sklearn.linear_model import LinearRegression

from app_instance import app
import config
from data import df, NUMERIC_VARS, CAT_VARS, reg_model
from components import metric_card, freq_table_html

def filter_df(continents, regions):
    mask = pd.Series([True] * len(df), index=df.index)
    if continents: mask &= df['Continent'].isin(continents)
    if regions: mask &= df['Region'].isin(regions)
    return df[mask]

def register_callbacks():
    @app.callback(
        Output('t1-metrics', 'children'), Output('t1-map', 'figure'),
        Output('t1-pie', 'figure'), Output('t1-bar', 'figure'),
        Input('t1-continent', 'value'), Input('t1-region', 'value')
    )
    def tab1_update(continents, regions):
        dff = filter_df(continents, regions)
        if len(dff) == 0: dff = df
        
        metrics = [
            metric_card('Countries', f'{len(dff)}'),
            metric_card('Avg Criminality', f"{dff['Criminality avg'].mean():.2f}"),
            metric_card('Avg Resilience', f"{dff['Resilience avg'].mean():.2f}"),
            metric_card('High Crime Count', f"{len(dff[dff['Crime_Level'] == 'High'])}")
        ]
        
        fig_map = px.choropleth(dff, locations="Country", locationmode="country names", color="Criminality avg", hover_name="Country", color_continuous_scale=px.colors.sequential.YlOrRd, title="Global Heatmap of Criminality")
        fig_map.update_layout(**config.CHART_LAYOUT, geo=dict(showframe=False, showcoastlines=True, bgcolor='rgba(0,0,0,0)', projection_type='equirectangular'))

        fig_pie = px.pie(dff, names='Crime_Level', title='Crime Level Composition', color_discrete_sequence=['#F43F5E', '#F59E0B', '#10B981'])
        fig_pie.update_traces(hole=.4, textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(**config.CHART_LAYOUT)

        top10 = dff.nlargest(10, 'Criminality avg').sort_values('Criminality avg', ascending=True)
        fig_bar = px.bar(top10, x='Criminality avg', y='Country', orientation='h', title='Top 10 Countries by Criminality', color='Criminality avg', color_continuous_scale='Reds')
        fig_bar.update_layout(**config.CHART_LAYOUT, yaxis={'categoryorder':'total ascending'})
        
        return metrics, fig_map, fig_pie, fig_bar

    @app.callback(
        Output('t2-num-hist', 'figure'), Output('t2-freq-table', 'children'),
        Input('t2-num-var', 'value')
    )
    def tab2_num(var):
        if not var: return go.Figure(), ""
        df_clean = df.dropna(subset=[var])
        
        fig = px.histogram(df_clean, x=var, nbins=20, title=f'{var} Distribution', color_discrete_sequence=[config.PRIMARY])
        fig.update_layout(**config.CHART_LAYOUT)
        
        try:
            series = df_clean[var]
            labels_cut, _ = pd.cut(series, bins=8, retbins=True)
            freq = labels_cut.value_counts().sort_index()
            total = freq.sum()
            rows, cum = [], 0
            for interval, f in freq.items():
                if pd.isna(interval): continue
                cum += f
                rows.append([f'{interval.left:.2f} \u2013 {interval.right:.2f}', f'{f}', f'{f/total*100:.1f}%', f'{cum}'])
            table = freq_table_html(['Class Interval', 'Frequency', 'Relative (%)', 'Cumulative'], rows)
        except Exception as e:
            table = html.Div(f"Could not generate frequency table: {str(e)}", style={'color': config.TEXT_WHITE})
        return fig, table

    @app.callback(
        Output('t2-cat-bar', 'figure'), Output('t2-cat-pie', 'figure'), Output('t2-cat-table', 'children'),
        Input('t2-cat-var', 'value')
    )
    def tab2_cat(var):
        if not var: return go.Figure(), go.Figure(), ""
        counts = df[var].value_counts().reset_index()
        counts.columns = [var, 'count']
        total = counts['count'].sum()
        
        fig_bar = px.bar(counts, x=var, y='count', title=f'Counts by {var}', color_discrete_sequence=[config.PRIMARY_LIGHT])
        fig_bar.update_layout(**config.CHART_LAYOUT)
        fig_pie = px.pie(counts, names=var, values='count', title=f'Distribution of {var}', color_discrete_sequence=config.CHART_COLORS)
        fig_pie.update_layout(**config.CHART_LAYOUT)
        
        rows, cum = [], 0
        for _, row in counts.iterrows():
            cum += row['count']
            rows.append([row[var], f"{row['count']}", f"{row['count']/total*100:.1f}%", f'{cum}'])
        table = freq_table_html(['Category', 'Frequency', 'Relative (%)', 'Cumulative'], rows)
        return fig_bar, fig_pie, table

    @app.callback(
        Output('t3-boxplot', 'figure'), Output('t3-stats-table', 'children'), Output('t3-ci-table', 'children'),
        Input('t3-var', 'value')
    )
    def tab3_eda(var):
        if not var: return go.Figure(), "", ""
        s = df[var].dropna()
        fig = go.Figure(go.Box(x=s, boxpoints='outliers', marker_color=config.RED, line_color=config.PRIMARY, fillcolor='rgba(59, 130, 246, 0.2)', name=var))
        fig.update_layout(**config.CHART_LAYOUT, title='Box Plot (Outlier Detection)')
        
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        stats_data = [
            ('Mean', f'{s.mean():.3f}'), ('Median', f'{s.median():.3f}'), ('Std Dev', f'{s.std():.3f}'),
            ('Q1', f'{q1:.3f}'), ('Q3', f'{q3:.3f}'), ('IQR', f'{q3-q1:.3f}'),
            ('Min', f'{s.min():.3f}'), ('Max', f'{s.max():.3f}')
        ]
        rows = []
        for k, v in stats_data:
            rows.append(html.Tr([html.Td(k, style={'padding':'8px 12px', 'fontWeight':'600', 'color': '#F8FAFC'}), html.Td(v, style={'padding':'8px 12px', 'color':'#F8FAFC'})]))
        tbl = html.Table(html.Tbody(rows), style={'width':'100%', 'background':'rgba(255,255,255,0.05)', 'borderRadius':'8px', 'border': '1px solid rgba(255,255,255,0.1)'})

        ci_rows = []
        for v_name in NUMERIC_VARS:
            ss = df[v_name].dropna()
            mean, sem = ss.mean(), scipy_stats.sem(ss)
            lo, hi = scipy_stats.t.interval(0.95, df=len(ss)-1, loc=mean, scale=sem)
            ci_rows.append([v_name, f'{mean:.2f}', f'{lo:.2f}', f'{hi:.2f}', f'{hi-lo:.2f}'])
        ci_table = freq_table_html(['Variable', 'Mean', '95% CI Lower', '95% CI Upper', 'Width'], ci_rows)
        return fig, tbl, ci_table

    @app.callback(
        Output('norm-x', 'min'), Output('norm-x', 'max'),
        Input('norm-mu', 'value'), Input('norm-sigma', 'value')
    )
    def norm_x_ranges(mu, sigma):
        mu, sigma = float(mu or 5), max(float(sigma or 1), 0.1)
        return round(max(0, mu - 4*sigma), 1), round(mu + 4*sigma, 1)

    @app.callback(
        Output('norm-chart', 'figure'), Output('norm-metrics', 'children'),
        Input('norm-mu', 'value'), Input('norm-sigma', 'value'), Input('norm-x', 'value')
    )
    def tab4_prob(mu, sigma, x):
        mu, sigma, x = float(mu or 5), max(float(sigma or 1), 0.1), float(x or 5)
        xs = np.linspace(max(0, mu - 4*sigma), mu + 4*sigma, 500)
        ys = norm.pdf(xs, mu, sigma)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color=config.PRIMARY, width=3), name='N(μ, σ)'))
        
        xs_fill = xs[xs <= x]
        ys_fill = ys[xs <= x]
        fig.add_trace(go.Scatter(x=np.concatenate([xs_fill, [x]]), y=np.concatenate([ys_fill, [0]]),
                                 fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.4)', line=dict(width=0), name='P(X ≤ x)'))
        
        fig.update_layout(**config.CHART_LAYOUT, title=f"Normal Curve with Area under threshold X={x}")
        pz = norm.cdf(x, mu, sigma)
        met = [metric_card(f'P(X ≤ {x})', f'{pz:.4f}', {'minWidth': '120px'}), metric_card(f'P(X > {x})', f'{1-pz:.4f}', {'minWidth': '120px'}), metric_card('Z-Score', f'{(x-mu)/sigma:.2f}', {'minWidth': '120px'})]
        return fig, met

    @app.callback(
        Output('reg-scatter-simple', 'figure'), Output('reg-stats-simple', 'children'),
        Input('reg-x', 'value')
    )
    def tab5_simple_reg(x_var):
        if not x_var: return go.Figure(), ""
        df_clean = df[[x_var, 'Criminality avg', 'Country']].dropna()
        X = df_clean[[x_var]]
        y = df_clean['Criminality avg']
        model = LinearRegression().fit(X, y)
        y_pred = model.predict(X)
        
        fig = px.scatter(df_clean, x=x_var, y='Criminality avg', hover_name='Country', color_discrete_sequence=[config.PRIMARY_LIGHT])
        fig.add_trace(go.Scatter(x=df_clean[x_var], y=y_pred, mode='lines', line=dict(color=config.RED, width=3), name='Trend'))
        fig.update_layout(**config.CHART_LAYOUT, title=f'Criminality vs {x_var}')
        
        r2 = model.score(X, y)
        coef = model.coef_[0]
        intercept = model.intercept_
        
        stats_data = [
            ('R² Score', f'{r2:.4f}'),
            ('Coefficient (Slope)', f'{coef:.4f}'),
            ('Intercept', f'{intercept:.4f}'),
            ('Equation', f'y = {coef:.3f}x + {intercept:.3f}')
        ]
        rows = []
        for k, v in stats_data:
            rows.append(html.Tr([html.Td(k, style={'padding':'12px 16px', 'fontWeight':'600', 'color': '#F8FAFC'}), html.Td(v, style={'padding':'12px 16px', 'color':'#F8FAFC'})]))
        tbl = html.Table(html.Tbody(rows), style={'width':'100%', 'background':'rgba(255,255,255,0.05)', 'borderRadius':'8px', 'border': '1px solid rgba(255,255,255,0.1)'})

        return fig, tbl

    @app.callback(
        Output('pred-output', 'children'),
        Input('sl-resilience', 'value'), Input('sl-trafficking', 'value'),
        Input('sl-cyber', 'value'), Input('sl-state', 'value'),
        Input('sl-financial', 'value'), Input('sl-aml', 'value')
    )
    def tab5_pred(v1, v2, v3, v4, v5, v6):
        pred = reg_model.predict([[v1, v2, v3, v4, v5, v6]])[0]
        return f"{pred:.2f}"
