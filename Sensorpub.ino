#include <WiFi.h>
#include <Wire.h>
#include <DHT.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ------------------- Config -------------------
bool DEBUG = false;

// Sensors
const int PIN_DHT_SENSOR = 4;
const int DHT_SENSOR_TYPE = DHT22;
const int PIN_LDR_SENSOR = 39;




// Serial
const long SERIAL_BAUD_RATE = 115200;

// WiFi
const char* WIFI_SSID = "sanjayandroid";
const char* WIFI_PWD = "sanjayandroid";

// MQTT
const char* MQTT_BROKER_IP = "10.58.217.136";
const char* PUBLISH_TOPIC = "esp32/data";
WiFiClient espClient;
PubSubClient client(espClient);


DHT dht(PIN_DHT_SENSOR, DHT_SENSOR_TYPE);

long lastMsg = 0;


// ------------------- Setup -------------------
void setup() {
  // --- Serial Communication ---
  Serial.begin(SERIAL_BAUD_RATE);

  // Init Wifi and MQTT coms
  setup_wifi();

  client.setServer(MQTT_BROKER_IP, 1883);
  client.setCallback(callback);

  // --- Initialize Sensors ---
  dht.begin();

}

void setup_wifi() {
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PWD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("Client IP address: ");
  Serial.println(WiFi.localIP());
}


// Function to return temp and humidity
void readTemp(float &temperature) {
  
  temperature = dht.readTemperature();

  if (isnan(temperature)) {
    if (DEBUG) Serial.println("Error: Unable to read from DHT sensor.");
    temperature = -1;
  }
}



// Function to read LDR
int readLdr() {
  int value = analogRead(PIN_LDR_SENSOR);  
  return value;
}

// MQTT Callback
void callback(char* topic, byte* message, unsigned int length) {
  String messageTemp;
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }

  // Debug output
  if (DEBUG) {
    Serial.print("MQTT Message arrived [");
    Serial.print(topic);
    Serial.print("]: ");
    Serial.println(messageTemp);
  }

}

// Reconnect
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 sec");
      delay(5000);
    }
  }
}

// Loop
void loop() {

  // MQTT Connect
  if (!client.connected()) reconnect();
  client.loop();

  // Code to run after every 5 seconds
  long now = millis();
  if (now - lastMsg > 5000) {  
    lastMsg = now;

    // --- Read Sensor Values ---
    float temperature = 0;
    readTemp(temperature);
    int ldrValue = readLdr();

    // --- Debug Output ---
    if (DEBUG) {
      Serial.print("Temperature: "); Serial.print(temperature); Serial.print(" °C\t");
      Serial.print("LDR Value: "); Serial.println(ldrValue);

      Serial.println("---------------------------");
    }


    // --- Create JSON ---
    StaticJsonDocument<200> doc;
    doc["temperature"] = temperature;
    doc["ldr"] = ldrValue;


    // Serialize JSON to string
    char jsonBuffer[256];
    serializeJson(doc, jsonBuffer);

    if (DEBUG) {
      Serial.print("Publishing JSON: "); Serial.println(jsonBuffer);
    }

    // Publish JSON
    client.publish(PUBLISH_TOPIC, jsonBuffer);
  }
}