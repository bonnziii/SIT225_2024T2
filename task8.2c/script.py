import asyncio
import pandas as pd
import plotly.graph_objs as go
import time
import os
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
from arduino_iot_cloud import ArduinoCloudClient
import ssl
import certifi
import threading
import signal

# Device ID and Secret Key from Arduino IoT Cloud
DEVICE_ID = '86f7ea8b-a2d7-49bd-80e4-fe8874c54f9b'
SECRET_KEY = 'l#B#Y@9#rOczgWCKkxx7Q5uon'

# Buffer settings
BUFFER_SIZE = 100  # Number of readings to buffer
data_buffer = []

# File paths
csv_filename = f"accelerometer_data_{time.strftime('%Y%m%d_%H%M%S')}.csv"
png_filename = f"accelerometer_graph_{time.strftime('%Y%m%d_%H%M%S')}.png"

# Arduino Cloud setup details
xValue = None
yValue = None
zValue = None

# SSL context for secure connection
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

# Callback functions for each variable
def on_x_value(client, value):
    global xValue
    xValue = value
    process_data()

def on_y_value(client, value):
    global yValue
    yValue = value
    process_data()

def on_z_value(client, value):
    global zValue
    zValue = value
    process_data()

# Initialize Arduino Cloud client
client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
client.register('xValue', value=None, on_write=on_x_value)
client.register('yValue', value=None, on_write=on_y_value)
client.register('zValue', value=None, on_write=on_z_value)

# Function to process data and add to buffer
def process_data():
    if xValue is not None and yValue is not None and zValue is not None:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        data_buffer.append([timestamp, xValue, yValue, zValue])
        # Print the data to the terminal
        print(f"Timestamp: {timestamp}, X: {xValue}, Y: {yValue}, Z: {zValue}")
        
        # Save to CSV in real-time
        save_data_to_csv()

        # Keep buffer size constant
        if len(data_buffer) > BUFFER_SIZE:
            data_buffer.pop(0)

# Function to save data to CSV continuously
def save_data_to_csv():
    df = pd.DataFrame(data_buffer, columns=['timestamp', 'x', 'y', 'z'])
    df.to_csv(csv_filename, index=False)

# Function to save graph as PNG
def save_graph_as_png():
    if len(data_buffer) > 0:
        df = pd.DataFrame(data_buffer, columns=['timestamp', 'x', 'y', 'z'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['x'], mode='lines', name='X-axis'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['y'], mode='lines', name='Y-axis'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['z'], mode='lines', name='Z-axis'))

        fig.update_layout(title='Accelerometer Data (X, Y, Z)',
                          xaxis_title='Timestamp',
                          yaxis_title='Acceleration')
        fig.write_image(png_filename)
        print(f"Graph saved as {png_filename}")

# Async function to start the client with error handling
async def start_client():
    while True:
        try:
            await client.run(interval=1, backoff=5)  # Attempt to run client
        except Exception as e:
            print(f"Error in client loop: {e}")
            await asyncio.sleep(5)  # Retry after 5 seconds

# Function to run the client in the background
def run_client_in_background():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_client())
    loop.run_forever()

# Set up Dash app for visualization
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Live Accelerometer Data Visualization"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='graph-update',
        interval=1000,  # Keep data request at every 1 second
        n_intervals=0
    )
])

# Callback to update the graph
@app.callback(
    Output('live-graph', 'figure'),
    Input('graph-update', 'n_intervals')
)
def update_graph(n):
    if len(data_buffer) > 0:
        df = pd.DataFrame(data_buffer, columns=['timestamp', 'x', 'y', 'z'])

        # Create a new figure for the graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['x'], mode='lines', name='X-axis'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['y'], mode='lines', name='Y-axis'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['z'], mode='lines', name='Z-axis'))

        fig.update_layout(title='Accelerometer Data (X, Y, Z)',
                          xaxis_title='Timestamp',
                          yaxis_title='Acceleration')

        return fig
    else:
        return go.Figure()

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print("Gracefully shutting down...")
    save_graph_as_png()
    exit(0)

# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)

# Run Dash app and client
if __name__ == '__main__':
    threading.Thread(target=run_client_in_background, daemon=True).start()
    app.run_server(debug=True, port=8050)
