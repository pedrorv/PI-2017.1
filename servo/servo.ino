#include "Servo.h"

Servo motorX;
Servo motorY;
const int Y = 9;
const int X = 10; 

void setup() {
  // put your setup code here, to run once:
  motorX.attach(X);
  motorY.attach(Y);
}

void loop() {
  // put your main code here, to run repeatedly:
  motorX.write(45);
  delay(1000);
  motorX.write(125);
  delay(1000);
  motorY.write(0);
  delay(1000);
  motorY.write(50);
  delay(1000);
}
