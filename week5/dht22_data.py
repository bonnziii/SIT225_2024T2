import firebase_admin
from firebase_admin import credentials, db
import random
import time

# Initialize Firebase
cred = credentials.Certificate('sit225-f035c-firebase-adminsdk-ggf3h-7b7ee0411c.json')  # Path to your Firebase private key JSON file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sit225-f035c-default-rtdb.asia-southeast1.firebasedatabase.app/'  
})

# Set the reference point in Firebase
ref = db.reference('sensors/DHT22')

# Function to insert random DHT22 data
def insert_random_dht22_data():
    data = {
        "sensor_name": "DHT22",
        "timestamp": time.strftime('%Y%m%d%H%M%S'),
        "data": {
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(50.0, 70.0), 2)
        }
    }
    ref.push(data)  # Push data to Firebase
    print("Data inserted:", data)

# Insert random data 5 times
for _ in range(5):
    insert_random_dht22_data()
    time.sleep(1)
