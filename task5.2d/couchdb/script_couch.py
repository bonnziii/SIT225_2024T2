import time  
import couchdb
import json
import pandas as pd
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import ssl


# MQTT broker details
broker = "797787b221c646ee8d02f24c144282f9.s1.eu.hivemq.cloud"
port = 8883
topic = "gyroscope/data"

mqtt_user = "Arduinouser"  # MQTT username
mqtt_password = "anisshNY12"  # MQTT password

# CouchDB connection details
couchdb_url = "http://admin:anisshNY@127.0.0.1:5984/"  # CouchDB credentials
couch = couchdb.Server(couchdb_url)

# Check if the database exists or create it
db_name = "gyroscope_data"
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

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
        # Insert the data into CouchDB
        db.save(data)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"Error inserting data into CouchDB: {e}")

client = mqtt.Client()

# Configure SSL/TLS connection
client.tls_set_context(ssl.create_default_context())
client.username_pw_set(mqtt_user, mqtt_password)

client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Function to retrieve data from CouchDB and save as CSV
def save_to_csv():
    print("Saving data to CSV...")
    try:
        # Create an empty list to hold the gyroscope data
        data_list = []

        # Iterate over each document in the CouchDB database
        for doc_id in db:
            doc = db[doc_id]  # Get the document by its ID
            
            # Check if the document contains the x, y, z fields
            if 'x' in doc and 'y' in doc and 'z' in doc:
                # Extract only the x, y, and z fields
                data_list.append({'x': doc['x'], 'y': doc['y'], 'z': doc['z']})

        # Convert the data_list to a pandas DataFrame
        df = pd.DataFrame(data_list)
        
        # Save to CSV
        df.to_csv('gyroscope_data_couchdb.csv', index=False)
        print("Data saved to gyroscope_data_couchdb.csv")
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

