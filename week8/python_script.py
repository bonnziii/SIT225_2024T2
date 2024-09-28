import csv
import time
from datetime import datetime
from arduino_iot_cloud import ArduinoCloudClient

# Arduino Cloud setup details
DEVICE_ID = 'b80b9c29-ccc0-4e89-8b1e-0f5eba884a62'
SECRET_KEY = '4DHueuYVyxpIyI!Qm4DlzmdYQ'

# Buffers and variables
BUFFER_SIZE = 20
data_buffer_x = []
data_buffer_y = []
data_buffer_z = []
saved_data_buffer = []

# Callback functions for each variable
def on_py_x(client, value):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Capture timestamp for this value
    data_buffer_x.append((timestamp, value))
    print(f"py_x: {value}")  # Print real-time data to terminal
    check_buffer_and_save()

def on_py_y(client, value):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Capture timestamp for this value
    data_buffer_y.append((timestamp, value))
    print(f"py_y: {value}")  # Print real-time data to terminal
    check_buffer_and_save()

def on_py_z(client, value):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Capture timestamp for this value
    data_buffer_z.append((timestamp, value))
    print(f"py_z: {value}")  # Print real-time data to terminal
    check_buffer_and_save()

# Save to a CSV file in real-time and check buffer size
def save_to_csv():
    filename = f"sensor_data_{get_timestamp()}.csv"
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "py_x", "py_y", "py_z"])
        for i in range(len(saved_data_buffer)):
            writer.writerow(saved_data_buffer[i])

# Check buffer size and transfer old data
def check_buffer_and_save():
    # If buffer size is met, save to a new CSV
    if len(data_buffer_x) >= BUFFER_SIZE and len(data_buffer_y) >= BUFFER_SIZE and len(data_buffer_z) >= BUFFER_SIZE:
        # Store timestamped data in the saved buffer
        for i in range(BUFFER_SIZE):
            # Access timestamp and value separately
            timestamp_x, x_value = data_buffer_x[i]
            timestamp_y, y_value = data_buffer_y[i]
            timestamp_z, z_value = data_buffer_z[i]
            
            # Store timestamped data in the saved buffer
            saved_data_buffer.append([timestamp_x, x_value, y_value, z_value])

        # Save data to CSV in real-time
        save_to_csv()

        # Clear the current data buffers
        data_buffer_x.clear()
        data_buffer_y.clear()
        data_buffer_z.clear()

        # Clear the saved buffer after writing to CSV
        saved_data_buffer.clear()

# Timestamp format for filenames
def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# Main function to connect to Arduino Cloud
def main():
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register("py_x", value=None, on_write=on_py_x)
    client.register("py_y", value=None, on_write=on_py_y)
    client.register("py_z", value=None, on_write=on_py_z)
    client.start()

if __name__ == "__main__":
    main()
