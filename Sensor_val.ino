
#include "DHT.h"

// DHT22 configuration
#define DHTPIN 4        // GPIO pin connected to DHT22
#define DHTTYPE DHT22   // Specify DHT22 sensor

// Sensors
const int ldrPin = 39;     // ADC pin for LDR

int ldrValue = 0;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);   // Start serial communication
  dht.begin();          // Initialize the DHT sensor
}

void loop() {
  readTemp();   // Read and print temperature & humidity
  readLdr();            // Read and print LDR

  delay(2000);          // Wait 2s before repeating (needed for DHT22!)
}

// Function to read humidity & temperature
void readTemp() {
  float temperature = dht.readTemperature();

  if (isnan(temperature)) {
    Serial.println("Error: Unable to read from DHT sensor.");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
}

// Function to read LDR
int readLdr() {
  int ldrValue = analogRead(ldrPin);
  Serial.print("LDR Value: ");
  Serial.println(ldrValue);
  return ldrValue;
}