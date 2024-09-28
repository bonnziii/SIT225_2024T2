import time
import csv
from arduino_iot_cloud import ArduinoCloudClient

# Replace with your actual device ID and secret key
DEVICE_ID = "b01195de-cd28-4c07-b49e-5a912fd3436d"
SECRET_KEY = "oR0MZwRBygs9FHi#!Lokns@2!"

# File names for CSV logging
csv_files = {
    "accel_x": "accel_x.csv",
    "accel_y": "accel_y.csv",
    "accel_z": "accel_z.csv"
}

# Convert UNIX epoch time to human-readable format
def convert_to_readable_timestamp(epoch_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

# Function to log data to the respective CSV file with a human-readable timestamp
def log_data(axis, value):
    timestamp = convert_to_readable_timestamp(time.time())
    with open(csv_files[axis], mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, value])
    print(f"Logged {value} to {csv_files[axis]} at {timestamp}")

# Callback functions to handle incoming data
def on_accel_x_changed(client, value):
    log_data("accel_x", value)

def on_accel_y_changed(client, value):
    log_data("accel_y", value)

def on_accel_z_changed(client, value):
    log_data("accel_z", value)

def main():
    print("Connecting to Arduino IoT Cloud...")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

    # Register callbacks for sensor variables
    client.register("accel_x", value=None, on_write=on_accel_x_changed)
    client.register("accel_y", value=None, on_write=on_accel_y_changed)
    client.register("accel_z", value=None, on_write=on_accel_z_changed)

    # Start the cloud client
    client.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
