#include <ESP8266WiFi.h>
#include <Servo.h>

//#define SERIAL_DEBUG

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
  #ifdef SERIAL_DEBUG
    Serial.print("Servo1: ");
    Serial.println(value);
  #endif
  
  uint8_t v = map(value, 0, 255, 50, 150);
  s1L.write(v);
  s1R.write(v);
}

void servo2Write(uint8_t value){
  #ifdef SERIAL_DEBUG
    Serial.print("Servo2: ");
    Serial.println(value);
  #endif
  
  uint8_t v = map(value, 0, 255, 70, 160);
  s2.write(v);
}

void loop() {      
  if (Serial.available() > 0) {
    String terminalText = Serial.readStringUntil('\n');
    uint8_t seperatorIndex = terminalText.indexOf("-");
    
    if (seperatorIndex == -1){
      int value = terminalText.toInt();
      servo1Write(value);
      
    } else {
      String a = terminalText.substring(0, seperatorIndex);
      String b = terminalText.substring(seperatorIndex+1);
      servo1Write(a.toInt());
      servo2Write(b.toInt());
    }
    
  }
}
