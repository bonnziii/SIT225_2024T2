import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_table

# Load and prepare the data
df = pd.read_csv('gyroscope_data.csv')
df.columns = ['Timestamp', 'X-axis', 'Y-axis', 'Z-axis']

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Gyroscope Data Visualization'),

    # Dropdown to select graph type
    dcc.Dropdown(
        id='graph-type-dropdown',
        options=[
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Distribution Plot', 'value': 'histogram'}
        ],
        value='line',
        clearable=False
    ),
    
    # Dropdown to select which axis to visualize (X, Y, Z, or all)
    dcc.Dropdown(
        id='axis-dropdown',
        options=[
            {'label': 'X-axis', 'value': 'X-axis'},
            {'label': 'Y-axis', 'value': 'Y-axis'},
            {'label': 'Z-axis', 'value': 'Z-axis'},
            {'label': 'All', 'value': 'all'}
        ],
        value='all',
        multi=False,
        clearable=False
    ),
    
    # Input field to enter the number of samples to display
    dcc.Input(
        id='sample-size',
        type='number',
        placeholder="Number of samples",
        value=len(df)
    ),
    
    # Next and Previous buttons to navigate through samples
    html.Button('Previous', id='prev-button', n_clicks=0),
    html.Button('Next', id='next-button', n_clicks=0),
    
    # Graph component
    dcc.Graph(id='gyro-graph'),
    
    # Summary table of the data currently being displayed
    dash_table.DataTable(id='data-summary')
])

# Global variable to keep track of the current page
current_page = 0

# Callback to update the graph and data summary
@app.callback(
    [Output('gyro-graph', 'figure'),
     Output('data-summary', 'data')],
    [Input('graph-type-dropdown', 'value'),
     Input('axis-dropdown', 'value'),
     Input('sample-size', 'value'),
     Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')],
    [State('prev-button', 'n_clicks_timestamp'),
     State('next-button', 'n_clicks_timestamp')]
)
def update_graph(graph_type, selected_axis, sample_size, prev_clicks, next_clicks, prev_timestamp, next_timestamp):
    global current_page
    
    # Determine if we are navigating to the next or previous data samples
    samples_per_page = sample_size
    total_samples = len(df)
    max_pages = total_samples // samples_per_page
    
    if prev_timestamp and prev_timestamp > next_timestamp:
        current_page = max(0, current_page - 1)
    elif next_timestamp and next_timestamp > prev_timestamp:
        current_page = min(max_pages, current_page + 1)

    start_idx = current_page * samples_per_page
    end_idx = start_idx + samples_per_page
    df_display = df.iloc[start_idx:end_idx]
    
    # Select the data to plot based on the selected axis
    if selected_axis == 'all':
        data_cols = ['X-axis', 'Y-axis', 'Z-axis']
    else:
        data_cols = [selected_axis]
    
    # Generate the appropriate graph type
    if graph_type == 'line':
        fig = px.line(df_display, x='Timestamp', y=data_cols, title=f'Gyroscope {selected_axis} Data (Line Chart)')
    elif graph_type == 'scatter':
        fig = px.scatter(df_display, x='Timestamp', y=data_cols, title=f'Gyroscope {selected_axis} Data (Scatter Plot)')
    elif graph_type == 'histogram':
        fig = px.histogram(df_display, x='Timestamp', y=data_cols, histfunc='avg', title=f'Gyroscope {selected_axis} Data (Distribution Plot)')
    
    # Generate the summary statistics
    summary_stats = df_display.describe().reset_index().to_dict('records')
    
    return fig, summary_stats

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
