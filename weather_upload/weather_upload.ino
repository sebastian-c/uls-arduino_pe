// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

// REQUIRES the following Arduino libraries:
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor

#include "DHT.h"

#define DHTPIN 2     // Digital pin connected to the DHT sensor
// Define model
#define DHTTYPE DHT11   // DHT 11
// Initialize DHT sensor.
DHT dht(DHTPIN, DHTTYPE);

// Define button pin
int buttonPin = 7;

void setup() {
  Serial.begin(9600);
  Serial.println(F("[MESSAGE] DHT11 test!"));

  pinMode(buttonPin, INPUT_PULLUP); 

  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("[MESSAGE] Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("[DATA] {humidity_perc : "));
  Serial.print(h);
  Serial.print(F(", temperature_c : "));
  Serial.print(t);
  Serial.print(F(", heat_index_c : "));
  Serial.print(hic);
  Serial.println(F("}"));

  // If button on board is pressed
  if(digitalRead(buttonPin) == LOW) {
    Serial.print(F("[COMMAND] Button press registered on pin "));
    Serial.println(buttonPin);
  } ;
}
