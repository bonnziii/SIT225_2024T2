import firebase_admin
from firebase_admin import credentials, db
import random
import time

# Initialize Firebase
cred = credentials.Certificate('sit225-f035c-firebase-adminsdk-ggf3h-7b7ee0411c.json')  # Path to your Firebase private key JSON file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sit225-f035c-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace with your Firebase database URL
})

# Set the reference point in Firebase
ref = db.reference('sensors/SR04')

# Function to insert random SR04 data
def insert_random_sr04_data():
    data = {
        "sensor_name": "SR04 Ultrasonic",
        "timestamp": time.strftime('%Y%m%d%H%M%S'),
        "data": {
            "distance": round(random.uniform(10.0, 100.0), 2)
        }
    }
    ref.push(data)  # Push data to Firebase
    print("Data inserted:", data)

# Insert random data 5 times
for _ in range(5):
    insert_random_sr04_data()
    time.sleep(1)
