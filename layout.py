from dash import dcc, html
import config
from data import df, NUMERIC_VARS, CAT_VARS, reg_model, X_all, y_all
from components import filter_row, card, section_label

def create_layout():
    return html.Div([
        html.Div([
            html.Div([
                html.H1('Global Organized Crime Analytics', style={'color': config.TEXT_WHITE, 'fontWeight': '800', 'fontSize': '42px', 'marginBottom': '12px', 'letterSpacing': '-1px'}),
                html.P('Interactive dashboard analyzing criminality and resilience to organized crime across 193 countries.', style={'color': config.TEXT_SEC, 'fontSize': '15px', 'lineHeight': '1.6', 'marginBottom': '20px', 'maxWidth': '850px'}),
                html.Div([
                    html.Span('Data Source: Global OC Index', style={'background': 'rgba(255,255,255,0.08)', 'color': config.TEXT_WHITE, 'borderRadius': '6px', 'padding': '6px 16px', 'fontSize': '13px', 'marginRight': '12px', 'border': '1px solid rgba(255,255,255,0.1)'}),
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '48px 24px'}),
        ], style={'background': 'rgba(15, 23, 42, 0.95)', 'borderBottom': '1px solid rgba(255,255,255,0.05)', 'boxShadow': '0 4px 20px rgba(0,0,0,0.5)'}),

        html.Div([
            dcc.Tabs(id='main-tabs', value='tab-1', children=[
                dcc.Tab(label='Global Overview', value='tab-1', className='tab', selected_className='tab--selected', children=[
                    html.Div([
                        filter_row(
                            ('Filter by Continent', dcc.Dropdown(id='t1-continent', options=[{'label': o, 'value': o} for o in sorted(df['Continent'].dropna().unique())], multi=True, style={'fontSize': '14px'})),
                            ('Filter by Region', dcc.Dropdown(id='t1-region', options=[{'label': o, 'value': o} for o in sorted(df['Region'].dropna().unique())], multi=True, style={'fontSize': '14px'}))
                        ),
                        html.Div(id='t1-metrics', style={'display': 'flex', 'gap': '20px', 'marginBottom': '24px', 'flexWrap': 'wrap'}),
                        card([
                            html.H3('Global Criminality Heatmap', style={'color': config.TEXT_WHITE, 'marginBottom': '16px'}),
                            dcc.Graph(id='t1-map', config={'displayModeBar': False}, style={'height': '450px'})
                        ], style={'padding': '24px'}),
                        html.Div([
                            html.Div([card([dcc.Graph(id='t1-pie', config={'displayModeBar': False}, style={'height': '350px'})], style={'height': '100%', 'padding': '16px'})], style={'flex': '1', 'minWidth': '320px'}),
                            html.Div([card([dcc.Graph(id='t1-bar', config={'displayModeBar': False}, style={'height': '350px'})], style={'height': '100%', 'padding': '16px'})], style={'flex': '1.5', 'minWidth': '400px'}),
                        ], style={'display': 'flex', 'gap': '24px', 'alignItems': 'stretch'}),
                    ], style={'padding': '32px 0'}),
                ]),

                dcc.Tab(label='Distributions & Frequencies', value='tab-2', className='tab', selected_className='tab--selected', children=[
                    html.Div([
                        card([
                            html.H3('Numerical Variable Analysis', style={'color': config.TEXT_WHITE, 'marginBottom': '16px'}),
                            html.Div([section_label('Select Metric'),
                                      dcc.Dropdown(id='t2-num-var', options=[{'label': v, 'value': v} for v in NUMERIC_VARS],
                                                   value='Criminality avg', clearable=False, style={'fontSize': '14px', 'maxWidth': '350px', 'marginBottom': '20px'})]),
                            html.Div([
                                html.Div([dcc.Graph(id='t2-num-hist', config={'displayModeBar': False}, style={'height': '350px'})], style={'flex': '60', 'minWidth': '300px'}),
                                html.Div([html.Div(id='t2-freq-table')], style={'flex': '40', 'overflowX': 'auto', 'minWidth': '250px'}),
                            ], style={'display': 'flex', 'gap': '32px', 'alignItems': 'flex-start', 'flexWrap': 'wrap'}),
                        ], className='glass-card dropdown-wrapper-card'),

                        card([
                            html.H3('Categorical Variable Analysis', style={'color': config.TEXT_WHITE, 'marginBottom': '16px'}),
                            html.Div([section_label('Select Category'),
                                      dcc.Dropdown(id='t2-cat-var', options=[{'label': v, 'value': v} for v in CAT_VARS if v != 'Country'],
                                                   value='Region', clearable=False, style={'fontSize': '14px', 'maxWidth': '350px', 'marginBottom': '20px'})]),
                            html.Div([
                                html.Div([dcc.Graph(id='t2-cat-bar', config={'displayModeBar': False}, style={'height': '300px'})], style={'flex': '1'}),
                                html.Div([dcc.Graph(id='t2-cat-pie', config={'displayModeBar': False}, style={'height': '300px'})], style={'flex': '1'}),
                            ], style={'display': 'flex', 'gap': '24px', 'marginBottom': '24px', 'flexWrap': 'wrap'}),
                            html.Div(id='t2-cat-table'),
                        ], className='glass-card dropdown-wrapper-card'),
                    ], style={'padding': '32px 0'}),
                ]),

                dcc.Tab(label='Exploratory Data Analysis', value='tab-3', className='tab', selected_className='tab--selected', children=[
                    html.Div([
                        card([
                            html.H3('Analyze Variable Outliers & Spread', style={'color': config.TEXT_WHITE, 'marginBottom': '16px'}),
                            html.Div([
                                dcc.Dropdown(id='t3-var', options=[{'label': v, 'value': v} for v in NUMERIC_VARS],
                                             value='Criminal markets avg', clearable=False, style={'fontSize': '14px', 'maxWidth':'300px'})
                            ], style={'marginBottom': '24px'}),
                            html.Div([
                                html.Div([dcc.Graph(id='t3-boxplot', config={'displayModeBar': False}, style={'height': '350px'})], style={'flex': '60'}),
                                html.Div([html.Div(id='t3-stats-table')], style={'flex': '40'}),
                            ], style={'display': 'flex', 'gap': '32px', 'alignItems': 'flex-start', 'flexWrap': 'wrap'}),
                        ], className='glass-card dropdown-wrapper-card'),

                        card([
                            html.H3('Confidence Intervals (95%)', style={'color': config.TEXT_WHITE, 'marginBottom': '16px'}),
                            html.Div(id='t3-ci-table', style={'overflowX': 'auto'}),
                        ]),
                    ], style={'padding': '32px 0'}),
                ]),

                dcc.Tab(label='Probability Models', value='tab-4', className='tab', selected_className='tab--selected', children=[
                    html.Div([
                        card([
                            html.H3('Normal Distribution Modeling', style={'color': config.TEXT_WHITE, 'marginBottom': '8px'}),
                            html.Div([
                                html.Div([section_label('μ (Mean)'), dcc.Input(id='norm-mu', type='number', value=round(float(df['Criminality avg'].mean()), 2), step=0.01, style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid rgba(255,255,255,0.1)', 'background': 'rgba(0,0,0,0.3)', 'color': config.TEXT_WHITE, 'fontSize': '15px'})], style={'flex': '1', 'maxWidth': '200px'}),
                                html.Div([section_label('σ (Std Dev)'), dcc.Input(id='norm-sigma', type='number', value=round(float(df['Criminality avg'].std()), 2), min=0.01, step=0.01, style={'width': '100%', 'padding': '10px 14px', 'borderRadius': '8px', 'border': '1px solid rgba(255,255,255,0.1)', 'background': 'rgba(0,0,0,0.3)', 'color': config.TEXT_WHITE, 'fontSize': '15px'})], style={'flex': '1', 'maxWidth': '200px'}),
                                html.Div([section_label('X Value Threshold'), dcc.Slider(id='norm-x', min=0, max=10, step=0.1, value=6.0, marks={i: str(i) for i in range(11)}, tooltip={"placement": "bottom", "always_visible": True})], style={'flex': '2', 'paddingTop': '4px'}),
                            ], style={'display': 'flex', 'gap': '32px', 'marginBottom': '24px', 'alignItems': 'flex-end', 'flexWrap': 'wrap'}),
                            dcc.Graph(id='norm-chart', config={'displayModeBar': False}, style={'height': '380px'}),
                            html.Div(id='norm-metrics', style={'display': 'flex', 'gap': '16px', 'marginTop': '24px', 'flexWrap': 'wrap'}),
                        ]),
                    ], style={'padding': '32px 0'}),
                ]),

                dcc.Tab(label='Prediction Engine & Regressions', value='tab-5', className='tab', selected_className='tab--selected', children=[
                    html.Div([
                        card([
                            html.H3('Simple Linear Regression Explorer', style={'color': config.TEXT_WHITE, 'marginBottom': '8px'}),
                            html.Div([
                                html.Div([
                                    section_label('X Variable (Independent)'),
                                    dcc.Dropdown(id='reg-x', options=[{'label': v, 'value': v} for v in NUMERIC_VARS if v != 'Criminality avg'], value='Resilience avg', clearable=False, style={'fontSize': '14px'}),
                                ], style={'flex': '1', 'minWidth': '200px'}),
                                html.Div([
                                    section_label('Y Variable (Dependent)'),
                                    html.Div('Criminality average', style={'fontSize': '14px', 'padding': '8px 12px', 'background': 'rgba(0,0,0,0.3)', 'border': '1px solid rgba(255,255,255,0.1)', 'borderRadius': '6px', 'color': config.PRIMARY, 'fontWeight': '600'}),
                                ], style={'flex': '1', 'minWidth': '200px'}),
                            ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px', 'flexWrap': 'wrap'}),
                            html.Div([
                                html.Div([dcc.Graph(id='reg-scatter-simple', config={'displayModeBar': False}, style={'height': '360px'})], style={'flex': '65'}),
                                html.Div([html.Div(id='reg-stats-simple')], style={'flex': '35', 'minWidth': '220px'}),
                            ], style={'display': 'flex', 'gap': '20px', 'alignItems': 'flex-start', 'flexWrap': 'wrap'}),
                        ], className='glass-card dropdown-wrapper-card'),

                        card([
                            html.H3('Multiple Linear Regression Live Predictor', style={'color': config.TEXT_WHITE, 'marginBottom': '8px'}),
                            html.Div([
                                html.Div([
                                    html.Div([section_label('Resilience Avg'), dcc.Slider(1, 10, 0.5, value=5, id='sl-resilience', marks={1:'1', 10:'10'}, tooltip={"placement": "bottom", "always_visible": True})], style={'marginBottom': '24px'}),
                                    html.Div([section_label('Human Trafficking'), dcc.Slider(1, 10, 0.5, value=6, id='sl-trafficking', marks={1:'1', 10:'10'}, tooltip={"placement": "bottom", "always_visible": True})], style={'marginBottom': '24px'}),
                                    html.Div([section_label('Cyber-dependent crimes'), dcc.Slider(1, 10, 0.5, value=4, id='sl-cyber', marks={1:'1', 10:'10'}, tooltip={"placement": "bottom", "always_visible": True})], style={'marginBottom': '24px'}),
                                    html.Div([section_label('State-embedded actors'), dcc.Slider(1, 10, 0.5, value=7, id='sl-state', marks={1:'1', 10:'10'}, tooltip={"placement": "bottom", "always_visible": True})], style={'marginBottom': '24px'}),
                                    html.Div([section_label('Financial crimes'), dcc.Slider(1, 10, 0.5, value=5, id='sl-financial', marks={1:'1', 10:'10'}, tooltip={"placement": "bottom", "always_visible": True})], style={'marginBottom': '24px'}),
                                    html.Div([section_label('Anti-money laundering'), dcc.Slider(1, 10, 0.5, value=3, id='sl-aml', marks={1:'1', 10:'10'}, tooltip={"placement": "bottom", "always_visible": True})]),
                                ], style={'flex': '45', 'background': 'rgba(15, 23, 42, 0.5)', 'borderRadius': '12px', 'padding': '32px', 'border': '1px solid rgba(255,255,255,0.05)', 'minWidth': '300px'}),
                                
                                html.Div([
                                    html.Div([
                                        html.P('Predicted Global Criminality Score', style={'color': 'rgba(255,255,255,0.8)', 'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '12px', 'textTransform': 'uppercase', 'letterSpacing': '1px'}),
                                        html.Div(id='pred-output', style={'fontSize': '72px', 'fontWeight': '800', 'background': 'linear-gradient(to right, #F43F5E, #F59E0B)', '-webkit-background-clip': 'text', '-webkit-text-fill-color': 'transparent'}),
                                        html.P('/ 10.00', style={'color': 'rgba(255,255,255,0.4)', 'fontSize': '18px', 'fontWeight': '600'}),
                                    ], style={'background': 'rgba(0,0,0,0.4)', 'borderRadius': '16px', 'padding': '40px 32px', 'textAlign': 'center', 'border': '1px solid rgba(244, 63, 94, 0.3)', 'boxShadow': '0 0 40px rgba(244, 63, 94, 0.1)', 'marginBottom': '24px'}),
                                    
                                    html.Div([
                                        html.H4('Multiple Linear Model Insights', style={'color': config.TEXT_WHITE, 'marginBottom': '12px', 'fontSize': '15px'}),
                                        html.Div([html.Span('R² Score:', style={'color': config.TEXT_SEC}), html.Span(f' {reg_model.score(X_all, y_all):.4f}', style={'color': config.PRIMARY_LIGHT, 'fontWeight': '700', 'float': 'right'})], style={'marginBottom': '8px', 'fontSize': '14px'}),
                                        html.Div([html.Span('Strongest Predictor:', style={'color': config.TEXT_SEC}), html.Span(' Human Trafficking', style={'color': config.PRIMARY_LIGHT, 'fontWeight': '700', 'float': 'right'})], style={'fontSize': '14px'}),
                                    ], style={'background': 'rgba(0,0,0,0.2)', 'borderRadius': '12px', 'padding': '24px', 'border': '1px dashed rgba(255,255,255,0.1)'})
                                ], style={'flex': '55', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'minWidth': '300px'}),
                            ], style={'display': 'flex', 'gap': '32px', 'flexWrap': 'wrap'}),
                        ]),
                    ], style={'padding': '32px 0'}),
                ]),

            ]),
        ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '0 24px'}),

    ], style={'fontFamily': "'Inter', sans-serif"})
