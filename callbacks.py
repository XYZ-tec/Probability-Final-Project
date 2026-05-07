from dash import Input, Output, html, callback_context
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
from components import kpi_chip, kpi_divider, metric_card, freq_table_html

def filter_df(continents, regions):
    mask = pd.Series([True] * len(df), index=df.index)
    if continents: mask &= df['Continent'].isin(continents)
    if regions: mask &= df['Region'].isin(regions)
    return df[mask]

def apply_axis_styles(fig):
    fig.update_xaxes(**config.AXIS_STYLE)
    fig.update_yaxes(**config.AXIS_STYLE)
    return fig

def register_callbacks():

    # ── Nav tab switching ──────────────────────────────────────────────
    @app.callback(
        [Output(f'content-{i}', 'style') for i in range(1, 6)] +
        [Output(f'nav-{i}', 'className') for i in range(1, 6)],
        [Input(f'nav-{i}', 'n_clicks') for i in range(1, 6)],
        prevent_initial_call=True
    )
    def switch_tab(*args):
        ctx = callback_context
        active = 1
        if ctx.triggered:
            triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
            try:
                active = int(triggered_id.split('-')[1])
            except Exception:
                active = 1

        show = {'display': 'block', 'paddingTop': '24px', 'paddingBottom': '48px'}
        hide = {'display': 'none'}
        styles = [show if i == active else hide for i in range(1, 6)]
        classes = ['nav-pill nav-active' if i == active else 'nav-pill' for i in range(1, 6)]
        return styles + classes

    # ── Tab 1: Global Overview ─────────────────────────────────────────
    @app.callback(
        Output('t1-metrics', 'children'), Output('t1-map', 'figure'),
        Output('t1-pie', 'figure'), Output('t1-bar', 'figure'),
        Input('t1-continent', 'value'), Input('t1-region', 'value')
    )
    def tab1_update(continents, regions):
        dff = filter_df(continents, regions)
        if len(dff) == 0:
            dff = df

        high_crime = len(dff[dff['Crime_Level'] == 'High'])

        metrics = [
            kpi_chip('Countries', str(len(dff)), '#3B82F6'),
            kpi_divider(),
            kpi_chip('Avg Criminality', f"{dff['Criminality avg'].mean():.2f}", '#F43F5E'),
            kpi_divider(),
            kpi_chip('Avg Resilience', f"{dff['Resilience avg'].mean():.2f}", '#10B981'),
            kpi_divider(),
            kpi_chip('High Crime', str(high_crime), '#F43F5E'),
        ]

        fig_map = px.choropleth(
            dff, locations="Country", locationmode="country names",
            color="Criminality avg", hover_name="Country",
            color_continuous_scale=px.colors.sequential.YlOrRd,
            title="", template='none'
        )
        map_layout = {k: v for k, v in config.CHART_LAYOUT.items() if k != 'margin'}
        fig_map.update_layout(
            **map_layout,
            margin=dict(t=10, l=0, r=0, b=10),
            geo=dict(showframe=False, showcoastlines=True,
                     bgcolor='rgba(0,0,0,0)', projection_type='equirectangular')
        )

        fig_pie = px.pie(
            dff, names='Crime_Level', title='',
            color_discrete_sequence=['#F43F5E', '#F59E0B', '#10B981'], template='none'
        )
        fig_pie.update_traces(hole=.4, textposition='inside', textinfo='percent+label')
        pie_layout = {k: v for k, v in config.CHART_LAYOUT.items() if k != 'margin'}
        fig_pie.update_layout(**pie_layout, margin=dict(t=10, l=20, r=20, b=10))

        top10 = dff.nlargest(10, 'Criminality avg').sort_values('Criminality avg', ascending=True)
        fig_bar = px.bar(
            top10, x='Criminality avg', y='Country', orientation='h',
            title='', color='Criminality avg',
            color_continuous_scale='Reds', template='none'
        )
        bar_layout = {k: v for k, v in config.CHART_LAYOUT.items() if k != 'margin'}
        fig_bar.update_layout(**bar_layout, margin=dict(t=10, l=10, r=40, b=30))
        fig_bar.update_yaxes(categoryorder='total ascending', **config.AXIS_STYLE)
        fig_bar.update_xaxes(**config.AXIS_STYLE)

        return metrics, fig_map, fig_pie, fig_bar

    # ── Tab 2: Distributions ───────────────────────────────────────────
    @app.callback(
        Output('t2-num-hist', 'figure'), Output('t2-freq-table', 'children'),
        Input('t2-num-var', 'value')
    )
    def tab2_num(var):
        if not var:
            return go.Figure(), ""
        df_clean = df.dropna(subset=[var])

        fig = px.histogram(df_clean, x=var, nbins=20, title=f'{var} Distribution',
                           color_discrete_sequence=[config.PRIMARY], template='none')
        fig.update_layout(**config.CHART_LAYOUT)
        apply_axis_styles(fig)

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
            table = html.Div(f"Could not generate table: {str(e)}", style={'color': config.TEXT_WHITE})
        return fig, table

    @app.callback(
        Output('t2-cat-bar', 'figure'), Output('t2-cat-pie', 'figure'), Output('t2-cat-table', 'children'),
        Input('t2-cat-var', 'value')
    )
    def tab2_cat(var):
        if not var:
            return go.Figure(), go.Figure(), ""
        counts = df[var].value_counts().reset_index()
        counts.columns = [var, 'count']
        total = counts['count'].sum()

        fig_bar = px.bar(counts, x=var, y='count', title=f'Counts by {var}',
                         color_discrete_sequence=[config.PRIMARY_LIGHT], template='none')
        fig_bar.update_layout(**config.CHART_LAYOUT)
        apply_axis_styles(fig_bar)

        fig_pie = px.pie(counts, names=var, values='count', title=f'Distribution of {var}',
                         color_discrete_sequence=config.CHART_COLORS, template='none')
        fig_pie.update_layout(**config.CHART_LAYOUT)

        rows, cum = [], 0
        for _, row in counts.iterrows():
            cum += row['count']
            rows.append([row[var], f"{row['count']}", f"{row['count']/total*100:.1f}%", f'{cum}'])
        table = freq_table_html(['Category', 'Frequency', 'Relative (%)', 'Cumulative'], rows)
        return fig_bar, fig_pie, table

    # ── Tab 3: EDA ─────────────────────────────────────────────────────
    @app.callback(
        Output('t3-boxplot', 'figure'), Output('t3-stats-table', 'children'), Output('t3-ci-table', 'children'),
        Input('t3-var', 'value')
    )
    def tab3_eda(var):
        if not var:
            return go.Figure(), "", ""
        s = df[var].dropna()
        fig = go.Figure(go.Box(x=s, boxpoints='outliers', marker_color=config.RED,
                               line_color=config.PRIMARY, fillcolor='rgba(59, 130, 246, 0.15)', name=var))
        fig.update_layout(**config.CHART_LAYOUT, title='Box Plot (Outlier Detection)')
        apply_axis_styles(fig)

        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        stats_data = [
            ('Mean', f'{s.mean():.3f}'), ('Median', f'{s.median():.3f}'), ('Std Dev', f'{s.std():.3f}'),
            ('Q1', f'{q1:.3f}'), ('Q3', f'{q3:.3f}'), ('IQR', f'{q3-q1:.3f}'),
            ('Min', f'{s.min():.3f}'), ('Max', f'{s.max():.3f}')
        ]
        rows = []
        for k, v in stats_data:
            rows.append(html.Tr([
                html.Td(k, style={'padding': '8px 12px', 'fontWeight': '600', 'color': '#F8FAFC'}),
                html.Td(v, style={'padding': '8px 12px', 'color': '#F8FAFC'})
            ]))
        tbl = html.Table(html.Tbody(rows), style={
            'width': '100%', 'background': 'rgba(255,255,255,0.04)',
            'borderRadius': '8px', 'border': f'1px solid rgba(255,255,255,0.08)'
        })

        ci_rows = []
        for v_name in NUMERIC_VARS:
            ss = df[v_name].dropna()
            mean, sem = ss.mean(), scipy_stats.sem(ss)
            lo, hi = scipy_stats.t.interval(0.95, df=len(ss)-1, loc=mean, scale=sem)
            ci_rows.append([v_name, f'{mean:.2f}', f'{lo:.2f}', f'{hi:.2f}', f'{hi-lo:.2f}'])
        ci_table = freq_table_html(['Variable', 'Mean', '95% CI Lower', '95% CI Upper', 'Width'], ci_rows)
        return fig, tbl, ci_table

    # ── Tab 4: Probability Models ──────────────────────────────────────
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
        fig.add_trace(go.Scatter(
            x=np.concatenate([xs_fill, [x]]), y=np.concatenate([ys_fill, [0]]),
            fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.3)',
            line=dict(width=0), name='P(X ≤ x)'
        ))
        fig.update_layout(**config.CHART_LAYOUT, title=f'Normal Curve · threshold X = {x}')
        apply_axis_styles(fig)
        pz = norm.cdf(x, mu, sigma)
        met = [
            metric_card(f'P(X ≤ {x})', f'{pz:.4f}', {'minWidth': '120px'}),
            metric_card(f'P(X > {x})', f'{1-pz:.4f}', {'minWidth': '120px'}),
            metric_card('Z-Score', f'{(x-mu)/sigma:.2f}', {'minWidth': '120px'})
        ]
        return fig, met

    # ── Tab 5: Prediction Engine ───────────────────────────────────────
    @app.callback(
        Output('reg-scatter-simple', 'figure'), Output('reg-stats-simple', 'children'),
        Input('reg-x', 'value')
    )
    def tab5_simple_reg(x_var):
        if not x_var:
            return go.Figure(), ""
        df_clean = df[[x_var, 'Criminality avg', 'Country']].dropna()
        X = df_clean[[x_var]]
        y = df_clean['Criminality avg']
        model = LinearRegression().fit(X, y)
        y_pred = model.predict(X)

        fig = px.scatter(df_clean, x=x_var, y='Criminality avg', hover_name='Country',
                         color_discrete_sequence=[config.PRIMARY_LIGHT], template='none')
        fig.add_trace(go.Scatter(x=df_clean[x_var], y=y_pred, mode='lines',
                                 line=dict(color=config.RED, width=2.5), name='Trend'))
        fig.update_layout(**config.CHART_LAYOUT, title=f'Criminality vs {x_var}')
        apply_axis_styles(fig)

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
            rows.append(html.Tr([
                html.Td(k, style={'padding': '10px 14px', 'fontWeight': '600', 'color': '#F8FAFC'}),
                html.Td(v, style={'padding': '10px 14px', 'color': '#F8FAFC'})
            ]))
        tbl = html.Table(html.Tbody(rows), style={
            'width': '100%', 'background': 'rgba(255,255,255,0.04)',
            'borderRadius': '8px', 'border': f'1px solid rgba(255,255,255,0.08)'
        })
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
