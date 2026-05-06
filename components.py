from dash import html
from config import TEXT_SEC, TEXT_WHITE

def card(children, style=None, className='glass-card'):
    base = {'padding': '24px', 'marginBottom': '24px', 'overflow': 'visible'}
    if style: base.update(style)
    return html.Div(children, className=className, style=base)

def section_label(text):
    return html.P(text, style={'color': TEXT_SEC, 'fontSize': '12px', 'fontWeight': '700', 'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '1px'})

def metric_card(title, value, custom_style=None):
    if custom_style is None: custom_style = {}
    return html.Div([
        html.Div(str(value), className='metric-value', style={'lineHeight': '1', 'marginBottom': '6px'}),
        html.Div(title, style={'fontSize': '13px', 'color': TEXT_SEC, 'fontWeight': '500', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
    ], className='glass-card', style={'padding': '20px 24px', 'flex': '1', 'minWidth': '150px', **custom_style})

def freq_table_html(headers, rows):
    header_cells = [html.Th(h, style={'background': 'rgba(59, 130, 246, 0.2)', 'color': TEXT_WHITE, 'padding': '12px 16px', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': '600', 'borderBottom': '1px solid rgba(255,255,255,0.1)'}) for h in headers]
    data_rows = []
    for i, row in enumerate(rows):
        bg = 'rgba(255,255,255,0.02)' if i % 2 == 0 else 'transparent'
        cells = [html.Td(cell, style={'padding': '12px 16px', 'fontSize': '13px', 'color': '#F8FAFC', 'borderBottom': '1px solid rgba(255,255,255,0.05)', 'background': bg}) for cell in row]
        data_rows.append(html.Tr(cells))
    return html.Table([html.Thead(html.Tr(header_cells)), html.Tbody(data_rows)], style={'width': '100%', 'borderCollapse': 'collapse', 'borderRadius': '8px', 'overflow': 'hidden'})

def filter_row(*items):
    children = []
    for lbl, dd in items:
        children.append(html.Div([section_label(lbl), dd], style={'flex': '1', 'minWidth': '200px', 'overflow':'visible'}))
    return html.Div(children, className='glass-card dropdown-wrapper-card', style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap', 'marginBottom': '24px', 'padding': '20px', 'alignItems': 'center'})
