from dash import dcc, html
import config
from data import df, NUMERIC_VARS, CAT_VARS, reg_model, X_all, y_all
from components import card, section_label

BG = '#050D1A'
CARD = '#0D1829'
BORDER = '#1E2D45'
NAV_BG = '#080F1C'

_dd_style = {'fontSize': '13px', 'minWidth': '160px'}

def _nav_btn(label, nav_id, active=False):
    return html.Button(
        label,
        id=nav_id,
        n_clicks=0,
        className='nav-pill nav-active' if active else 'nav-pill'
    )

def _map_pill(label, active=False):
    return html.Button(label, className='map-pill map-pill-active' if active else 'map-pill')

def _stat_mini(label, value, color='#3B82F6'):
    return html.Div([
        html.Div(label, style={'fontSize': '10px', 'color': '#64748B', 'textTransform': 'uppercase', 'letterSpacing': '0.06em', 'marginBottom': '3px'}),
        html.Div(value, style={'fontSize': '15px', 'fontWeight': '700', 'color': color, 'fontFamily': "'Inter', sans-serif"}),
    ], style={'background': '#07101E', 'border': f'1px solid {BORDER}', 'borderRadius': '8px', 'padding': '10px 12px'})


def create_layout():
    return html.Div([

        # ── STICKY HEADER ─────────────────────────────────────────────
        html.Div([
            html.Div([
                # Left: icon + title
                html.Div([
                    html.Div('⬡', style={
                        'width': '36px', 'height': '36px', 'borderRadius': '8px',
                        'background': '#0F1E35', 'border': f'1px solid {BORDER}',
                        'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                        'color': '#3B82F6', 'fontSize': '18px', 'flexShrink': '0'
                    }),
                    html.Div([
                        html.Div('Global Organized Crime Analytics', style={
                            'fontSize': '15px', 'fontWeight': '600', 'color': '#F8FAFC', 'lineHeight': '1'
                        }),
                        html.Div('Intelligence Dashboard · 2023 Dataset', style={
                            'fontSize': '11px', 'color': '#64748B', 'marginTop': '3px'
                        }),
                    ]),
                ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),

                # Right: dynamic KPI chips + export
                html.Div([
                    html.Div(id='t1-metrics', style={'display': 'flex', 'alignItems': 'center'}),
                    html.Div(style={'width': '1px', 'height': '28px', 'background': BORDER, 'margin': '0 14px', 'flexShrink': '0'}),
                    html.Button('↓ Export', style={
                        'background': 'transparent', 'border': f'1px solid {BORDER}',
                        'borderRadius': '6px', 'color': '#94A3B8', 'fontSize': '12px',
                        'fontWeight': '500', 'padding': '6px 12px', 'cursor': 'pointer',
                        'fontFamily': "'Inter', sans-serif"
                    }),
                ], style={'display': 'flex', 'alignItems': 'center'}),
            ], style={
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between',
                'maxWidth': '1440px', 'margin': '0 auto', 'width': '100%', 'padding': '0 28px'
            }),
        ], style={
            'position': 'sticky', 'top': '0', 'zIndex': '200',
            'height': '64px', 'display': 'flex', 'alignItems': 'center',
            'background': BG, 'borderBottom': f'1px solid {BORDER}', 'flexShrink': '0'
        }),

        # ── NAV BAR + FILTERS ──────────────────────────────────────────
        html.Div([
            html.Div([
                # Nav pills
                html.Div([
                    _nav_btn('Global Overview',        'nav-1', active=True),
                    _nav_btn('Distributions',          'nav-2'),
                    _nav_btn('Exploratory Data',       'nav-3'),
                    _nav_btn('Probability Models',     'nav-4'),
                    _nav_btn('Prediction Engine',      'nav-5'),
                ], style={'display': 'flex', 'gap': '6px', 'alignItems': 'center', 'flex': '1'}),

                # Filters + live badge
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='t1-continent',
                            options=[{'label': o, 'value': o} for o in sorted(df['Continent'].dropna().unique())],
                            multi=True, placeholder='All Continents',
                            style=_dd_style, className='nav-dropdown'
                        ),
                    ], style={'minWidth': '160px', 'overflow': 'visible', 'zIndex': '300', 'position': 'relative'}),
                    html.Div([
                        dcc.Dropdown(
                            id='t1-region',
                            options=[{'label': o, 'value': o} for o in sorted(df['Region'].dropna().unique())],
                            multi=True, placeholder='All Regions',
                            style=_dd_style, className='nav-dropdown'
                        ),
                    ], style={'minWidth': '160px', 'overflow': 'visible', 'zIndex': '300', 'position': 'relative'}),
                    html.Div([
                        html.Span(style={
                            'width': '7px', 'height': '7px', 'borderRadius': '50%',
                            'background': '#10B981', 'display': 'inline-block', 'marginRight': '6px'
                        }),
                        html.Span('Live', style={'fontSize': '12px', 'color': '#64748B'}),
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginLeft': '4px', 'flexShrink': '0'}),
                ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginLeft': '16px'}),
            ], style={
                'display': 'flex', 'alignItems': 'center',
                'maxWidth': '1440px', 'margin': '0 auto', 'width': '100%', 'padding': '0 28px'
            }),
        ], style={
            'position': 'sticky', 'top': '64px', 'zIndex': '199',
            'height': '50px', 'display': 'flex', 'alignItems': 'center',
            'background': NAV_BG, 'borderBottom': f'1px solid {BORDER}'
        }),

        # ── CONTENT WRAPPER ────────────────────────────────────────────
        html.Div([

            # ── TAB 1: GLOBAL OVERVIEW ──────────────────────────────
            html.Div([

                # Heatmap card
                html.Div([
                    # Card header
                    html.Div([
                        html.Div([
                            html.Div('Global Criminality Heatmap', style={'fontSize': '14px', 'fontWeight': '600', 'color': '#F8FAFC'}),
                            html.Div('Geographic distribution · choropleth · click region to drill down', style={'fontSize': '11px', 'color': '#64748B', 'marginTop': '3px'}),
                        ]),
                        html.Div([
                            _map_pill('Criminality', active=True),
                            _map_pill('Resilience'),
                            _map_pill('Vulnerability'),
                            html.Div(style={'width': '1px', 'height': '20px', 'background': BORDER, 'margin': '0 6px'}),
                            html.Button('Filter Regions', style={
                                'background': 'transparent', 'border': f'1px solid {BORDER}',
                                'borderRadius': '6px', 'color': '#64748B', 'fontSize': '11px',
                                'padding': '4px 10px', 'cursor': 'pointer', 'fontFamily': "'Inter', sans-serif"
                            }),
                        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '6px', 'flexShrink': '0'}),
                    ], style={
                        'display': 'flex', 'alignItems': 'flex-start', 'justifyContent': 'space-between',
                        'marginBottom': '14px', 'flexWrap': 'wrap', 'gap': '10px'
                    }),
                    # Map
                    dcc.Graph(id='t1-map', config={'displayModeBar': False}, style={'height': '380px'}),
                ], className='glass-card', style={'padding': '20px', 'marginBottom': '20px'}),

                # 3-column row
                html.Div([
                    # Top 10 bar
                    html.Div([
                        card([
                            html.Div([
                                html.Div('Top 10 Highest Criminality', style={'fontSize': '13px', 'fontWeight': '600', 'color': '#F8FAFC'}),
                                html.Button('View All', style={'fontSize': '11px', 'color': '#3B82F6', 'background': 'none', 'border': 'none', 'cursor': 'pointer', 'fontFamily': "'Inter', sans-serif"}),
                            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '12px', 'paddingBottom': '12px', 'borderBottom': f'1px solid {BORDER}'}),
                            dcc.Graph(id='t1-bar', config={'displayModeBar': False}, style={'height': '260px'}),
                        ], style={'padding': '18px', 'marginBottom': '0', 'height': '100%'}),
                    ], style={'flex': '1.5', 'minWidth': '280px', 'display': 'flex', 'flexDirection': 'column'}),

                    # Crime level pie
                    html.Div([
                        card([
                            html.Div([
                                html.Div('Crime Level Distribution', style={'fontSize': '13px', 'fontWeight': '600', 'color': '#F8FAFC'}),
                            ], style={'marginBottom': '12px', 'paddingBottom': '12px', 'borderBottom': f'1px solid {BORDER}'}),
                            dcc.Graph(id='t1-pie', config={'displayModeBar': False}, style={'height': '260px'}),
                        ], style={'padding': '18px', 'marginBottom': '0', 'height': '100%'}),
                    ], style={'flex': '1', 'minWidth': '240px', 'display': 'flex', 'flexDirection': 'column'}),

                    # Info / alerts card
                    html.Div([
                        card([
                            html.Div([
                                html.Div('Data & Alerts', style={'fontSize': '13px', 'fontWeight': '600', 'color': '#F8FAFC'}),
                            ], style={'marginBottom': '12px', 'paddingBottom': '12px', 'borderBottom': f'1px solid {BORDER}'}),
                            html.Div([
                                html.Div([
                                    _stat_mini('Coverage', '100%', '#10B981'),
                                    _stat_mini('Indicators', '9', '#3B82F6'),
                                ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '8px', 'marginBottom': '8px'}),
                                html.Div([
                                    _stat_mini('Avg Δ 2022→23', '+0.12', '#F43F5E'),
                                    _stat_mini('Data Year', '2023', '#3B82F6'),
                                ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '8px', 'marginBottom': '12px'}),
                                html.Div([
                                    html.Div('⚠', style={'color': '#F43F5E', 'fontSize': '14px', 'marginRight': '8px', 'flexShrink': '0'}),
                                    html.Div([
                                        html.Div('Spike Detected', style={'fontSize': '12px', 'fontWeight': '600', 'color': '#F87171', 'marginBottom': '3px'}),
                                        html.Div('Human trafficking metrics show unusual variance in East Africa sub-region.', style={'fontSize': '11px', 'color': 'rgba(248,113,113,0.65)', 'lineHeight': '1.5'}),
                                    ]),
                                ], style={
                                    'display': 'flex', 'padding': '10px 12px',
                                    'background': '#160A0E', 'border': '1px solid #4C1525',
                                    'borderRadius': '8px'
                                }),
                            ]),
                        ], style={'padding': '18px', 'marginBottom': '0', 'height': '100%'}),
                    ], style={'flex': '1', 'minWidth': '220px', 'display': 'flex', 'flexDirection': 'column'}),

                ], style={'display': 'flex', 'gap': '20px', 'alignItems': 'stretch', 'flexWrap': 'wrap'}),

            ], id='content-1', style={'display': 'block', 'paddingTop': '24px', 'paddingBottom': '48px'}),

            # ── TAB 2: DISTRIBUTIONS ────────────────────────────────
            html.Div([
                card([
                    html.H3('Numerical Variable Analysis', style={'color': config.TEXT_WHITE, 'marginBottom': '14px', 'fontSize': '15px'}),
                    html.Div([
                        section_label('Select Metric'),
                        dcc.Dropdown(id='t2-num-var',
                            options=[{'label': v, 'value': v} for v in NUMERIC_VARS],
                            value='Criminality avg', clearable=False,
                            style={'fontSize': '13px', 'maxWidth': '350px', 'marginBottom': '18px'})
                    ]),
                    html.Div([
                        html.Div([dcc.Graph(id='t2-num-hist', config={'displayModeBar': False}, style={'height': '340px'})], style={'flex': '60', 'minWidth': '300px'}),
                        html.Div([html.Div(id='t2-freq-table')], style={'flex': '40', 'overflowX': 'auto', 'minWidth': '250px'}),
                    ], style={'display': 'flex', 'gap': '28px', 'alignItems': 'flex-start', 'flexWrap': 'wrap'}),
                ], className='glass-card dropdown-wrapper-card'),

                card([
                    html.H3('Categorical Variable Analysis', style={'color': config.TEXT_WHITE, 'marginBottom': '14px', 'fontSize': '15px'}),
                    html.Div([
                        section_label('Select Category'),
                        dcc.Dropdown(id='t2-cat-var',
                            options=[{'label': v, 'value': v} for v in CAT_VARS if v != 'Country'],
                            value='Region', clearable=False,
                            style={'fontSize': '13px', 'maxWidth': '350px', 'marginBottom': '18px'})
                    ]),
                    html.Div([
                        html.Div([dcc.Graph(id='t2-cat-bar', config={'displayModeBar': False}, style={'height': '300px'})], style={'flex': '1'}),
                        html.Div([dcc.Graph(id='t2-cat-pie', config={'displayModeBar': False}, style={'height': '300px'})], style={'flex': '1'}),
                    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'flexWrap': 'wrap'}),
                    html.Div(id='t2-cat-table'),
                ], className='glass-card dropdown-wrapper-card'),
            ], id='content-2', style={'display': 'none', 'paddingTop': '24px', 'paddingBottom': '48px'}),

            # ── TAB 3: EDA ──────────────────────────────────────────
            html.Div([
                card([
                    html.H3('Analyze Variable Outliers & Spread', style={'color': config.TEXT_WHITE, 'marginBottom': '14px', 'fontSize': '15px'}),
                    html.Div([
                        dcc.Dropdown(id='t3-var',
                            options=[{'label': v, 'value': v} for v in NUMERIC_VARS],
                            value='Criminal markets avg', clearable=False,
                            style={'fontSize': '13px', 'maxWidth': '300px'})
                    ], style={'marginBottom': '20px'}),
                    html.Div([
                        html.Div([dcc.Graph(id='t3-boxplot', config={'displayModeBar': False}, style={'height': '340px'})], style={'flex': '60'}),
                        html.Div([html.Div(id='t3-stats-table')], style={'flex': '40'}),
                    ], style={'display': 'flex', 'gap': '28px', 'alignItems': 'flex-start', 'flexWrap': 'wrap'}),
                ], className='glass-card dropdown-wrapper-card'),

                card([
                    html.H3('Confidence Intervals (95%)', style={'color': config.TEXT_WHITE, 'marginBottom': '14px', 'fontSize': '15px'}),
                    html.Div(id='t3-ci-table', style={'overflowX': 'auto'}),
                ]),
            ], id='content-3', style={'display': 'none', 'paddingTop': '24px', 'paddingBottom': '48px'}),

            # ── TAB 4: PROBABILITY MODELS ────────────────────────────
            html.Div([
                card([
                    html.H3('Normal Distribution Modeling', style={'color': config.TEXT_WHITE, 'marginBottom': '8px', 'fontSize': '15px'}),
                    html.Div([
                        html.Div([
                            section_label('μ (Mean)'),
                            dcc.Input(id='norm-mu', type='number',
                                value=round(float(df['Criminality avg'].mean()), 2), step=0.01,
                                style={'width': '100%', 'padding': '9px 12px', 'borderRadius': '8px',
                                       'border': f'1px solid {BORDER}', 'background': 'rgba(0,0,0,0.3)',
                                       'color': config.TEXT_WHITE, 'fontSize': '14px', 'fontFamily': "'Inter', sans-serif"})
                        ], style={'flex': '1', 'maxWidth': '200px'}),
                        html.Div([
                            section_label('σ (Std Dev)'),
                            dcc.Input(id='norm-sigma', type='number',
                                value=round(float(df['Criminality avg'].std()), 2), min=0.01, step=0.01,
                                style={'width': '100%', 'padding': '9px 12px', 'borderRadius': '8px',
                                       'border': f'1px solid {BORDER}', 'background': 'rgba(0,0,0,0.3)',
                                       'color': config.TEXT_WHITE, 'fontSize': '14px', 'fontFamily': "'Inter', sans-serif"})
                        ], style={'flex': '1', 'maxWidth': '200px'}),
                        html.Div([
                            section_label('X Value Threshold'),
                            dcc.Slider(id='norm-x', min=0, max=10, step=0.1, value=6.0,
                                marks={i: str(i) for i in range(11)},
                                tooltip={"placement": "bottom", "always_visible": True})
                        ], style={'flex': '2', 'paddingTop': '4px'}),
                    ], style={'display': 'flex', 'gap': '28px', 'marginBottom': '20px', 'alignItems': 'flex-end', 'flexWrap': 'wrap'}),
                    dcc.Graph(id='norm-chart', config={'displayModeBar': False}, style={'height': '360px'}),
                    html.Div(id='norm-metrics', style={'display': 'flex', 'gap': '14px', 'marginTop': '20px', 'flexWrap': 'wrap'}),
                ]),
            ], id='content-4', style={'display': 'none', 'paddingTop': '24px', 'paddingBottom': '48px'}),

            # ── TAB 5: PREDICTION ENGINE ─────────────────────────────
            html.Div([
                card([
                    html.H3('Simple Linear Regression Explorer', style={'color': config.TEXT_WHITE, 'marginBottom': '8px', 'fontSize': '15px'}),
                    html.Div([
                        html.Div([
                            section_label('X Variable (Independent)'),
                            dcc.Dropdown(id='reg-x',
                                options=[{'label': v, 'value': v} for v in NUMERIC_VARS if v != 'Criminality avg'],
                                value='Resilience avg', clearable=False, style={'fontSize': '13px'}),
                        ], style={'flex': '1', 'minWidth': '200px'}),
                        html.Div([
                            section_label('Y Variable (Dependent)'),
                            html.Div('Criminality average', style={
                                'fontSize': '13px', 'padding': '8px 12px',
                                'background': 'rgba(0,0,0,0.3)', 'border': f'1px solid {BORDER}',
                                'borderRadius': '6px', 'color': config.PRIMARY, 'fontWeight': '600'
                            }),
                        ], style={'flex': '1', 'minWidth': '200px'}),
                    ], style={'display': 'flex', 'gap': '14px', 'marginBottom': '20px', 'flexWrap': 'wrap'}),
                    html.Div([
                        html.Div([dcc.Graph(id='reg-scatter-simple', config={'displayModeBar': False}, style={'height': '340px'})], style={'flex': '65'}),
                        html.Div([html.Div(id='reg-stats-simple')], style={'flex': '35', 'minWidth': '220px'}),
                    ], style={'display': 'flex', 'gap': '18px', 'alignItems': 'flex-start', 'flexWrap': 'wrap'}),
                ], className='glass-card dropdown-wrapper-card'),

                card([
                    html.H3('Multiple Linear Regression Live Predictor', style={'color': config.TEXT_WHITE, 'marginBottom': '8px', 'fontSize': '15px'}),
                    html.Div([
                        html.Div([
                            html.Div([section_label('Resilience Avg'), dcc.Slider(1, 10, 0.5, value=5, id='sl-resilience', marks={1:'1',10:'10'}, tooltip={"placement":"bottom","always_visible":True})], style={'marginBottom':'22px'}),
                            html.Div([section_label('Human Trafficking'), dcc.Slider(1, 10, 0.5, value=6, id='sl-trafficking', marks={1:'1',10:'10'}, tooltip={"placement":"bottom","always_visible":True})], style={'marginBottom':'22px'}),
                            html.Div([section_label('Cyber-dependent crimes'), dcc.Slider(1, 10, 0.5, value=4, id='sl-cyber', marks={1:'1',10:'10'}, tooltip={"placement":"bottom","always_visible":True})], style={'marginBottom':'22px'}),
                            html.Div([section_label('State-embedded actors'), dcc.Slider(1, 10, 0.5, value=7, id='sl-state', marks={1:'1',10:'10'}, tooltip={"placement":"bottom","always_visible":True})], style={'marginBottom':'22px'}),
                            html.Div([section_label('Financial crimes'), dcc.Slider(1, 10, 0.5, value=5, id='sl-financial', marks={1:'1',10:'10'}, tooltip={"placement":"bottom","always_visible":True})], style={'marginBottom':'22px'}),
                            html.Div([section_label('Anti-money laundering'), dcc.Slider(1, 10, 0.5, value=3, id='sl-aml', marks={1:'1',10:'10'}, tooltip={"placement":"bottom","always_visible":True})]),
                        ], style={'flex':'45','background':f'rgba(13,24,41,0.8)','borderRadius':'12px','padding':'28px','border':f'1px solid {BORDER}','minWidth':'300px'}),

                        html.Div([
                            html.Div([
                                html.P('Predicted Global Criminality Score', style={'color':'rgba(255,255,255,0.7)','fontSize':'13px','fontWeight':'600','marginBottom':'10px','textTransform':'uppercase','letterSpacing':'1px'}),
                                html.Div(id='pred-output', style={'fontSize':'68px','fontWeight':'800','background':'linear-gradient(to right, #F43F5E, #F59E0B)','-webkit-background-clip':'text','-webkit-text-fill-color':'transparent'}),
                                html.P('/ 10.00', style={'color':'rgba(255,255,255,0.35)','fontSize':'16px','fontWeight':'600'}),
                            ], style={'background':'rgba(0,0,0,0.35)','borderRadius':'14px','padding':'36px 28px','textAlign':'center','border':f'1px solid rgba(244,63,94,0.25)','marginBottom':'20px'}),

                            html.Div([
                                html.H4('Multiple Linear Model Insights', style={'color':config.TEXT_WHITE,'marginBottom':'10px','fontSize':'14px'}),
                                html.Div([html.Span('R² Score:', style={'color':config.TEXT_SEC}), html.Span(f' {reg_model.score(X_all, y_all):.4f}', style={'color':config.PRIMARY_LIGHT,'fontWeight':'700','float':'right'})], style={'marginBottom':'8px','fontSize':'13px'}),
                                html.Div([html.Span('Strongest Predictor:', style={'color':config.TEXT_SEC}), html.Span(' Human Trafficking', style={'color':config.PRIMARY_LIGHT,'fontWeight':'700','float':'right'})], style={'fontSize':'13px'}),
                            ], style={'background':'rgba(0,0,0,0.2)','borderRadius':'10px','padding':'20px','border':f'1px dashed {BORDER}'}),
                        ], style={'flex':'55','display':'flex','flexDirection':'column','justifyContent':'center','minWidth':'300px'}),
                    ], style={'display':'flex','gap':'28px','flexWrap':'wrap'}),
                ]),
            ], id='content-5', style={'display': 'none', 'paddingTop': '24px', 'paddingBottom': '48px'}),

        ], style={
            'maxWidth': '1440px', 'margin': '0 auto', 'width': '100%',
            'padding': '0 28px', 'minHeight': 'calc(100vh - 114px)'
        }),

    ], style={'fontFamily': "'Inter', sans-serif", 'minHeight': '100vh', 'background': BG, 'color': '#F8FAFC'})
