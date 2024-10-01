import time
from pymongo import MongoClient
import pandas as pd
import json
import paho.mqtt.client as mqtt
import ssl

# MQTT broker details
broker = "797787b221c646ee8d02f24c144282f9.s1.eu.hivemq.cloud"
port = 8883
topic = "gyroscope/data"

mqtt_user = "Arduinouser"  #HiveMQ username
mqtt_password = "anisshNY12"  #HiveMQ password

# MongoDB connection using provided connection string
try:
    mongo_client = MongoClient("mongodb+srv://s221435713:anisshNY12@sit225.6hc75.mongodb.net/")
    db = mongo_client["gyroscopeDB"]
    collection = db["gyroscopeData"]
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit()

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker successfully.")
        client.subscribe(topic)  # Subscribe to the topic published by Arduino
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")

def on_message(client, userdata, msg):
    # Decode the JSON message from the Arduino
    try:
        print(f"Message received from topic {msg.topic}")
        data = json.loads(msg.payload.decode())
        print(f"Received data: {data}")
        # Insert the data into MongoDB
        collection.insert_one(data)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")

client = mqtt.Client()

# Configure SSL/TLS connection
client.tls_set_context(ssl.create_default_context())
client.username_pw_set(mqtt_user, mqtt_password)

client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Function to retrieve data from MongoDB and save as CSV
def save_to_csv():
    print("Saving data to CSV...")
    try:
        cursor = collection.find()
        data_list = list(cursor)

        # Convert to DataFrame
        df = pd.DataFrame(data_list)
        
        # Drop MongoDB '_id' column if it exists
        if '_id' in df.columns:
            df.drop(columns=['_id'], inplace=True)

        # Save to CSV
        df.to_csv('gyroscope_data.csv', index=False)
        print("Data saved to gyroscope_data.csv")
    except Exception as e:
        print(f"Failed to save CSV: {e}")

# Start the loop to collect data for 30 minutes
try:
    client.loop_start()  # Start MQTT loop in a separate thread
    print("Collecting data... Press Ctrl+C to stop.")
    time.sleep(1800)  # Run for 30 minutes (1800 seconds)
except KeyboardInterrupt:
    print("Stopping data collection manually.")
finally:
    client.loop_stop()  # Stop MQTT loop
    save_to_csv()  # Save collected data to CSV
