#include <Arduino_LSM6DS3.h>  // Include the sensor library

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud
  while (!Serial);     // Wait for the serial connection to establish

  // Initialize the IMU (LSM6DS3)
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);  // Stop if the sensor can't be found
  }

  Serial.println("Gyroscope Initialized");
}

void loop() {
  float x, y, z;

  // Read the gyroscope values
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);

    // Send the gyroscope data as CSV string (x, y, z)
    Serial.print(x);
    Serial.print(",");
    Serial.print(y);
    Serial.print(",");
    Serial.println(z);

    delay(1000);  // Sample every 1000ms 
  }
}
