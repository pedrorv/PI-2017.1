#include "Servo.h"
#include "LiquidCrystal.h"

Servo motorX;
Servo motorY;
const int X = 10;
const int Y = 9;

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  Serial.begin(9600);
  motorX.attach(X);
  motorY.attach(Y);

  lcd.begin(16, 2);
}

void loop() {
  while (Serial.available() == 0) {};
  String xyAngles = Serial.readStringUntil("x");
  xyAngles.replace("x", "");
  int xAngle = xyAngles.toInt() % 1000;
  int yAngle = xyAngles.toInt() / 1000;

  lcd.setCursor(0, 0);
  lcd.print("   ");
  lcd.setCursor(0, 1);
  lcd.print("   ");

  lcd.setCursor(0, 0);
  lcd.print(xAngle);
  lcd.setCursor(0, 1);
  lcd.print(yAngle);

  motorX.write(xAngle);
  motorY.write(yAngle);

  delay(3000);
}
