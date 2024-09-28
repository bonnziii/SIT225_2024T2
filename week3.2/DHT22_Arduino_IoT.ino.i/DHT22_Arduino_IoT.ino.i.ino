#include "thingProperties.h"
#include <DHT.h>

// DHT sensor setup
#define DHTPIN 2     // Digital pin connected to the DHT22 sensor
#define DHTTYPE DHT22   // DHT22 (AM2302)

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

// Threshold values for triggering alarm
const float tempThreshold = 30.0; // Temperature threshold in degrees Celsius
const float humidThreshold = 70.0; // Humidity threshold in percentage

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  delay(1500);  // Wait for Serial Monitor connection

  // Initialize cloud properties and connect to Arduino IoT Cloud
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  // Optional: Set debug message level
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

  // Initialize DHT sensor
  dht.begin();
}

void loop() {
  // Update Arduino Cloud connection
  ArduinoCloud.update();

  // Read temperature and humidity values from DHT22 sensor
  float temp = dht.readTemperature();
  float humid = dht.readHumidity();

  // Check for failed readings and retry
  if (isnan(temp) || isnan(humid)) {
    Serial.println("Failed to read from DHT sensor!");
    return;  // Skip updating if there's an issue
  }

  // Assign values to cloud variables
  tempValue = temp;
  humidValue = humid;

  // Print sensor values to Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(tempValue);
  Serial.print(" °C, ");
  Serial.print("Humidity: ");
  Serial.print(humidValue);
  Serial.println(" %");

  // Check if temperature or humidity exceeds threshold
  if (tempValue > tempThreshold || humidValue > humidThreshold) {
    alarmStatus = true;  // Trigger alarm in cloud
  } else {
    alarmStatus = false; // Reset alarm when values are normal
  }

  delay(5000); // Delay for 5 seconds before next read
}

// Callback function when alarm status changes
void onAlarmStatusChange() {
  Serial.println("--onAlarmStatusChange");
  if (alarmStatus) {
    Serial.println("Alarm triggered! Values exceed threshold.");
  } else {
    Serial.println("Alarm reset. Values are normal.");
  }
}
