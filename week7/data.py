import serial
import time

# Set the serial port for your Arduino (check port)
ser = serial.Serial('/dev/tty.usbmodem1401', 9600)  # Change to the correct port on your system (e.g., COM3 or /dev/ttyUSB0)

# Open the CSV file for writing data
file = open("dht22_data.csv", "w")
file.write("Temperature,Humidity\n")

# Collect data for 30 minutes (1800 seconds)
start_time = time.time()
while time.time() - start_time < 1800:  # Adjust the duration as needed
    line = ser.readline().decode('utf-8').strip()  # Read from serial
    file.write(line + "\n")

# Close the file and serial connection
file.close()
ser.close()