from dash import html
from config import TEXT_SEC, TEXT_WHITE

def card(children, style=None, className='glass-card'):
    base = {'padding': '24px', 'marginBottom': '20px', 'overflow': 'visible'}
    if style: base.update(style)
    return html.Div(children, className=className, style=base)

def section_label(text):
    return html.P(text, style={
        'color': TEXT_SEC, 'fontSize': '11px', 'fontWeight': '700',
        'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '1px'
    })

def kpi_chip(label, value, color='#3B82F6'):
    return html.Div([
        html.Div(label, style={
            'fontSize': '10px', 'color': '#64748B',
            'textTransform': 'uppercase', 'letterSpacing': '0.08em', 'marginBottom': '2px'
        }),
        html.Div(value, style={
            'fontSize': '20px', 'fontWeight': '700',
            'fontFamily': "'Inter', sans-serif", 'color': color, 'lineHeight': '1'
        }),
    ], style={'padding': '0 14px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-end'})

def kpi_divider():
    return html.Div(style={'width': '1px', 'height': '28px', 'background': '#1E2D45', 'flexShrink': '0'})

def metric_card(title, value, custom_style=None):
    if custom_style is None: custom_style = {}
    return html.Div([
        html.Div(str(value), className='metric-value', style={'lineHeight': '1', 'marginBottom': '6px'}),
        html.Div(title, style={'fontSize': '13px', 'color': TEXT_SEC, 'fontWeight': '500', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
    ], className='glass-card', style={'padding': '20px 24px', 'flex': '1', 'minWidth': '150px', **custom_style})

def freq_table_html(headers, rows):
    header_cells = [html.Th(h, style={
        'background': 'rgba(59, 130, 246, 0.15)', 'color': TEXT_WHITE, 'padding': '10px 14px',
        'textAlign': 'left', 'fontSize': '12px', 'fontWeight': '600',
        'borderBottom': '1px solid rgba(255,255,255,0.08)'
    }) for h in headers]
    data_rows = []
    for i, row in enumerate(rows):
        bg = 'rgba(255,255,255,0.02)' if i % 2 == 0 else 'transparent'
        cells = [html.Td(cell, style={
            'padding': '10px 14px', 'fontSize': '12px', 'color': '#F8FAFC',
            'borderBottom': '1px solid rgba(255,255,255,0.04)', 'background': bg
        }) for cell in row]
        data_rows.append(html.Tr(cells))
    return html.Table(
        [html.Thead(html.Tr(header_cells)), html.Tbody(data_rows)],
        style={'width': '100%', 'borderCollapse': 'collapse', 'borderRadius': '8px', 'overflow': 'hidden'}
    )

def filter_row(*items):
    children = []
    for lbl, dd in items:
        children.append(html.Div([section_label(lbl), dd], style={'flex': '1', 'minWidth': '200px', 'overflow': 'visible'}))
    return html.Div(children, className='glass-card dropdown-wrapper-card', style={
        'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap',
        'marginBottom': '20px', 'padding': '18px', 'alignItems': 'center'
    })
