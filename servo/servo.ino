#include "Servo.h"

Servo motorX;
Servo motorY;
const int Y = 9;
const int X = 10; 

void setup() {
  // put your setup code here, to run once:
  motorX.attach(X);
  motorY.attach(Y);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("X: ");
  Serial.println(motorX.read());
  Serial.print("Y: ");
  Serial.println(motorY.read());
}
