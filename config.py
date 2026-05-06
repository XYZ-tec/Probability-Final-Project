import plotly.graph_objects as go

TEXT_SEC = '#94A3B8'
TEXT_WHITE = '#FFFFFF'
PRIMARY = '#3B82F6'
PRIMARY_LIGHT = '#60A5FA'
GREEN = '#10B981'
RED = '#F43F5E'
AMBER = '#F59E0B'
CHART_COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#F43F5E', '#8B5CF6', '#14B8A6', '#EC4899']

_dark_template = go.layout.Template()
_dark_template.layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=TEXT_SEC, family='Inter, sans-serif'),
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, linecolor='rgba(255,255,255,0.1)', automargin=True),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, linecolor='rgba(255,255,255,0.1)', automargin=True),
)

CHART_LAYOUT = dict(
    template=_dark_template,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=TEXT_SEC, family='Inter, sans-serif'),
    title_font=dict(size=15, color=TEXT_WHITE, weight='bold'),
    margin=dict(t=50, l=120, r=40, b=40),
)

INDEX_STRING = '''<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>Global Organized Crime Dashboard</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      
      /* Base styles limit to body to prevent aggressive cascading */
      body { 
          font-family: 'Inter', sans-serif; background: #0B1120; min-height: 100vh;
          background-image: radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.15), transparent 25%),
                            radial-gradient(circle at 85% 30%, rgba(16, 185, 129, 0.1), transparent 25%); 
          color: #000000;
      }
      
      h1, h2, h3, h4 { color: #F8FAFC; }
      
      .tab--selected { border-bottom: 3px solid #3B82F6 !important; color: #3B82F6 !important; font-weight: 600 !important; }
      .tab { color: #94A3B8 !important; background: transparent !important; border: none !important; border-bottom: 3px solid transparent !important; padding: 14px 24px !important; font-size: 15px !important; cursor: pointer !important; transition: 0.3s; }
      .tab:hover { color: #F8FAFC !important; }
      
      /* Scrollbar */
      ::-webkit-scrollbar { width: 8px; }
      ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
      ::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.5); border-radius: 4px; }
      
      /* Cards and Stacking Contexts (Fixes "Sticky" Dropdown overlaps) */
      .glass-card { 
          background: rgba(30, 41, 59, 0.4); 
          backdrop-filter: blur(12px); 
          border: 1px solid rgba(255, 255, 255, 0.1); 
          border-radius: 12px; 
          box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); 
          transition: all 0.2s;
          position: relative;
      }
      
      /* Hover interactions: careful with z-index so dropdowns render ABOVE other cards! */
      .glass-card:hover { border: 1px solid rgba(59, 130, 246, 0.3); z-index: 50; }
      
      /* Elevate wrapper cards that specifically contain drop downs */
      .dropdown-wrapper-card { z-index: 100 !important; overflow: visible !important; }

      .metric-value { font-size: 32px; font-weight: 800; background: linear-gradient(to right, #60A5FA, #34D399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; color: transparent; }
    </style>
  </head>
  <body>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
  </body>
</html>'''
