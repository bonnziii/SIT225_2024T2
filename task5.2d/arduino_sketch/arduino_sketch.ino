#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <Arduino_LSM6DS3.h> // For Gyroscope data

// WiFi credentials
const char* ssid = "DODO-8BEF"; //WiFi SSID
const char* password = "FLCCVDF5MB"; //WiFi password

// MQTT broker details 
const char* mqttServer = "797787b221c646ee8d02f24c144282f9.s1.eu.hivemq.cloud";
const int mqttPort = 8883; // Use TLS port
const char* mqttUser = "Arduinouser"; //HiveMQ username
const char* mqttPassword = "anisshNY12"; //HiveMQ password
const char* topic = "gyroscope/data"; // The topic

WiFiSSLClient wifiClient; // Use SSL client for secured connection
PubSubClient client(wifiClient);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Connect to WiFi
  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // Wait for connection and print status
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Current WiFi status: ");
    Serial.println(WiFi.status());
    Serial.println("Retrying WiFi connection...");
  }

  Serial.println("Connected to WiFi");

  // Set MQTT server and connect
  client.setServer(mqttServer, mqttPort);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    // Include MQTT username and password for secure connection
    if (client.connect("ArduinoClient", mqttUser, mqttPassword)) {
      Serial.println("Connected to MQTT");
    } else {
      Serial.print("Failed to connect to MQTT, State: ");
      Serial.println(client.state());
      delay(2000);
    }
  }

  // Initialize IMU sensor
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    while (1);
  }
}

void loop() {
  if (IMU.gyroscopeAvailable()) {
    float x, y, z;
    IMU.readGyroscope(x, y, z);
    
    // Format message as JSON
    String message = "{\"x\":" + String(x) + ",\"y\":" + String(y) + ",\"z\":" + String(z) + "}";
    
    // Publish message
    client.publish(topic, message.c_str());
    
    delay(1000); // Send data every second
  }
}