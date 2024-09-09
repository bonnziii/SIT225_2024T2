import serial
import time
import firebase_admin
from firebase_admin import credentials, db
import json
import csv

# Initialize Firebase
cred = credentials.Certificate("sit225-f035c-firebase-adminsdk-ggf3h-0fb0886c61.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sit225-f035c-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Serial connection with Arduino (Update with your serial port)
ser = serial.Serial('/dev/tty.usbmodem1401', 9600)

# Function to send data to Firebase
def send_to_firebase(data):
    ref = db.reference('/gyroscope')
    ref.push(data)  # Push the data to Firebase under /gyroscope

# Open CSV file to write data
with open('gyroscope_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'X-axis', 'Y-axis', 'Z-axis'])

    print("Collecting data...")
    
    while True:
        try:
            if ser.in_waiting > 0:
                # Read serial data
                line = ser.readline().decode('utf-8').strip()
                gyroscope_data = line.split(',')

                if len(gyroscope_data) == 3:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    
                    # Create JSON object
                    json_data = {
                        "timestamp": timestamp,
                        "x": gyroscope_data[0],
                        "y": gyroscope_data[1],
                        "z": gyroscope_data[2]
                    }

                    # Send to Firebase
                    send_to_firebase(json_data)

                    # Log to CSV
                    writer.writerow([timestamp] + gyroscope_data)
                    print(f"Logged to CSV and Firebase: {json_data}")
                
                # Flush to ensure data is written
                file.flush()

        except KeyboardInterrupt:
            print("\nStopping data collection.")
            ser.close()
            break
import pandas as pd

# Query Firebase data
def query_firebase():
    ref = db.reference('/gyroscope')
    data = ref.get()
    return data

# Save the queried data to CSV
def save_to_csv(data):
    with open('queried_gyroscope_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'X-axis', 'Y-axis', 'Z-axis'])
        
        for key, value in data.items():
            writer.writerow([value['timestamp'], value['x'], value['y'], value['z']])
        print("Data saved to CSV.")

# Query data and save it to CSV
queried_data = query_firebase()
save_to_csv(queried_data)
