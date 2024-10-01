import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from datetime import datetime
import os
import time

#Arduino Cloud credentials
DEVICE_ID = "1ff750b2-c336-4826-97c8-4300eb97c1d3"
SECRET_KEY = "yvQlwTQFMAD3AxwZOPjZgRiNx"

# Initialize counters and file storage
csv_filename = ''
image_folder = 'captured_images'
graph_folder = 'graphs'
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
if not os.path.exists(graph_folder):
    os.makedirs(graph_folder)
sequence_number = 1
accel_data = []

# Global variables to hold the latest accelerometer values
accel_x = None
accel_y = None
accel_z = None

# To track the time interval for data collection
start_time = time.time()

# Function to store data every 10 seconds
def store_accel_data():
    global csv_filename, sequence_number, accel_data, accel_x, accel_y, accel_z, start_time
    
    # Store x, y, z values along with timestamp
    if accel_x is not None and accel_y is not None and accel_z is not None:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        accel_data.append([timestamp, accel_x, accel_y, accel_z])
    
    # Check if 10 seconds have passed since the last storage
    if time.time() - start_time >= 10:
        # Create timestamped filenames
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        csv_filename = f"{sequence_number}_{timestamp}.csv"
        image_filename = f"{sequence_number}_{timestamp}.jpg"
        graph_filename = f"{sequence_number}_{timestamp}.png"
        
        # Save accelerometer data to CSV
        df = pd.DataFrame(accel_data, columns=['timestamp', 'accel_x', 'accel_y', 'accel_z'])
        df.to_csv(os.path.join(graph_folder, csv_filename), index=False)
        
        print(f"Data saved to {csv_filename}")
        
        # Generate graph for the accelerometer data
        plot_graph(df, graph_filename)
        
        # Capture image from webcam
        capture_image(image_filename)
        
        # Clear data for next interval and reset start time
        accel_data = []
        sequence_number += 1
        start_time = time.time()

def capture_image(filename):
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        # Allow camera to warm up
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        ret, frame = cap.read()
        
        # If frame is captured successfully
        if ret:
            image_path = os.path.join(image_folder, filename)
            cv2.imwrite(image_path, frame)
            print(f"Image captured and saved as {filename}")
        else:
            print("Error: Could not capture image.")

        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Image capture error: {e}")

def plot_graph(df, filename):
    try:
        # Plot the accelerometer data
        plt.figure(figsize=(10, 5))
        plt.plot(df['timestamp'], df['accel_x'], label='accel_x')
        plt.plot(df['timestamp'], df['accel_y'], label='accel_y')
        plt.plot(df['timestamp'], df['accel_z'], label='accel_z')
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.xticks(rotation=45)
        plt.title('Accelerometer Data Over Time')
        plt.legend()
        plt.grid(True)
        graph_path = os.path.join(graph_folder, filename)
        plt.savefig(graph_path)
        plt.close()
        print(f"Graph saved as {filename}")
    except Exception as e:
        print(f"Graph generation error: {e}")

# Callback functions for accelerometer data changes
def on_accel_x_changed(client, value):
    global accel_x
    accel_x = value
    store_accel_data()

def on_accel_y_changed(client, value):
    global accel_y
    accel_y = value
    store_accel_data()

def on_accel_z_changed(client, value):
    global accel_z
    accel_z = value
    store_accel_data()

def main():
    print("Starting the main() function")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register cloud variables (accel_x, accel_y, accel_z)
    client.register(
        "accel_x", value=None, on_write=on_accel_x_changed
    )
    client.register(
        "accel_y", value=None, on_write=on_accel_y_changed
    )
    client.register(
        "accel_z", value=None, on_write=on_accel_z_changed
    )

    # Start cloud client
    client.start()

if __name__ == "__main__":
    try:
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
