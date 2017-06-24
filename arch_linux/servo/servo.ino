#include "Servo.h"
#include "LiquidCrystal.h"

Servo motorX;
Servo motorY;
const int X = 10;
const int Y = 9;
const int servoDelay = 15;
const int laser = 11;
int ligado = 0;

void setup() {
  Serial.begin(9600);

  pinMode(laser, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
  motorX.write(93);
  motorY.write(75);
  motorX.attach(X);
  motorY.attach(Y);
}

void loop() {
  while (Serial.available() == 0) {};
  String xyAngles = Serial.readStringUntil('x');
  xyAngles.replace("x", "");
  int xAngle = xyAngles.toInt() % 1000;
  int yAngle = xyAngles.toInt() / 1000;

  ligado = 1;

  if (xAngle == 180) {
    ligado = 1;
  } else {    
    motorX.write(xAngle);
    motorY.write(yAngle);  
  }

  if (ligado == 1) {
    digitalWrite(laser, HIGH);
    digitalWrite(LED_BUILTIN, HIGH);
  }

  delay(1);
}
