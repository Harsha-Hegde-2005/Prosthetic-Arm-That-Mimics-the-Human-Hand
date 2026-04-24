#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

// Servo pulse limits
#define SERVO_MIN  100
#define SERVO_MAX  500

int servoChannel[5] = {0, 1, 2, 3, 4};

// ---------- SAFETY ----------
unsigned long lastSerialTime = 0;
const unsigned long SERIAL_TIMEOUT = 2000; // 2 seconds

// ---------- FUNCTIONS ----------
void setServoAngle(int channel, int angle) {
  angle = constrain(angle, 0, 180);
  int pulse = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(channel, 0, pulse);
}

void resetAllServos() {
  for (int i = 0; i < 5; i++) {
    setServoAngle(servoChannel[i], 0);
  }
}

// ---------- SETUP ----------
void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);   // SDA, SCL for ESP32

  pwm.begin();
  pwm.setPWMFreq(50);  // Servo frequency
  delay(500);

  // 🔹 MOVE ALL SERVOS TO 0° AT STARTUP
  resetAllServos();

  Serial.println("ESP32 Ready - Servos at 0°");
  lastSerialTime = millis();
}

// ---------- LOOP ----------
void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    int values[5];
    int index = 0;

    char *token = strtok((char*)data.c_str(), ",");
    while (token != NULL && index < 5) {
      values[index++] = atoi(token);
      token = strtok(NULL, ",");
    }

    if (index == 5) {
      for (int i = 0; i < 5; i++) {
        setServoAngle(servoChannel[i], values[i]);
      }
      lastSerialTime = millis();  // update serial activity time
    }
  }

  // 🔹 SAFETY: IF SERIAL STOPS → RESET SERVOS TO 0°
  if (millis() - lastSerialTime > SERIAL_TIMEOUT) {
    resetAllServos();
  }
}