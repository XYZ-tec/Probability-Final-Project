from app_instance import app
from config import INDEX_STRING
from layout import create_layout
from callbacks import register_callbacks
import warnings
warnings.filterwarnings('ignore')

# Assign custom index string CSS
app.index_string = INDEX_STRING

# Initialize Component Layout
app.layout = create_layout()

# Register all routing callbacks
register_callbacks()

if __name__ == '__main__':
    app.run(debug=True, port=8050)
