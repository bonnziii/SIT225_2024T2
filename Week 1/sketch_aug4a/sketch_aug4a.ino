const int ledPin = 13; // LED connected to digital pin 13

void setup() {
  pinMode(ledPin, OUTPUT); // Set the LED pin as output
  Serial.begin(9600);      // Start serial communication at 9600 baud
}

void loop() {
  if (Serial.available() > 0) {     // Check if data is available to read
    int blinkTimes = Serial.parseInt(); // Read the number from the serial buffer
    
    // Blink the LED the specified number of times
    for (int i = 0; i < blinkTimes; i++) {
      digitalWrite(ledPin, HIGH);  // Turn the LED on
      delay(1000);                 // Wait for 1 second
      digitalWrite(ledPin, LOW);   // Turn the LED off
      delay(1000);                 // Wait for 1 second
    }
    
    // Send a random number back to the Python script
    int randomNumber = random(1, 10);
    Serial.println(randomNumber);
  }
}
