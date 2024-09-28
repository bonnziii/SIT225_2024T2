#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include "arduino_secrets.h" 

// Wi-Fi credentials (linking to secrets)
const char SSID[] = SECRET_SSID; // Network SSID (name)
const char PASS[] = SECRET_OPTIONAL_PASS; // Network password (use for WPA, or use as key for WEP)

// Callback for alarm status changes
void onAlarmStatusChange();

// Cloud variables
float tempValue;       // Temperature in degrees Celsius
float humidValue;      // Humidity in percentage
bool alarmStatus;      // Boolean for triggering alarm

void initProperties(){
  // Link cloud variables to Arduino IoT Cloud
  ArduinoCloud.addProperty(tempValue, READWRITE, ON_CHANGE, NULL);
  ArduinoCloud.addProperty(humidValue, READWRITE, ON_CHANGE, NULL);
  ArduinoCloud.addProperty(alarmStatus, READWRITE, ON_CHANGE, onAlarmStatusChange);
}

// Wi-Fi Connection setup
WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);
