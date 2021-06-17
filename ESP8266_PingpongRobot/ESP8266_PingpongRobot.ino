#include <ESP8266WiFi.h>
#include <Servo.h>

#define SERVO1L_PIN D6
#define SERVO1R_PIN D5
#define SERVO2_PIN D7

Servo s1L, s1R, s2;

void setup() {
  s1L.attach(SERVO1L_PIN); 
  s1R.attach(SERVO1R_PIN); 
  s2.attach(SERVO2_PIN); 
  Serial.begin(9600);
  servo1Write(125);
}

void servo1Write(uint8_t value){
  uint8_t v = map(value, 0, 255, 50, 180);
  s1L.write(v);
  s1R.write(v);
}

void loop() {      
  if (Serial.available() > 0) {
    String terminalText = Serial.readStringUntil('\n');
    int value = terminalText.toInt();
    servo1Write(value);
  }
}
