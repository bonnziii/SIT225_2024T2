import time
import csv
from arduino_iot_cloud import ArduinoCloudClient

# Replace with your actual device ID and secret key
DEVICE_ID = "b01195de-cd28-4c07-b49e-5a912fd3436d"
SECRET_KEY = "oR0MZwRBygs9FHi#!Lokns@2!"

# File name for combined CSV logging
combined_csv_file = "combined_accel_data.csv"

# Dictionary to hold the most recent values for x, y, z
accel_data = {
    "timestamp": None,
    "accel_x": None,
    "accel_y": None,
    "accel_z": None
}

# Convert UNIX epoch time to human-readable format
def convert_to_readable_timestamp(epoch_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

# Function to check if all data is available to be logged
def is_all_data_available():
    return all(value is not None for value in accel_data.values())

# Function to write combined data to CSV
def log_combined_data():
    with open(combined_csv_file, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([accel_data["timestamp"], accel_data["accel_x"], accel_data["accel_y"], accel_data["accel_z"]])
    print(f"Logged combined data to {combined_csv_file} at {accel_data['timestamp']}")

# Callback functions to handle incoming data
def on_accel_x_changed(client, value):
    accel_data["accel_x"] = value
    accel_data["timestamp"] = convert_to_readable_timestamp(time.time())
    if is_all_data_available():
        log_combined_data()

def on_accel_y_changed(client, value):
    accel_data["accel_y"] = value
    accel_data["timestamp"] = convert_to_readable_timestamp(time.time())
    if is_all_data_available():
        log_combined_data()

def on_accel_z_changed(client, value):
    accel_data["accel_z"] = value
    accel_data["timestamp"] = convert_to_readable_timestamp(time.time())
    if is_all_data_available():
        log_combined_data()

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
