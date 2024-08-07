import serial
import time
import random
from datetime import datetime

# Set up serial communication
boud_rate = 9600
serial_port = '/dev/tty.usbmodem1401' # Adjust the port as necessary
ser = serial.Serial(serial_port, boud_rate, timeout=1)

def log_event(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - {message}")

while True:
    # Send a random number to Arduino
    send_number = random.randint(1, 10)
    ser.write(bytes(str(send_number) + '\n', 'utf-8'))
    log_event(f"Sent: {send_number}")
    
    # Wait for Arduino to blink LED and respond
    while ser.in_waiting == 0:
        time.sleep(0.1)  # Wait for response
    
    received_number = ser.readline().decode('utf-8').strip()
    if received_number.isdigit():
        log_event(f"Received: {received_number}")
        wait_time = int(received_number)
        
        # Sleep for the specified number of seconds
        log_event(f"Sleeping for {wait_time} seconds")
        time.sleep(wait_time)
        log_event("Done sleeping")
