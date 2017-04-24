#include "Servo.h"

Servo motorX;
Servo motorY;
const int X = 10;
const int Y = 9;

void setup() {
  Serial.begin(9600);
  motorX.attach(X);
  motorY.attach(Y);
}

void loop() {
  while (Serial.available() == 0) {};
  int xyAngles = Serial.parseInt();
  int xAngle = xyAngles % 1000;
  int yAngle = xyAngles / 1000;

  motorX.write(xAngle);
  motorY.write(yAngle);

  delay(15);
}
