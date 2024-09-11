#include <Arduino.h>

const int analogPin = A0;
float voltage = 0.0;

void setup() {
  Serial.begin(115200);
  pinMode(analogPin, INPUT);
}

void loop() {
  int sensorValue = analogRead(analogPin);
  voltage = map(sensorValue, 0, 1023, -12000, 12000) / 1000.0;
  
  // Serial.print("Pot Value: ");
  // Serial.println(sensorValue);
  // delay(2000); // Delay for 2 seconds

  Serial.print("Voltage: ");
  Serial.println(voltage);

  delay(1);
}