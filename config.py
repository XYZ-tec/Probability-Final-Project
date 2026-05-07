import plotly.graph_objects as go

TEXT_SEC = '#94A3B8'
TEXT_WHITE = '#FFFFFF'
PRIMARY = '#3B82F6'
PRIMARY_LIGHT = '#60A5FA'
GREEN = '#10B981'
RED = '#F43F5E'
AMBER = '#F59E0B'
CHART_COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#F43F5E', '#8B5CF6', '#14B8A6', '#EC4899']

CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=TEXT_SEC, family='Inter, sans-serif'),
    title_font=dict(size=14, color=TEXT_WHITE),
    margin=dict(t=50, l=120, r=40, b=40),
)

AXIS_STYLE = dict(
    showgrid=True, gridcolor='rgba(255,255,255,0.05)',
    zeroline=False, linecolor='rgba(255,255,255,0.08)', automargin=True
)

INDEX_STRING = '''<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>Global Organized Crime Analytics</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }

      body {
        font-family: 'Inter', sans-serif;
        background: #050D1A;
        min-height: 100vh;
        color: #F8FAFC;
      }

      h1, h2, h3, h4 { color: #F8FAFC; }

      /* ── Scrollbar ──────────────────────────────────── */
      ::-webkit-scrollbar { width: 6px; height: 6px; }
      ::-webkit-scrollbar-track { background: rgba(8,15,28,0.8); }
      ::-webkit-scrollbar-thumb { background: #1E2D45; border-radius: 4px; }
      ::-webkit-scrollbar-thumb:hover { background: #2D4A6E; }

      /* ── Glass cards ────────────────────────────────── */
      .glass-card {
        background: #0D1829;
        border: 1px solid #1E2D45;
        border-radius: 12px;
        position: relative;
        overflow: visible;
      }
      .glass-card:hover { border-color: rgba(59,130,246,0.25); }
      .dropdown-wrapper-card { z-index: 100 !important; overflow: visible !important; }

      /* ── Metric value gradient ──────────────────────── */
      .metric-value {
        font-size: 30px;
        font-weight: 800;
        background: linear-gradient(to right, #60A5FA, #34D399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
      }

      /* ── Nav pills ──────────────────────────────────── */
      .nav-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        cursor: pointer;
        transition: all 0.15s ease;
        background: transparent;
        color: #64748B;
        border: 1px solid #1E2D45;
        white-space: nowrap;
      }
      .nav-pill:hover { color: #CBD5E1; border-color: #334155; }
      .nav-pill.nav-active {
        background: #1E3A5F;
        color: #93C5FD;
        border-color: #2D5FA6;
      }

      /* ── Map toggle pills ───────────────────────────── */
      .map-pill {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        cursor: pointer;
        transition: all 0.15s;
        background: transparent;
        color: #64748B;
        border: 1px solid #1E2D45;
      }
      .map-pill:hover { color: #94A3B8; border-color: #334155; }
      .map-pill.map-pill-active {
        background: #1E3A5F;
        color: #93C5FD;
        border-color: #2D5FA6;
      }

      /* ── Nav dropdowns ──────────────────────────────── */
      .nav-dropdown .Select-control {
        background: rgba(8,15,28,0.9) !important;
        border: 1px solid #1E2D45 !important;
        border-radius: 6px !important;
        min-height: 32px !important;
        height: 32px !important;
        font-size: 12px !important;
        box-shadow: none !important;
        cursor: pointer !important;
      }
      .nav-dropdown .Select-control:hover { border-color: #334155 !important; }
      .nav-dropdown .Select-placeholder,
      .nav-dropdown .Select-value-label { color: #64748B !important; font-size: 12px !important; line-height: 30px !important; }
      .nav-dropdown .Select-value { line-height: 30px !important; }
      .nav-dropdown .Select-input { height: 30px !important; }
      .nav-dropdown .Select-arrow-zone { padding-top: 0 !important; }
      .nav-dropdown .Select-arrow { border-top-color: #475569 !important; }
      .nav-dropdown .Select-menu-outer {
        background: #0D1829 !important;
        border: 1px solid #1E2D45 !important;
        border-radius: 8px !important;
        z-index: 500 !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
      }
      .nav-dropdown .Select-option {
        background: #0D1829 !important;
        color: #94A3B8 !important;
        font-size: 12px !important;
        padding: 8px 14px !important;
      }
      .nav-dropdown .Select-option:hover,
      .nav-dropdown .Select-option.is-focused { background: #1E2D45 !important; color: #F8FAFC !important; }
      .nav-dropdown .Select-option.is-selected { background: #1E3A5F !important; color: #93C5FD !important; }
      .nav-dropdown .VirtualizedSelectFocusedOption { background: #1E2D45 !important; }

      /* Multi-value tags in nav dropdowns */
      .nav-dropdown .Select-multi-value-wrapper { display: flex; flex-wrap: nowrap; overflow: hidden; align-items: center; }
      .nav-dropdown .Select--multi .Select-value {
        background: #1E3A5F !important;
        border: 1px solid #2D5FA6 !important;
        border-radius: 4px !important;
        color: #93C5FD !important;
        font-size: 11px !important;
        margin: 2px !important;
        line-height: 20px !important;
      }
      .nav-dropdown .Select--multi .Select-value-icon { color: #93C5FD !important; border-right-color: #2D5FA6 !important; }
      .nav-dropdown .Select--multi .Select-value-icon:hover { background: #1E2D45 !important; color: #F8FAFC !important; }

      /* ── Dash slider overrides ──────────────────────── */
      .rc-slider-track { background: #3B82F6 !important; }
      .rc-slider-handle { border-color: #3B82F6 !important; background: #3B82F6 !important; }
      .rc-slider-dot-active { border-color: #3B82F6 !important; }

      /* Remove default Dash tab styles (not used, but prevents flash) */
      .tab--selected { border-bottom: 3px solid #3B82F6 !important; color: #3B82F6 !important; font-weight: 600 !important; }
      .tab { color: #94A3B8 !important; background: transparent !important; border: none !important; border-bottom: 3px solid transparent !important; padding: 14px 24px !important; font-size: 15px !important; }
    </style>
  </head>
  <body>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
  </body>
</html>'''
