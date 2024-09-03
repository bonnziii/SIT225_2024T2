import sys
import traceback
import random
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
from datetime import datetime

DEVICE_ID = "dd1697fd-8e83-4fd6-8e76-c5a682528705"
SECRET_KEY = "EGZLQOeTqJKMg7SGpTl#Bmfbj"

# Callback function on distance change event.
def on_ultrasonic_distance_changed(client, value):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_line = f"{timestamp},{value}\n"

    # Open the CSV file in append mode and write the data
    with open('ultrasonic_data.csv', 'a') as file:
        file.write(data_line)
    
    # Print the timestamp and distance to the console 
    print(f"Logged: {data_line.strip()}")

def main():
    print("Starting the main() function")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register with 'distance' cloud variable and listen on its value changes in the callback function
    client.register(
        "distance", value=None, 
        on_write=on_ultrasonic_distance_changed
    )

    # Start cloud client
    client.start()

if __name__ == "__main__":
    try:
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
