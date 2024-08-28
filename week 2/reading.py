import serial
import time

# Replace with the correct serial port identified using ls /dev/tty.*
ser = serial.Serial('/dev/tty.usbmodem1401', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

filename = f'DHT22_data_{time.strftime("%Y%m%d%H%M%S")}.csv'

with open(filename, 'a') as file:
    file.write("Timestamp,Temperature,Humidity\n")

# Set the duration for overnight data collection (e.g., 8 hours = 28800 seconds)
duration = 8 * 60 * 60  # 8 hours in seconds
start_time = time.time()

try:
    while time.time() - start_time < duration:
        line = ser.readline().decode('utf-8').strip()
        if line:
            # Format the timestamp as YYYYMMDDHHMMSS
            timestamp = time.strftime("%Y%m%d%H%M%S")
            # Ensure proper formatting with commas separating the data fields
            formatted_line = f"{timestamp},{line}\n"
            with open(filename, 'a') as file:
                file.write(formatted_line)
                print(f"Logged: {formatted_line.strip()}")
        time.sleep(30)  # 30-second interval between readings
except KeyboardInterrupt:
    print("Data collection stopped.")

ser.close()
